"""
说明：修改平行链群组
"""
import json
import pytest
import time
import os

class TestGroup:

    def editAndQueryGroup(self, name, admin, input):
        """
        修改群组
        """
        err, result = input.test.pchain.EditChainGroup(name=name, admin=admin)
        assert err == 0, "修改群组失败：" + result
   
        err, result = input.test.pchain.QueryChainGroup(name=name)
        assert err == 0, "查询群组失败：" + result
        tmp = result.split("\n")[0]
        result = tmp.split(": ")[1]
        result = json.loads(result)
        assert sorted(result["admin"]) == sorted(admin), "修改后 群组不符合预期"  
    
    # case01 创建平行链时群组成员是3个，修改群组，减少成员，3->2
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n 创建平行链时群组成员是3个，修改群组，减少成员，3->2")
        admin = [input.conf.addrs[0], input.conf.addrs[1]]
        self.editAndQueryGroup("hipow1", admin, input)
    
    # case02 修改平行链群组时,admin不存在，可以修改成功
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n修改平行链群组时,admin不存在，可以修改成功")
        admin = [input.conf.addrs[0], "121212121212122121"]
        self.editAndQueryGroup("hixpoa1", admin, input)

    #case03 给不同链，设置不同权限
    @pytest.mark.p2
    def test_case03(self, input):
        print("\n 给不同链，设置不同权限")
        groups = [
                  {"name": "hisingle1", "admin":input.conf.addrs},
                  {"name": "hipow1", "admin": [input.conf.addrs[0], input.conf.addrs[1]]}
                 ]
        for i in range(len(groups)):
            self.editAndQueryGroup(groups[i]["name"], groups[i]["admin"], input)
   
    #case04 连续更新hitdpos链群组
    @pytest.mark.p2
    def test_case04(self, input):
        print("\n连续更新hitdpos1链群组：node123-->node1,3 --->node1,2--->node2,3-->node123")
        changeArray = [[0], [0, 2], [0, 1], [1, 2], [1, 0, 2]]
        for i in range(len(changeArray)):
            index = 0 
            nextNum = 0
            admin = []
            if i > 0:
                #前一组数据的最后一位，用来修改群组
                index = changeArray[i - 1][0]
            for j in range(len(changeArray[i])):
                #当前数据，用来查询群组
                nextNum = changeArray[i][j]
                admin.append(input.conf.addrs[changeArray[i][j]])

            err, result = input.test.pchain.EditChainGroup(name="hitdpos1", admin=admin, 
                                                           keys=input.keys[index])
            assert err == 0, "修改hitdpos1群组失败：" + result
            err, result = input.test.pchain.QueryChainGroup(name="hitdpos1", keys=input.keys[nextNum])
            assert err == 0, "查询hitdpos1群组失败：" + result
            tmp = result.split("\n")[0]
            tmp = tmp.split(": ")[1]
            tmp = json.loads(tmp)
            assert sorted(tmp["admin"]) == sorted(admin), "修改后 hitdpos1群组不符合预期"
   
    #case05 修改已停用的链的群组
    @pytest.mark.p2
    def test_case05(self, input):      
        print("\n 修改已停用的链的群组")
        err, result = input.test.pchain.StopChain(name="hipow1")
        assert err == 0, "停用链失败：" + result        
        #等2个区块，链停用
        input.test.xlib.WaitNumHeight(2)   
        err, result = input.test.xlib.QueryBlockHeight(name="hipow1")       
        
        assert "not find chain hipow1" in result, "停用链后,查看链的区块高度不合预期 ：" + result
        admin = [input.conf.addrs[0], input.conf.addrs[1]]
        self.editAndQueryGroup("hipow1", admin, input)
  
  
