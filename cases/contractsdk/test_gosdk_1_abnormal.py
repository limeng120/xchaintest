"""
说明: 测试go合约sdk的异常场景
"""
import json
import pytest


class TestGOFeatursErr:
    """
    测试go合约sdk的异常场景
    """

    cname = "features_go"

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case01(self, input_args):
        """
        查询不存在的tx
        """
        # 间隔3个区块,加载blockid
        print("\n【异常】查询不存在的txid")
        invoke_args = {
            "txid": "c31db35d644e89919bb5668368b4d9e8c7d475f3eb9c8eb6604a0ad43246a779"
        }
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "QueryTx", args
        )
        assert err != 0 and "transaction not found" in result, "查询不存在的tx成功： " + result

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case02(self, input_args):
        """
        查询不存在的区块
        """
        # 间隔3个区块,加载blockid
        print("\n【异常】查询不存在的block")
        invoke_args = {
            "blockid": "306edc9c26a6df7557455455f87c408b49036758152087a6d8d2617a5e9c234b"
        }
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "QueryBlock", args
        )
        assert err != 0 and "block not exist in this chain" in result, (
            "查询getBlock区块失败： " + result
        )

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case03(self, input_args):
        """
        【异常】合约余额不足
        """
        print("\n【异常】合约余额不足")
        invoke_args = {"to": "123456", "amount": "1000000000000000"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "Transfer", args
        )
        assert err != 0 and "no enough money" in result, "合约余额不足成功, 不符合预期： " + result

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case04(self, input_args):
        """
        【异常】转账金额为负数
        """
        print("\n【异常】转账金额为负数")
        invoke_args = {"to": "123456", "amount": "-100"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "Transfer", args
        )
        assert err != 0 and "amount should not be negative" in result, (
            "合约余额不足成功, 不符合预期： " + result
        )

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case05(self, input_args):
        """
        【异常】转账金额不是数字
        """
        print("\n【异常】转账金额不是数字")
        invoke_args = {"to": "123456", "amount": "hello"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "Transfer", args
        )
        assert err != 0 and "message:bad amount format" in result, (
            "合约余额不足成功, 不符合预期： " + result
        )
