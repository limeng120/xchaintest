"""
说明: 测试cpp wasm合约 部署、调用、查询、升级
"""
import json
import time
import pytest


class TestCppWasm:
    """
    测试cpp wasm合约 部署、调用、查询、升级
    """

    file = "cppTemplate/counter.wasm"
    cname = "c_counter"

    @pytest.mark.p0
    def test_case01(self, input_args):
        """
        部署cpp wasm合约
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", self.cname, self.file, contract_account, args
        )
        assert err == 0 or "already exist" in result, "部署cpp wasm合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        升级cpp wasm合约，合约未被调用过
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.upgrade_contract(
            "wasm", self.cname, self.file, contract_account
        )
        assert err == 0, "升级cpp wasm合约失败： " + result

        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result
        time.sleep(2)
        err, result_query = input_args.test.xlib.query_acc_contract(
            contract_account, self.cname
        )
        assert err == 0, "查询账户下的合约失败： " + result_query
        assert txid == result_query["txid"], "升级后，检查合约txid，不一致"

    @pytest.mark.p0
    def test_case03(self, input_args):
        """
        调用cpp wasm合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "increase", args
        )
        assert err == 0, "调用cpp wasm合约失败： " + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

    @pytest.mark.p0
    def test_case04(self, input_args):
        """
        查询cpp wasm合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err == 0, "查询cpp wasm合约失败： " + result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        升级cpp wasm合约，合约被调用过
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.upgrade_contract(
            "wasm", self.cname, self.file, contract_account
        )
        assert err == 0, "升级cpp wasm合约失败： " + result

        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result
        time.sleep(2)
        err, result_query = input_args.test.xlib.query_acc_contract(
            contract_account, self.cname
        )
        assert err == 0, "查询账户下的合约失败： " + result_query
        assert txid == result_query["txid"], "升级后，检查合约txid，不一致"

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        调用cpp wasm合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "wasm", self.cname, "increase", args
        )
        assert err == 0, "调用cpp wasm合约失败： " + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        查询cpp wasm合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "wasm", self.cname, "get", args
        )
        assert err == 0, "查询cpp wasm合约失败： " + result

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        部署cpp wasm合约，合约名称长度是4
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        cname = "test"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", cname, self.file, contract_account, args
        )
        assert err == 0 or "already exist" in result, "部署cpp wasm合约失败： " + result

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        部署cpp wasm合约，合约名称长度是16
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        cname = "test012345678901"
        err, result = input_args.test.xlib.deploy_contract(
            "wasm", "cpp", cname, self.file, contract_account, args
        )
        assert err == 0 or "already exist" in result, "部署cpp wasm合约失败： " + result
