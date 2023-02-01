# !/usr/bin/env python3
"""
lib for parachain
"""
import json
import time

from .xclient_libs import Xlibs
from .xclient_ops import Xclient


class ParaChain:
    """
    平行链相关lib
    """

    # 初始化
    def __init__(self, conf):
        self.conf = conf
        self.xlib = Xlibs(conf)
        self.xclient = Xclient(conf)

    def create_chain(self, chain_conf, **kwargs):
        """
        创建平行链
        chain_conf：平行链的配置
        """
        chain_conf = "'" + chain_conf + "'"
        res = [
            "xkernel",
            "invoke",
            "'$parachain'",
            "--method",
            "createChain",
            "-a",
            chain_conf,
        ]
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        if err == 0:
            time.sleep(30)
        return err, result

    def query_chain_group(self, name, **kwargs):
        """
        查询平行链的群组
        name: 平行链名
        """
        args = {"name": name}
        args = json.dumps(args)
        args = "'" + args + "'"
        res = ["xkernel", "query", "'$parachain'", "--method", "getGroup", "-a", args]
        for key, value in kwargs.items():
            if key == "keys":
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    def edit_chain_group(self, name, admin, **kwargs):
        """
        修改平行链的群组
        name: 平行链名
        admin 群组成员
        """
        admin = json.dumps(admin)
        print(admin)
        args = {"name": name, "admin": admin}
        args = json.dumps(args)
        args = "'" + args + "'"
        res = ["xkernel", "invoke", "'$parachain'", "--method", "editGroup", "-a", args]
        for key, value in kwargs.items():
            if key == "keys":
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    def stop_chain(self, name, **kwargs):
        """
        停用平行链
        name: 平行链名
        """
        args = {"name": name}
        args = json.dumps(args)
        args = "'" + args + "'"
        res = ["xkernel", "invoke", "'$parachain'", "--method", "stopChain", "-a", args]
        for key, value in kwargs.items():
            if key == "keys":
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    def gen_chain_conf(self, consensus, name, group=False, group_name=""):
        """
        根据共识和链名，生成用于创建平行链的字符串
        consensus：共识类型，pow single poa xpos tdpos xpos
        name: 链名
        group: bool 是否同时设置群组
        group_name: 外部可传入群组的名称，用于异常测试
        """
        cons_data = {
            "version": "1",
            "predistribution": [
                {"address": self.conf.addrs[0], "quota": "100000000000000000000"}
            ],
            "maxblocksize": "128",
            "award": "1000000",
            "decimals": "8",
            "award_decay": {"height_gap": 31536000, "ratio": 1},
            "gas_price": {
                "cpu_rate": 1000,
                "mem_rate": 1000000,
                "disk_rate": 1,
                "xfee_rate": 1,
            },
            "new_account_resource_amount": 1000,
            "genesis_consensus": {},
        }

        if consensus == "pow":
            cons_data["genesis_consensus"] = {
                "name": "pow",
                "config": {
                    "defaultTarget": "545259519",
                    "adjustHeightGap": "5",
                    "expectedPeriod": "15",
                    "maxTarget": "486604799",
                },
            }
        elif consensus == "single":
            cons_data["genesis_consensus"] = {
                "name": "single",
                "config": {"miner": self.conf.addrs[0], "period": "3000"},
            }
        elif consensus in ("tdpos", "xpos"):
            cons_data["genesis_consensus"] = {
                "name": "tdpos",
                "config": {
                    "timestamp": "1559021720000000000",
                    "proposer_num": "2",
                    "period": "3000",
                    "alternate_interval": "3000",
                    "term_interval": "6000",
                    "block_num": "20",
                    "vote_unit_price": "1",
                    "init_proposer": {"1": [self.conf.addrs[0], self.conf.addrs[1]]},
                },
            }
            if consensus == "xpos":
                cons_data["genesis_consensus"]["config"]["bft_config"] = {}
        elif consensus in ("poa", "xpoa"):
            cons_data["genesis_consensus"] = {
                "name": "xpoa",
                "config": {
                    "version": "1",
                    "period": 3000,
                    "block_num": 20,
                    "init_proposer": {"address": self.conf.addrs},
                },
            }
            if consensus == "xpoa":
                cons_data["genesis_consensus"]["config"]["bft_config"] = {}
        elif consensus == "poaraft":
            cons_data["genesis_consensus"] = {
                "version": "1",
                "expand_consensus": {
                    "name": "poa",
                    "config": {"init_validators": {"validators": self.conf.addrs}},
                },
                "safety_consensus": {
                    "name": "raft",
                    "config": {"block_num": 10, "period": 3000},
                },
            }
        else:
            err = 1
            result = "共识不能识别：" + consensus
            return err, result
        if self.conf.nofee:
            cons_data["nofee"] = True
        if self.conf.crypto == "gm":
            cons_data["crypto"] = self.conf.crypto
        cons_data = json.dumps(cons_data)
        chain_conf = {"name": name, "data": cons_data}
        if group:
            if group_name == "":
                group_name = name

            group_info = {"name": group_name, "admin": self.conf.addrs}
            group_str = json.dumps(group_info)
            chain_conf["group"] = group_str

        print(chain_conf)
        err = 0
        result = json.dumps(chain_conf)
        return err, result

    def query_chain(self, **kwargs):
        """
        查询所有平行链
        不包括xuper
        """
        s = ("status", "-L")
        cmd = " ".join(s)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        if err != 0:
            return err, result
        result = json.loads(result)
        chain_list = []
        for chain in result:
            if chain["name"] != "xuper":
                chain_list.append(chain["name"])
        return err, chain_list
