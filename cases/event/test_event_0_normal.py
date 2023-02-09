"""
说明: 测试事件订阅
"""
import json
import pytest


class TestEvent:
    """
    测试事件订阅
    """

    eventfile = "eventlog"

    @pytest.mark.p0
    def test_case01(self, input_args):
        """
        不指定过滤参数，订阅
        """
        print("不指定过滤参数，订阅")
        err, result = input_args.test.event.contract_event_test("", self.eventfile)
        assert err == 0, "不指定过滤参数，订阅失败：" + result

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        指定高度区间订阅，start大于当前区块高度
        """
        print("指定高度区间订阅，start大于当前区块高度")
        err, cur_height = input_args.test.xlib.query_height()
        assert err == 0, "查询当前高度失败：" + cur_height
        start_height = int(cur_height) + 5
        end_height = int(cur_height) + 100
        event_filter = {"range": {"start": str(start_height), "end": str(end_height)}}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile, False, 5
        )
        assert err == 0, "start大于当前区块高度，订阅失败：" + result

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        指定高度区间订阅，start小于当前区块高度
        """
        print("指定高度区间订阅，start小于当前区块高度")
        err, cur_height = input_args.test.xlib.query_height()
        assert err == 0, "查询当前高度失败：" + cur_height
        start_height = int(cur_height) - 10
        end_height = int(cur_height) + 100
        event_filter = {"range": {"start": str(start_height), "end": str(end_height)}}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "start小于当前区块高度，订阅失败：" + result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        指定高度区间订阅，仅设置start
        """
        print("指定高度区间订阅，仅设置start")
        err, cur_height = input_args.test.xlib.query_height()
        assert err == 0, "查询当前高度失败：" + cur_height
        event_filter = {"range": {"start": str(cur_height)}}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "仅设置start，订阅失败：" + result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        指定高度区间订阅，仅设置end
        """
        print("指定高度区间订阅，仅设置end")
        err, cur_height = input_args.test.xlib.query_height()
        assert err == 0, "查询当前高度失败：" + cur_height
        end_height = int(cur_height) + 100
        event_filter = {"range": {"end": str(end_height)}}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "仅设置end，订阅失败：" + result

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        设置"exclude_tx": true
        不含tx，所以预期的event是空
        """
        print("设置exclude_tx: true")
        event_filter = {"exclude_tx": True}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile, empty_event=True
        )
        assert err == 0, "设置exclude_tx: true，订阅失败：" + result

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        设置"exclude_tx_event": true
        """
        print("设置exclude_tx_event: true")
        event_filter = {"exclude_tx_event": True}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置exclude_tx_event: true，订阅失败：" + result

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        设置合约名，订阅
        """
        print("设置合约名，订阅")
        event_filter = {"contract": "c_counter"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置合约名，订阅失败：" + result

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        设置合约名，事件名，订阅
        """
        print("设置合约名，订阅")
        event_filter = {"contract": "c_counter", "event_name": "increase"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置合约名，事件名，订阅失败：" + result

    @pytest.mark.p2
    def test_case10(self, input_args):
        """
        设置事件名，订阅
        """
        print("设置事件名，订阅")
        event_filter = {"event_name": "increase"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置事件名，订阅失败：" + result

    @pytest.mark.p2
    def test_case11(self, input_args):
        """
        设置发起人，订阅
        """
        print("设置发起人，订阅")
        event_filter = {"initiator": input_args.addrs[0]}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置发起人，订阅失败：" + result

    @pytest.mark.p2
    def test_case12(self, input_args):
        """
        设置auth_require，订阅
        """
        print("设置auth_require，订阅")
        event_filter = {"auth_require": input_args.addrs[0]}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置auth_require，订阅失败：" + result

    @pytest.mark.p2
    def test_case13(self, input_args):
        """
        设置from_addr，订阅
        """
        print("设置from_addr，订阅")
        event_filter = {"from_addr": input_args.client_addr}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.trans_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置from_addr，订阅失败：" + result

    @pytest.mark.p2
    def test_case14(self, input_args):
        """
        设置to_addr，订阅
        """
        print("设置to_addr，订阅")
        event_filter = {"to_addr": "qatest"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.trans_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "设置to_addr，订阅失败：" + result

    @pytest.mark.p2
    def test_case15(self, input_args):
        """
        contract参数支持正则
        """
        print("contract参数支持正则，订阅")
        event_filter = {"contract": "count"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "contract参数支持正则，订阅失败：" + result

    @pytest.mark.p2
    def test_case16(self, input_args):
        """
        event参数支持正则
        """
        print("event参数支持正则，订阅")
        event_filter = {"event_name": "inc"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.contract_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "event参数支持正则，订阅失败：" + result

    @pytest.mark.p2
    def test_case17(self, input_args):
        """
        initiator参数支持正则
        """
        print("initiator参数支持正则，订阅")
        addr1 = input_args.addrs[0]
        addr3 = input_args.addrs[2]
        event_filter = {"initiator": addr1 + "|" + addr3}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.trans_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "initiator参数支持正则，订阅失败：" + result

    @pytest.mark.p2
    def test_case18(self, input_args):
        """
        auth_require参数支持正则
        """
        print("auth_require参数支持正则，订阅")
        addr1 = input_args.addrs[0]
        addr3 = input_args.addrs[2]
        event_filter = {"auth_require": addr1 + "|" + addr3}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.trans_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "auth_require参数支持正则，订阅失败：" + result

    @pytest.mark.p2
    def test_case19(self, input_args):
        """
        from_addr参数支持正则
        """
        print("from_addr参数支持正则，订阅")
        addr1 = input_args.addrs[0]
        addr3 = input_args.addrs[2]
        event_filter = {"from_addr": addr1 + "|" + addr3}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.trans_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "from_addr参数支持正则，订阅失败：" + result

    @pytest.mark.p2
    def test_case20(self, input_args):
        """
        to_addr参数支持正则
        """
        print("to_addr参数支持正则，订阅")
        addr3 = input_args.addrs[2]
        event_filter = {"to_addr": addr3 + "|qatest"}
        event_filter = json.dumps(event_filter)
        err, result = input_args.test.event.trans_event_test(
            event_filter, self.eventfile
        )
        assert err == 0, "to_addr参数支持正则，订阅失败：" + result
