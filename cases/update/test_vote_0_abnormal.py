# pylint: disable=W0603
"""
说明：测试提案后，异常的投票、异常的撤销提案
"""
import pytest

PROPOSE_ID = ""


class TestVoteErr:
    """
    测试提案后，异常的投票、异常的撤销提案
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        【异常】投票不足51%，trigger之后释放投票冻结的代币
        """
        print("\n【异常】投票不足51%，trigger之后释放投票冻结的代币")

        err, balance1 = input_args.test.xlib.govern_token(
            method_type="query", addr=input_args.addrs[0]
        )
        assert err == 0, balance1

        validator = input_args.addrs
        err, version = input_args.test.update.gen_cons_json("tdpos", validator)
        assert err == 0, version
        global PROPOSE_ID
        err, PROPOSE_ID = input_args.test.update.propose_update()
        assert err == 0, PROPOSE_ID
        err, result = input_args.test.update.vote_update(PROPOSE_ID, amount=10)
        assert err == 0, result

        # 15个区块后触发升级，等20个区块
        input_args.test.xlib.wait_num_height(20)

        # 预期提案状态为rejected
        err, result = input_args.test.update.query_propose(PROPOSE_ID)
        assert err == 0, "查询提案失败：" + result
        assert "rejected" in result

        err, balance2 = input_args.test.xlib.govern_token(
            method_type="query", addr=input_args.addrs[0]
        )
        assert err == 0, balance2
        assert str(balance1) == str(balance2)

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        【异常】提案有投票记录，提案状态是reject时，发起投票
        """
        print("\n【异常】有投票记录，提案状态是reject时，发起投票")
        # 注意 id是上个case的
        err, result = input_args.test.update.vote_update(PROPOSE_ID, amount=10)
        assert err != 0, result
        assert "proposal status is rejected,can not vote now" in result

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】提案有投票记录，提案状态是reject时，撤销提案
        """
        print("\n【异常】有投票记录，提案状态是reject时，撤销提案")
        # 注意 id是上个case的
        err, result = input_args.test.update.thaw_propose(PROPOSE_ID)
        assert err != 0, result
        assert "some one has voted 10 tickets, can not thaw now" in result

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        【异常】发起提案后，无人投票
        """
        print("\n【异常】发起提案后，无人投票")
        validator = input_args.addrs
        err, version = input_args.test.update.gen_cons_json("tdpos", validator)
        assert err == 0, version
        global PROPOSE_ID
        err, PROPOSE_ID = input_args.test.update.propose_update()
        assert err == 0, PROPOSE_ID

        # 15个区块后触发升级，等20个区块
        input_args.test.xlib.wait_num_height(20)

        # 预期提案状态为rejected
        err, result = input_args.test.update.query_propose(PROPOSE_ID)
        assert err == 0, "查询提案失败：" + result
        assert "rejected" in result

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        【异常】无投票记录，提案状态是rejected，发起投票
        """
        print("\n【异常】提案状态是rejected，发起投票")
        # 注意 id是上个case的
        err, result = input_args.test.update.vote_update(PROPOSE_ID, amount=10)
        assert err != 0, result
        assert "proposal status is rejected,can not vote now" in result

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        【异常】无投票记录，提案状态是rejected，撤销提案
        """
        print("\n【异常】提案状态是rejected，发起投票")
        # 注意 id是上个case的
        err, result = input_args.test.update.thaw_propose(PROPOSE_ID)
        assert err != 0, result
        assert (
            "proposal status is rejected, only a voting proposal could be thawed"
            in result
        )

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        【异常】提案状态是passed，发起投票，预期失败
        """
        print("\n【异常】提案状态是passed，发起投票，预期失败")
        validator = input_args.addrs
        # 获取当前区块高度
        err, height = input_args.test.xlib.query_height()
        assert err == 0, height
        stop = int(height) + 10
        trigger = int(height) + 15

        err, version = input_args.test.update.gen_cons_json(
            "tdpos", validator, stop_vote_height=stop, trigger_height=trigger
        )
        assert err == 0, version
        global PROPOSE_ID
        err, PROPOSE_ID = input_args.test.update.propose_update()
        assert err == 0, PROPOSE_ID

        err, result = input_args.test.update.vote_update(PROPOSE_ID)
        assert err == 0, result

        input_args.test.xlib.wait_num_height(12)

        # 等到stop高度之后，查询提案状态
        err, result = input_args.test.update.query_propose(PROPOSE_ID)
        assert err == 0, "查询提案失败：" + result
        assert "passed" in result

        # 再次投票
        err, result = input_args.test.update.vote_update(PROPOSE_ID, amount=1)
        assert err != 0, result
        assert "proposal status is passed,can not vote now" in result

    @pytest.mark.abnormal
    def test_case08(self, input_args):
        """
        【异常】提案状态是passed，发起撤销提案，预期失败
        """
        print("\n【异常】提案状态是passed，撤销提案，预期失败")
        # 撤销提案，id来自上个case
        err, result = input_args.test.update.thaw_propose(PROPOSE_ID)
        assert err != 0, result
        assert (
            "some one has voted 60000000000000000000 tickets, can not thaw now"
            in result
        )
        # 等待达到trigger高度，冻结的代币才能返回
        input_args.test.xlib.wait_num_height(6)

    @pytest.mark.abnormal
    def test_case09(self, input_args):
        """
        【异常】提案状态是completed_success，发起投票，预期失败
        """
        print("\n【异常】提案状态是completed_success，发起投票，预期失败")
        # trigger高度之后，查询提案状态
        err, result = input_args.test.update.query_propose(PROPOSE_ID)
        assert err == 0, "查询提案失败：" + result
        assert "completed_success" in result

        # 再次投票
        err, result = input_args.test.update.vote_update(PROPOSE_ID, amount=1)
        assert err != 0, result
        assert "proposal status is completed_success,can not vote now" in result

    @pytest.mark.abnormal
    def test_case10(self, input_args):
        """
        【异常】提案状态是completed_success，发起撤销提案，预期失败
        """
        print("\n【异常】提案状态是completed_success，撤销提案，预期失败")
        # 撤销提案
        err, result = input_args.test.update.thaw_propose(PROPOSE_ID)
        assert err != 0, result
        assert (
            "some one has voted 60000000000000000000 tickets, can not thaw now"
            in result
        )

    @pytest.mark.abnormal
    def test_case11(self, input_args):
        """
        【异常】提案状态是voting，且已有投票，发起撤销提案失败
        """
        print("\n【异常】提案状态是voting，且已有投票，发起撤销提案失败")
        validator = input_args.addrs
        err, version, propose_id = input_args.test.update.update_consensus(
            "tdpos", validator
        )
        assert err == 0, "提案和投票失败：" + version

        # 预期提案状态为voting
        err, result = input_args.test.update.query_propose(propose_id)
        assert err == 0, "查询提案失败：" + result
        assert "voting" in result

        # 撤销提案
        err, result = input_args.test.update.thaw_propose(propose_id)
        assert err != 0, result
        assert (
            "some one has voted 60000000000000000000 tickets, can not thaw now"
            in result
        )

        # 等6个区块,冻结的代币被返还，下面用例需要使用代币
        input_args.test.xlib.wait_num_height(20)

    @pytest.mark.abnormal
    def test_case12(self, input_args):
        """
        【异常】提案状态是canceled，发起撤销提案失败
        """
        print("\n【异常】提案状态是canceled，发起撤销提案失败")
        validator = input_args.addrs
        err, version = input_args.test.update.gen_cons_json("tdpos", validator)
        assert err == 0, version
        err, propose_id = input_args.test.update.propose_update()
        assert err == 0, PROPOSE_ID

        # 预期提案状态为voting
        err, result = input_args.test.update.query_propose(propose_id)
        assert err == 0, "查询提案失败：" + result
        assert "voting" in result

        # 撤销提案
        err, result = input_args.test.update.thaw_propose(propose_id)
        assert err == 0, result

        # 预期提案状态为cancelled
        err, result = input_args.test.update.query_propose(propose_id)
        assert err == 0, "查询提案失败：" + result
        assert "cancelled" in result

        # 再次撤销提案
        err, result = input_args.test.update.thaw_propose(propose_id)
        assert err != 0, result
        assert (
            "proposal status is cancelled, only a voting proposal could be thawed"
            in result
        )

    @pytest.mark.abnormal
    def test_case13(self, input_args):
        """
        【异常】json缺少必填参数, trigger高度之后提案状态是completed_failure
        """
        print("\n【异常】json缺少必填参数, trigger高度之后提案状态是completed_failure")
        validator = input_args.addrs
        global PROPOSE_ID
        err, version, PROPOSE_ID = input_args.test.update.update_consensus(
            "aaa", validator
        )
        assert err == 0, "提案和投票失败：" + version

        # 15个区块后触发升级，等20个区块
        input_args.test.xlib.wait_num_height(20)

        # 预期提案状态为completed_failure
        err, result = input_args.test.update.query_propose(PROPOSE_ID)
        assert err == 0, "查询提案失败：" + result
        assert "completed_failure" in result

    @pytest.mark.abnormal
    def test_case14(self, input_args):
        """
        【异常】提案状态是completed_failure，发起投票，预期失败
        """
        print("\n【异常】提案状态是completed_failure，发起投票，预期失败")
        # 再次投票
        err, result = input_args.test.update.vote_update(PROPOSE_ID, amount=1)
        assert err != 0, result
        assert "proposal status is completed_failure,can not vote now" in result

    @pytest.mark.abnormal
    def test_case15(self, input_args):
        """
        【异常】提案状态是completed_failure，发起撤销提案，预期失败
        """
        print("\n【异常】提案状态是completed_failure，撤销提案，预期失败")
        # 撤销提案
        err, result = input_args.test.update.thaw_propose(PROPOSE_ID)
        assert err != 0, result
        assert (
            "some one has voted 60000000000000000000 tickets, can not thaw now"
            in result
        )

    @pytest.mark.abnormal
    def test_case16(self, input_args):
        """
        【异常】给不存在的提案投票
        """
        print("\n【异常】给不存在的提案投票")
        # 撤销提案
        err, result = input_args.test.update.vote_update("10000000000", amount=1)
        assert err != 0, result
        assert "vote failed, no proposal found" in result

    @pytest.mark.abnormal
    def test_case17(self, input_args):
        """
        【异常】撤销不存在的提案
        """
        print("\n【异常】撤销不存在的提案")
        # 撤销提案
        err, result = input_args.test.update.thaw_propose("10000000000")
        assert err != 0, result
        assert "thaw failed, no proposal found" in result

    @pytest.mark.abnormal
    def test_case18(self, input_args):
        """
        【异常】查询不存在的提案
        """
        print("\n【异常】查询不存在的提案")
        # 撤销提案
        err, result = input_args.test.update.query_propose("10000000000")
        assert err != 0, "查询提案失败：" + result
        assert "query failed, no proposal found" in result
