# !/usr/bin/env python3
"""
lib for update
"""

import os
import json

from .xclient_libs import Xlibs
from .xclient_ops import Xclient


class Update:
    """
    链上治理：共识升级
    """

    # 初始化
    def __init__(self, conf):
        self.conf = conf
        self.xlib = Xlibs(conf)
        self.xclient = Xclient(conf)

    def gen_cons_json(self, cons_name, validator, **kwargs):
        """
        升级共识的json
        cons_name: 共识名称
        validator: 矿工列表
        version: 共识版本，不设置则自动读取当前版本
        percent: 最小票数百分比
        stop_vote_height: 停止投票高度
        trigger_height: 触发高度
        """
        err = 0
        # 获取当前区块高度
        err, height = self.xlib.query_height()
        if err != 0:
            return err, height
        percent = kwargs["percent"] if "percent" in kwargs.keys() else "51"
        stop_vote_height = (
            kwargs["stop_vote_height"]
            if "stop_vote_height" in kwargs.keys()
            else int(height) + 14
        )
        trigger_height = (
            kwargs["trigger_height"]
            if "trigger_height" in kwargs.keys()
            else int(height) + 15
        )
        version = kwargs["version"] if "version" in kwargs.keys() else ""
        if version == "":
            # 查询当前共识版本
            err, result = self.xlib.consensus_status()
            if err != 0:
                return err, result
            result = json.loads(result)
            version = result["version"]
            version = int(version) + 1
            version = str(version)

        args = {}

        update_json = {
            "args": {
                "min_vote_percent": percent,
                "stop_vote_height": str(stop_vote_height),
            },
            "trigger": {
                "height": int(trigger_height),
                "module": "xkernel",
                "contract": "$consensus",
                "method": "updateConsensus",
                "args": {},
            },
        }
        # 两阶段共识
        if "raft" in cons_name:
            update_json["trigger"]["contract"] = "$pluggable_consensus"

        if cons_name in ("poa", "xpoa"):
            args["name"] = "xpoa"
            args["config"] = {
                "version": version,
                "period": 3000,
                "block_num": 10,
                "contract_name": "xpoa_validates",
                "method_name": "get_validates",
                "init_proposer": {"address": validator},
            }
            if cons_name == "xpoa":
                args["config"]["bft_config"] = {}
        elif cons_name in ("tdpos", "xpos"):
            args["name"] = "tdpos"
            args["config"] = {
                "version": version,
                "timestamp": "1559021720000000000",
                "proposer_num": str(len(validator)),
                "period": "3000",
                "alternate_interval": "3000",
                "term_interval": "6000",
                "block_num": "10",
                "vote_unit_price": "1",
                "init_proposer": {"1": validator},
            }
            if cons_name == "xpos":
                args["config"]["bft_config"] = {}
        elif cons_name == "pow":
            args["name"] = cons_name
            args["config"] = {
                "version": version,
                "defaultTarget": "545259519",
                "adjustHeightGap": "5",
                "expectedPeriod": "15",
                "maxTarget": "486604799",
            }
        elif cons_name == "single":
            args["name"] = cons_name
            args["config"] = {
                "version": version,
                "miner": "TeyyPLpp9L7QAcxHangtcHTu7HUZ6iydY",
                "period": "3000",
            }
        elif cons_name == "poa2raft":
            args["version"] = version
            args["expand_consensus"] = {
                "name": "poa2",
                "config": {"init_validators": {"validators": validator}},
            }
            args["safety_consensus"] = {
                "name": "raft",
                "config": {"block_num": 10, "period": 3000},
            }

        elif cons_name == "poaraft2":
            args["version"] = version
            args["expand_consensus"] = {
                "name": "poa",
                "config": {"init_validators": {"validators": validator}},
            }
            args["safety_consensus"] = {
                "name": "raft2",
                "config": {"block_num": 10, "period": 3000},
            }
        elif cons_name == "poa2raft2":
            args["version"] = version
            args["expand_consensus"] = {
                "name": "poa2",
                "config": {"init_validators": {"validators": validator}},
            }
            args["safety_consensus"] = {
                "name": "raft2",
                "config": {"block_num": 10, "period": 3000},
            }
        elif cons_name == "poaraft":
            args["version"] = version
            args["expand_consensus"] = {
                "name": "poa",
                "config": {"init_validators": {"validators": validator}},
            }
            args["safety_consensus"] = {
                "name": "raft",
                "config": {"block_num": 10, "period": 3000},
            }
        else:
            args = {}
        update_json["trigger"]["args"] = args
        print(json.dumps(update_json))
        desc = os.path.join(self.conf.client_path, "update.json")
        if not os.path.exists(desc):
            file2 = open(desc, mode="a", encoding="UTF-8")
            file2.close()
        with open(desc, "w") as desc_file:
            json.dump(update_json, desc_file)
            desc_file.close()
        return err, version

    def propose_update(self):
        """
        发起升级的提案
        """
        res = ["proposal", "propose", "--proposal", "update.json"]
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd)
        if err != 0:
            return err, result
        propose_id = self.xlib.get_value_from_res(result)
        return err, propose_id

    def vote_update(self, propose_id, amount=60000000000000000000):
        """
        为提案投票
        """
        res = ["proposal", "vote", "--pid", propose_id, "--amount", amount]
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd)
        return err, result

    def query_propose(self, propose_id):
        """
        查询提案内容
        """
        res = ["proposal", "query", "--pid", propose_id]
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd)
        return err, result

    def thaw_propose(self, propose_id):
        """
        撤销提案
        """
        res = ["proposal", "thaw", "--pid", propose_id]
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd)
        return err, result

    def update_consensus(self, cons_name, validator, **kwargs):
        """
        升级共识
        cons_name: 共识名称
        validator: 矿工列表
        version: 共识版本，不设置则自动读取当前版本
        """
        err, version = self.gen_cons_json(cons_name, validator, **kwargs)
        if err != 0:
            return err, "生成json失败 " + version, ""

        err, propose_id = self.propose_update()
        if err != 0:
            return err, "发起提案失败:" + propose_id, ""

        err, result = self.vote_update(propose_id)
        if err != 0:
            return err, "投票失败：" + result, ""

        err, result = self.query_propose(propose_id)
        if err != 0:
            return err, "查询提案状态失败：" + result, ""
        # 返回升级后的version、提案id
        return err, version, propose_id

    def check_update(self, cons_name, validator, version):
        """
        检查升级后的结果
        """
        for _ in range(5):
            err, result = self.xlib.consensus_status()
            if err != 0:
                return err, result
            result = json.loads(result)
            validators_info = json.loads(result["validators_info"])
            validators_now = validators_info["validators"]
            if validators_now is not None:
                break

        # single模式，node1为矿工
        if cons_name == "single":
            validator = [self.conf.addrs[0]]
        # pow模式，不需比较矿工候选人
        if cons_name == "pow":
            validator = validators_now

        if result["version"] != str(version):
            err = 1
            result = "版本错误: " + str(result) + " 预期version " + str(version)
        elif "raft" not in cons_name and result["consensus_name"] != cons_name:
            err = 1
            result = "共识错误: " + str(result) + " 预期共识 " + str(cons_name)
        elif sorted(validators_now) != sorted(validator):
            err = 1
            result = "候选人错误: " + str(result) + " 预期候选人 " + str(validator)
        else:
            err = 0
            result = ""
        return err, result
