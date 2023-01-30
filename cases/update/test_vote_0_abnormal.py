"""
说明：测试提案后，异常的投票、异常的撤销提案
"""
import json
import pytest
import time
import os

class TestVoteErr:

    id = ""
    # 【异常】投票不足51%，trigger之后释放投票冻结的代币
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n【异常】投票不足51%，trigger之后释放投票冻结的代币")

        err, balance1 = input.test.xlib.GovernToken(type="query", addr=input.addrs[0])
        assert err == 0, balance1

        validator = input.addrs
        err, version = input.test.update.genConsJson("tdpos", validator)
        assert err == 0, version

        global id
        err, id = input.test.update.proposeUpdate()
        assert err == 0, id
        err, result = input.test.update.voteUpdate(id, amount=10)
        assert err == 0, result

        # 15个区块后触发升级，等20个区块
        input.test.xlib.WaitNumHeight(20)
        
        # 预期提案状态为rejected
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "rejected" in result

        err, balance2 = input.test.xlib.GovernToken(type="query", addr=input.addrs[0])
        assert err == 0, balance2
        assert str(balance1) == str(balance2)
        
    # 【异常】有投票记录，提案状态是reject时，发起投票
    @pytest.mark.abnormal
    def test_case02(self, input):
        print("\n【异常】有投票记录，提案状态是reject时，发起投票")
        # 注意 id是上个case的
        err, result = input.test.update.voteUpdate(id, amount=10)
        assert err != 0, result
        assert "proposal status is rejected,can not vote now" in result

    # 【异常】有投票记录，提案状态是reject时，撤销提案
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】有投票记录，提案状态是reject时，撤销提案")
        # 注意 id是上个case的
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "some one has voted 10 tickets, can not thaw now" in result

    # 【异常】发起提案后，无人投票
    @pytest.mark.abnormal
    def test_case04(self, input):
        print("\n【异常】发起提案后，无人投票")
        validator = input.addrs
        err, version = input.test.update.genConsJson("tdpos", validator)
        assert err == 0, version

        global id
        err, id = input.test.update.proposeUpdate()
        assert err == 0, id

        # 15个区块后触发升级，等20个区块
        input.test.xlib.WaitNumHeight(20)
        
        # 预期提案状态为rejected
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "rejected" in result

    # 【异常】无投票记录，提案状态是rejected，发起投票
    @pytest.mark.abnormal
    def test_case05(self, input):
        print("\n【异常】提案状态是rejected，发起投票")
        # 注意 id是上个case的
        err, result = input.test.update.voteUpdate(id, amount=10)
        assert err != 0, result
        assert "proposal status is rejected,can not vote now" in result

    # 【异常】无投票记录，提案状态是rejected，撤销提案
    @pytest.mark.abnormal
    def test_case06(self, input):
        print("\n【异常】提案状态是rejected，发起投票")
        # 注意 id是上个case的
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "proposal status is rejected, only a voting proposal could be thawed" in result

    # 【异常】提案状态是passed，发起投票，预期失败
    @pytest.mark.abnormal
    def test_case07(self, input):
        print("\n【异常】提案状态是passed，发起投票，预期失败")
        validator = input.addrs
        # 获取当前区块高度
        err, height = input.test.xlib.QueryBlockHeight()
        assert err == 0, height
        stop = int(height) + 10
        trigger = int(height) + 15
        
        err, version = input.test.update.genConsJson("tdpos", validator, \
        stop_vote_height=stop, trigger_height=trigger)
        assert err == 0, version

        global id
        err, id = input.test.update.proposeUpdate()
        assert err == 0, id

        err, result = input.test.update.voteUpdate(id)
        assert err == 0, result

        input.test.xlib.WaitNumHeight(12)

        # 等到stop高度之后，查询提案状态
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "passed" in result

        # 再次投票
        err, result = input.test.update.voteUpdate(id, amount=1)
        assert err != 0, result
        assert "proposal status is passed,can not vote now" in result

    # 【异常】提案状态是passed，发起撤销提案，预期失败
    @pytest.mark.abnormal
    def test_case08(self, input):
        print("\n【异常】提案状态是passed，撤销提案，预期失败")
        # 撤销提案，id来自上个case
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "some one has voted 60000000000000000000 tickets, can not thaw now" in result
        # 等待达到trigger高度，冻结的代币才能返回
        input.test.xlib.WaitNumHeight(6)

    # 【异常】提案状态是completed_success，发起投票，预期失败
    @pytest.mark.abnormal
    def test_case09(self, input):
        print("\n【异常】提案状态是completed_success，发起投票，预期失败")
        # trigger高度之后，查询提案状态
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "completed_success" in result

        # 再次投票
        err, result = input.test.update.voteUpdate(id, amount=1)
        assert err != 0, result
        assert "proposal status is completed_success,can not vote now" in result

    # 【异常】提案状态是completed_success，发起撤销提案，预期失败
    @pytest.mark.abnormal
    def test_case1O(self, input):
        print("\n【异常】提案状态是completed_success，撤销提案，预期失败")
        # 撤销提案
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "some one has voted 60000000000000000000 tickets, can not thaw now" in result     
    
    # 【异常】提案状态是voting，且已有投票，发起撤销提案失败
    @pytest.mark.abnormal
    def test_case11(self, input):
        print("\n【异常】提案状态是voting，且已有投票，发起撤销提案失败")
        validator = input.addrs
        err, version, id = input.test.update.updateConsensus("tdpos", validator)
        assert err == 0, "提案和投票失败：" + version
       
        # 预期提案状态为voting
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "voting" in result

        # 撤销提案
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "some one has voted 60000000000000000000 tickets, can not thaw now" in result

        # 等6个区块,冻结的代币被返还，下面用例需要使用代币
        input.test.xlib.WaitNumHeight(20)

    # 【异常】提案状态是canceled，发起撤销提案失败
    @pytest.mark.abnormal
    def test_case12(self, input):
        print("\n【异常】提案状态是canceled，发起撤销提案失败")
        validator = input.addrs
        err, version = input.test.update.genConsJson("tdpos", validator)
        assert err == 0, version
        err, id = input.test.update.proposeUpdate()
        assert err == 0, id
        
        # 预期提案状态为voting
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "voting" in result

        # 撤销提案
        err, result = input.test.update.thawPropose(id)
        assert err == 0, result

        # 预期提案状态为cancelled
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "cancelled" in result

        # 再次撤销提案
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "proposal status is cancelled, only a voting proposal could be thawed" in result

    # 【异常】json缺少必填参数, trigger高度之后提案状态是completed_failure
    @pytest.mark.abnormal
    def test_case13(self, input):
        print("\n【异常】json缺少必填参数, trigger高度之后提案状态是completed_failure")
        validator = input.addrs
        global id
        err, version, id = input.test.update.updateConsensus("aaa", validator)
        assert err == 0, "提案和投票失败：" + version
        
        # 15个区块后触发升级，等20个区块
        input.test.xlib.WaitNumHeight(20)
        
        # 预期提案状态为completed_failure
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "completed_failure" in result

    # 【异常】提案状态是completed_failure，发起投票，预期失败
    @pytest.mark.abnormal
    def test_case14(self, input):
        print("\n【异常】提案状态是completed_failure，发起投票，预期失败")
        # 再次投票
        err, result = input.test.update.voteUpdate(id, amount=1)
        assert err != 0, result
        assert "proposal status is completed_failure,can not vote now" in result

    # 【异常】提案状态是completed_failure，发起撤销提案，预期失败
    @pytest.mark.abnormal
    def test_case15(self, input):
        print("\n【异常】提案状态是completed_failure，撤销提案，预期失败")
        # 撤销提案
        err, result = input.test.update.thawPropose(id)
        assert err != 0, result
        assert "some one has voted 60000000000000000000 tickets, can not thaw now" in result     
 
    # 【异常】给不存在的提案投票
    @pytest.mark.abnormal
    def test_case16(self, input):
        print("\n【异常】给不存在的提案投票")
        # 撤销提案
        err, result = input.test.update.voteUpdate("10000000000", amount=1)
        assert err != 0, result
        assert "vote failed, no proposal found" in result     
 
    # 【异常】撤销不存在的提案
    @pytest.mark.abnormal
    def test_case17(self, input):
        print("\n【异常】撤销不存在的提案")
        # 撤销提案
        err, result = input.test.update.thawPropose("10000000000")
        assert err != 0, result
        assert "thaw failed, no proposal found" in result  
    
    # 【异常】查询不存在的提案
    @pytest.mark.abnormal
    def test_case18(self, input):
        print("\n【异常】查询不存在的提案")
        # 撤销提案
        err, result = input.test.update.queryPropose("10000000000")
        assert err != 0, "查询提案失败：" + result
        assert "query failed, no proposal found" in result  