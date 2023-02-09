"""
说明: 测试cpp合约sdk
"""
import json
import pytest


class TestFeatures1:
    """
    测试cpp合约sdk
    """

    file = "cppTemplate/features.wasm"
    cname = "features"

    widthCount = "".zfill(1024)

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        合约部署features合约
        """
        print("部署features合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname, self.file, contract_account, args
        )
        assert err == 0 or "exist" in result, "部署features合约失败： " + result

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        调put方法,写入1个kv
        """
        print("\n调put方法,写入1个kv")
        invoke_args = {"key": "test1", "value": "value1"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "调put方法,写入1个kv 失败" + result

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        调get方法,查询1个kv
        """
        print("\n调get方法,查询1个kv")
        invoke_args = {"key": "test1"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err == 0, "调get方法,查询1个kv 失败" + result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        调put方法，写入key长度1k,value长度1K
        """
        print("\n调put方法,key长度1k,value长度1k")
        invoke_args = {
            "key": "test" + self.widthCount,
            "value": "value" + self.widthCount,
        }
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "调put方法：key和value长度1K, 失败" + result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        调get方法,key长度1k,value长度1K
        """
        print("\n调get方法,key长度1k,value长度1K")
        invoke_args = {"key": "test" + self.widthCount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err == 0, "调get方法,key和value长度1k 失败" + result
        # value值长度是1024
        assert "value" + self.widthCount in result

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        调put方法，写入key长度1k
        """
        print("\n调put方法,key长度1k")
        invoke_args = {"key": "admin" + self.widthCount, "value": "adminvalue"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "调put方法：key长度1K, 失败" + result

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        调get方法，key长度1k
        """
        print("\n调get方法,key长度1k")
        invoke_args = {"key": "admin" + self.widthCount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err == 0, "调get方法,key长度1k 失败" + result

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        调put方法，写入value长度1k
        """
        print("\n调put方法,value长度1k")
        invoke_args = {"key": "case1", "value": "lkvalue" + self.widthCount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "调put方法,vaue长度1k 失败" + result

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        调get方法,查询value长度1k
        """
        print("\n调get方法,value长度1k")
        invoke_args = {"key": "case1"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err == 0, "调get方法,vaue长度1k 失败" + result

    @pytest.mark.p2
    def test_case10(self, input_args):
        """
        put已经加入的值
        """
        print("\nput已经加入的值")
        invoke_args = {"key": "case1", "value": "qatestval1"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "put已经加入的值 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", json.dumps({"key": "case1"})
        )
        assert err == 0 and "qatestval1" in result, "调get方法,查询已经加入的值 失败" + result

    @pytest.mark.p2
    def test_case11(self, input_args):
        """
        调put方法,value值为" "
        """
        print("\nput的value值为")
        invoke_args = {"key": "dudu", "value": " "}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "put的value值为 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", json.dumps({"key": "dudu"})
        )
        assert err == 0, "调get方法,查询已经加入的值 失败" + result

    @pytest.mark.p2
    def test_case12(self, input_args):
        """
        调put方法,key为空字符串" "
        """
        print("\n调put方法,key为空字符串" "")
        invoke_args = {"key": " ", "value": "value2"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "调put方法,key为空字符串" " 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", json.dumps({"key": " "})
        )
        assert err == 0, "调get方法,key为空字符串" " 失败" + result

    @pytest.mark.p2
    def test_case13(self, input_args):
        """
        调get方法,key,value都为空
        """
        print("\n调用get方法,key,value都为空")
        invoke_args = {"key": " ", "value": " "}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "get方法,key,value都为空 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", json.dumps({"key": " "})
        )
        assert err == 0, "调get方法,key为空失败" + result

    @pytest.mark.p2
    def test_case14(self, input_args):
        """
        key,value为特殊字符
        """
        print("\nput的key,value为特殊字符")
        invoke_args = {"key": "!)(%^&*()O:@_-></!#$^", "value": "!@#$%^&*()_+=?><|"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "put", args
        )
        assert err == 0, "put的key,value为特殊字符 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", json.dumps({"key": "!)(%^&*()O:@_-></!#$^"})
        )
        assert err == 0, "调get方法,查询特殊字符 失败" + result
