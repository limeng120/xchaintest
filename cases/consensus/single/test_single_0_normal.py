"""
说明：single共识节点网络的测试
"""
import numpy as np
import pytest


class TestSingle:

    #查询区块高度
    @pytest.mark.p2
    def test_trunkHeight(self, input):

        err, result = input.test.TrunkHeight()

        if np.std(result) > 3:
            err = 1

        s = " ".join(str(x) for x in result)
        assert err == 0, "查询区块高度失败：" + s

    #查询分叉率
    @pytest.mark.p2
    def test_birfurcationRatio(self, input):

        err, result = input.test.BifurcationRatio()

        s = " ".join(str(x) for x in result)
        assert err == 0, "查询分叉率失败: " + s

    #执行基本功能测试，包括转账，创建合约账户，合约部署
    @pytest.mark.p2
    def test_basicFunction(self, input):
        err, result = input.test.BasicFunction(host=input.host)
        assert err == 0, "执行基本功能测试失败： " + result