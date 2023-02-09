"""
说明: 测试cpp合约sdk的异常场景
"""
import json
import pytest


class TestFeatursErr:
    """
    测试cpp合约sdk的异常场景
    """

    file = "cppTemplate/features.wasm"
    cname = "features"

    def transfer_use(self, invoke_args, input_args):
        """
        转账
        """

        err, cname_balan = input_args.test.xlib.get_balance(account=self.cname)
        if int(cname_balan) < 10:
            err, result = input_args.test.xlib.transfer(to=self.cname, amount="1000000")
            assert err == 0 and result != "Select utxo error", "转账给合约账户 失败： " + result

        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "transfer", args
        )
        assert err != 0, "转账成功， 不符合预期： " + result
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
            "wasm", self.cname, "query_tx", args
        )
        assert err == 0, "查询不存在的tx成功： " + result
        msg = "contract response: "
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
            "wasm", self.cname, "query_block", args
        )
        assert err == 0, "查询getBlock区块失败： " + result
        msg = "contract response: "
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】调put方法，key，value为null
        """
        print("\n【异常】调put方法,key,value为None")
        invoke_args = [
            {"key": "testvalue", "value": None},
            {"key": None, "value": "ss"},
            {"key": None, "value": None},
        ]
        for put_args in invoke_args:
            args = json.dumps(put_args)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "put", args
            )
            assert err != 0, "调put方法,key,value为null成功, 不符合预期： " + result
            msg = "expect string value, got <nil>"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        【异常】调put方法，key，value为小数
        """
        print("\n【异常】调put方法,key,value为小数")
        invoke_args = [
            {"key": "cde", "value": 1.34},
            {"key": 1.34, "value": "abc"},
            {"key": 1.34, "value": 1.34},
        ]
        for put_args in invoke_args:
            args = json.dumps(put_args)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "put", args
            )
            assert err != 0, "调put方法,key,value为小数成功,不符合预期： " + result
            msg = "expect string value, got 1.34"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        【异常】put不传/漏传kv
        """
        print("\n【异常】put不传/漏传key")
        invoke_args = [
            {},
            {"key": "", "value": ""},
            {"key": "", "value": "err"},
            {"value": "err"},
        ]
        for put_args in invoke_args:
            args = json.dumps(put_args)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "put", args
            )
            assert err != 0, "异常条件put不传/漏传key成功， 不符合预期： " + result
            msg = "contract error status:500 message:missing key"
            assert msg in result, "报错信息错误"

        print("\n【异常】put不传/漏传value")
        invoke_args = [{"key": "dudu", "value": ""}, {"key": "testerr"}]
        for put_args in invoke_args:
            args = json.dumps(put_args)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "put", args
            )
            assert err != 0, "异常条件put不传/漏传value成功， 不符合预期： " + result
            msg = "contract error status:500 message:missing value"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        【异常】调put方法，写入kv，并给合约转账，amount设为负数
        """
        print("\n【异常】调put方法，写入kv，并给合约转账,amount设为负数")
        invoke_args = {"key": "test$", "value": "value$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args, amount=-10
        )
        assert err != 0, "put方法，写入kv,并给合约转账,amount设为负数成功,不符合预期：" + result
        msg = "Amount in transaction can not be negative number"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        【异常】调get方法，key为null
        """
        invoke_args = {"key": None}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err != 0, "get方法，key为null成功,不符合预期： " + result
        msg = "expect string value, got <nil>"
        assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", json.dumps({})
        )
        assert err != 0, "get方法，key为null金额成功,不符合预期： " + result
        msg = "message:failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case08(self, input_args):
        """
        【异常】调get方法，key为小数
        """
        invoke_args = {"key": 1.34}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err != 0, "get方法，key为小数 成功,不符合预期：" + result
        msg = "bad key key, expect string value, got 1.34"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case09(self, input_args):
        """
        【异常】get不存在的key
        """
        invoke_args = {"key": "notexit"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err != 0, "get不存在的key成功,不符合预期：" + result
        msg = "contract error status:500 message:failed"
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
            "wasm", self.cname, "get", args, amount=-10
        )
        assert err != 0, "get方法，写入kv,并给合约转账,amount设为负数成功,不符合预期：" + result
        msg = "Amount in transaction can not be negative number"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case12(self, input_args):
        """
        【异常】iterator 迭代访问,start为空,或者都为空
        """
        print("\n【异常】iterator 迭代访问,start为空")
        invoke_args = [
            {"limit": "test110"},
            {"start": "", "limit": "test110"},
            {},
            {"start": "", "limit": ""},
        ]
        for iter_args in invoke_args:
            args = json.dumps(iter_args)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "iterator", args
            )
            assert err != 0, "iterator 迭代访问,start为空成功,不符合预期： " + result
            msg = "500 message:missing start"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case13(self, input_args):
        """
        【异常】iterator 迭代访问,limit为空
        """
        print("\n【异常】iterator 迭代访问,limit为空")
        invoke_args = [{"start": "test1"}, {"start": "test12", "limit": ""}]
        for iter_args in invoke_args:
            args = json.dumps(iter_args)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "iterator", args
            )
            assert err != 0, "iterator 迭代访问,limit为空成功,不符合预期： " + result
            msg = "500 message:missing limit"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case14(self, input_args):
        """
        【异常】iterator 迭代访问,limit和start都为空
        """
        print("\n【异常】call:调用不存在的合约")
        invoke_args = {"contract": "counter_gn11", "key": "qakey", "method": "increase"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "call", args
        )
        assert err != 0, "call:调用不存在的合约 成功,不符合预期： " + result
        msg = "contract error status:500 message:call failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case15(self, input_args):
        """
        【异常】call:调用不存在的合约方法
        """
        print("\n【异常】call:调用不存在的合约方法")
        invoke_args = {"contract": "counter_gn", "key": "qakey", "method": "increase11"}

        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "call", args
        )
        assert err != 0, "调用不存在的合约方法  成功,不符合预期： " + result
        msg = "contract error status:500 message:call failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case16(self, input_args):
        """
        【异常】json_load_dump 读取参数value格式不对
        """
        invoke_args = [
            {"value": "hello"},
            {"value": "!@#$%^&*()_-++?><;"},
            {"value": ""},
            {"value": " "},
            {},
        ]
        for loadargs in invoke_args:
            args = json.dumps(loadargs)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "json_load_dump", args
            )
            assert err != 0, "json_load_dump 读取参数value格式不对且成功,不符合预期： " + result
            msg = "code = Unknown desc = Err:500-50501-contract invoke failed+trap error:allocate exception"
            assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", json.dumps({"value": 3.14})
        )
        assert err != 0, "json_load_dump 读取参数value为小数且成功,不符合预期： " + result
        msg = "bad key value, expect string value, got 3.14"
        assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", json.dumps({"value": True})
        )
        assert err != 0, "json_load_dump 读取参数value为bool且成功,不符合预期： " + result
        msg = "bad key value, expect string value, got true"
        assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", json.dumps({"value": 22})
        )
        assert err != 0, "json_load_dump 读取参数value为数字且成功,不符合预期： " + result
        msg = "bad key value, expect string value, got 22"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case17(self, input_args):
        """
        【异常】transfer，转账,参数不足
        """
        print("\n【异常】transfer，转账xuper，参数to缺少")
        invoke_args = [{"to": "", "amount": ""}, {"amount": "10"}, None]
        for trans_args in invoke_args:
            result = self.transfer_use(trans_args, input_args)
            msg = "missing to"
            assert msg in result, "报错信息错误"

        print("\n【异常】transfer，转账xuper，参数amount缺少")
        result = self.transfer_use({"to": "123", "amount": ""}, input_args)
        msg = "missing amount"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case18(self, input_args):
        """
        【异常】转账,参数为空
        """
        print("\n【异常】转账,参数为空")
        result = self.transfer_use({"to": " ", "amount": " "}, input_args)
        msg = "message:transfer failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case19(self, input_args):
        """
        【异常】features合约余额不足，转账
        """
        print("\n【异常】features合约余额不足，转账")
        # 1.部署一个合约
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", "features999", self.file, contract_account, args
        )
        assert err == 0 or "exist" in result, "部署features合约失败： " + result
        # 2.直接转账
        invoke_args = {"to": "testAccount", "amount": "1.5"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", "features999", "transfer", args
        )
        assert err != 0, "features合约不足时转账成功, 不符合预期： " + result
        msg = "transfer failed"
        assert msg in result, "报错信息错误"
