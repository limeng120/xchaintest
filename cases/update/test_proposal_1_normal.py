"""
说明：测试 撤销提案
"""
import pytest


class TestThaw:
    """
    撤销提案
    """

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        提案状态是voting，且无投票，撤销提案
        """
        print("\n提案状态是voting，且无投票，撤销提案")
        validator = input_args.addrs
        err, version = input_args.test.update.gen_cons_json("tdpos", validator)
        assert err == 0, version
        err, propose_id = input_args.test.update.propose_update()
        assert err == 0, propose_id

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
