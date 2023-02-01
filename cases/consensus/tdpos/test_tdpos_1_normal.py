"""
说明：测试候选人变更

本用例的执行的前提条件
1. 当前tdpos共识网络有3节点，node1～node3，其中node1, node2为初始矿工节点
2. 为了便于验证，proposer_num = 2， block_num = 10
"""

import json
import pytest


class TestNVRR:
    """
    测试候选人变更
    """

    def check_val_change(self, validators, input_args):
        """
        检查投票、撤销投票、撤销提名操作后，候选人是否在下个term生效。注意：如果操作发生在term的最后3个区块，则在下下个term生效
        """
        # 获取当前的共识状态
        err, result = input_args.test.xlib.consensus_status()
        assert err == 0, result

        # 获取当前term
        consensus = json.loads(result)
        validators_info = json.loads(consensus["validators_info"])
        term = validators_info["curterm"]

        term_a = term + 1
        term_b = term + 2
        print(
            "候选人变为"
            + str(validators)
            + "，会发生在TermA: "
            + str(term_a)
            + " 或者TermB: "
            + str(term_b)
        )

        # 等到进入termA
        err, result = input_args.test.wait_term_change(term_a)
        assert err == 0, result

        err, result = input_args.test.check_validators(validators)
        if err != 0:
            # term_a 没变更，则等到termB 查询是否变更
            err, result = input_args.test.wait_term_change(term_b)
            assert err == 0, result
            err, result = input_args.test.check_validators(validators)
            assert err == 0, result

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        依次提名所有节点为候选人
        """
        print("\n依次提名所有节点为候选人 ")
        nominate_amount = 100
        for candidate in input_args.addrs:
            err, result = input_args.test.nominate(
                candidate, nominate_amount, input_args.acl_account, input_args.keys
            )
            assert err == 0, "提名候选人失败" + result
            nominate_amount += 100

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        依次给提名的候选人投票
        """
        print("\n依次给提名的候选人投票")
        vote_amount = 100
        for candidate in input_args.addrs:
            err, result = input_args.test.vote(
                candidate, vote_amount, input_args.client_addr, input_args.client_key
            )
            assert err == 0, "给候选人投票失败" + result
            vote_amount += 100
        validators = [input_args.node2, input_args.node3]
        self.check_val_change(validators, input_args)

    @pytest.mark.abnormal
    def test_clear(self, input_args):
        """
        清环境：撤销全部提名和投票
        """
        print("\n 清空vote和nominate")
        err, result = input_args.test.clear_vote_nominate()
        assert err == 0, result
