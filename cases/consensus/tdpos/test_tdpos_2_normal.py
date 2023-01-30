"""
说明：测试候选人变更

本用例的执行的前提条件
1. 当前tdpos共识网络有3节点，node1～node3，其中node1, node2为初始矿工节点
2. 为了便于验证，proposer_num = 2， block_num = 10
"""

import os
import json
import pytest

class TestNVRR:

    def checkValChange(self, validators, input):
        """
        检查投票、撤销投票、撤销提名操作后，候选人是否在下个term生效。注意：如果操作发生在term的最后3个区块，则在下下个term生效
        """
        #获取当前的共识状态
        err, result = input.test.xlib.ConsensusStatus()
        assert err == 0, result

        # 获取当前term
        consensus = json.loads(result)
        validators_info = json.loads(consensus["validators_info"])
        term = validators_info["curterm"]

        termA = term + 1
        termB = term + 2
        print("候选人变为" + str(validators) + \
            "，会发生在TermA: " + str(termA) + " 或者TermB: " + str(termB))

        # 等到进入termA
        err, result = input.test.waitTermChange(termA)
        assert err == 0, result

        err, result = input.test.CheckValidators(validators)
        if err != 0:
            # termA 没变更，则等到termB 查询是否变更
            err, result = input.test.waitTermChange(termB)
            assert err == 0, result
            err, result = input.test.CheckValidators(validators)
            assert err == 0, result

    # case01: 依次提名所有节点为候选人 
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n依次提名所有节点为候选人 ")
        nominate_amount = 100
        for candidate in input.addrs:
            err, result = input.test.Nominate(candidate, nominate_amount, input.acl_account, input.keys)
            assert err == 0, "提名候选人失败" + result
            nominate_amount += 100

    # case02: 依次给提名的候选人投票
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n依次给提名的候选人投票")
        vote_amount = 100
        for candidate in input.addrs:
            err, result = input.test.Vote(candidate, vote_amount, input.client_addr, input.client_key)
            assert err == 0, "给候选人投票失败" + result
            vote_amount += 100
        validators = [input.node2, input.node3]
        self.checkValChange(validators, input)

    # 清环境：撤销全部提名和投票
    @pytest.mark.abnormal
    def test_clear(self, input):   
        print("\n 清空vote和nominate") 
        err, result = input.test.clearVoteNominate()   
        assert err == 0, result
