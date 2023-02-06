"""
说明: 测试evm合约sdk
"""
import json
import pytest


class TestStoraget:
    """
    测试evm合约sdk
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

    # 合约余额
    amount = "100"
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
        合约部署storagetest合约
        """
        print("\n部署storagetest合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.deploy_contract(
            "evm", "", self.cname, self.file, contract_account, "None", abi=self.abi
        )
        assert err == 0 or "already exist" in result, "部署storagetest合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        uint数据类型的增删改查,传入合法uint
        """
        print("\nuint数据类型的增删改查,传入合法uint")
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setUint", json.dumps({"x": "10"})
        )
        assert err == 0, "uint数据类型的增删改查,传入合法uint 失败： " + result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getUint", "None"
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        assert result == '[{"0":"10"},{"1":"11"},{"2":"12"}]', (
            "查询Uint设置后的数据 有误" + result
        )

        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setUint", json.dumps({"x": "01234567"})
        )
        assert err == 0, "uint数据类型的增删改查,传入合法uint 失败： " + result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getUint", json.dumps({"x": "01234567"})
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        assert result == '[{"0":"342391"},{"1":"342392"},{"2":"342393"}]', (
            "查询Uint设置后的数据 有误" + result
        )

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        uint数据类型的增删改查，传入uint边界值
        """
        print("\nuint数据类型的增删改查,传入uint边界值")
        args = json.dumps({"x": "0"})
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setUint", args
        )
        assert err == 0, "传入uint边界值 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getUint", "None"
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        expect_result = '[{"0":"0"},{"1":"1"},{"2":"2"}]'
        assert result == expect_result, "查询Uint设置后的数据 有误" + result

        args = json.dumps(
            {
                "x": "111111111111111111111111111111111\
11111111111111111111111111111111111111111111"
            }
        )
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setUint", args
        )
        assert err == 0, "传入uint边界值 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getUint", "None"
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        expect_result = '[{"0":"11111111111111111111111111111111111111111111111111111111111111111111111111111"},\
               {"1":"11111111111111111111111111111111111111111111111111111111111111111111111111112"},\
               {"2":"11111111111111111111111111111111111111111111111111111111111111111111111111113"}]'
        assert result == expect_result.replace(" ", ""), "查询Uint设置后的数据 有误" + result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        bool数据类型的增删改查，传入合法bool值
        """
        print("\nbool数据类型的增删改查，传入合法bool值")
        invoke_args = [{"x": "true"}, {"x": "1"}, {"x": "false"}, {"x": "0"}]
        for getarg in invoke_args:
            args = json.dumps(getarg)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setBool", args
            )
            assert err == 0, "传入合法bool值 失败" + result
            err, result = input_args.test.xlib.query_contract(
                "evm", self.cname, "getBool", "None"
            )
            assert err == 0, result
            result = input_args.test.xlib.get_value_from_res(result)
            if getarg in ({"x": "false"}, {"x": "0"}):
                assert result == '[{"retBool":"false"}]', "查询bool数据 有误" + result
            else:
                assert result == '[{"retBool":"true"}]', "查询bool数据 有误" + result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        string数据类型的增删改查，传入合法string
        """
        print("\nstring数据类型的增删改查，传入合法string")
        invoke_args = ["hello", " hello world_! ", ""]
        for getarg in invoke_args:
            args = json.dumps({"x": getarg})
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setString", args
            )
            assert err == 0, "传入合法string值 失败" + result
            err, get_result = input_args.test.xlib.query_contract(
                "evm", self.cname, "getString", "None"
            )
            assert err == 0, get_result
            result = input_args.test.xlib.get_value_from_res(get_result)
            ret_str = '[{"retString":"' + getarg + '"}]'
            assert result == ret_str, "查询string数据 有误" + get_result

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        address数据类型的增删改查，传入合法address
        """
        print("\naddress数据类型的增删改查，传入合法address")
        invoke_args = "3131313231313131313131313131313131313133"
        args = json.dumps({"x": invoke_args})
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setAddress", args
        )
        assert err == 0, "设置address数据 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getAddress", "None"
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        assert result == '[{"retAddress":"' + invoke_args + '"}]', (
            "查询address数据 有误" + result
        )

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        uint array数据类型的增删改查，传入uint
        """
        print("\n uint array数据类型的增删改查,传入uint")
        invoke_args = [
            "[1,2,3,4]",
            "[0]",
            "[11111111111111111111111111111111111111111111111111111111111111111111111111111]",
        ]
        for getarg in invoke_args:
            args = json.dumps({"uintArrays": getarg})
            # 获取旧数组
            err, result = input_args.test.xlib.query_contract(
                "evm", self.cname, "getUints", "None"
            )
            result = input_args.test.xlib.get_value_from_res(result)
            old_result = json.loads(json.loads(result)[0]["0"])

            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setUints", args
            )
            assert err == 0, "传入uint array 失败" + result
            err, result = input_args.test.xlib.query_contract(
                "evm", self.cname, "getUints", "None"
            )
            assert err == 0, result
            result = input_args.test.xlib.get_value_from_res(result)

            # 数组追加
            old_result.extend(json.loads(getarg))
            assert result == '[{"0":"' + str(old_result).replace(" ", "") + '"}]', (
                "查询uint array数据 有误" + result
            )

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        原生代币转账，调evm合约同时给合约账号转账
        """
        print("\n 原生代币转账,调evm合约同时给合约账号转账")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        self.trans_use(contract_account, input_args)
        args = json.dumps({"x": "10"})
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setUint",
            args,
            account=contract_account,
            amount=self.amount,
        )
        assert err == 0, "调evm合约同时给合约账号转账 失败： " + result

        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(
            self.amount
        ), ("查询" + self.cname + "余额 失败" + after_cname)

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        部署erc20合约
        """
        print("\n部署erc20合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.deploy_contract(
            "evm",
            "",
            self.tokeName,
            self.tokenFile,
            contract_account,
            "None",
            abi=self.tokenAbi,
        )
        assert err == 0 or "already exist" in result, "部署erc20合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

    @pytest.mark.p2
    def test_case10(self, input_args):
        """
        部署调用合约
        """
        print("\n部署调用合约")
        args = json.dumps({"token": self.tokenAddr})
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.deploy_contract(
            "evm",
            "",
            self.testNest,
            self.TESTNesTokenbin,
            contract_account,
            args,
            abi=self.TESTNesTokenAbi,
        )
        assert err == 0 or "already exist" in result, "部署调用合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

    @pytest.mark.p2
    def test_case11(self, input_args):
        """
        跨合约调用，跨合约查询原始合约的合约名
        """
        print("\n跨合约调用,跨合约查询原始合约的合约名")
        err, result = input_args.test.xlib.query_contract(
            "evm", self.testNest, "getTokenAddress", "None"
        )
        assert err == 0, "跨合约查询原始合约失败：" + result
        result = input_args.test.xlib.get_value_from_res(result)
        assert json.loads(result)[0]["0"] == self.tokenAddr, "跨合约查询合约名有误" + result

    @pytest.mark.p2
    def test_case12(self, input_args):
        """
        跨合约调用，跨合约调用原始合约的方法做erc20代币转账
        """
        print("\n 跨合约调用,跨合约调用原始合约的方法做erc20代币转账")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        invoke_args = [
            "B4E26DF80E3F548455634ABE87937FC0E1368225",
            "313131312D2D2D2D2D746573746E657374313030",
            "D4CA13E87044275C8BA7A7217286868E2C2F357A",
        ]
        for getarg in invoke_args:
            get_args = json.dumps({"_owner": getarg})
            err, old_result = input_args.test.xlib.query_contract(
                "evm", self.tokeName, "balanceOf", get_args
            )
            assert err == 0, "查询 代币余额失败： " + old_result
            old_result = input_args.test.xlib.get_value_from_res(old_result)
            old_result = json.loads(old_result)[0]["0"]
            # 转账
            to_args = {"_to": getarg, "_value": "10"}
            args = json.dumps(to_args)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.tokeName, "transfer", args, account=contract_account
            )
            assert err == 0, "直接调用原始合约的方法做erc20代币转账 转账失败： " + result

            err, new_result = input_args.test.xlib.query_contract(
                "evm", self.tokeName, "balanceOf", get_args
            )
            assert err == 0, "直接调用原始合约的方法做erc20代币转账 转账失败： " + new_result
            new_result = input_args.test.xlib.get_value_from_res(new_result)
            assert int(json.loads(new_result)[0]["0"]) == int(old_result) + int(10), (
                "转账后查询代币 余额有误" + new_result
            )

    @pytest.mark.p2
    def test_case13(self, input_args):
        """
        原生代币转账,evm合约向外转账
        """
        print("\n原生代币转账,evm合约向外转账")
        invoke_args = [
            "3131313231313131313131313131313131313132",
            "D4CA13E87044275C8BA7A7217286868E2C2F357A",
            "313131312D2D2D2D2D2D2D2D2D636F756E746572",
        ]
        i = 0
        for arg in invoke_args:
            err, result = input_args.test.xlib.addr_trans("e2x", arg)
            assert err == 0, "evm地址转合约名失败： " + result

            if i == 0:
                address = "XC" + result.split()[1] + "@" + input_args.conf.name
            else:
                address = result.split()[1]
            # 查询合约余额
            self.trans_use(address, input_args)
            # 转账
            to_args = {"receiver": arg, "amount": "1"}
            args = json.dumps(to_args)
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "send", args, fee=10
            )
            assert err == 0, "evm合约向外转账 失败： " + result
            # 查询转账后的余额
            err, new_result = input_args.test.xlib.get_balance(account=self.cname)
            assert err == 0, "转账后查询合约余额 失败： " + new_result
            assert int(new_result) == int(self.befor_cname) - int(1), (
                "转账后查询合约 余额有误" + new_result
            )

            err, new_acl_result = input_args.test.xlib.get_balance(account=address)
            assert err == 0, "转账后查询evm账户余额 失败： " + new_result
            assert int(new_acl_result) == int(self.befor_account) + int(1), (
                "转账后查询evm账户 余额有误" + new_acl_result
            )
            if err == 0:
                # 等待tx上链
                txid = input_args.test.xlib.get_txid_from_res(result)
                err, result = input_args.test.xlib.wait_tx_on_chain(txid)
                assert err == 0, result
            i = i + 1

    @pytest.mark.p2
    def test_case14(self, input_args):
        """
        int数据类型的增删改查,传入合法int
        """
        print("\nint数据类型的增删改查,传入合法int")
        value = [10, -10, 0]
        for value_int in value:
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setInt", json.dumps({"x": str(value_int)})
            )
            assert err == 0, result
            err, result = input_args.test.xlib.query_contract(
                "evm", self.cname, "getInt", "None"
            )
            result = input_args.test.xlib.get_value_from_res(result)
            assert err == 0 and '[{"retInt":"' + str(value_int) + '"}]' in result

    @pytest.mark.p2
    def test_case15(self, input_args):
        """
        int数据类型的增删改查,传入int边界值
        """
        print("\nint数据类型的增删改查,传入int边界值")
        value = [
            -57896044618658097711785492504343953926634992332820282019728792003956564819967,
            57896044618658097711785492504343953926634992332820282019728792003956564819967,
        ]
        for value_int in value:
            err, result = input_args.test.xlib.invoke_contract(
                "evm", self.cname, "setInt", json.dumps({"x": str(value_int)})
            )
            assert err == 0, result
            err, result = input_args.test.xlib.query_contract(
                "evm", self.cname, "getInt", "None"
            )
            result = input_args.test.xlib.get_value_from_res(result)
            assert err == 0 and '[{"retInt":"' + str(value_int) + '"}]' in result

    @pytest.mark.p2
    def test_case16(self, input_args):
        """
        int数组数据类型的增删改查,传入合法int数组
        """
        print("\nint数组数据类型的增删改查,传入合法int数组")
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setIntArr", json.dumps({"x": "[10,-10,0]"})
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getIntArr", "None"
        )
        assert err == 0 and "10,-10,0" in result

    @pytest.mark.p2
    def test_case17(self, input_args):
        """
        int数组数据类型的增删改查,传入int边界值
        """
        print("\nint数组数据类型的增删改查,传入int边界值")
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setIntArr",
            json.dumps(
                {
                    "x": "[-57896044618658097711785492504343953926634992332820282019728792003956564819967,\
57896044618658097711785492504343953926634992332820282019728792003956564819967]"
                }
            ),
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getIntArr", "None"
        )
        assert (
            err == 0
            and "-57896044618658097711785492504343953926634992332820282019728792003956564819967,\
57896044618658097711785492504343953926634992332820282019728792003956564819967"
            in result
        )

    @pytest.mark.p2
    def test_case18(self, input_args):
        """
        address数据类型的增删改查，传入合法address
        """
        print("\naddress数组数据类型的增删改查，传入合法address数组")
        invoke_args = "[3131313231313131313131313131313131313133,3131313231313131313131313131313131313133]"
        args = json.dumps({"x": invoke_args})
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setAddrArr", args
        )
        assert err == 0, "设置address数据 失败" + result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getAddrArr", "None"
        )
        assert (
            err == 0
            and "3131313231313131313131313131313131313133,3131313231313131313131313131313131313133"
            in result
        )

    @pytest.mark.p2
    def test_case19(self, input_args):
        """
        bytes数据类型的增删改查,传入合法byte，值是1个byte32
        """
        print("\nbytes数据类型的增删改查,传入合法byte，值是1个byte32")
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setBytesAuto",
            json.dumps(
                {
                    "x": "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"
                }
            ),
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getBytesAuto", "None"
        )
        assert err == 0

    @pytest.mark.p2
    def test_case20(self, input_args):
        """
        bytes数据类型的增删改查,传入合法byte，值是2个byte32
        """
        print("\nbytes数据类型的增删改查,传入合法byte，值是2个byte32")
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setBytesAuto",
            json.dumps(
                {
                    "x": "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd\
e4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"
                }
            ),
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getBytesAuto", "None"
        )
        assert err == 0

    @pytest.mark.p2
    def test_case21(self, input_args):
        """
        bytes数据类型的增删改查,传入合法byte，值是0x1111
        """
        print("\nbytes数据类型的增删改查,传入合法byte，值是0x1111")
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setBytesAuto", json.dumps({"x": "0x1111"})
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getBytesAuto", "None"
        )
        assert err == 0

    @pytest.mark.p2
    def test_case22(self, input_args):
        """
        bytes32数据类型的增删改查,传入合法bytes32
        """
        print("\nbytes32数据类型的增删改查,传入合法bytes32")
        err, result = input_args.test.xlib.invoke_contract(
            "evm",
            self.cname,
            "setBytes",
            json.dumps(
                {
                    "x": "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"
                }
            ),
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getBytes", "None"
        )
        assert err == 0

    @pytest.mark.p2
    def test_case23(self, input_args):
        """
        bytes32数据类型的增删改查,传入合法bytes32
        """
        print("\nbytes32数据类型的增删改查,传入合法bytes32")
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "setBytes", json.dumps({"x": "0x1111"})
        )
        assert err == 0, result
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "getBytes", "None"
        )
        assert err == 0
