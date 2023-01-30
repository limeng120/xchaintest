"""
说明：修改平行链群组的异常场景
"""
import json
import pytest
import time
import os

class TestGroupErr:

    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n 非管理员修改平行链群组信息")
        admin = [input.conf.addrs[0], input.conf.addrs[1]]
        err, result = input.test.pchain.EditChainGroup(name="hixpoa1", admin=admin, keys="output/data/alice")
        assert err != 0, "非管理员修改平行链群组信息成功，不符合预期：" + result
        msg = "invoke failed+http.StatusForbidden"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input):     
        print("\nsingle共识：修改平行链群组时,矿工不是群组成员")
        # 群组成员初始是node1~3、设置群组成员为node2
        admin = [input.conf.addrs[1]]
        err, result = input.test.pchain.EditChainGroup(name="hisingle1", admin=admin, keys=input.keys[1])
        assert err == 0, "修改hisingle的群组失败，不符合预期" + result
        
        h1 = []
        h2 = []
        #查看区块高度，node2，3不涨块
        #等2个区块，链停用
        input.test.xlib.WaitNumHeight(2)   
        # 查询node2的平行链高度
        err, h1 = input.test.xlib.QueryBlockHeight(name="hisingle1", host=input.conf.hosts["node2"])
        assert err == 0, h1
        
        #等xuper出2个区块后，hisingle1 区块高度不变化
        input.test.xlib.WaitNumHeight(2)  

        # 查询node2的平行链高度
        err, h2 = input.test.xlib.QueryBlockHeight(name="hisingle1", host=input.conf.hosts["node2"])
        assert err == 0, h2

        assert h1 == h2, "矿工不在群组内，节点涨块,不符合预期 h1=" + str(h1) + "h2=" + str(h2) 

        # 还原群组成员为node1~3
        admin = [input.conf.addrs[0], input.conf.addrs[1], input.conf.addrs[2]]
        err, result = input.test.pchain.EditChainGroup(name="hisingle1", admin=admin, keys=input.keys[1])
        assert err == 0, "修改hisingle的群组失败，不符合预期" + result
            
    @pytest.mark.abnormal
    def test_case03(self, input):     
        print("\n修改xuper链群组")
        admin = [input.conf.addrs[1], input.conf.addrs[2]]
        err, result = input.test.pchain.EditChainGroup(name="xuper", admin=admin)
        assert err != 0, "修改xuper链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input):     
        print("\n查看xuper链群组")
        err, result = input.test.pchain.QueryChainGroup(name="xuper")
        assert err != 0, "查看xuper链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal        
    def test_case05(self, input):     
        print("\n非管理员，查看群组")
        err, result = input.test.pchain.QueryChainGroup(name="hixpoa1", keys="output/data/alice")
        assert err != 0, "非管理员，查看群组链成功，不符合预期：" + result
        msg = "http.StatusForbidden"
        assert msg in result, "报错信息错误"



   








     


    
        
  
  