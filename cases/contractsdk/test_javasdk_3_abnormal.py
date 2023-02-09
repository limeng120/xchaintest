"""
说明: 测试java合约sdk的异常场景
"""
import json
import time
import pytest


class TestCallErr:
    """
    测试java合约sdk的异常场景
    """

    c1name = "callc1"
    c2name = "callc2"

    def check_balance(self, input_args, c1_bal, c2_bal):
        """
        校验余额是否符合预期
        """
        err, c1_balance = input_args.test.xlib.get_balance(account=self.c1name)
        assert err == 0 and int(c1_balance) == c1_bal, (
            self.c1name + "余额不是" + str(c1_bal) + "，而是" + c1_balance
        )
        err, c2_balance = input_args.test.xlib.get_balance(account=self.c2name)
        assert err == 0 and int(c2_balance) == c2_bal, (
            self.c2name + "余额不是" + str(c2_bal) + "，而是" + c2_balance
        )

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case01(self, input_args):
        """
        【异常】callc1 callc2合约余额不足，调用callc1合约invoke方法
        """
        print("\n【异常】callc1 callc2合约余额不足，调用callc1合约invoke方法")
        self.check_balance(input_args, 0, 0)
        invoke_args = {"to": "test"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.c1name, "invoke", args, fee=30
        )
        assert err != 0, "异常情况callc1 callc2合约余额不足，调用callc1合约invoke方法成功" + result
        msg = "no enough money(UTXO) to start this transaction"
        assert msg in result, "报错信息错误"

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case02(self, input_args):
        """
        【异常】callc1 合约余额不足，调用callc1合约invoke方法
        """
        invoke_args = {"to": "test"}
        args = json.dumps(invoke_args)
        print("\n【异常】callc1 合约余额不足，调用callc1合约invoke方法")
        err, result = input_args.test.xlib.transfer(to=self.c2name, amount="1000")
        assert err == 0, "转账给callc2 失败" + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        self.check_balance(input_args, 0, 1000)

        err, result = input_args.test.xlib.invoke_contract(
            "native", self.c1name, "invoke", args, fee=30
        )
        assert err != 0, "异常情况callc1 callc2合约余额不足，调用callc1合约invoke方法成功" + result
        msg = "no enough money(UTXO) to start this transaction"
        assert msg in result, "报错信息错误"

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case03(self, input_args):
        """
        【异常】callc2合约余额不足，调用callc1合约invoke方法
        """
        print("\n【异常】callc2合约余额不足，调用callc1合约invoke方法")
        err, result = input_args.test.xlib.transfer(to=self.c1name, amount="2")
        assert err == 0, "转账给callc1 失败" + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        self.check_balance(input_args, 2, 1000)

        # c1=2 c2=1000, 第1次invoke可成功
        invoke_args = {"to": "test"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.c1name, "invoke", args, fee=30
        )
        assert err == 0, result

        self.check_balance(input_args, 1, 0)

        # c1=1 c2=0, 第2次invoke失败
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.c1name, "invoke", args, fee=30
        )
        assert err != 0, "异常情况callc1 callc2合约余额不足，调用callc1合约invoke方法成功" + result
        msg = "put nil value"
        assert msg in result, "报错信息错误"

        # 消耗c1的余额1
        err, result = input_args.test.xlib.transfer(to=self.c2name, amount="1000")
        assert err == 0, result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        self.check_balance(input_args, 1, 1000)

        time.sleep(60)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.c1name, "invoke", args, fee=30
        )
        assert err == 0, result

        self.check_balance(input_args, 0, 0)
