"""
说明: 测试cpp wasm合约 部署、调用、查询、升级的异常场景
"""
import json
import pytest


class TestCppWasmErr:
    """
    测试cpp wasm合约 部署、调用、查询、升级的异常场景
    """

    file = "cppTemplate/counter.wasm"
    cname = "c_counter"
    # 1个不存在的合约账户
    ca = "XC9876543210987654@xuper"
    deploy = {"creator": "abc"}

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        重复部署
        """
        print("\n重复部署")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname, self.file, contract_account, args
        )
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname, self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "already exists"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        使用普通账号部署合约
        """
        print("\n使用普通账号部署合约")
        address = input_args.addrs[0]
        args = json.dumps(self.deploy)
        err, address = input_args.test.xlib.get_address("data/keys")
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname, self.file, address, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        使用不存在的合约账号，部署合约
        """
        print("\n使用不存在的合约账号，部署合约")
        args = json.dumps(self.deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname, self.file, self.ca, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        升级合约，用非部署账号
        """
        print("\n升级合约，用非部署账号")
        err, result = input_args.test.xlib.upgrade_contract(
            "wasm", self.cname, self.file, self.ca
        )
        assert err != 0, "升级cpp wasm合约成功，不合预期： " + result
        msg = "verify contract owner permission failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        升级合约，用部署账号对应的普通账号
        """
        print("\n升级合约，用部署账号对应的普通账号")
        err, address = input_args.test.xlib.get_address("data/keys")
        err, result = input_args.test.xlib.upgrade_contract(
            "wasm", self.cname, self.file, address
        )
        assert err != 0, "升级cpp wasm合约成功，不合预期： " + result
        msg = "verify contract owner permission failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        升级不存在的合约
        """
        print("\n升级不存在的合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.upgrade_contract(
            "wasm", self.cname + "err", self.file, contract_account
        )
        assert err != 0, "升级cpp wasm合约成功，不合预期： " + result
        msg = "contract for account not confirmed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        使用native关键字部署cpp合约
        """
        print("\n使用native关键字部署cpp合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "native", "cpp", self.cname + "new", self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "unsupported native contract runtime c"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case08(self, input_args):
        """
        部署cpp合约，使用错误的runtime:go
        """
        print("\n部署cpp合约，使用错误的runtime:go")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "go", self.cname + "new", self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg1 = "no such file or directory"
        msg2 = "run not found"
        assert msg1 in result or msg2 in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case09(self, input_args):
        """
        部署cpp合约，使用错误的runtime:java
        """
        print("\n部署cpp合约，使用错误的runtime:java")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "java", self.cname + "new", self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "bad runtime"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case10(self, input_args):
        """
        部署cpp合约，使用错误的文件：java编译的二进制
        """
        print("\n部署cpp合约，使用错误的文件：java编译的二进制")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        java_file = "javaTemplate/counter-0.1.0-jar-with-dependencies.jar"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname + "new", java_file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "run wasm2c error"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case12(self, input_args):
        """
        部署cpp合约，使用错误的文件：go native编译的二进制
        """
        print("\n部署cpp合约，使用错误的文件：go native编译的二进制")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        go_file = "goTemplate/counter"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname + "new", go_file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功，不合预期： " + result
        msg = "run wasm2c error"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case13(self, input_args):
        """
        调用不存在的合约
        """
        print("\n调用不存在的合约")
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname + "err", "increase", args
        )
        assert err != 0, "调用cpp wasm合约成功，不合预期： " + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case14(self, input_args):
        """
        调用合约,value不是string类型
        """
        print("\n调用合约,value不是string类型")
        invoke_args = {"key": 10}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "increase", args
        )
        assert err != 0, "调用cpp wasm合约成功，不合预期： " + result
        msg = "bad key key"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case15(self, input_args):
        """
        部署合约，合约名不足4位，有效位是4~16
        """
        print("\n部署合约，合约名不足4位，有效位是4~16")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        cname = "aaa"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", cname, self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功， 不合预期： " + result
        msg = "contract name length expect [4~16], actual: 3"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case16(self, input_args):
        """
        部署合约，合约名超过16位，有效位是4~16
        """
        print("\n部署合约，合约名超过16位，有效位是4~16")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        cname = "a1234567890123456"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", cname, self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功， 不合预期： " + result
        msg = "contract name length expect [4~16], actual: 17"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case17(self, input_args):
        """
        部署合约，合约名含特殊字符
        """
        print("\n部署合约，合约名含特殊字符")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        cname = "counter#"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", cname, self.file, contract_account, args
        )
        assert err != 0, "部署cpp wasm合约成功， 不合预期： " + result
        msg = "contract name does not fit the rule of contract name"
        assert msg in result, "报错信息错误"
