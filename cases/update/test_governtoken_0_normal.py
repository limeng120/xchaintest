"""
说明：测试治理代币
"""
import pytest


class TestGToken:
    """
    测试治理代币
    """

    alice_key = "output/data/alice"

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        初始化代币
        """
        print("\n初始化代币")
        err, result = input_args.test.xlib.govern_token(method_type="init")
        assert err == 0 or "Govern tokens has been initialized" in result, (
            "初始化治理代币失败： " + result
        )

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        代币转账
        """
        print("\n代币转账")
        err, alice_addr = input_args.test.xlib.get_address(self.alice_key)

        err, balance1 = input_args.test.xlib.get_total_token(addr=alice_addr)
        if err != 0:
            balance1 = 0

        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=alice_addr, amount="1"
        )
        assert err == 0, "代币转账失败:" + result

        err, balance2 = input_args.test.xlib.get_total_token(addr=alice_addr)
        assert err == 0, "代币查询失败"
        assert int(balance1) + 1 == int(balance2)

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        转账金额等于余额
        """
        print("\n转账金额等于余额")
        _, alice_addr = input_args.test.xlib.get_address(self.alice_key)
        err, balance1 = input_args.test.xlib.get_total_token(addr=alice_addr)
        amount = str(balance1)

        # 给alice转账xuper，转代币需要gas
        err, result = input_args.test.xlib.transfer(to=alice_addr, amount=1)
        assert err == 0, result

        err, result = input_args.test.xlib.govern_token(
            method_type="transfer",
            addr=input_args.node1,
            amount=amount,
            key=self.alice_key,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        转账金额等于0
        """
        print("\n转账金额等于0")
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=input_args.node1, amount="0"
        )
        assert err == 0, "代币转账失败:" + result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        查询账户的代币余额
        """
        print("\n查询账户的代币余额")
        err, result = input_args.test.xlib.govern_token(
            method_type="query", addr=input_args.node1
        )
        assert err == 0, result
