"""
说明：停用平行链群组的异常场景
"""
import json
import pytest
import time
import os

class TestStopChainErr:

    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n 普通节点停用权限，非admin节点")
        err, result = input.test.pchain.StopChain(name="hixpoa1", keys="output/data/alice")
        assert err != 0, "非admin节点停用链成功，不符合预期：" + result
        msg = "invoke failed+http.StatusForbidden"
        assert msg in result, "报错信息错误"      
    
    @pytest.mark.abnormal
    def test_case02(self, input):     
        print("\n停用name为空字符串的链")
        err, result = input.test.pchain.StopChain(name="")
        assert err != 0, "停用name为空字符串的链成功，不符合预期：" + result
        msg = "chain name is empty"
        assert msg in result, "报错信息错误"      
            
    @pytest.mark.abnormal
    def test_case03(self, input):     
        print("\n停用不存在的链")
        err, result = input.test.pchain.StopChain(name="notexit")
        assert err != 0, "停用不存在的链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"     

    @pytest.mark.abnormal
    def test_case04(self, input):     
        print("\n停用xuper链")
        err, result = input.test.pchain.StopChain(name="xuper")
        assert err != 0, "停用xuper链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"
           


   








     


    
        
  
  