"""
说明: 查询平行链的共识信息
"""
import json
import pytest


class TestQuery:
    """
    查询平行链的共识信息
    """

    @pytest.mark.p1
    def test_case01(self, input_args):
        """
        查询pow共识的平行链
        """
        err, result = input_args.test.xlib.consensus_status(name="hipow1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "pow", "共识类别有误"

    @pytest.mark.p1
    def test_case02(self, input_args):
        """
        查询single共识的平行链
        """
        err, result = input_args.test.xlib.consensus_status(name="hisingle1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "single", "共识类别有误"

    @pytest.mark.p1
    def test_case03(self, input_args):
        """
        查询tdpos共识的平行链
        """
        err, result = input_args.test.xlib.consensus_status(name="hitdpos1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "tdpos", "共识类别有误"

    @pytest.mark.p1
    def test_case04(self, input_args):
        """
        查询xpos共识的平行链
        """
        err, result = input_args.test.xlib.consensus_status(name="hixpos1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "xpos", "共识类别有误"

    @pytest.mark.p1
    def test_case05(self, input_args):
        """
        查询poa共识的平行链
        """
        err, result = input_args.test.xlib.consensus_status(name="hipoa1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "poa", "共识类别有误"

    @pytest.mark.p1
    def test_case06(self, input_args):
        """
        查询xpoa共识的平行链
        """
        err, result = input_args.test.xlib.consensus_status(name="hixpoa1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "xpoa", "共识类别有误"
