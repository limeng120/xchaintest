"""
说明：测试治理代币
"""
import pytest


class TestGToken:
    """
    测试治理代币
    """

    alice_key = "output/data/alice"

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        【异常】重复初始化代币
        """
        print("\n【异常】重复初始化代币")
        err, result = input_args.test.xlib.govern_token(method_type="init")
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        【异常】转账金额超过余额
        """
        print("\n【异常】转账金额超过余额")
        err, alice_addr = input_args.test.xlib.get_address(self.alice_key)
        err, balance1 = input_args.test.xlib.get_total_token(addr=alice_addr)

        amount = str(int(balance1) + 1)
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer",
            addr=input_args.node1,
            amount=amount,
            key=self.alice_key,
        )
        assert err != 0, result
        assert "sender's insufficient balance" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】转账：代币数为浮点类型
        """
        print("\n【异常】转账：代币数为浮点类型")
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=input_args.node1, amount="1.0"
        )
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        【异常】转账：代币数为负数
        """
        print("\n【异常】转账：代币数为负数")
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=input_args.node1, amount="-1"
        )
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        【异常】转账：代币数为字符串
        """
        print("\n【异常】转账：代币数为字符串")
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=input_args.node1, amount="aaa"
        )
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        【异常】转账：代币数为特殊字符
        """
        print("\n【异常】转账：代币数为特殊字符")
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=input_args.node1, amount="!!!"
        )
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        【异常】查询没有代币的账户的代币余额
        """
        print("\n查询没有代币的账户的代币余额")
        err, result = input_args.test.xlib.govern_token(method_type="query", addr="aaa")
        assert err != 0, result
