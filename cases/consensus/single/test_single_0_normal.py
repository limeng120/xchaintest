"""
说明：single共识节点网络的测试
"""
import numpy as np
import pytest


class TestSingle:
    """
    single共识节点网络的测试
    """

    @pytest.mark.p2
    def test_trunk_height(self, input_args):
        """
        查询区块高度
        """
        err, result = input_args.test.trunk_height()

        if np.std(result) > 3:
            err = 1

        s = " ".join(str(x) for x in result)
        assert err == 0, "查询区块高度失败：" + s

    @pytest.mark.p2
    def test_birfurcation_ratio(self, input_args):
        """
        查询分叉率
        """
        err, result = input_args.test.bifurcation_ratio()

        s = " ".join(str(x) for x in result)
        assert err == 0, "查询分叉率失败: " + s

    @pytest.mark.p2
    def test_basic_function(self, input_args):
        """
        执行基本功能测试，包括转账，创建合约账户，合约部署
        """
        err, result = input_args.test.basic_function(host=input_args.host)
        assert err == 0, "执行基本功能测试失败： " + result
