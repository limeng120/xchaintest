"""
说明: 测试事件订阅
"""
import json
import pytest
import time
import os

class TestEvent():

    eventfile = "eventlog"

    # case01 不指定过滤参数，订阅
    @pytest.mark.p0
    def test_case01(self, input):
        print("不指定过滤参数，订阅")
        err, result = input.test.event.ContractEventTest("", self.eventfile)
        assert err == 0, "不指定过滤参数，订阅失败：" + result 
        
    # case02 指定高度区间订阅，start大于当前区块高度
    @pytest.mark.p2
    def test_case02(self, input):
        print("指定高度区间订阅，start大于当前区块高度")
        err, curHeight = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询当前高度失败：" + curHeight
        startHeight  = int(curHeight) + 5
        endHeight = int(curHeight) + 100
        filter = {
            "range": {
                "start": str(startHeight),
                "end": str(endHeight)
            }
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile, False, 5)
        assert err == 0, "start大于当前区块高度，订阅失败：" + result

    # case03 指定高度区间订阅，start小于当前区块高度
    @pytest.mark.p2
    def test_case03(self, input):
        print("指定高度区间订阅，start小于当前区块高度")
        err, curHeight = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询当前高度失败：" + curHeight
        startHeight = int(curHeight) - 10
        endHeight = int(curHeight) + 100
        filter = {
            "range": {
                "start": str(startHeight),
                "end": str(endHeight)
            }
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "start小于当前区块高度，订阅失败：" + result

    # case04 指定高度区间订阅，仅设置start
    @pytest.mark.p2
    def test_case04(self, input):
        print("指定高度区间订阅，仅设置start")
        err, curHeight = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询当前高度失败：" + curHeight
        filter = {
            "range": {
                "start": str(curHeight)
            }
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "仅设置start，订阅失败：" + result

    # case05 指定高度区间订阅，仅设置end
    @pytest.mark.p2
    def test_case05(self, input):
        print("指定高度区间订阅，仅设置end")
        err, curHeight = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询当前高度失败：" + curHeight
        endHeight = int(curHeight) + 100
        filter = {
            "range": {
                "end": str(endHeight)
            }
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "仅设置end，订阅失败：" + result

    # case06 设置"exclude_tx": true
    # 不含tx，所以预期的event是空
    @pytest.mark.p2
    def test_case06(self, input):
        print("设置exclude_tx: true")
        filter = {
            "exclude_tx": True
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile, emptyEvent=True)
        assert err == 0, "设置exclude_tx: true，订阅失败：" + result
    
    # case07 设置"exclude_tx_event": true
    @pytest.mark.p2
    def test_case07(self, input):
        print("设置exclude_tx_event: true")
        filter = {
            "exclude_tx_event": True
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "设置exclude_tx_event: true，订阅失败：" + result

    # case08 设置合约名，订阅
    @pytest.mark.p2
    def test_case08(self, input):
        print("设置合约名，订阅")
        filter = {
            "contract": "c_counter"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "设置合约名，订阅失败：" + result

    # case09 设置合约名，事件名，订阅
    @pytest.mark.p2
    def test_case09(self, input):
        print("设置合约名，订阅")
        filter = {
            "contract": "c_counter",
            "event_name": "increase"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "设置合约名，事件名，订阅失败：" + result

    # case10 设置事件名，订阅
    @pytest.mark.p2
    def test_case10(self, input):
        print("设置事件名，订阅")
        filter = {
            "event_name": "increase"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "设置事件名，订阅失败：" + result

    # case11 设置发起人，订阅
    @pytest.mark.p2
    def test_case11(self, input):
        print("设置发起人，订阅")
        filter = {
            "initiator": input.conf.addrs[1]
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "设置发起人，订阅失败：" + result

    # case12 设置auth_require，订阅
    @pytest.mark.p2
    def test_case12(self, input):
        print("设置auth_require，订阅")
        filter = {
            "auth_require": input.conf.addrs[1]
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "设置auth_require，订阅失败：" + result

    # case13 设置from_addr，订阅
    @pytest.mark.p2
    def test_case13(self, input):
        print("设置from_addr，订阅")
        filter = {
            "from_addr": input.conf.client_addr
        }
        filter = json.dumps(filter)
        err, result = input.test.event.TransEventTest(filter, self.eventfile)
        assert err == 0, "设置from_addr，订阅失败：" + result

    # case14 设置to_addr，订阅
    @pytest.mark.p2
    def test_case14(self, input):
        print("设置to_addr，订阅")
        filter = {
            "to_addr": "qatest"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.TransEventTest(filter, self.eventfile)
        assert err == 0, "设置to_addr，订阅失败：" + result

    # case15 contract参数支持正则
    @pytest.mark.p2
    def test_case15(self, input):
        print("contract参数支持正则，订阅")
        filter = {
            "contract": "count"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "contract参数支持正则，订阅失败：" + result
   
    # case16 event参数支持正则
    @pytest.mark.p2
    def test_case16(self, input):
        print("event参数支持正则，订阅")
        filter = {
            "event_name": "inc"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.ContractEventTest(filter, self.eventfile)
        assert err == 0, "event参数支持正则，订阅失败：" + result

    # case17 initiator参数支持正则
    @pytest.mark.p2
    def test_case17(self, input):
        print("initiator参数支持正则，订阅")
        addr1 = input.conf.addrs[0]
        addr3 = input.conf.addrs[2]
        filter = {
            "initiator": addr1 + "|" + addr3
        }
        filter = json.dumps(filter)
        err, result = input.test.event.TransEventTest(filter, self.eventfile)
        assert err == 0, "initiator参数支持正则，订阅失败：" + result

    # case18 auth_require参数支持正则
    @pytest.mark.p2
    def test_case18(self, input):
        print("auth_require参数支持正则，订阅")
        addr1 = input.conf.addrs[0]
        addr3 = input.conf.addrs[2]
        filter = {
            "auth_require": addr1 + "|" + addr3
        }
        filter = json.dumps(filter)
        err, result = input.test.event.TransEventTest(filter, self.eventfile)
        assert err == 0, "auth_require参数支持正则，订阅失败：" + result

    # case19 from_addr参数支持正则
    @pytest.mark.p2
    def test_case19(self, input):
        print("from_addr参数支持正则，订阅")
        addr1 = input.conf.addrs[0]
        addr3 = input.conf.addrs[2]
        filter = {
            "from_addr": addr1 + "|" + addr3
        }
        filter = json.dumps(filter)
        err, result = input.test.event.TransEventTest(filter, self.eventfile)
        assert err == 0, "from_addr参数支持正则，订阅失败：" + result

    # case20 to_addr参数支持正则
    @pytest.mark.p2
    def test_case20(self, input):
        print("to_addr参数支持正则，订阅")
        addr3 = input.conf.addrs[2]
        filter = {
            "to_addr": addr3 + "|qatest"
        }
        filter = json.dumps(filter)
        err, result = input.test.event.TransEventTest(filter, self.eventfile)
        assert err == 0, "to_addr参数支持正则，订阅失败：" + result