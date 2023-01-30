"""
说明: 测试go合约sdk的异常场景   
"""
import json
import pytest
import time

class TestGOFeatursErr():
    file = "goTemplate/features"
    cname = "features_go"

    #查询不存在的tx
    @pytest.mark.abnormal
    def test_case01(self, input):
        # 间隔3个区块,加载blockid
        print("\n【异常】查询不存在的txid")
        invokeArgs = {
            "txid": "c31db35d644e89919bb5668368b4d9e8c7d475f3eb9c8eb6604a0ad43246a779"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "QueryTx", args)
        assert err != 0 and "transaction not found" in result, "查询不存在的tx成功： " + result
      
    #查询不存在的区块
    @pytest.mark.abnormal
    def test_case02(self, input):
        # 间隔3个区块,加载blockid
        print("\n【异常】查询不存在的block")
        invokeArgs = {
            "blockid": "306edc9c26a6df7557455455f87c408b49036758152087a6d8d2617a5e9c234b"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "QueryBlock", args)
        assert err != 0 and  "block not exist in this chain" in result, "查询getBlock区块失败： " + result

    #【异常】合约余额不足
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】合约余额不足")
        invokeArgs = {"to":"123456", "amount":"1000000000000000"}  
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "Transfer", args)
        assert err != 0 and "no enough money" in result, "合约余额不足成功, 不符合预期： " + result
    
    #【异常】转账金额为负数
    @pytest.mark.abnormal
    def test_case04(self, input):
        print("\n【异常】转账金额为负数")
        invokeArgs = {"to":"123456", "amount":"-100"}  
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "Transfer", args)
        assert err != 0 and "amount should not be negative" in result,\
                                      "合约余额不足成功, 不符合预期： " + result
    
    #【异常】转账金额不是数字
    @pytest.mark.abnormal
    def test_case05(self, input):
        print("\n【异常】转账金额不是数字")
        invokeArgs = {"to":"123456", "amount":"hello"}  
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "Transfer", args)
        assert err != 0 and "message:bad amount format" in result,\
                                 "合约余额不足成功, 不符合预期： " + result
