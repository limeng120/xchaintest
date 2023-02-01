"""
测试环境是否可用、准备运行测试用例的测试账号
"""

import pytest


class TestEnv:
    """
    测试环境是否可用、准备运行测试用例的测试账号
    """

    @pytest.mark.p0
    def test_trunk_height(self, input_args):
        """
        查询区块高度
        """
        err, result = input_args.test.xlib.query_height()
        assert err == 0, "查询区块高度失败：" + result

    @pytest.mark.p0
    def test_birfurcation_ratio(self, input_args):
        """
        查询分叉率
        """
        err, result = input_args.test.bifurcation_ratio()
        s = " ".join(str(x) for x in result)
        assert err == 0, "查询分叉率失败: " + s

    @pytest.mark.p0
    def test_basic_function(self, input_args):
        """
        执行基本功能测试，包括转账，创建合约账户，合约部署
        """
        err, result = input_args.test.basic_function()
        assert err == 0, "执行基本功能测试失败： " + result

    @pytest.mark.p0
    def test_init_govern_token(self, input_args):
        """
        初始化治理代币
        """
        err, result = input_args.test.xlib.govern_token(method_type="init")
        assert err == 0 or "Govern tokens has been initialized" in result, (
            "初始化治理代币失败： " + result
        )
