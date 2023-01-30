"""
说明: 测试事件订阅的异常场景
"""
import json
import pytest
import time
import os

class TestEventErr():

    eventfile = "eventlog"

    # case01 最大订阅连接数，超过则报错
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("测试最大订阅数")
        maxEvent = 5
        # 1.启动超限制的监听进程
        for i in range(maxEvent + 1):
            logfile = "log" + str(i)
            input.test.event.WatchEvent("\'\'", logfile)
            time.sleep(2)

        time.sleep(3)
        # 2.清理xchain-cli进程
        input.test.event.KillWatchCli()
        # 3.预期第6个进程，无法正常监听事件
        _, result = input.test.sh.exec_shell(input.conf.client_path, "cat log5")
        expect = "rpc error: code = Unknown desc = maximum connections exceeded"
        assert result == expect, "超过最大订阅数未出现失败，不合预期:" + result
        time.sleep(10)

    # case02 指定高度区间订阅，start大于end
    @pytest.mark.abnormal
    def test_case02(self, input):
        print("指定高度区间订阅，start大于end")
        err, curHeight = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询当前高度失败：" + curHeight
        startHeight = int(curHeight) + 100
        endHeight = int(curHeight) - 100
        filter = {
            "range": {
                "start": str(startHeight),
                "end": str(endHeight)
            }
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile, emptyEvent=True)
        assert err == 0, "指定高度区间订阅，start大于end，测试失败：" + result
      
    # case03 指定高度区间订阅，end小于当前区块高度
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("指定高度区间订阅，end小于当前区块高度")
        err, curHeight = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询当前高度失败：" + curHeight
        endHeight = int(curHeight) - 5
        filter = {
            "range": {
                "end": str(endHeight)
            }
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile, emptyEvent=True)
        assert err == 0, "指定高度区间订阅，end小于当前区块高度，测试失败：" + result

    # case04 设置合约名、不存在的事件名，订阅
    @pytest.mark.abnormal
    def test_case04(self, input):
        print("设置to_addr，订阅")
        filter = {
            "contract": "c_counter",
            "event_name": "increaseA"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile, emptyEvent=True)
        assert err == 0, "设置合约名、不存在的事件名，订阅，测试失败：" + result