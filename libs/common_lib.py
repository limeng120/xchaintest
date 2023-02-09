# !/usr/bin/env python3
"""
Common lib for all consensus
"""

import json

from .xclient_ops import Xclient
from .xclient_ops import Shell
from .xclient_libs import Xlibs
from .event_lib import Event
from .parachain_lib import ParaChain
from .update_lib import Update


class Common:
    """
    各个共识的通用功能，包括
    """

    # 初始化
    def __init__(self, conf):
        """
        获取配置，配置的内容包括：
        端口ports, 默认端口
        """
        self.conf = conf

        # 定义xclient, 默认端口的xclient，执行shell，可用的lib，需要传入配置
        self.xclient = Xclient(conf)
        self.sh = Shell()
        self.xlib = Xlibs(conf)
        self.event = Event(conf)
        self.pchain = ParaChain(conf)
        self.update = Update(conf)

    # 查看区块高度
    def trunk_height(self, **kwargs):
        """
        Query Block Height
        """
        res = []
        for node in self.conf.hosts.values():
            err, result = self.xlib.query_height(host=node, **kwargs)
            if err != 0:
                return err, res
            res.append(int(result))
        return err, res

    # 查看分叉率
    def bifurcation_ratio(self, **kwargs):
        """
        Query Bifurcation Ratio
        """
        res = []
        for node in self.conf.hosts.values():
            status_args = ("status", "-B", "-H", node)
            cmd = " ".join(status_args)
            err, result = self.xclient.exec(
                cmd, other="|grep bifurcationRatio|awk '{print $2}'", **kwargs
            )
            if err != 0:
                return err, res
            res.append(result)
        return err, res

    # 检查账户余额，不足amount，则转入amount
    def tranfer_when_not_enough(self, acc, amount, **kwargs):
        """
        acc 接收转账的账号，可以是普通账户，可以是acl账户
        amount 转账金额
        """
        # 检查合约账号余额，余额不足1000000000，转账
        err, balance1 = self.xlib.get_balance(account=acc, **kwargs)
        if err != 0:
            return err, balance1
        if int(balance1) < int(amount):
            # 转账测试
            err, result = self.xlib.transfer(
                to=acc, amount=amount, keys="data/keys", **kwargs
            )
            if err != 0:
                return err, result
            txid = result
            err, result = self.xlib.wait_tx_on_chain(txid, **kwargs)
            if err != 0:
                return err, result
            err, balance2 = self.xlib.get_balance(account=acc, **kwargs)
            if err != 0:
                return err, balance2
            if int(balance2) - int(balance1) < int(amount):
                err = 1
                result = "转账后，金额增加数目不对"
                return err, result
        return 0, balance1

    # 基本功能测试
    def basic_function(self, **kwargs):
        """
        Test Basic Function
        """
        account = "2111111111111111"
        name = kwargs["name"] if "name" in kwargs.keys() else self.conf.name
        acl_account = "XC" + account + "@" + name
        amount = "1000000000"
        addr = self.conf.client_addr

        # 创建合约账户测试
        err, result = self.xlib.create_contract_account(
            account=account, keys="data/keys", **kwargs
        )
        # 创建失败 且 账户不存在，返回
        if err != 0 and "account already exists" not in result:
            return err, result
        if err == 0:
            # 等两个块，让创建合约账号被确认，再执行下面的测试
            self.xlib.wait_num_height(2, name)

        # 检查合约账号余额，余额不足1000000000，转账
        err, result = self.tranfer_when_not_enough(acl_account, amount, **kwargs)
        if err != 0:
            return err, result

        # 部署合约
        cname = "hello_cpp"
        file = "cppTemplate/counter.wasm"
        desc = json.dumps({"creator": addr})
        err, result = self.xlib.deploy_contract(
            "wasm", "cpp", cname, file, acl_account, desc, **kwargs
        )
        if err != 0 and "already exists" not in result:
            return err, result
        if err == 0:
            # 等待tx上链
            txid = self.xlib.get_txid_from_res(result)
            err, result = self.xlib.wait_tx_on_chain(txid, **kwargs)
            assert err == 0, result

        # 合约调用测试
        desc = json.dumps({"key": "dudu"})
        err, result = self.xlib.invoke_contract(
            "wasm", cname, "increase", desc, **kwargs
        )
        if err != 0:
            return err, result

        # 合约查询测试
        query = {"key": "dudu"}
        desc = json.dumps(query)
        err, result = self.xlib.query_contract("wasm", cname, "get", desc, **kwargs)

        # 给node2 转账
        err, result = self.tranfer_when_not_enough(self.conf.addrs[1], amount, **kwargs)
        return err, result
