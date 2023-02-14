"""
说明: 测试cpp合约sdk
"""
import json
import pytest


class TestFeatures2:
    """
    测试cpp合约sdk
    """

    cname = "features"
    # 合约余额
    amount = "70"
    befor_account = ""
    befor_cname = ""

    def trans_use(self, account, input_args):
        """
        转账
        """
        # 1.先给合约账户转账
        err, cname_balan = input_args.test.xlib.get_balance(account=self.cname)
        if int(cname_balan) < int(self.amount):
            err, result = input_args.test.xlib.transfer(to=self.cname, amount="1000000")
            assert err == 0 and result != "Select utxo error", "转账给合约账户 失败： " + result

        # 2.查询账户余额
        err, self.befor_account = input_args.test.xlib.get_balance(account=account)
        assert err == 0, "查询 " + account + " 余额 失败" + self.befor_account
        err, self.befor_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0, "查询 " + self.cname + " 余额 失败" + self.befor_cname

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        调put方法,并给合约转账
        """
        print("\n调put方法,并给合约转账")
        invoke_args = {"key": "test$", "value": "value$"}
        args = json.dumps(invoke_args)
        # "查询features"
        err, befor_features = input_args.test.xlib.get_balance(account=self.cname)
        # 转账
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args, amount=1
        )
        assert err == 0, "调put方法,并给合约转账 失败" + result
        err, after_features = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_features) == int(befor_features) + int(1), (
            "查询" + self.cname + "余额 失败" + after_features
        )

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        调get方法，读取key，并给合约转账
        """
        print("\n调get方法，读取key,并给合约转账")
        invoke_args = {"key": "test$"}
        args = json.dumps(invoke_args)
        # "查询features"
        err, befor_features = input_args.test.xlib.get_balance(account=self.cname)
        # 转账
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "get", args, amount=1
        )
        assert err == 0, "调put方法,并给合约转账 失败" + result
        err, after_features = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_features) == int(befor_features) + int(1), (
            "查询" + self.cname + "余额 失败" + after_features
        )

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        logging 从合约内写一条日志
        写入logs/xchain.log文件中 自动化没有 cat logs/xchain.log |grep "log from contract"
        """
        print("\nlogging 从合约内写一条日志")
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "logging", "None"
        )
        assert err == 0, "从合约内写一条日志 失败" + result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        iterator迭代访问,limit大于start
        """
        print("\niterator迭代访问,limit大于start")
        invoke_args = {"start": "test1", "limit": "test110"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "iterator", args
        )
        assert err == 0, "迭代访问,limit大于start失败" + result
        assert result.split("response:")[-1].count("test") == 1, "返回的个数不匹配" + result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        iterator 迭代访问,limit等于start
        """
        print("\niterator迭代访问,limit等于start")
        invoke_args = [
            {"start": "test1", "limit": "test1"},
            {"start": "test210", "limit": "test210"},
        ]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "iterator", args
            )
            assert err == 0, "迭代访问,limit等于start失败" + result
            getdiff = result.split("\n")[0].split("response:")[-1]
            assert getdiff == " ", "范围内有数据,失败" + result

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        iterator 迭代访问,limit,start范围不存在
        """
        print("\niterator迭代访问,limit,start范围不存在")
        invoke_args = [
            {"start": "test1050", "limit": "test1055"},
            {"start": " ", "limit": " "},
        ]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "iterator", args
            )
            assert err == 0, "迭代访问,limit,start范围不存在 失败" + result
            getdiff = result.split("\n")[0].split("response:")[-1]
            assert getdiff == " ", "范围内有数据,失败" + result

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        caller 获取合约发起者
        """
        print("\ncaller 获取合约发起者")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "caller", "None", account=contract_account
        )
        assert err == 0, "caller 获取合约发起者 失败" + result
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "caller", "None", keys="data/keys/"
        )
        assert err == 0, "caller 获取合约发起者 失败" + result

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        call 发起跨合约调用
        """
        print("\ncall 发起跨合约调用")
        # 1.合约调用
        invoke_args = {"contract": "hello_cpp", "key": "dudu", "method": "increase"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "call", args
        )
        assert err == 0, "call 发起跨合约调用 失败" + result
        value1 = input_args.test.xlib.get_value_from_res(result)
        # 2.查询合约调用次数
        query = {"key": "dudu"}
        args = json.dumps(query)
        err, get_result = input_args.test.xlib.query_contract(
            "wasm", "hello_cpp", "get", args
        )
        value2 = input_args.test.xlib.get_value_from_res(get_result)
        assert value1 == value2, "查询跨合约调用次数不匹配" + get_result

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        json_literal 返回 json 一个字面量
        """
        print("\njson_literal 返回 json 一个字面量")
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "json_literal", "None"
        )
        assert err == 0, "json_literal 返回 json 一个字面量 失败" + result

    @pytest.mark.p2
    def test_case10(self, input_args):
        """
        json_load_dump 读取参数 value,array类型
        """
        print("\njson_load_dump 读取参数 value,array类型")
        invoke_args = '["hello","world"]'
        args = json.dumps({"value": invoke_args})
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", args
        )
        assert err == 0, "json_load_dump 读取参数 value,array类型 失败" + result

        assert json.loads(result.split("response:")[-1].split("\n")[0]) == json.loads(
            invoke_args
        ), ("array类型结果值不匹配" + result)

    @pytest.mark.p2
    def test_case11(self, input_args):
        """
        json_load_dump 读取参数 value,bool类型
        """
        print("\njson_load_dump 读取参数 value,bool类型")
        invoke_args = [{"value": "true"}, {"value": "false"}]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "json_load_dump", args
            )
            assert err == 0, "json_load_dump 读取参数 value,bool类型 失败" + result

    @pytest.mark.p2
    def test_case12(self, input_args):
        """
        json_load_dump 读取参数 value,float类型
        """
        print("\njson_load_dump 读取参数 value,float类型")
        invoke_args = {"value": "3.14"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", args
        )
        assert err == 0, "json_load_dump 读取参数 value,float类型 失败" + result

    @pytest.mark.p2
    def test_case13(self, input_args):
        """
        json_load_dump 读取参数 value,int类型
        """
        print("\njson_load_dump 读取参数 value,int类型")
        invoke_args = {"value": "5"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", args
        )
        assert err == 0, "json_load_dump 读取参数 value,int类型 失败" + result

    @pytest.mark.p2
    def test_case14(self, input_args):
        """
        json_load_dump 读取参数 value,string类型
        """
        print("\njson_load_dump 读取参数 value,string类型")
        invoke_args = ['"hello"', "null", '"!@#$%^&*()_-++?><;"']
        for arg in invoke_args:
            args = json.dumps({"value": arg})
            err, result = input_args.test.xlib.invoke_contract(
                "wasm", self.cname, "json_load_dump", args
            )
            assert err == 0, "json_load_dump 读取参数 value,string类型 失败" + result
            assert json.loads(
                result.split("response:")[-1].split("\n")[0]
            ) == json.loads(arg), ("string类型结果值不匹配" + result)

    @pytest.mark.p2
    def test_case15(self, input_args):
        """
        json_load_dump 读取参数 value,object类型
        """
        print("\njson_load_dump 读取参数 value,object类型")
        invoke_args = '{"data":{"content":[{"id":"001","value":"testvalue"},\
        {"id":"002","value":" testvalue1"}]},"message":"success"}'
        args = json.dumps({"value": invoke_args})
        print(args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "json_load_dump", args
        )
        assert err == 0, "json_load_dump 读取参数 value,object类型 失败" + result
        assert json.loads(result.split("response:")[-1].split("\n")[0]) == json.loads(
            invoke_args
        ), ("object类型结果值不匹配" + result)

    @pytest.mark.p2
    def test_case16(self, input_args):
        """
        getTx，查询交易
        """
        print("\nquery_tx,查询交易")
        err, txid = input_args.test.xlib.transfer(to=self.cname, amount="1")
        assert err == 0, txid

        # 等tx上链
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        invoke_args = {"tx_id": txid}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "query_tx", args
        )
        assert err == 0, "查询query_tx交易失败： " + result
        err, blockid = input_args.test.xlib.query_tx(txid)
        assert blockid in result, "查询结果错误"

    @pytest.mark.p2
    def test_case17(self, input_args):
        """
        getBlock，查询区块
        """
        print("\nquery_block,查询区块")
        err, txid = input_args.test.xlib.transfer(to=self.cname, amount="1")
        assert err == 0, txid
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result
        err, blockid = input_args.test.xlib.query_tx(txid)
        assert err == 0, "查询block失败：" + blockid
        assert blockid != " "
        invoke_args = {"blockid": blockid}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "query_block", args
        )
        assert err == 0, "查询query_block区块失败： " + result

    @pytest.mark.p2
    def test_case18(self, input_args):
        """
        transfer,使用合约账户转账
        """
        print("\ntransfer,使用合约账户转账")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        # 查余额
        self.trans_use("testAccount", input_args)
        invoke_args = {"to": "testAccount", "amount": self.amount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "transfer", args, account=contract_account, fee=100
        )
        assert err == 0, "使用合约账户转账失败： " + result
        print("转账后查询账户")
        err, after_account = input_args.test.xlib.get_balance(account="testAccount")
        assert err == 0 and int(after_account) == int(self.befor_account) + int(
            self.amount
        ), ("查询testAccount余额 失败" + after_account)

        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(
            self.amount
        ), ("查询" + self.cname + "余额 失败" + after_cname)

    @pytest.mark.p2
    def test_case19(self, input_args):
        """
        transfer,使用普通账户转账
        """
        print("\ntransfer,使用普通账户转账")
        # 查余额
        self.trans_use("testAccount", input_args)
        invoke_args = {"to": "testAccount", "amount": self.amount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "transfer", args, keys="data/keys/", fee=100
        )
        assert err == 0, "使用普通账户转账失败： " + result
        print("转账后查询账户")
        err, after_account = input_args.test.xlib.get_balance(account="testAccount")
        assert err == 0 and int(after_account) == int(self.befor_account) + int(
            self.amount
        ), ("查询testAccount余额 失败" + after_account)

        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(
            self.amount
        ), ("查询" + self.cname + "余额 失败" + after_cname)

    @pytest.mark.p2
    def test_case20(self, input_args):
        """
        transfer,自身转账
        """
        print("\ntransfer,自身转账")
        # 查余额
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        self.trans_use(contract_account, input_args)
        invoke_args = {"to": contract_account, "amount": self.amount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "transfer", args, account=contract_account, fee=100
        )
        assert err == 0, "自身转账失败： " + result
        print("转账后查询合约账户")
        err, after_account = input_args.test.xlib.get_balance(account=contract_account)
        gitdiff = int(self.befor_account) - int(100) + int(self.amount)
        assert err == 0 and int(after_account) == gitdiff, "查询账户余额 失败" + after_account

        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(
            self.amount
        ), ("查询" + self.cname + "余额 失败" + after_cname)
