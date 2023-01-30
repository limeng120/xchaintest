"""
说明: 测试go合约sdk    
"""
import json
import pytest
import time
import os

txid = None
blockid = None

class TestGoFeatures():

    file = "goTemplate/features"
    cname = "features_go"
    amount="100"

    # 合约部署features合约
    @pytest.mark.p2
    def test_case01(self, input):
        print("部署features合约") 
        contract_account = "XC" + input.account + "@" + input.conf.name   
        err, result = input.test.xlib.DeployContract("native", "go", self.cname, self.file, contract_account, "None")
        assert err == 0 or "exist" in result, "部署features合约失败： " + result
    
    @pytest.mark.p2
    def test_case02(self, input):
        #1.先给合约账户转账
        err, result = input.test.xlib.Transfer(to=self.cname, amount= "1000000")
        assert err == 0, "转账失败：" + result
        txid = input.test.xlib.GetTxidFromRes(result)
        # 等待tx上链
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

        print("\n根据txid 查询交易信息")
        args = json.dumps({"txid":txid})
        err, result =input.test.xlib.QueryContract("native", self.cname, "QueryTx", args)
        assert err == 0, result
        result = input.test.xlib.GetValueFromRes(result)
        blockid = json.loads(result.split()[-1])["blockid"]
        err, blockid_cli = input.test.xlib.QueryTx(txid)
        assert err == 0 and blockid_cli == blockid, "blockid 错误"

        print("\n根据block 查询交易信息") 
        args = json.dumps({"block_id":blockid})
        err, result =input.test.xlib.QueryContract("native", self.cname, "QueryBlock", args)
        assert err == 0, result
        result = input.test.xlib.GetValueFromRes(result)
        assert err == 0 and json.loads(result.split()[-1])["in_trunk"] == True, "查询区块 失败" + result
            
    @pytest.mark.p2
    def test_case03(self, input):
        #查余额
        err, self.befor_account = input.test.xlib.Balance(account="123456")
        assert err == 0, "查询 " + "123456" + " 余额 失败" + self.befor_account
        err, self.befor_cname = input.test.xlib.Balance(account=self.cname)     
        assert err == 0, "查询 " + self.cname + " 余额 失败" + self.befor_cname   

        invokeArgs = {
            "to": "123456",
            "amount": self.amount
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, \
                                "transfer", args, fee = 100)
        assert err == 0, "使用普通账户转账失败： " + result
        print("转账后查询账户")
        err, after_account = input.test.xlib.Balance(account="123456")   
        assert err == 0 and int(after_account) == int(self.befor_account) + int(self.amount), \
                                                          "查询123456余额 失败" + after_account

        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(self.amount), \
                                                        "查询" + self.cname + "余额 失败" + after_cname
    
    @pytest.mark.p2
    def test_case04(self, input):
        print("\nlogging 从合约内写一条日志")
        #写入logs/xchain.log文件中 自动化没有 cat logs/xchain.log |grep "log from contract"
        err, result = input.test.xlib.QueryContract("native", self.cname, "Logging", "None") 
        assert err == 0, "从合约内写一条日志 失败" + result 
