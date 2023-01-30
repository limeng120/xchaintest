# !/usr/bin/env python3
"""
Common lib for all consensus
"""

import os
import json

from .xclient_ops import Xclient
from .xclient_ops import Shell
from .xclient_libs import Xlibs
from .event_lib import Event
from .parachain_lib import ParaChain
from .update_lib import Update

class Common(object):
    """
    各个共识的通用功能，包括
    """
    #初始化
    def __init__(self,conf):
        """
        获取配置，配置的内容包括：
        端口ports, 默认端口
        """
        self.conf = conf

        #定义xclient, 默认端口的xclient，执行shell，可用的lib，需要传入配置
        self.xclient = Xclient(conf)
        self.sh = Shell()
        self.xlib = Xlibs(conf)
        self.event = Event(conf)
        self.pchain = ParaChain(conf)
        self.update = Update(conf)

    #查看区块高度
    def TrunkHeight(self, **kwargs):
        """
        Query Block Height
        """
        res = []
        for n in self.conf.hosts.values():
            err, result = self.xlib.QueryBlockHeight(host=n)
            if err != 0:
                return err, res
            else:
                res.append(int(result))
        return err, res


    #查看分叉率
    def BifurcationRatio(self, **kwargs):
        """
        Query Bifurcation Ratio
        """
        res = []
        for n in self.conf.hosts.values():
            s = ("status", "-B", "-H", n)
            cmd = " ".join(s)
            err, result = self.xclient.exec(cmd, other="|grep bifurcationRatio|awk '{print $2}'", **kwargs)
            if err != 0:
                return err, res
            else:
                res.append(result)
        return err, res

    # 检查账户余额，不足amount，则转入amount
    def TranferWhenNotEnough(self, acc, amount, **kwargs):
        """
        acc 接收转账的账号，可以是普通账户，可以是acl账户
        amount 转账金额
        """
        # 检查合约账号余额，余额不足1000000000，转账
        err, balance1 = self.xlib.Balance(account=acc, **kwargs)
        if err != 0:
            return err, balance1
        if int(balance1) < int(amount):
            #转账测试
            err, result = self.xlib.Transfer(to=acc, amount=amount, keys="data/keys", **kwargs)
            if err != 0:
                return err, result
            txid = result
            err, result = self.xlib.WaitTxOnChain(txid, **kwargs)
            if err != 0:
                return err, result
            err, balance2 = self.xlib.Balance(account=acc, **kwargs)
            if err != 0:
                return err, balance2
            if int(balance2) - int(balance1) < int(amount):
                err = 1
                result = "转账后，金额增加数目不对"
                return err, result  
        return 0, balance1

    #基本功能测试
    def BasicFunction(self, **kwargs):
        """
        Test Basic Function
        """
        account = "2111111111111111"
        name = kwargs["name"] if "name" in kwargs.keys() else self.conf.name
        acl_account = "XC" + account + "@" + name
        amount="1000000000"
        addr = self.conf.client_addr

        #创建合约账户测试
        err, result = self.xlib.CreateContractAccount(account=account, keys="data/keys", **kwargs)
        #创建失败 且 账户不存在，返回
        if err != 0 and "account already exists" not in result:
            return err, result
        if err == 0:
            # 等两个块，让创建合约账号被确认，再执行下面的测试
            self.xlib.WaitNumHeight(2, name)

        # 检查合约账号余额，余额不足1000000000，转账
        err, result = self.TranferWhenNotEnough(acl_account, amount, **kwargs)
        if err != 0:
            return err, result

        # 部署go native合约
        cname = "hello_go"
        file = "goTemplate/counter"
        deploy = {
            "creator": addr
        }
        desc = json.dumps(deploy)
        err, result = self.xlib.DeployContract("native", "go", cname, file, acl_account, desc, **kwargs)
        if err != 0 and "already exists" not in result:
            return err, result
        if err == 0:
            # 等待tx上链
            txid = self.xlib.GetTxidFromRes(result)
            err, result = self.xlib.WaitTxOnChain(txid, **kwargs)
            assert err == 0, result

        # 合约调用测试
        invoke = {
            "key": "dudu"
        }
        desc = json.dumps(invoke)
        err, result = self.xlib.InvokeContract("native", cname, "increase", desc, **kwargs)
        if err != 0:
            return err, result

        # 合约查询测试
        query = {
            "key": "dudu"
        }
        desc = json.dumps(query)
        err, result = self.xlib.QueryContract("native", cname, "get", desc, **kwargs)

        # 给node2 转账
        err, result = self.TranferWhenNotEnough(self.conf.addrs[1], amount, **kwargs)
        return err, result

        
