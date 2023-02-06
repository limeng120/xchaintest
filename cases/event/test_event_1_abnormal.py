"""
说明: 测试事件订阅的异常场景
"""
import json
import time
import pytest


class TestEventErr:
    """
    测试事件订阅的异常场景
    """

    eventfile = "eventlog"

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        最大订阅连接数，超过则报错
        """
        print("测试最大订阅数")
        max_event = 5
        # 1.启动超限制的监听进程
        for i in range(max_event + 1):
            logfile = "log" + str(i)
            input_args.test.event.watch_event("''", logfile)
            time.sleep(2)

        time.sleep(3)
        # 2.清理xchain-cli进程
        input_args.test.event.kill_watch_cli()
        # 3.预期第6个进程，无法正常监听事件
        _, result = input_args.test.sh.exec_shell(
            input_args.conf.client_path, "cat log5"
        )
        expect = "rpc error: code = Unknown desc = maximum connections exceeded"
        assert result == expect, "超过最大订阅数未出现失败，不合预期:" + result
        time.sleep(10)

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        指定高度区间订阅，start大于end
        """
        print("指定高度区间订阅，start大于end")
        err, cur_height = input_args.test.xlib.query_height()
        assert err == 0, "查询当前高度失败：" + cur_height
        start_height = int(cur_height) + 100
        end_height = int(cur_height) - 100
        event_filter = {"range": {"start": str(start_height), "end": str(end_height)}}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile, empty_event=True
        )
        assert err == 0, "指定高度区间订阅，start大于end，测试失败：" + result

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        指定高度区间订阅，end小于当前区块高度
        """
        print("指定高度区间订阅，end小于当前区块高度")
        err, cur_height = input_args.test.xlib.query_height()
        assert err == 0, "查询当前高度失败：" + cur_height
        end_height = int(cur_height) - 5
        event_filter = {"range": {"end": str(end_height)}}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile, empty_event=True
        )
        assert err == 0, "指定高度区间订阅，end小于当前区块高度，测试失败：" + result

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        case04 设置合约名、不存在的事件名，订阅
        """
        print("设置to_addr，订阅")
        event_filter = {"contract": "c_counter", "event_name": "increaseA"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile, empty_event=True
        )
        assert err == 0, "设置合约名、不存在的事件名，订阅，测试失败：" + result
