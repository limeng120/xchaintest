# !/usr/bin/env python3
"""
lib for event
"""

import os
import json
import subprocess

from .xclient_libs import Xlibs
from .xclient_ops import Xclient
from .xclient_ops import record


class Event:
    """
    事件订阅相关
    """

    def __init__(self, conf):
        self.conf = conf
        self.xlib = Xlibs(conf)
        self.xclient = Xclient(conf)

    def watch_event(self, event_filter, logfile, *args, **kwargs):
        """
        启动./bin/xchain-cli watch，监控事件
        event_filter 过滤条件，json格式
        logfile 存储watch命令行的输出
        """
        res = ["watch"]
        for x in args:
            res.append("--" + x)
        if event_filter != "''":
            res.append("--filter")
            res.append(event_filter)
        cmd = " ".join(str(x) for x in res)
        self.xclient.exec_host_backend(cmd, logfile, **kwargs)

    def kill_watch_cli(self):
        """
        kill ./bin/xchain-cli watch进程
        """
        cmd = (
            "ps aux|grep xchain-cli|grep "
            + self.conf.default_host
            + "|grep -v grep| grep watch |awk -F ' ' '{print $2}' | xargs kill -9 >/dev/null 2>&1"
        )
        err, result = subprocess.getstatusoutput(cmd)
        if self.conf.all_log:
            record(cmd, result)
        elif err != 0:
            record(cmd, result)
        return err, result

    def trigger_event(self):
        """
        调用多种Counter合约，触发合约事件
        invokeRes：合约执行结果，用dict保存
        """
        invoke_res = []
        key = "dudu"
        method = "increase"
        invoke_args = {"key": key}
        args = json.dumps(invoke_args)

        invoke_res = []

        # 调用counter合约的increase方法
        cname = "c_counter"
        err, result = self.xlib.invoke_contract("wasm", cname, method, args)
        assert err == 0, "调用" + cname + "合约失败： " + result
        print("调用结果" + str(result))
        txid = self.xlib.get_txid_from_res(result)
        value = self.xlib.get_value_from_res(result)
        invoke_res.append(
            {
                "txid": txid,
                "contract": cname,
                "name": method,
                "key": key,
                "value": value,
            }
        )
        # cname = "gn_counter"
        # # for cname in ["java_counter", "gn_counter"]:
        # err, result = self.xlib.invoke_contract("native", cname, method, args)
        # assert err == 0, "调用" + cname + "合约失败： " + result
        # txid = self.xlib.get_txid_from_res(result)
        # value = self.xlib.get_value_from_res(result)
        # invoke_res.append(
        #     {
        #         "txid": txid,
        #         "contract": cname,
        #         "name": method,
        #         "key": key,
        #         "value": value,
        #     }
        # )
        return invoke_res

    def gen_expect_event(self, event_filter, invoke_res, empty_event):
        """
        根据filter参数，构造预期的event
        event_filter : 监听事件的过滤条件
        invoke_res: 合约调用的结果
        expect_event: 返回值，预期的事件信息
        empty_event: 是否生成空的event
        """
        tmp_event = {}
        if empty_event:
            return tmp_event
        # 1.不同合约事件的body有区别，分别构造event body
        for res in invoke_res:
            body = res["value"]
            event = {"contract": res["contract"], "name": "increase", "body": body}
            tmp_event[res["txid"]] = event

        expect_event = {}
        # 2.指定合约事件的名称，只把该合约的事件加到expectEvent
        if "contract" in event_filter and "event_name" in event_filter:
            # 从filter中获取合约名 事件名
            cname_in_filter = json.loads(event_filter.strip("'"))["contract"]
            event_in_filter = json.loads(event_filter.strip("'"))["event_name"]
            for txid, event in tmp_event.items():
                if (
                    cname_in_filter in event["contract"]
                    and event_in_filter in event["name"]
                ):
                    expect_event[txid] = event

        # 指定事件名
        elif "event_name" in event_filter:
            # 从filter中获取合约名 事件名
            event_in_filter = json.loads(event_filter.strip("'"))["event_name"]
            for txid, event in tmp_event.items():
                if event_in_filter in event["name"]:
                    expect_event[txid] = event

        # 指定合约名
        elif "contract" in event_filter:
            # 从filter中获取合约名
            cname_in_filter = json.loads(event_filter.strip("'"))["contract"]
            print(cname_in_filter)
            for txid, event in tmp_event.items():
                if cname_in_filter in event["contract"]:
                    expect_event[txid] = event

        # 指定发起人或者签名人，预期只收到第1个事件
        elif "initiator" in event_filter or "auth_require" in event_filter:
            for txid, event in tmp_event.items():
                expect_event[txid] = event
                break

        else:
            expect_event = tmp_event
        return expect_event

    def read_event_file(self, file):
        """
        读取文件内容
        file: 存储监听事件结果的文件
        block: json格式，监听到的区块
        """
        file_path = os.path.join(self.conf.client_path, file)
        with open(file_path) as eventfile:
            content = eventfile.read().replace("}\n{", "},{")
            content = "[" + content + "]"
            print("实际的事件:" + str(content))
            block = json.loads(content)
            return block

    def check_event(self, expect_event, file):
        """
        检查文件记录的event，与预期的event，是否一致
        expect_event: 预期的事件
        file:    记录event的文件
        """
        block = self.read_event_file(file)
        succ = 0
        # 从文件内容找预期的tx，验证tx的event
        for b in block:
            txs = b["txs"]
            for tx in txs:
                # 找到预期的tx
                if tx["txid"] in expect_event:
                    # 如果tx的event不符合预期，失败返回
                    if tx["events"][0] != expect_event[tx["txid"]]:
                        print("txid: " + tx["txid"])
                        print("expect event :" + str(expect_event[tx["txid"]]))
                        print("real event   :" + str(tx["events"][0]))
                        return 1, "事件不符合预期"
                    # 匹配成功的tx数，增加1
                    succ += 1
        if succ != len(expect_event):
            return 1, "事件个数不符合预期"
        return 0, ""

    def check_exclude_event(self, expect_event, file):
        """
        检查设置了"exclude_tx_event": True的结果
        expect_event: 预期的事件
        file:    记录event的文件
        """
        block = self.read_event_file(file)
        succ = 0
        # 从文件内容找预期的tx，验证tx的event
        for b in block:
            txs = b["txs"]
            for tx in txs:
                # 找到预期的tx
                if tx["txid"] in expect_event:
                    if "events" in tx:
                        return 1, "预期不存在event字段，不符合预期"
                    succ += 1
        if succ != len(expect_event):
            return 1, "监听到的tx个数不符合预期"
        return 0, ""

    def contract_event_test(self, event_filter, eventfile, empty_event=False, wait=0):
        """
        合约事件订阅测试全流程：
        1.启动./bin/xchain-cli watch开始监听
        2.执行合约调用，触发事件
        3.kill xchain-cli进程
        4.查看监听结果是否与步骤二的结果一致

        Args:
        event_filter 订阅事件的过滤参数
        """
        event_filter = "'" + event_filter + "'"

        # 1. 启动cli进程，监听事件
        self.watch_event(event_filter, eventfile, "skip-empty-tx", "oneline")

        if wait != 0:
            self.xlib.wait_num_height(wait)

        # 2. 触发事件
        invoke_res = self.trigger_event()

        # 3. 等待步骤2的tx上链
        for item in invoke_res:
            err, result = self.xlib.wait_tx_on_chain(item["txid"], first_sleep=0)

        # 4. 停止cli进程
        self.kill_watch_cli()

        if err != 0:
            return err, result

        # 5. 拼接预期的event
        expect_event = self.gen_expect_event(event_filter, invoke_res, empty_event)
        print("预期的事件： " + str(expect_event))

        # 6. 比对实际接收的event，与预期event是否一致
        if "exclude_tx_event" in event_filter:
            err, result = self.check_exclude_event(expect_event, eventfile)
        else:
            err, result = self.check_event(expect_event, eventfile)
        return err, result

    def trans_event_test(self, event_filter, eventfile):
        """
        转账交易订阅测试全流程：
        1.启动./bin/xchain-cli watch开始监听
        2.执行转账，触发事件
        3.kill xchain-cli进程
        4.查看监听结果是否与步骤二的结果一致

        Args:
        event_filter 订阅事件的过滤参数
        """
        event_filter = "'" + event_filter + "'"
        # 1. 启动cli进程，监听事件
        self.watch_event(event_filter, eventfile, "skip-empty-tx", "oneline")

        # 2. 触发事件
        err, result = self.xlib.transfer(to="qatest", amount=1)
        if err != 0:
            return err, result

        # 3. 等待步骤2的tx上链
        txid = self.xlib.get_txid_from_res(result)
        err, result = self.xlib.wait_tx_on_chain(txid)

        # 4. 停止cli进程
        self.kill_watch_cli()

        if err != 0:
            return err, result

        # 5. 比对实际接收的event，预期包含步骤2的txid
        block = self.read_event_file(eventfile)
        print("预期的事件： " + txid)
        for b in block:
            txs = b["txs"]
            for tx in txs:
                if tx["txid"] == txid:
                    return 0, "succ, 找到预期的event"
        return 1, "存在不符合预期的tx, txid:" + txid

    def check_evm_event(self, expect_event, file):
        """
        检查文件记录的event，与预期的event，是否一致
        expect_event: 预期的事件
        file:    记录event的文件
        """
        block = self.read_event_file(file)
        # 从文件内容找预期的tx，验证tx的event
        for b in block:
            txs = b["txs"]
            for tx in txs:
                # 找到预期的tx
                if tx["txid"] == expect_event["txid"]:
                    # 如果tx的event不符合预期，失败返回
                    if tx["events"] != expect_event["events"]:
                        print("txid: " + tx["txid"])
                        print("expect event :" + str(expect_event["events"]))
                        print("real event   :" + str(tx["events"]))
                        return 1, "事件不符合预期"
                    return 0, ""
        return 1, "未找到预期的tx"

    def evm_event_test(self, event_filter, eventfile, **kwargs):
        """
        合约事件订阅测试全流程：
        1.启动./bin/xchain-cli watch开始监听
        2.执行合约调用，触发事件
        3.kill xchain-cli进程
        4.查看监听结果是否与步骤二的结果一致

        Args:
        event_filter 订阅事件的过滤参数
        contract 合约名
        method 合约方法
        args 合约参数
        events 预期的事件，数组类型
        """
        event_filter = "'" + event_filter + "'"

        # 1. 启动cli进程，监听事件
        self.watch_event(event_filter, eventfile, "skip-empty-tx", "oneline")

        # 2. 触发事件
        err, result = self.xlib.invoke_contract(
            "evm", kwargs["contract"], kwargs["method"], kwargs["args"]
        )
        assert err == 0, "调用" + kwargs["contract"] + "合约失败： " + result
        txid = self.xlib.get_txid_from_res(result)

        # 3. 等待步骤2的tx上链
        err, result = self.xlib.wait_tx_on_chain(txid)
        assert err == 0, txid + "上链失败"

        # 4. 停止cli进程
        self.kill_watch_cli()

        if err != 0:
            return err, result

        # 5. 预期的event
        expect_event = {}
        expect_event["txid"] = txid
        expect_event["events"] = kwargs["events"]
        print("预期的事件： " + str(expect_event))

        # 6. 比对实际接收的event，与预期event是否一致
        err, result = self.check_evm_event(expect_event, eventfile)
        return err, result
