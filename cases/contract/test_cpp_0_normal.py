"""
说明: 测试cpp wasm合约 部署、调用、查询、升级
"""
import json
import pytest
import time

class TestCppWasm():

    file = "cppTemplate/counter.wasm"
    cname = "c_counter"

    # case01 部署cpp wasm合约
    @pytest.mark.p0
    def test_case01(self, input):
        contract_account = "XC" + input.account + "@" + input.conf.name
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)
        err, result = input.test.xlib.DeployContract("wasm", "cpp", self.cname, self.file, contract_account, args)
        assert err == 0 or "already exist" in result, "部署cpp wasm合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

    # case02 升级cpp wasm合约，合约未被调用过
    @pytest.mark.p2
    def test_case02(self, input):
        contract_account = "XC" + input.account + "@" + input.conf.name
        err, result = input.test.xlib.UpgradeContract("wasm", self.cname, self.file, contract_account)       
        assert err == 0, "升级cpp wasm合约失败： " + result
        
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

        err, result_query = input.test.xlib.QueryAccContract(contract_account, self.cname)
        assert err == 0, "查询账户下的合约失败： " + result_query
        assert txid == result_query["txid"], "升级后，检查合约txid，不一致"
        
    # case03 调用cpp wasm合约
    @pytest.mark.p0
    def test_case03(self, input):
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("wasm", self.cname, "increase", args)
        assert err == 0, "调用cpp wasm合约失败： " + result
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

    # case04 查询cpp wasm合约
    @pytest.mark.p0
    def test_case04(self, input):
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("wasm", self.cname, "get", args)
        assert err == 0, "查询cpp wasm合约失败： " + result

    # case05 升级cpp wasm合约，合约被调用过
    @pytest.mark.p2
    def test_case05(self, input):
        contract_account = "XC" + input.account + "@" + input.conf.name
        err, result = input.test.xlib.UpgradeContract("wasm", self.cname, self.file, contract_account)
        assert err == 0, "升级cpp wasm合约失败： " + result
        
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

        err, result_query = input.test.xlib.QueryAccContract(contract_account, self.cname)
        assert err == 0, "查询账户下的合约失败： " + result_query
        assert txid == result_query["txid"], "升级后，检查合约txid，不一致"

    # case06 调用cpp wasm合约
    @pytest.mark.p2
    def test_case06(self, input):
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("wasm", self.cname, "increase", args)
        assert err == 0, "调用cpp wasm合约失败： " + result
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

    # case07 查询cpp wasm合约
    @pytest.mark.p2
    def test_case07(self, input):
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("wasm", self.cname, "get", args)
        assert err == 0, "查询cpp wasm合约失败： " + result

    # case08 部署cpp wasm合约，合约名称长度是4
    @pytest.mark.p2
    def test_case08(self, input):
        contract_account = "XC" + input.account + "@" + input.conf.name
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)
        cname = "test"
        err, result = input.test.xlib.DeployContract("wasm", "cpp", cname, self.file, contract_account, args)
        assert err == 0 or "already exist" in result, "部署cpp wasm合约失败： " + result

    # case09 部署cpp wasm合约，合约名称长度是16
    @pytest.mark.p2
    def test_case09(self, input):
        contract_account = "XC" + input.account + "@" + input.conf.name
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)
        cname = "test012345678901"
        err, result = input.test.xlib.DeployContract("wasm", "cpp", cname, self.file, contract_account, args)
        assert err == 0 or "already exist" in result, "部署cpp wasm合约失败： " + result