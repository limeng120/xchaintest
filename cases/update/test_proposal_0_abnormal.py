"""
说明：发起提案返失败的case，发起提案的正常用例在升级case中已验证。
"""
import pytest


class TestProposeErr:
    """
    发起提案返失败的case
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        【异常】min_vote_percent设为50
        """
        print("\n【异常】min_vote_percent设为50")
        validator = input_args.addrs
        err, version = input_args.test.update.gen_cons_json(
            "tdpos", validator, percent="50"
        )
        assert err == 0, version
        err, result = input_args.test.update.propose_update()
        assert err != 0 and "min_vote_percent err" in result, result

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        【异常】 stop_vote_height 小于当前区块高度
        """
        print("\n【异常】stop_vote_height 小于当前区块高度")
        validator = input_args.addrs
        err, version = input_args.test.update.gen_cons_json(
            "tdpos", validator, stop_vote_height="1"
        )
        assert err == 0, version
        err, result = input_args.test.update.propose_update()
        assert err != 0, result
        assert "stop voting height must be larger than current trunk height" in result

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】 stop_vote_height 大于trigger
        """
        print("\n【异常】stop_vote_height 大于trigger")
        validator = input_args.addrs
        # 获取当前区块高度
        err, height = input_args.test.xlib.query_height()
        assert err == 0, height
        stop = int(height) + 20
        trigger = int(height) + 10

        err, version = input_args.test.update.gen_cons_json(
            "tdpos", validator, stop_vote_height=stop, trigger_height=trigger
        )
        assert err == 0, version
        err, result = input_args.test.update.propose_update()
        assert err != 0, result
        assert "trigger_height must be bigger than stop_vote_height" in result, result
