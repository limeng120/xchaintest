"""
说明: 测试平行链上执行基本功能：转账、创建合约账户、合约部署调用
"""
import pytest


class TestChainBasic:
    """
    测试平行链上执行基本功能：转账、创建合约账户、合约部署调用
    """

    def basic(self, input_args, name):
        """
        执行基本功能
        """
        print(name + "共识的平行链，执行基本功能")
        # 最多失败重试3次
        for _ in range(3):
            err, result = input_args.test.basic_function(name=name)
            if err == 0:
                break
        assert err == 0, name + "平行链上，基本功能执行失败：" + result

    @pytest.mark.p1
    def test_case02(self, input_args):
        """
        single共识的平行链，测试基本功能
        """
        self.basic(input_args, name="hisingle1")

    @pytest.mark.p1
    def test_case03(self, input_args):
        """
        tdpos共识的平行链，测试基本功能
        """
        self.basic(input_args, name="hitdpos1")

    @pytest.mark.p1
    def test_case04(self, input_args):
        """
        xpos共识的平行链，测试基本功能
        """
        self.basic(input_args, name="hixpos1")

    @pytest.mark.p1
    def test_case05(self, input_args):
        """
        poa共识的平行链，测试基本功能
        """
        self.basic(input_args, name="hipoa1")

    # @pytest.mark.p1
    # def test_case06(self, input_args):
    #     """
    #     xpoa共识的平行链，测试基本功能
    #     """
    #     self.basic(input_args, name="hixpoa1")
