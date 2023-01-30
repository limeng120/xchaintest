"""
说明: 测试evm合约 部署、调用、查询
"""
import json
import pytest
import time

class TestEVM():

    file = "evmTemplate/Counter.bin"
    cname = "e_counter"
    abi = "evmTemplate/Counter.abi"

    @pytest.mark.p0
    def test_case01(self, input): 
        """
        部署合约
        """        
        print("\n部署合约") 
        contract_account = "XC" + input.account + "@" + input.conf.name 
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)   
        err, result = input.test.xlib.DeployContract("evm", "", self.cname, \
            self.file, contract_account, args, abi = self.abi)         
        assert err == 0 or "already exist" in result, "部署evm合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result
    
    @pytest.mark.p0
    def test_case02(self, input):
        """
        调用合约
        """
        print("\n调用合约")
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "increase", args)
        assert err == 0, "调用evm合约失败： " + result
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

    @pytest.mark.p0
    def test_case03(self, input):
        """
        查询合约
        """
        print("\n查询合约")
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("evm", self.cname, "get", args)
        assert err == 0, "查询evm合约失败： " + result
