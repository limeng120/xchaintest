"""
说明: 测试evm合约sdk的异常场景
"""
import json
import pytest


class TestStoragetErr:
    """
    测试evm合约sdk的异常场景
    """

    abi = "evmTemplate/StorageBasicData.abi"
    file = "evmTemplate/StorageBasicData.bin"
    cname = "storagetest"

    tokenAbi = "evmTemplate/TESTToken.abi"
    tokenFile = "evmTemplate/TESTToken.bin"
    tokeName = "testtoken100"
    tokenAddr = "313131312D2D2D2D74657374746F6B656E313030"

    TESTNesTokenbin = "evmTemplate/TESTNestToken.bin"
    TESTNesTokenAbi = "evmTemplate/TESTNestToken.abi"
    testNest = "testnest100"

    def transfer_when_not_enough(self, to_args, file, input_args):
        """
        代币不足场景，给他人转账，预期失败
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(to_args)
        err, result = input_args.test.xlib.invoke_contract(
            "evm", file, "transfer", args, account=contract_account
        )

        key_err, key_result = input_args.test.xlib.invoke_contract(
            "evm", file, "transfer", args
        )
        assert err != 0 or key_err != 0, "代币余额不足,转账成功,不符合预期：" + result + key_result
        msg = "contract invoke failed"
        assert msg in result or msg in key_result, "报错信息错误"

    @pytest.mark.abnormal
    def transfer_use(self, file, input_args):
        """
        转账金额非法，为-1、a、0，预期代币转账失败
        """
        invoke_args = ["-1", "a", "0"]
        if file == self.tokeName:
            contract_account = "XC" + input_args.account + "@" + input_args.conf.name
            # 转账数额为0
            to_args = {"_to": self.tokenAddr, "_value": "0"}
            args = json.dumps(to_args)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", file, "transfer", args, account=contract_account
            )
            assert err == 0, "代币数为0 转账失败,不符合预期：" + result
            # [异常]转账数额为-1
            invoke_args = ["-1", "a"]
        for arg in invoke_args:
            get_args = json.dumps({"_to": self.tokenAddr, "_value": arg})
            err, result = input_args.test.xlib.invoke_contract(
                "evm", file, "transfer", get_args
            )
            assert err != 0, "转账数额为" + arg + " 转账成功,不符合预期：" + result
            msg = "contract invoke failed"
            assert msg in result, "报错信息错误"

    def querybalance(self, file, input_args):
        """
        查询代币余额
        """
        err, result = input_args.test.xlib.query_contract(
            "evm",
            file,
            "balanceOf",
            '{"_owner":"313131312D2D2D2D2D2D2D2D2D2D616263646566"}',
        )
        assert err == 0, "查询不存在的账户 失败, 不符合预期： " + result

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        【异常】uint数据类型的增删改查，传入非uint值
        """
        print("\nuint数据类型的增删改查,传入非uint值")
        invoke_args = [{"x": "-10"}, {"x": "aaaa"}, {"x": "!@#$%^&*_+"}]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setUint", args
            )
            assert err != 0, "传入uint边界值成功，不符合预期" + result
            msg = "invoke failed"
            assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setUint", '{"x":}'
        )
        assert err != 0, "传入uint边界值成功，不符合预期" + result
        msg = "invalid character '}' looking for beginning of value"
        assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setUint",
            json.dumps(
                {
                    "x": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
                }
            ),
        )
        assert err == 0, "数据溢出出错 不符合预期" + result
        err, get_res = input_args.test.xlib.query_contract(
            "evm", self.cname, "getUint", "None"
        )
        msg = '[{"0":"25870071517096625434027777777777777777777777777777777777777777777777777777777"},\
                      {"1":"25870071517096625434027777777777777777777777777777777777777777777777777777778"},\
                        {"2":"25870071517096625434027777777777777777777777777777777777777777777777777777779"}]'
        assert msg.replace(" ", "") in get_res, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        【异常】bool数据类型的增删改查，传入非bool值
        """
        print("\nuint数据类型的增删改查,传入uint边界值")
        invoke_args = [{"x": "-1"}, {"x": "qqqq"}, {"x": "+!@"}]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setBool", args
            )
            assert err != 0, "传入非bool值成功,不符合预期" + result
            msg = "invoke failed"
            assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setBool", '{"x":}'
        )
        assert err != 0, "传入非bool值成功,不符合预期" + result
        msg = "invalid character '}' looking for beginning of value"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        【异常】address数据类型的增删改查，传入非法address
        1.设置address数据，比合法地址少1位
        2.设置address数据为xchain普通账号、合约账号、合约名
        """
        print("\n address数据类型的增删改查,传入非法address")
        invoke_args = [
            {"x": "313131323131313131313131313131313131313"},
            {"x": "TeyyPLpp9L7QAcxHangtcHTu7HUZ6iydY"},
            {"x": "XC2111111111111111@xuper"},
            {"x": self.cname},
        ]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setAddress", args
            )
            assert err != 0, "传入address值成功,不符合预期" + result
            msg = "invoke failed"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        【异常】uint array数据类型的增删改查，传入非数组格式
        """
        print("\n address数据类型的增删改查,传入非法address")
        invoke_args = ["[1,]", "1", "[-10]", "[aaa]", "[!@#$%^&]"]
        for arg in invoke_args:
            args = json.dumps({"uintArrays": arg})
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setUints", args
            )
            assert err != 0, "传入非uint arrayl值成功,不符合预期" + result
            msg = "invoke failed"
            assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setUints", '{"uintArrays":}'
        )
        assert err != 0, "传入非uint arrayl值成功,不符合预期" + result
        msg = "invalid character '}' looking for beginning of value"
        assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setUints",
            json.dumps(
                {
                    "uintArrays": "[111111111111111111111111111111\
111111111111111111111111111111111111111111111111111111111]"
                }
            ),
        )
        assert err == 0, "数据溢出出错 不符合预期" + result
        err, get_res = input_args.test.xlib.query_contract(
            "evm", self.cname, "getUints", "None"
        )
        msg = "25870071517096625434027777777777777777777777777777777777777777777777777777777"
        assert msg.replace(" ", "") in get_res, "报错信息错误"

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        【异常】原生代币转账，调evm合约同时给合约转账
        """
        print("\n【异常】原生代币转账，调evm合约同时给合约转账")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setUint",
            json.dumps({"x": "-10"}),
            account=contract_account,
            amount=100,
        )
        assert err != 0, "调evm合约同时给合约,转账为负数 成功,不符合预期" + result
        msg = "negative value not allowed for uint256"
        assert msg in result, "报错信息错误"

        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setUint",
            json.dumps({"x": "10"}),
            account=contract_account,
            amount=1000000000000000000000000,
        )
        assert err != 0, "给合约自身转账,当前账户余额不足成功,不符合预期" + result
        msg = "enough money(UTXO) to start this transaction"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case08(self, input_args):
        """
        【异常】原生代币转账，evm合约向外转账
        """
        print("\n【异常】原生代币转账，evm合约向外转账")
        err, result = input_args.test.xlib.addr_trans("x2e", self.cname)
        assert err == 0, "合约名转evm地址失败： " + result
        address = result.split()[1]
        invoke_args = [
            {"receiver": "XC2111111111111111@xuper", "amount": "1"},
            {"receiver": "gq2sEvq1ijTtpnGfcSrGXCztKtq31rgDZ", "amount": "1"},
            {"receiver": "aaaa", "amount": "1"},
            {"receiver": address, "amount": "1"},
        ]
        for arg in invoke_args:
            args = json.dumps(arg)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "send", args
            )
            assert err != 0, "evm合约向外转账成功,不符合预期" + result
            msg = "contract invoke failed"
            assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case09(self, input_args):
        """
        直接调用原生合约方法做erc20代币转账，转出账户余额不足
        """
        print("\n直接调用原生合约方法做erc20代币转账，转出账户余额不足")
        to_args = {
            "_to": "313131312D2D2D2D2D746573746E657374313030",
            "_value": "19999999999999999999999999999",
        }
        self.transfer_when_not_enough(to_args, self.tokeName, input_args)

    @pytest.mark.abnormal
    def test_case10(self, input_args):
        """
        直接调用原生合约方法做erc20代币转账，转账数额非正整数
        """
        print("\n 直接调用原生合约方法做erc20代币转账，转账数额非正整数")
        self.transfer_use(self.tokeName, input_args)

    @pytest.mark.abnormal
    def test_case11(self, input_args):
        """
        直接调用原生合约方法做erc20代币余额查询,查询不存在的账户
        """
        print("\n直接调用原生合约方法做erc20代币余额查询,查询不存在的账户")
        self.querybalance(self.tokeName, input_args)

    @pytest.mark.abnormal
    def test_case12(self, input_args):
        """
        跨合约调用原生合约方法做erc20代币转账，转出账户余额不足
        """
        print("\n跨合约调用原生合约方法做erc20代币转账，转出账户余额不足")
        to_args = {
            "_to": "D4CA13E87044275C8BA7A7217286868E2C2F357A",
            "_value": "5000000000000000000",
        }
        self.transfer_when_not_enough(to_args, self.testNest, input_args)

    @pytest.mark.abnormal
    def test_case13(self, input_args):
        """
        跨合约调用原生合约方法做erc20代币转账，转账数额非正整数
        """
        print("\n跨合约调用原生合约方法做erc20代币转账，转账数额非正整数")
        self.transfer_use(self.testNest, input_args)

    @pytest.mark.abnormal
    def test_case14(self, input_args):
        """
        跨合约调用原生合约方法做erc20代币余额查询，查询不存在的账户
        """
        print("\n跨合约调用原生合约方法做erc20代币余额查询，查询不存在的账户")
        self.querybalance(self.testNest, input_args)

    @pytest.mark.abnormal
    def test_case15(self, input_args):
        """
        int数据类型的增删改查,传入非法int
        """
        print("\nint数据类型的增删改查,传入非法int")
        value = [
            "-57896044618658097711785492504343953926634992332820282019728792003956564819968",
            "57896044618658097711785492504343953926634992332820282019728792003956564819968",
        ]
        for v in value:
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setInt", json.dumps({"x": str(v)})
            )
            assert err != 0 and "value to large for int256" in result
        value = ["aaa", "!"]
        for v in value:
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setInt", json.dumps({"x": str(v)})
            )
            assert err != 0 and "failed to parse" in result

    @pytest.mark.abnormal
    def test_case16(self, input_args):
        """
        int数组数据类型的增删改查,传入非法int值
        """
        print("\nint数组数据类型的增删改查,传入非法int值")
        value = [
            "-57896044618658097711785492504343953926634992332820282019728792003956564819968",
            "57896044618658097711785492504343953926634992332820282019728792003956564819968",
        ]
        for v in value:
            args = json.dumps({"x": "[" + v + "]"})
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setIntArr", args
            )
            assert err != 0 and "value to large for int256" in result
        value = ["aaa", "!"]
        for v in value:
            args = json.dumps({"x": "[" + v + "]"})
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setIntArr", args
            )
            assert err != 0 and "failed to parse" in result

    @pytest.mark.abnormal
    def test_case17(self, input_args):
        """
        int数组数据类型的增删改查,传入非数组类型
        """
        print("\nint数组数据类型的增删改查,传入非数组类型")
        args = json.dumps({"x": "10"})
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setIntArr", args
        )
        assert err != 0 and "argument 0 should be array or slice" in result

    @pytest.mark.abnormal
    def test_case18(self, input_args):
        """
        address数据类型的增删改查，传入非数组
        """
        print("\naddress数组数据类型的增删改查，传入非数组")
        invoke_args = "3131313231313131313131313131313131313133"
        args = json.dumps({"x": invoke_args})
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setAddrArr", args
        )
        assert err != 0 and "argument 0 should be array or slice" in result

    @pytest.mark.abnormal
    def test_case19(self, input_args):
        """
        address数组数据类型的增删改查，传入非法address
        """
        print("\naddress数组数据类型的增删改查，传入非法address")
        invoke_args = ["[1,]", "1", "[-10]", "[aaa]", "[!@#$%^&]"]
        for arg in invoke_args:
            err, _ = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setAddrArr", arg
            )
            assert err != 0

    @pytest.mark.abnormal
    def test_case20(self, input_args):
        """
        bytes32数据类型的增删改查,传入非法bytes32
        """
        print("\nbytes32数据类型的增删改查,传入非法bytes32")
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setBytesAuto", json.dumps({"x": "0x111"})
        )
        assert err != 0 and "cannot map from" in result

    @pytest.mark.abnormal
    def test_case21(self, input_args):
        """
        bytes32数据类型的增删改查,传入非法bytes32,值是2个byte32
        """
        print("\nbytes32数据类型的增删改查,传入非法bytes32,值是2个byte32")
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setBytes",
            json.dumps(
                {
                    "x": "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd\
e4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"
                }
            ),
        )
        assert err != 0 and "byte to long for bytes32" in result
