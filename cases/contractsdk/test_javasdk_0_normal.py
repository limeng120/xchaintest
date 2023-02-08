"""
说明: 测试java合约sdk
"""
import json
import pytest


class TestBuiltin:
    """
    测试java合约sdk
    """

    file = "javaTemplate/builtin-types-0.1.0-jar-with-dependencies.jar"
    cname = "builtin_types_j"
    # 合约余额
    amount = "70"
    befor_account = ""
    befor_cname = ""
    widthCount = "".zfill(1024)

    def get_list(self, invoke_args, input_args):
        """
        调用getlist合约方法
        """
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "getList", args
        )
        assert err == 0, "调getList方法，传入start 失败" + result

    def trans_use(self, input_args):
        """
        转账
        """
        # 1.先给合约账户转账
        err, cname_balan = input_args.test.xlib.get_balance(account=self.cname)
        if int(cname_balan) < int(self.amount):
            err, result = input_args.test.xlib.transfer(to=self.cname, amount="1000000")
            assert err == 0 and result != "Select utxo error", "转账给合约账户 失败： " + result

        # 2.查询账户余额
        err, self.befor_account = input_args.test.xlib.get_balance(
            account="testAccount"
        )
        assert err == 0, "查询testAccount余额 失败" + self.befor_account
        err, self.befor_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0, "查询" + self.cname + "余额 失败" + self.befor_cname

    @pytest.mark.skip("虚拟机部署java")
    def test_case01(self, input_args):
        """
        合约部署builtin-types合约
        """
        print("\n合约部署builtin-types合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.deploy_contract(
            "native", "java", self.cname, self.file, contract_account, "None"
        )
        assert err == 0 or "exist" in result, "部署builtin-types合约失败： " + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case02(self, input_args):
        """
        getTx，查询交易
        """
        print("\ngetTx,查询交易")
        err, result = input_args.test.xlib.transfer(to="abc", amount="1")
        assert err == 0, result

        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        invoke_args = {"txid": txid}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "getTx", args
        )
        assert err == 0, "查询getTx交易失败： " + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case03(self, input_args):
        """
        getBlock，查询区块
        """
        print("\ngetBlock，查询区块")
        err, result = input_args.test.xlib.transfer(to="abc", amount="1")
        assert err == 0, result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result
        err, blockid = input_args.test.xlib.query_tx(txid)
        assert err == 0, "查询block失败：" + blockid
        assert blockid != " "
        invoke_args = {"blockid": blockid}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "getBlock", args
        )
        assert err == 0, "查询getBlock区块失败： " + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case04(self, input_args):
        """
        transfer，转账
        """
        print("\ntransfer，转账")
        # 查余额
        self.trans_use(input_args)
        invoke_args = {"to": "testAccount", "amount": self.amount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "transfer", args, fee=1
        )
        assert err == 0, "转账失败： " + result
        print("转账后查询账户")
        err, after_account = input_args.test.xlib.get_balance(account="testAccount")
        assert err == 0 and int(after_account) == int(self.befor_account) + int(
            self.amount
        ), ("查询testAccount余额 失败" + after_account)

        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(
            self.amount
        ), ("查询" + self.cname + "余额 失败" + after_cname)

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case05(self, input_args):
        """
        调put方法,写入1个kv，记录个数
        """
        print("\n调put方法,写入1个kv")
        invoke_args = {"key": "test1", "value": "value1"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "put", args
        )
        assert err == 0, "调put方法,写入kv 失败" + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case06(self, input_args):
        """
        调get方法,查询1个kv，记录个数
        """
        print("\n调get方法,查询1个kv")
        invoke_args = {"key": "test1"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "get", args
        )
        assert err == 0, "调get方法,查询kv 失败" + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case07(self, input_args):
        """
        调getList方法，传入start
        """
        print("\n调getList方法，传入start")
        invoke_args = {"start": "test1"}
        self.get_list(invoke_args, input_args)

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case10(self, input_args):
        """
        调getList方法，传入start, start后无数据
        """
        print("\n调getList方法，传入start,start后无数据")
        invoke_args = {"start": "key"}
        self.get_list(invoke_args, input_args)

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case11(self, input_args):
        """
        调put方法，key含特殊字符,value含特殊字符
        """
        print("\n调put方法，key含特殊字符,value含特殊字符")
        invoke_args = {"key": "test$", "value": "value$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "put", args
        )
        assert err == 0, "调put方法:key和value含特殊字符 失败" + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case12(self, input_args):
        """
        调get方法,key含特殊字符
        """
        print("\n调get方法,key含特殊字符")
        invoke_args = {"key": "test$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "get", args
        )
        assert err == 0, "调get方法,key含特殊字符 失败" + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case13(self, input_args):
        """
        调put方法,key长度1k,value长度1k
        """
        print("\n调put方法,key长度1k,value长度1k")
        invoke_args = {
            "key": "test" + self.widthCount,
            "value": "value" + self.widthCount,
        }
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "put", args
        )
        assert err == 0, "调put方法：key和value长度1K, 失败" + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case14(self, input_args):
        """
        调get方法，key长度1k
        """
        print("\n调get方法,key长度1k")
        invoke_args = {"key": "test" + self.widthCount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "get", args
        )
        assert err == 0, "调get方法,key长度1k 失败" + result
        result = input_args.test.xlib.get_value_from_res(result)
        # value值长度是1024
        assert result == "value" + self.widthCount

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case15(self, input_args):
        """
        authRequire，查询合约方法的调用者
        """
        print("\nauthRequire,查询合约方法的调用者")
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "authRequire", "None"
        )
        assert err == 0, "authRequire,查询合约方法的调用者 失败" + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case16(self, input_args):
        """
        transferAndPrintAmount，给合约转账，合约内部查询转账金额
        """
        print("\ntransferAndPrintAmount,给合约转账,合约内部查询转账金额")
        # 查余额
        self.trans_use(input_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "transferAndPrintAmount", "None", amount=10
        )
        assert err == 0, "合约内部转账失败： " + result
        print("转账后查询合约")
        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(10), (
            "查询" + self.cname + "余额 失败" + after_cname
        )

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case17(self, input_args):
        """
        调put方法，写入kv，并给合约转账
        """
        print("\n调put方法，写入kv，并给合约转账")
        # 查余额
        self.trans_use(input_args)
        invoke_args = {"key": "test$", "value": "value$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "put", args, amount=1
        )
        assert err == 0, "调put方法，写入kv,并给合约转账 失败" + result
        print("转账后查询合约")
        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(1), (
            "查询" + self.cname + "余额 失败" + after_cname
        )

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case18(self, input_args):
        """
        调get方法，读取key，并给合约转账
        """
        print("\n调get方法,写入kv,并给合约转账")
        # 查余额
        self.trans_use(input_args)
        invoke_args = {"key": "test$"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "get", args, amount=1
        )
        assert err == 0, "调get方法,写入kv,并给合约转账 失败" + result
        print("转账后查询合约")
        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(1), (
            "查询" + self.cname + "余额 失败" + after_cname
        )
