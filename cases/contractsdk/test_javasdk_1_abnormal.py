"""
说明: 测试java合约sdk的异常场景
"""
import json
import pytest


class TestBuiltinErr:
    """
    测试java合约sdk的异常
    """

    cname = "builtin_types_j"

    def transfer_use(self, invoke_args, input_args):
        """
        转账
        """
        # 1.先给合约账户转账
        err, cname_balan = input_args.test.xlib.get_balance(account=self.cname)
        if int(cname_balan) < 10:
            err, result = input_args.test.xlib.transfer(to=self.cname, amount="1000000")
            assert err == 0 and result != "Select utxo error", "转账给合约账户 失败： " + result

        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "transfer", args
        )
        assert err != 0, "异常条件转账成功， 不符合预期： " + result
        return result

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        查询不存在的tx
        """
        print("\n【异常】查询不存在的txid")
        invoke_args = {
            "txid": "e74f44d613c30637b6b0abbfa1f0ad4dc4fad3f36a947d0e7af8cdb216abd7b5"
        }
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "getTx", args
        )
        assert err != 0, "查询不存在的tx成功： " + result
        msg = "transaction not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        查询不存在的区块
        """
        print("\n【异常】查询不存在的block")
        invoke_args = {
            "blockid": "a18f905a1ce81a78d0ea8c56002870cc046e3fc86064201bc398a4b3a2758ce2"
        }
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "getBlock", args
        )
        assert err != 0, "查询getBlock区块失败： " + result
        msg = "block not exist in this chain"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】transfer，转账xuper，数额负数
        """
        print("\n【异常】transfer，转账xuper，数额负数")
        invoke_args = {"to": "testAccount", "amount": "-10"}
        result = self.transfer_use(invoke_args, input_args)
        msg = "amount must not be negative"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        【异常】transfer，转账xuper，参数to缺少
        """
        print("\n【异常】transfer，转账xuper，参数to缺少")
        invoke_args = {"amount": "10"}
        result = self.transfer_use(invoke_args, input_args)
        msg = "missing to"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        【异常】transfer，转账xuper，数额是小数
        """
        print("\n【异常】transfer，转账xuper，数额是小数")
        invoke_args = {"to": "testAccount", "amount": "1.5"}
        result = self.transfer_use(invoke_args, input_args)
        msg = "NumberFormatException"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        【异常】transfer，转账xuper，数额超余额
        """
        print("\n【异常】transfer，转账xuper，数额超余额")
        invoke_args = {"to": "testAccount", "amount": "10000000000000000000000"}
        result = self.transfer_use(invoke_args, input_args)
        msg = "no enough money(UTXO) to start this transaction"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        transfer，转账，数额0
        """
        print("\n【异常】transfer，转账，数额0")
        invoke_args = {"to": "testAccount", "amount": "0"}
        result = self.transfer_use(invoke_args, input_args)
        msg = "should  be large than zero"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case08(self, input_args):
        """
        【异常】transferAndPrintAmount，给合约转账，合约内部查询转账金额，amount设为负数
        """
        print("\n【异常】transferAndPrintAmount,给合约转账,合约内部查询转账金额,amount设为负数")
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "transferAndPrintAmount", "None", amount=-10
        )

        assert err != 0, "合约内部查询转账金额成功， 不符合预期： " + result
        msg = "amount must not be negative"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case09(self, input_args):
        """
        【异常】调put方法，写入kv，并给合约转账，amount设为负数
        """
        print("\n【异常】调put方法，写入kv，并给合约转账，amount设为负数")
        invoke_args = {"key": "test$", "value": "value$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "put", args, amount=-1
        )
        assert err != 0, "合约内部查询转账金额成功， 不符合预期： " + result
        msg = "Amount in transaction can not be negative number"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case10(self, input_args):
        """
        【异常】调get方法，读取key，并给合约转账，amount设为负数
        """
        print("\n【异常】调get方法，写入kv，并给合约转账，amount设为负数")
        invoke_args = {"key": "test$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "get", args, amount=-1
        )
        assert err != 0, "合约内部查询转账金额成功,不符合预期： " + result
        msg = "Amount in transaction can not be negative number"
        assert msg in result, "报错信息错误"
