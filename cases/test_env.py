"""
测试环境是否可用、准备运行测试用例的测试账号
"""

import pytest


class TestEnv:

    #查询区块高度
    @pytest.mark.p0
    def test_trunkHeight(self, input):
        err, result = input.test.xlib.QueryBlockHeight()
        assert err == 0, "查询区块高度失败：" + result

    #查询分叉率
    @pytest.mark.p0
    def test_birfurcationRatio(self, input):

        err, result = input.test.BifurcationRatio()

        s = " ".join(str(x) for x in result)
        assert err == 0, "查询分叉率失败: " + s

    #执行基本功能测试，包括转账，创建合约账户，合约部署
    @pytest.mark.p0
    def test_basicFunction(self, input):
        err, result = input.test.BasicFunction()
        assert err == 0, "执行基本功能测试失败： " + result

    #初始化治理代币
    @pytest.mark.p0
    def test_initGovernToken(self, input):
        err, result = input.test.xlib.GovernToken(type="init")
        assert err == 0 or "Govern tokens has been initialized" in result, "初始化治理代币失败： " + result