# !/usr/bin/env python3
"""
lib for event
"""

import os
import json
import time
import subprocess

from .xclient_libs import Xlibs
from .xclient_ops import Xclient
from .xclient_ops import record

class Event(object):
    """
    事件订阅相关
    """
    #初始化
    def __init__(self, conf):
        self.conf = conf
        self.xlib = Xlibs(conf)
        self.xclient = Xclient(conf)

    # 启动./bin/xchain-cli watch
    def WatchEvent(self, filter, logfile, *args, **kwargs):
        """
        监控事件
        filter 过滤条件，json格式
        logfile 存储watch命令行的输出
        """
        res = ['watch']
        for x in args:
            res.append("--" + x)
        if filter != "\'\'":
            res.append("--filter")
            res.append(filter)
        cmd = " ".join(str(x) for x in res)
        self.xclient.exec_host_backend(cmd, logfile, **kwargs)

    # kill ./bin/xchain-cli watch进程
    def KillWatchCli(self):
        cmd = "ps aux|grep xchain-cli|grep " + self.conf.default_host \
                + "|grep -v grep| grep watch |awk -F ' ' '{print $2}' | xargs kill -9 >/dev/null 2>&1"
        err, result = subprocess.getstatusoutput(cmd)
        if self.conf.all_log:
            record(cmd, result)
        elif err != 0:
            record(cmd, result)
        return err, result

    # 调用多种Counter合约，触发合约事件
    def TriggerEvent(self):
        """
        invokeRes：合约执行结果，用dict保存
        """
        invokeRes = []
        key = "dudu"
        method = "increase"
        invokeArgs = {"key": key}
        args = json.dumps(invokeArgs)

        invokeRes = []

        # 用node2的key调用合约
        cname = "c_counter"
        err, result = self.xlib.InvokeContract("wasm", cname, method, args, keys=self.conf.keys[1])
        assert err == 0, "调用" + cname + "合约失败： " + result
        txid = self.xlib.GetTxidFromRes(result)  
        value = self.xlib.GetValueFromRes(result) 
        invokeRes.append({"txid": txid, "contract": cname, "name": method, "key": key, "value": value})
        
        # 调用3种counter合约的increase方法
        cname = "c_counter"
        err, result = self.xlib.InvokeContract("wasm", cname, method, args)
        assert err == 0, "调用" + cname + "合约失败： " + result
        print("调用结果" + str(result))
        txid = self.xlib.GetTxidFromRes(result) 
        value = self.xlib.GetValueFromRes(result)   
        invokeRes.append({"txid": txid, "contract": cname, "name": method, "key": key, "value": value})
 
        for cname in ["java_counter", "gn_counter"]:
            err, result = self.xlib.InvokeContract("native", cname, method, args)
            assert err == 0, "调用" + cname + "合约失败： " + result
            txid = self.xlib.GetTxidFromRes(result)  
            value = self.xlib.GetValueFromRes(result)  
            invokeRes.append({"txid": txid, "contract": cname, "name": method, "key": key, "value": value})
        return invokeRes

    # 根据filter参数，构造预期的event
    def GenExpectEvent(self, filter, invokeRes, emptyEvent):
        """
        filter : 监听事件的过滤条件
        invokeRes: 合约调用的结果
        expectEvent: 返回值，预期的事件信息 
        emptyEvent: 是否生成空的event
        """
        tmpEvent = {}
        if emptyEvent == True:
            return tmpEvent
        # 1.不同合约事件的body有区别，分别构造event body
        for res in invokeRes:
            if res["contract"] == "c_counter":
                body = res["value"]
            elif res["contract"] == "java_counter":
                body = '{"value":"' + res["value"] + '","key":"dudu"}'
            else:
                body = '{"key":"dudu","value":"' + res["value"] + '"}'
            event = {"contract": res["contract"], "name": "increase", "body": body}
            tmpEvent[res["txid"]] = event  
        
        expectEvent = {}
        # 2.指定合约事件的名称，只把该合约的事件加到expectEvent
        if "contract" in filter and "event_name" in filter:
            # 从filter中获取合约名 事件名
            cname_in_filter = json.loads(filter.strip('\''))["contract"]
            event_in_filter = json.loads(filter.strip('\''))["event_name"]
            for txid, event in tmpEvent.items():
                if cname_in_filter in event["contract"] and event_in_filter in event["name"]:
                    expectEvent[txid] = event
        
        # 指定事件名
        elif "event_name" in filter:
            # 从filter中获取合约名 事件名
            event_in_filter = json.loads(filter.strip('\''))["event_name"]
            for txid, event in tmpEvent.items():
                if event_in_filter in event["name"]:
                    expectEvent[txid] = event

        # 指定合约名
        elif "contract" in filter:
            # 从filter中获取合约名
            cname_in_filter = json.loads(filter.strip('\''))["contract"]
            print(cname_in_filter)
            for txid, event in tmpEvent.items():
                if cname_in_filter in event["contract"]:
                    expectEvent[txid] = event

        # 指定发起人或者签名人，预期只收到第1个事件
        elif "initiator" in filter or "auth_require" in filter:
            for txid, event in tmpEvent.items():
                expectEvent[txid] = event
                break
        
        else:
            expectEvent = tmpEvent
        return expectEvent  

    # 读取文件内容
    def ReadEventFile(self, file):
        """
        file: 存储监听事件结果的文件
        block: json格式，监听到的区块
        """
        filePath = os.path.join(self.conf.client_path, file)
        with open(filePath) as eventfile:
            content = eventfile.read().replace("}\n{", "},{")
            content = "[" + content + "]"
            print("实际的事件:" + str(content))
            block = json.loads(content)
            return block

    # 检查文件记录的event，与预期的event，是否一致
    def CheckEvent(self, expectEvent, file):
        """
        expectEvent: 预期的事件
        file:    记录event的文件
        """
        block = self.ReadEventFile(file)
        succ = 0
        # 从文件内容找预期的tx，验证tx的event
        for b in block:
            txs = b["txs"]
            for tx in txs:
                # 找到预期的tx
                if tx["txid"] in expectEvent:
                    # 如果tx的event不符合预期，失败返回
                    if tx["events"][0] != expectEvent[tx["txid"]]:
                        print("txid: " + tx["txid"])
                        print("expect event :" + str(expectEvent[tx["txid"]]))
                        print("real event   :" + str(tx["events"][0]))
                        return 1, "事件不符合预期"
                    # 否则，匹配成功的tx数，增加1
                    else:
                        succ += 1
        if succ != len(expectEvent):
            return 1, "事件个数不符合预期"
        else:
            return 0, ""

    # 检查设置了"exclude_tx_event": True的结果
    def CheckExcludeEvent(self, expectEvent, file):
        """
        expectEvent: 预期的事件
        file:    记录event的文件
        """
        block = self.ReadEventFile(file)
        succ = 0
        # 从文件内容找预期的tx，验证tx的event
        for b in block:
            txs = b["txs"]
            for tx in txs:
                # 找到预期的tx
                if tx["txid"] in expectEvent:
                    if "events" in tx:
                        return 1, "预期不存在event字段，不符合预期"
                    else:
                        succ += 1
        if succ != len(expectEvent):
            return 1, "监听到的tx个数不符合预期"
        else:
            return 0, ""

    def ContractEventTest(self, filter, eventfile, emptyEvent=False, wait=0):
        """
        合约事件订阅测试全流程：
        1.启动./bin/xchain-cli watch开始监听
        2.执行合约调用，触发事件
        3.kill xchain-cli进程
        4.查看监听结果是否与步骤二的结果一致

        Args:
        filter 订阅事件的过滤参数
        """
        filter = "'" + filter + "'"

        # 1. 启动cli进程，监听事件
        self.WatchEvent(filter, eventfile, "skip-empty-tx", "oneline")

        if wait != 0:
            self.xlib.WaitNumHeight(wait)

        # 2. 触发事件
        invokeRes = self.TriggerEvent()

        # 3. 等待步骤2的tx上链
        for item in invokeRes:
            err, result = self.xlib.WaitTxOnChain(item["txid"], first_sleep=0)

        # 4. 停止cli进程
        self.KillWatchCli()

        if err != 0:
            return err, result

        # 5. 拼接预期的event
        expectEvent = self.GenExpectEvent(filter, invokeRes, emptyEvent)
        print("预期的事件： " + str(expectEvent))

        # 6. 比对实际接收的event，与预期event是否一致
        if "exclude_tx_event" in filter:
            err, result = self.CheckExcludeEvent(expectEvent, eventfile)
        else:
            err, result = self.CheckEvent(expectEvent, eventfile)
        return err, result

    def TransEventTest(self, filter, eventfile, emptyEvent=False):
        """
        转账交易订阅测试全流程：
        1.启动./bin/xchain-cli watch开始监听
        2.执行转账，触发事件
        3.kill xchain-cli进程
        4.查看监听结果是否与步骤二的结果一致

        Args:
        filter 订阅事件的过滤参数
        """
        filter = "'" + filter + "'"
        # 1. 启动cli进程，监听事件
        self.WatchEvent(filter, eventfile, "skip-empty-tx", "oneline")

        # 2. 触发事件
        err, result = self.xlib.Transfer(to="qatest", amount=1)
        if err != 0:
            return err, result

        # 3. 等待步骤2的tx上链
        txid = self.xlib.GetTxidFromRes(result)
        err, result = self.xlib.WaitTxOnChain(txid)

        # 4. 停止cli进程
        self.KillWatchCli()

        if err != 0:
            return err, result

        # 5. 比对实际接收的event，预期包含步骤2的txid
        block = self.ReadEventFile(eventfile)
        print("预期的事件： " + txid)
        for b in block:
            txs = b["txs"] 
            for tx in txs:
                if tx["txid"] == txid:
                    return 0, "succ, 找到预期的event"
        return 1, "存在不符合预期的tx, txid:" + tx["txid"] + "预期：" + txid

    # 检查文件记录的event，与预期的event，是否一致
    def CheckEvmEvent(self, expectEvent, file):
        """
        expectEvent: 预期的事件
        file:    记录event的文件
        """
        block = self.ReadEventFile(file)
        # 从文件内容找预期的tx，验证tx的event
        for b in block:
            txs = b["txs"]
            for tx in txs:
                # 找到预期的tx
                if tx["txid"] == expectEvent["txid"]:
                    # 如果tx的event不符合预期，失败返回
                    if tx["events"] != expectEvent["events"]:
                        print("txid: " + tx["txid"])
                        print("expect event :" + str(expectEvent["events"]))
                        print("real event   :" + str(tx["events"]))
                        return 1, "事件不符合预期"
                    # 否则，匹配成功的tx数，增加1
                    else:
                        return 0, ""

    def EvmEventTest(self, filter, eventfile, **kwargs):
        """
        合约事件订阅测试全流程：
        1.启动./bin/xchain-cli watch开始监听
        2.执行合约调用，触发事件
        3.kill xchain-cli进程
        4.查看监听结果是否与步骤二的结果一致

        Args:
        filter 订阅事件的过滤参数
        contract 合约名
        method 合约方法
        args 合约参数
        events 预期的事件，数组类型
        """
        filter = "'" + filter + "'"

        # 1. 启动cli进程，监听事件
        self.WatchEvent(filter, eventfile, "skip-empty-tx", "oneline")

        # 2. 触发事件
        err, result = self.xlib.InvokeContract("evm", kwargs["contract"], kwargs["method"], kwargs["args"])
        assert err == 0, "调用" + kwargs["contract"] + "合约失败： " + result
        txid = self.xlib.GetTxidFromRes(result) 

        # 3. 等待步骤2的tx上链
        err, result = self.xlib.WaitTxOnChain(txid)
        assert err == 0, txid + "上链失败"

        # 4. 停止cli进程
        self.KillWatchCli()

        if err != 0:
            return err, result

        # 5. 预期的event
        expectEvent = {}
        expectEvent["txid"] = txid
        expectEvent["events"] = kwargs["events"]
        print("预期的事件： " + str(expectEvent))

        # 6. 比对实际接收的event，与预期event是否一致
        err, result = self.CheckEvmEvent(expectEvent, eventfile)
        return err, result