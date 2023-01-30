"""
说明：poa, xpoa共识节点网络的测试
"""
import numpy as np
import pytest
import json
import os

class TestEdit:

    # case01: 变更前后，验证集无重合：node1、2变更为node3
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n变更前后，验证集无重合：node1、2变更为node3")
        nominates = [input.node3]
        acl_account = input.acc12["acl_account"]
        addrs = input.acc12["addrs"]
        keys = input.acc12["keys"]
        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err == 0, result
    
    # case02: 增加候选人：node3变更为node1、2、3
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n增加候选人：node3变更为node1、2、3")
        nominates = [input.node1, input.node2, input.node3]

        acl_account = input.acc33["acl_account"]
        addrs = input.acc33["addrs"]
        keys = input.acc33["keys"]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys, host=input.host3)
        assert err == 0, result

    # case03: 减少候选人，且当前集合超半数的成员签名：node1、2、3变更为node1、2，node1、3签名
    @pytest.mark.p2
    def test_case03(self, input):
        print("\n减少候选人，且当前集合超半数的成员签名：node1、2、3变更为node1、2")
        nominates = [input.node1, input.node2]
        acl_account = input.acc13["acl_account"]
        addrs = input.acc13["addrs"]
        keys = input.acc13["keys"]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err == 0, result

    # case04: 1个区块内，两次变更：node1、2变更为node2、3，变更为node1
    @pytest.mark.p2
    def test_case04(self, input):
        print("1个区块内，两次变更：node1、2变更为node2、3，变更为node1")
        nominates = [input.node2, input.node3]
        acl_account = input.acc12["acl_account"]
        addrs = input.acc12["addrs"]
        keys = input.acc12["keys"]
        
        # 提名node2，node3
        err, result = input.test.QuickEditValidates(nominates, acl_account, addrs, keys)
        assert err == 0, result

        nominates = [input.node2, input.node3]
        err, result = input.test.CheckValidates(nominates)
        assert err == 0, result
    
        # 提名node1
        acl_account = input.acc23["acl_account"]
        addrs = input.acc23["addrs"]
        keys = input.acc23["keys"]
        nominates = [input.node1]
        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys, host=input.host2)
        assert err == 0, result

    # case05: 相邻的三个区块内，两次变更：node1变更为node2、3，node1变更为node1、2
    @pytest.mark.p2
    def test_case05(self, input):
        print("相邻的三个区块内，两次变更：node1变更为node2、3，node1变更为node1、2")
        nominates = [input.node2, input.node3]

        acl_account = input.acc11["acl_account"]
        addrs = input.acc11["addrs"]
        keys = input.acc11["keys"]

        err, result = input.test.QuickEditValidates(nominates, acl_account, addrs, keys)
        assert err == 0, result

        nominates = [input.node2, input.node3]
        err, result = input.test.CheckValidates(nominates)
        assert err == 0, result
        
        # 1个区块后验证再修改, 修改为[node1, node2, node3]
        err, result = input.test.xlib.WaitNumHeight(1)

        acl_account = input.acc23["acl_account"]
        addrs = input.acc23["addrs"]
        keys = input.acc23["keys"]
        nominates = [input.node1, input.node2]
        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys, host=input.host2)
        assert err == 0, result
