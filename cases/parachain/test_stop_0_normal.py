"""
说明：测试停用平行链
"""
import json
import pytest
import time
import os

class TestStopChain:

    def stopAndQueryChain(self, name, input):
        """
        停用链
        """
        err, result = input.test.pchain.StopChain(name=name)
        assert err == 0, result
        # 当node1不是admin时，需用node2重试stopChain
        if "failed+http.StatusForbidden" in result:
            err, result = input.test.pchain.StopChain(name=name, keys=input.keys[1])
        assert err == 0, "停用链失败：" + result        
        #等2个区块，链停用
        input.test.xlib.WaitNumHeight(2)   
        err, result = input.test.xlib.QueryBlockHeight(name=name)   
        assert "not find chain " + name in str(result),\
             "停用链后,查看链的区块高度不合预期 ：" + str(result)
        
    def getAllParaChain(self, input):
        """
        组装启用着的平行链
        """
        paraChainList=[]
        for k, v in input.conf.hosts.items():            
            err, result = input.test.pchain.QueryParachain(host=v)
            assert err == 0, "查询所有启用着的平行链失败：" + result   
            for element in result:
                if element not in paraChainList:
                    paraChainList.append(element)
         
        return paraChainList

    # case01 停用所有链
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n停用所有链,查询不到平行链")        
        #组装启用着的平行链
        stopList = self.getAllParaChain(input)
        #停用链
        for p in stopList:
            self.stopAndQueryChain(p, input)
        #检查平行链是否全停止
        result = self.getAllParaChain(input)
        assert len(result) == 0, "还有未停用的平行链，失败：" + result
    
    # case02停用已经停用的链
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n停用已经停用的链")
        self.stopAndQueryChain("hisingle1", input)         
       
  
    