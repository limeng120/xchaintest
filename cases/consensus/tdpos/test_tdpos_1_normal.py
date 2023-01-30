"""
说明：测试候选人变更的投票，落在term边界情况的场景
测试前提：proposer = 2, block_num = 10, 即一个term20个块，矿工是node1、node2的环境运行

"""
import os
import json
import time
import pytest

class TestH3:

    # case01: 在本term结束前的三个区块内，执行投票，改变topK
    # 1. 创建3个node作为ak的acl账号
    # 2. 提名node1、node2、node3
    # 3. 给node1投票100，node2投票200，node3投票300
    # 4. 等待当前term结束，来到下个termA
    # 5. 等待termA的最后3个区块，给node1投票500
    # 6. 等待当前term结束，来到下个termB，查询候选人，预期是node2、3
    # 7. 等待当前term结束，来到下个termC，查询候选人，预期是node1、3

    @pytest.mark.p2
    def test_case01(self, input):
        print("在本term结束前的三个区块内，执行投票，改变topK")
        # 提名，使得（node2，node3）为最高，（初始矿工为node1，node2）
        nominate_amount = 100
        for candidate in input.addrs:
            err, result = input.test.Nominate(candidate, nominate_amount, input.acl_account, input.keys)
            assert err == 0, "提名候选人失败" + result
            nominate_amount += 100

        vote_amount = 100
        for candidate in input.addrs:
            err, result = input.test.Vote(candidate, vote_amount, input.client_addr, input.client_key)
            assert err == 0, "给候选人投票失败" + result
            vote_amount += 100
        
        #获取当前的共识状态
        err, result = input.test.xlib.ConsensusStatus()
        assert err == 0, result

        # 获取当前term
        consensus = json.loads(result)
        validators_info = json.loads(consensus["validators_info"])
        term = validators_info["curterm"]
        termA = term + 1
        print("TermA: " + str(termA))

        # 等到进入termA
        err, result = input.test.waitTermChange(termA)
        assert err == 0, result
 
        err, start = input.test.xlib.QueryBlockHeight()
        assert err == 0, start
        print("new term start height: " + str(start))

        vote_height = int(start)+ int(input.term_height) - 4
        print("vote height may be : " + str(vote_height))

        # 假设没有区块卡死的情况，term的倒数第三个区块，投票改变topK
        height = start
        while int(height) < vote_height:
            time.sleep(3)
            err, height = input.test.xlib.QueryBlockHeight()
            assert err == 0, height

        err, result = input.test.QuickVote(input.node1, 500, input.client_addr, input.client_key)
        assert err == 0, "给候选人投票失败" + result

        err, result = input.test.xlib.ConsensusStatus()
        assert err == 0, result
        
        # 等待进入termB。termB，候选人不变
        termB = termA + 1
        print("TermB: " + str(termB))
        err, result = input.test.waitTermChange(termB)
        assert err == 0, result

        # 验证validators，预期不变
        validators = [input.node2, input.node3]
        err, result = input.test.CheckValidators(validators)
        assert err == 0, "validators与预期的不符：" + result

        # 等待进入termC，候选人改变
        termC = termB + 1
        print("TermC: " + str(termC))
        err, result = input.test.waitTermChange(termC)
        assert err == 0, result

        # 验证validators，预期变为node1、3
        validators = [input.node1, input.node3]
        err, result = input.test.CheckValidators(validators)
        assert err == 0, "validators与预期的不符：" + result

    # case02 撤销全部提名和投票
    @pytest.mark.p2
    def test_case02(self, input):    
        err, result = input.test.clearVoteNominate()   
        assert err == 0, result
        