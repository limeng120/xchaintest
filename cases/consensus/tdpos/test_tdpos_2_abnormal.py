"""
说明：测试候选人变更的异常场景

本用例的执行的前提条件
1. 当前tdpos共识网络有3节点，node1～node3，其中node1, node2为初始矿工节点
2. 为了便于验证，proposer_num = 2， block_num = 10
"""

import os
import json

import pytest

class TestNVRRErr:

    # case01:【异常】发起提名的账号中，不含被提名人
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n【异常】发起提名的账号中，不含被提名人")
        err, result = input.test.QuickNominate(input.wrong_candidate, 100, input.acl_account, input.keys)
        assert err != 0, "【异常】account中不包含被提名人的地址" + result
        assert "candidate has not authenticated your submission" in result, "报错信息错误"

    # case02:【异常】提名的amount为 0
    @pytest.mark.abnormal
    def test_case02(self, input):
        print("\n【异常】提名的amount为 0")
        err, result = input.test.QuickNominate(input.node1, "0", input.acl_account, input.keys)
        assert err != 0, "提名候选人失败" + result
        assert "amount in contract can not be empty" in result, "报错信息错误"

    # case03:【异常】提名的amount为负数
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】提名的amount为负数")
        err, result = input.test.QuickNominate(input.node1, "-1", input.acl_account, input.keys)
        assert err != 0, "提名候选人失败" + result
        assert "amount in contract can not be empty" in result, "报错信息错误"

    # case04:【异常】提名的amount为字母
    @pytest.mark.abnormal
    def test_case04(self, input):
        print("\n【异常】提名的amount为字母")
        err, result = input.test.QuickNominate(input.node1, "a", input.acl_account, input.keys)
        assert err != 0, "提名候选人失败" + result
        assert "amount in contract can not be empty" in result, "报错信息错误"

    # case04:【异常】发起提名的人，代币余额不足
    @pytest.mark.abnormal
    def test_case05(self, input):
        print("\n【异常】发起提名的人，代币余额不足")
        nominate_amount = 1000000000000000
        err, result = input.test.QuickNominate(input.node1, nominate_amount, input.acl_account, input.keys)
        assert err != 0, "提名候选人失败" + result    
        assert "lock gov tokens failed, account available balance insufficient" in result, "报错信息错误"

    # case06:【异常】投票的候选人未提名
    @pytest.mark.abnormal
    def test_case06(self, input):
        print("\n【异常】投票的候选人未提名")
        vote_amount = 100
        err, result = input.test.QuickVote(input.wrong_candidate, vote_amount, input.client_addr, input.client_key)
        assert err != 0, "【异常】投票的候选人未提名: " + result
        assert "addr in vote candidate hasn't been nominated" in result or "Key not found" in result

    # case07:【异常】发起投票的人，代币余额不足
    @pytest.mark.abnormal
    def test_case07(self, input):
        print("\n【异常】发起投票的人，代币余额不足")
        vote_amount = 1000000000000000
        err, result = input.test.QuickVote(input.node1, vote_amount, input.node2, input.key2)
        assert err != 0, "【异常】投票人的账户代币，不满足投票的amount: " + result
        assert "lock gov tokens failed, account available balance insufficient" in result, "报错信息错误"

    # case08:【异常】撤销投票对应的候选人不存在
    @pytest.mark.abnormal
    def test_case08(self, input):
        print("\n【异常】撤销投票对应的候选人不存在")
        err, result = input.test.QuickRevokeVote(input.wrong_candidate, 200, input.node1, input.key1)
        assert err != 0, "【异常】撤销投票对应的候选人不存在：" + result
        assert "Key not found" in result, "报错信息错误"

    # case09:【异常】撤销的票数比实际多
    @pytest.mark.abnormal
    def test_case09(self, input):
        print("\n【异常】撤销的票数比实际多")
        err, result = input.test.QuickNominate(input.node2, "10", input.acl_account, input.keys)
        assert err == 0 or "had been nominate" in result, "提名候选人失败" + result

        err, result = input.test.QuickVote(input.node2, "10", input.client_addr, input.client_key)
        assert err == 0, "给候选人投票失败" + result

        err, result = input.test.QuickRevokeVote(input.node2, 200000, input.node1, input.key1)
        assert err != 0, "【异常】撤销的票数比实际多：" + result   
        assert "no valid candidate key when revoke" in result, "报错信息错误"   

    # case10:【异常】撤销的票数为0
    @pytest.mark.abnormal
    def test_case10(self, input):
        print("\n【异常】撤销的票数为0")
        err, result = input.test.QuickRevokeVote(input.node2, "0", input.node1, input.key1)
        assert err != 0, result    
        assert "amount in contract can not be empty" in result, "报错信息错误"

    # case11:【异常】撤销的票数为负数
    @pytest.mark.abnormal
    def test_case11(self, input):
        print("\n【异常】撤销的票数为负数")
        err, result = input.test.QuickRevokeVote(input.node2, "-1", input.node1, input.key1)
        assert err != 0, result    
        assert "amount in contract can not be empty" in result, "报错信息错误"
    
    # case12:【异常】重复撤销投票
    @pytest.mark.abnormal
    def test_case12(self, input):
        print("\n【异常】重复撤销投票")
        input.test.QuickRevokeVote(input.node2, 10, input.node1, input.key1)
        err, result = input.test.QuickRevokeVote(input.node2, 10, input.node1, input.key1)
        assert err != 0, result    
        assert "value not found," in result, "报错信息错误"

    # case13:【异常】撤销提名，候选人不存在
    @pytest.mark.abnormal
    def test_case13(self, input):
        print("\n【异常】撤销提名，候选人不存在")
        err, result = input.test.QuickRevokeNominate(input.wrong_candidate, input.acl_account, \
            input.keys, flag="--isMulti")
        assert err != 0, "撤销候选人失败：" + result
        assert "no valid candidate key when revoke" in result, "报错信息错误"
    
    # case14:【异常】撤销提名，发起人跟提名时候不是同一人
    @pytest.mark.abnormal
    def test_case14(self, input):
        print("【异常】不使用提名的合约账户撤销")
        err, result = input.test.QuickRevokeNominate(input.node2, input.node1, input.key1)
        assert err != 0, "【异常】不使用提名的合约账户撤销：" + result
        assert "value not found, please check your input parameters" in result, "报错信息错误"

    # case15:【异常】已经被撤销的提名，再次撤销
    @pytest.mark.abnormal
    def test_case15(self, input):
        print("【异常】已经被撤销的候选人，再次被撤销")
        # 第1次撤销
        input.test.QuickRevokeNominate(input.node2, input.acl_account, input.keys, flag="--isMulti")
        # 第2次撤销
        err, result = input.test.QuickRevokeNominate(input.node2, input.acl_account, input.keys, flag="--isMulti")
        assert err != 0, "撤销候选人失败：" + result
        assert "no valid candidate key when revoke" in result, "报错信息错误"

    # case16:【异常】提名已被提名过的候选人
    @pytest.mark.abnormal
    def test_case16(self, input):
        print("【异常】提名已被提名过的候选人")
        input.test.QuickNominate(input.node2, 10, input.acl_account, input.keys)
        err, result = input.test.QuickNominate(input.node2, 10, input.acl_account, input.keys)
        assert err != 0, "【异常】已提名候选人后，再次提名候选人，amount不一致" + result 
        assert "candidate had been nominate" in result, "报错信息错误"

    # case17:【异常】撤销提名，候选人为空字符串
    @pytest.mark.abnormal
    def test_case17(self, input):
        print("\n【异常】撤销提名，候选人为空字符串")
        err, result = input.test.QuickRevokeNominate("", input.acl_account, \
            input.keys, flag="--isMulti")
        assert err != 0, "撤销候选人失败：" + result
        assert "addr in nominate candidate tx can not be empty" in result, "报错信息错误"

    # 清环境：撤销全部提名和投票
    @pytest.mark.abnormal
    def test_clear(self, input):   
        print("\n 清空vote和nominate") 
        err, result = input.test.clearVoteNominate()   
        assert err == 0, result
        