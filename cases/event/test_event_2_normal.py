"""
说明: 测试evm合约的事件订阅
"""
import json
import pytest


class TestEvmEvent:
    """
    测试evm合约的事件订阅
    """

    file = "evmTemplate/eventTest.bin"
    cname = "eventTest"
    abi = "evmTemplate/eventTest.abi"
    eventfile = "eventlog"

    @pytest.mark.p0
    def test_case01(self, input_args):
        """
        部署合约
        """
        print("\n部署合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "evm", "", self.cname, self.file, contract_account, args, abi=self.abi
        )
        assert err == 0 or "already exist" in result, "部署evm合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

    @pytest.mark.p0
    def test_case02(self, input_args):
        """
        过滤条件订阅BytesOtherTypeEvent,以及 BytesOtherTypeEventIndexed
        """
        print("\ncase02 过滤条件订阅BytesOtherTypeEvent,以及 BytesOtherTypeEventIndexed")
        event_filter = {"contract": "eventTest", "event_name": "BytesOtherTypeEvent"}
        event_filter = json.dumps(event_filter)
        events = [
            {
                "contract": "eventTest",
                "name": "BytesOtherTypeEvent",
                "body": '["abcd","68656c6c6f","1234000000000000000000000000000000000000"]',
            },
            {
                "contract": "eventTest",
                "name": "BytesOtherTypeEventIndexed",
                "body": '["abcd","68656c6c6f","1234000000000000000000000000000000000000"]',
            },
        ]
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testBytes",
            args="{}",
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        不带过滤条件，也能监听到evm合约事件
        """
        print("\ncase03 不带过滤条件，也能监听到evm合约事件")
        events = [
            {
                "contract": "eventTest",
                "name": "BytesOtherTypeEvent",
                "body": '["abcd","68656c6c6f","1234000000000000000000000000000000000000"]',
            },
            {
                "contract": "eventTest",
                "name": "BytesOtherTypeEventIndexed",
                "body": '["abcd","68656c6c6f","1234000000000000000000000000000000000000"]',
            },
        ]
        err, result = input_args.test.event.evm_event_test(
            "",
            self.eventfile,
            contract=self.cname,
            method="testBytes",
            args="{}",
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        单独测不带Indexed的Uint256OneEvent
        """
        print("\ncase04 单独测不带Indexed的Uint256OneEvent")
        event_filter = {"contract": "eventTest", "event_name": "Uint256OneEvent"}
        event_filter = json.dumps(event_filter)
        events = [
            {"contract": "eventTest", "name": "Uint256OneEvent", "body": "[987656]"}
        ]
        args = {"a": "987656"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="TestUint256WithoutIndexed",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        单独测带Indexed的Uint256OneIndexEvent
        """
        print("\ncase05 单独测带Indexed的Uint256OneIndexEvent")
        event_filter = {"contract": "eventTest", "event_name": "Uint256OneIndexEvent"}
        event_filter = json.dumps(event_filter)
        events = [
            {
                "contract": "eventTest",
                "name": "Uint256OneIndexEvent",
                "body": "[1122333]",
            }
        ]
        args = {"a": "1122333"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="TestUint256Indexed",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        测试Uint相关事件
        """
        print("\ncase06 测试Uint相关事件")
        event_filter = {"contract": "eventTest", "event_name": "Uint256"}
        event_filter = json.dumps(event_filter)
        events = [
            {"contract": "eventTest", "name": "Uint256OneEvent", "body": "[135]"},
            {"contract": "eventTest", "name": "Uint256OneIndexEvent", "body": "[135]"},
            {
                "contract": "eventTest",
                "name": "Uint256TwoIndexEvent",
                "body": "[135,79]",
            },
            {
                "contract": "eventTest",
                "name": "Uint256TwoIndexFirstEvent",
                "body": "[135,79]",
            },
            {
                "contract": "eventTest",
                "name": "Uint256TwoIndexSecEvent",
                "body": "[135,79]",
            },
        ]
        args = {"a": "135", "b": "79"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testUint256Event",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        测试int相关事件
        """
        print("\ncase07 测试int相关事件")
        event_filter = {"contract": "eventTest", "event_name": "Int256"}
        event_filter = json.dumps(event_filter)
        events = [
            {"contract": "eventTest", "name": "Int256OneEvent", "body": "[56]"},
            {"contract": "eventTest", "name": "Int256OneIndexEvent", "body": "[56]"},
            {"contract": "eventTest", "name": "Int256TwoIndexEvent", "body": "[56,78]"},
            {
                "contract": "eventTest",
                "name": "Int256TwoIndexFirstEvent",
                "body": "[56,78]",
            },
            {
                "contract": "eventTest",
                "name": "Int256TwoIndexSecEvent",
                "body": "[56,78]",
            },
        ]
        args = {"a": "56", "b": "78"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testint256Event",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        测试Address相关事件
        """
        print("\ncase08 测试Address相关事件")
        event_filter = {"contract": "eventTest", "event_name": "Address"}
        event_filter = json.dumps(event_filter)
        events = [
            {
                "contract": "eventTest",
                "name": "AddressOneIndexEvent",
                "body": '["72BA7D8E73FE8EB666EA66BABC8116A41BFB10E2"]',
            },
            {
                "contract": "eventTest",
                "name": "AddressTwoIndexEvent",
                "body": '["72BA7D8E73FE8EB666EA66BABC8116A41BFB10E2","3131313231313131313131313131313131313131"]',
            },
            {
                "contract": "eventTest",
                "name": "AddressTwoIndexFirstEvent",
                "body": '["72BA7D8E73FE8EB666EA66BABC8116A41BFB10E2","3131313231313131313131313131313131313131"]',
            },
            {
                "contract": "eventTest",
                "name": "AddressTwoIndexSecEvent",
                "body": '["72BA7D8E73FE8EB666EA66BABC8116A41BFB10E2","3131313231313131313131313131313131313131"]',
            },
        ]
        args = {
            "a": "72bA7d8E73Fe8Eb666Ea66babC8116a41bFb10e2",
            "b": "3131313231313131313131313131313131313131",
        }
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testAddresxsEvent",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        测试Bool相关事件
        """
        print("\ncase09 测试Bool相关事件")
        event_filter = {"contract": "eventTest", "event_name": "Bool"}
        event_filter = json.dumps(event_filter)
        events = [
            {"contract": "eventTest", "name": "BoolOneIndexEvent", "body": "[false]"},
            {
                "contract": "eventTest",
                "name": "BoolTwoIndexEvent",
                "body": "[false,true]",
            },
            {
                "contract": "eventTest",
                "name": "BoolTwoIndexFirstEvent",
                "body": "[false,true]",
            },
            {
                "contract": "eventTest",
                "name": "BoolTwoIndexSecEvent",
                "body": "[false,true]",
            },
        ]
        args = {"a": False, "b": True}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testBoolEvent",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case10(self, input_args):
        """
        测试String相关事件
        """
        print("\ncase10 测试String相关事件")
        event_filter = {"contract": "eventTest", "event_name": "String"}
        event_filter = json.dumps(event_filter)
        events = [
            {
                "contract": "eventTest",
                "name": "StringOneIndexEvent",
                "body": '["97fc46276c172633607a331542609db1e3da793fca183d594ed5a61803a10792"]',
            },
            {
                "contract": "eventTest",
                "name": "StringTwoIndexEvent",
                "body": '["97fc46276c172633607a331542609db1e3da793fca183d594ed5a61803a10792",\
"08c833197070ad01833884fce732298cdca689458e79fefdf4791304cc7b9bce"]',
            },
            {
                "contract": "eventTest",
                "name": "StringTwoIndexFirstEvent",
                "body": '["97fc46276c172633607a331542609db1e3da793fca183d594ed5a61803a10792","xuperChain"]',
            },
            {
                "contract": "eventTest",
                "name": "StringTwoIndexSecEvent",
                "body": '["string","08c833197070ad01833884fce732298cdca689458e79fefdf4791304cc7b9bce"]',
            },
        ]
        args = {"a": "string", "b": "xuperChain"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testStringEvent",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case11(self, input_args):
        """
        测试bytes32相关事件
        """
        print("\ncase11 测试bytes32相关事件")
        event_filter = {"contract": "eventTest", "event_name": "Byte32"}
        event_filter = json.dumps(event_filter)
        events = [
            {
                "contract": "eventTest",
                "name": "Byte32OneIndexEvent",
                "body": '["4279746573333200000000000000000000000000000000000000000000000000"]',
            },
            {
                "contract": "eventTest",
                "name": "Byte32TwoIndexEvent",
                "body": '["4279746573333200000000000000000000000000000000000000000000000000",\
"3230000000000000000000000000000000000000000000000000000000000000"]',
            },
            {
                "contract": "eventTest",
                "name": "Byte32TwoIndexFirstEvent",
                "body": '["4279746573333200000000000000000000000000000000000000000000000000",\
"3230000000000000000000000000000000000000000000000000000000000000"]',
            },
            {
                "contract": "eventTest",
                "name": "Byte32TwoIndexSecEvent",
                "body": '["4279746573333200000000000000000000000000000000000000000000000000",\
"3230000000000000000000000000000000000000000000000000000000000000"]',
            },
        ]
        args = {"a": "Bytes32", "b": "20"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testBytes32Event",
            args=args,
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case12(self, input_args):
        """
        测试byte相关事件
        """
        print("\ncase12 测试byte相关事件")
        event_filter = {"contract": "eventTest", "event_name": "Bytes"}
        event_filter = json.dumps(event_filter)
        events = [
            {
                "contract": "eventTest",
                "name": "BytesOtherTypeEvent",
                "body": '["abcd","68656c6c6f","1234000000000000000000000000000000000000"]',
            },
            {
                "contract": "eventTest",
                "name": "BytesOtherTypeEventIndexed",
                "body": '["abcd","68656c6c6f","1234000000000000000000000000000000000000"]',
            },
        ]
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="testBytes",
            args="{}",
            events=events,
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case13(self, input_args):
        """
        测试相同名字，参数不同的事件
        """
        print("\ncase13 测试相同名字，参数不同的事件")
        event_filter = {"contract": "eventTest", "event_name": "SameNameEvent"}
        event_filter = json.dumps(event_filter)
        events = [
            {"contract": "eventTest", "name": "SameNameEvent", "body": '[12,"Hello"]'},
            {"contract": "eventTest", "name": "SameNameEvent", "body": '["Hello",12]'},
        ]
        args = {"n": "12", "s": "Hello"}
        args = json.dumps(args)
        err, result = input_args.test.event.evm_event_test(
            event_filter,
            self.eventfile,
            contract=self.cname,
            method="TestSameNameEvent",
            args=args,
            events=events,
        )
        assert err == 0, result
