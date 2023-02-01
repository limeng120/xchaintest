"""
说明: 测试evm合约 部署、调用、查询
"""
import json
import pytest


class TestEVM:
    """
    测试evm合约 部署、调用、查询
    """

    file = "evmTemplate/Counter.bin"
    cname = "e_counter"
    abi = "evmTemplate/Counter.abi"

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
        调用合约
        """
        print("\n调用合约")
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "evm", self.cname, "increase", args
        )
        assert err == 0, "调用evm合约失败： " + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

    @pytest.mark.p0
    def test_case03(self, input_args):
        """
        查询合约
        """
        print("\n查询合约")
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "evm", self.cname, "get", args
        )
        assert err == 0, "查询evm合约失败： " + result
