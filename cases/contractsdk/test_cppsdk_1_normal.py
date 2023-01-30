"""
说明: 测试cpp合约sdk     
"""
import json
import pytest
import time
import os

txid = None
blockid = None
class TestFeatures2():

    file = "cppTemplate/features.wasm"
    cname = "features"
    #合约余额
    amount="70"
    befor_account=""
    befor_cname =""    
   
    def trans_use(self, account, input):
        #1.先给合约账户转账
        err, cname_balan = input.test.xlib.Balance(account=self.cname)   
        if int(cname_balan)  < int(self.amount):
            err, result = input.test.xlib.Transfer(to=self.cname, amount= "1000000")
            assert err == 0 and  result != "Select utxo error", "转账给合约账户 失败： " + result

        #2.查询账户余额
        err, self.befor_account = input.test.xlib.Balance(account=account)
        assert err == 0, "查询 " + account + " 余额 失败" + self.befor_account
        err, self.befor_cname = input.test.xlib.Balance(account=self.cname)     
        assert err == 0, "查询 " + self.cname + " 余额 失败" + self.befor_cname 
   
    #调put方法,并给合约转账
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n调put方法,并给合约转账")     
        invokeArgs = {
            "key": "test$",
            "value": "value$"
        }
        args = json.dumps(invokeArgs)
        #"查询features"
        err, befor_features = input.test.xlib.Balance(account=self.cname)      
        #转账
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args, amount = 1) 
        assert err == 0, "调put方法,并给合约转账 失败" + result 
        err, after_features = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_features) == int(befor_features) + int(1), \
                                                            "查询" + self.cname + "余额 失败" + after_features
       
    #调get方法，读取key，并给合约转账
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n调get方法，读取key,并给合约转账")     
        invokeArgs = {
            "key": "test$"
        }
        args = json.dumps(invokeArgs)
        #"查询features"
        err, befor_features = input.test.xlib.Balance(account=self.cname)                                                       
        #转账
        err, result = input.test.xlib.InvokeContract("native", self.cname, "get", args, amount = 1) 
        assert err == 0, "调put方法,并给合约转账 失败" + result 
        err, after_features = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_features) == int(befor_features) + int(1), \
                                                            "查询" + self.cname + "余额 失败" + after_features

    #logging 从合约内写一条日志
    #2.写入logs/xchain.log文件中 自动化没有 cat logs/xchain.log |grep "log from contract"
    @pytest.mark.p2
    def test_case03(self, input):
        print("\nlogging 从合约内写一条日志")
        err, result = input.test.xlib.QueryContract("native", self.cname, "logging", "None") 
        assert err == 0, "从合约内写一条日志 失败" + result 
  
    #iterator 迭代访问,limit大于start 成功返回13条
    @pytest.mark.p2
    def test_case04(self, input):
        print("\niterator迭代访问,limit大于start")     
        invokeArgs = {"start":"test1", "limit":"test110"}        
        args = json.dumps(invokeArgs)  
        err, result = input.test.xlib.InvokeContract("native", self.cname, "iterator", args) 
        assert err == 0, "迭代访问,limit大于start失败" + result
        assert result.split("response:")[-1].count("test") == 1, "返回的个数不匹配" + result

    #iterator 迭代访问,limit等于start
    @pytest.mark.p2
    def test_case05(self, input):
        print("\niterator迭代访问,limit等于start")     
        invokeArgs = [
                        {"start":"test1", "limit":"test1"},
                        {"start":"test210", "limit":"test210"}
                        ]
        for i in range(len(invokeArgs)):
                args = json.dumps(invokeArgs[i]) 
                err, result = input.test.xlib.InvokeContract("native", self.cname, "iterator", args) 
                assert err == 0, "迭代访问,limit等于start失败" + result 
                getdiff = result.split("\n")[0].split("response:")[-1]
                assert getdiff == " ", "范围内有数据,失败" + result

    #iterator 迭代访问,limit,start范围不存在
    @pytest.mark.p2
    def test_case06(self, input):
        print("\niterator迭代访问,limit,start范围不存在")
        invokeArgs = [
                       {"start":"test1050", "limit":"test1055"},
                       {"start":" ", "limit":" "}
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps(invokeArgs[i]) 
            err, result = input.test.xlib.InvokeContract("native", self.cname, "iterator", args) 
            assert err == 0, "迭代访问,limit,start范围不存在 失败" + result
            getdiff = result.split("\n")[0].split("response:")[-1]
            assert getdiff == " ", "范围内有数据,失败" + result

    #caller 获取合约发起者
    @pytest.mark.p2
    def test_case07(self, input):
        print("\ncaller 获取合约发起者")
        contract_account = "XC" + input.account + "@" + input.conf.name 
        accouErr, accouResult = input.test.xlib.InvokeContract("native", self.cname, "caller", "None",\
                                                          account = contract_account) 
        assert accouErr == 0, "caller 获取合约发起者 失败" + accouResult
        keyErr, keyResult = input.test.xlib.InvokeContract("native", self.cname, "caller", "None", \
                                                  keys = "data/keys/") 
        assert keyErr == 0, "caller 获取合约发起者 失败" + keyResult
    
    #call 发起跨合约调用
    @pytest.mark.p2
    def test_case08(self, input):
        print("\ncall 发起跨合约调用")
        #1.合约调用
        invokeArgs = {"contract":"hello_go", "key":"dudu", "method":"increase"}
        args = json.dumps(invokeArgs) 
        err, result = input.test.xlib.InvokeContract("native", self.cname, "call", args) 
        assert err == 0, "call 发起跨合约调用 失败" + result
        value1 = input.test.xlib.GetValueFromRes(result)
        #2.查询合约调用次数
        query = {
            "key": "dudu"
        }
        args = json.dumps(query)
        err, getResult = input.test.xlib.QueryContract("native", "hello_go", "get", args) 
        value2 = input.test.xlib.GetValueFromRes(getResult)
        assert value1 == value2, "查询跨合约调用次数不匹配" + getResult

    #json_literal 返回 json 一个字面量
    @pytest.mark.p2
    def test_case09(self, input):
        print("\njson_literal 返回 json 一个字面量")    
        err, result = input.test.xlib.QueryContract("native", self.cname, "json_literal", "None") 
        assert err == 0, "json_literal 返回 json 一个字面量 失败" + result
    
    #json_load_dump 读取参数 value,array类型
    @pytest.mark.p2
    def test_case10(self, input):
        print("\njson_load_dump 读取参数 value,array类型")    
        invokeArgs = "[\"hello\",\"world\"]"
        args = json.dumps({"value":invokeArgs})
        err, result = input.test.xlib.InvokeContract("native", self.cname, "json_load_dump", args)
        assert err == 0, "json_load_dump 读取参数 value,array类型 失败" + result

        assert json.loads(result.split("response:")[-1].split("\n")[0])== json.loads(invokeArgs),\
                                                                     "array类型结果值不匹配" + result
    
    #json_load_dump 读取参数 value,bool类型
    @pytest.mark.p2
    def test_case11(self, input):
        print("\njson_load_dump 读取参数 value,bool类型")
        invokeArgs = [
                      {"value":"true"},
                      {"value":"false"}
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps(invokeArgs[i]) 
            err, result = input.test.xlib.InvokeContract("native", self.cname, "json_load_dump", args) 
            assert err == 0, "json_load_dump 读取参数 value,bool类型 失败" + result 

    #json_load_dump 读取参数 value,float类型
    @pytest.mark.p2
    def test_case12(self, input):
        print("\njson_load_dump 读取参数 value,float类型")
        invokeArgs = {"value":"3.14"}        
        args = json.dumps(invokeArgs) 
        err, result = input.test.xlib.InvokeContract("native", self.cname, "json_load_dump", args) 
        assert err == 0, "json_load_dump 读取参数 value,float类型 失败" + result 
    
    #json_load_dump 读取参数 value,int类型
    @pytest.mark.p2
    def test_case13(self, input):
        print("\njson_load_dump 读取参数 value,int类型")
        invokeArgs = {"value":"5"}        
        args = json.dumps(invokeArgs) 
        err, result = input.test.xlib.InvokeContract("native", self.cname, "json_load_dump", args) 
        assert err == 0, "json_load_dump 读取参数 value,int类型 失败" + result  

    #json_load_dump 读取参数 value,string类型
    @pytest.mark.p2
    def test_case14(self, input):
        print("\njson_load_dump 读取参数 value,string类型")
        invokeArgs = [
                        "\"hello\"",
                        "null",
                        "\"!@#$%^&*()_-++?><;\""
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps({"value":invokeArgs[i]})   
            err, result = input.test.xlib.InvokeContract("native", self.cname, "json_load_dump", args) 
            assert err == 0, "json_load_dump 读取参数 value,string类型 失败" + result 
            assert json.loads(result.split("response:")[-1].split("\n")[0]) == json.loads(invokeArgs[i]),\
                                                                     "string类型结果值不匹配" + result
    
    #json_load_dump 读取参数 value,object类型
    @pytest.mark.p2
    def test_case15(self, input):
        print("\njson_load_dump 读取参数 value,object类型")
        invokeArgs = "{\"data\":{\"content\":[{\"id\":\"001\",\"value\":\"testvalue\"},\
        {\"id\":\"002\",\"value\":\" testvalue1\"}]},\"message\":\"success\"}"
        args = json.dumps({"value":invokeArgs})   
        print(args)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "json_load_dump", args) 
        assert err == 0, "json_load_dump 读取参数 value,object类型 失败" + result 
        assert json.loads(result.split("response:")[-1].split("\n")[0]) == json.loads(invokeArgs),\
                                                                     "object类型结果值不匹配" + result
        global txid
        txid = result.split(":")[-1].strip()   
         
    #getTx，查询交易
    @pytest.mark.p2
    def test_case16(self, input):
        print("\nquery_tx,查询交易")

        #等tx上链
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

        invokeArgs = {
            "tx_id": txid
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "query_tx", args)
        assert err == 0, "查询query_tx交易失败： " + result
        err, blockid = input.test.xlib.QueryTx(txid)
        assert blockid in result, "查询结果错误"

    #getBlock，查询区块
    @pytest.mark.p2
    def test_case17(self, input):
        print("\nquery_block,查询区块")
        global blockid
        err, blockid = input.test.xlib.QueryTx(txid) 
        assert err == 0, "查询block失败：" + blockid
        assert blockid != " "         
        invokeArgs = {
            "blockid": blockid
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "query_block", args)
        assert err == 0, "查询query_block区块失败： " + result

    # transfer,使用合约账户转账(扣除70,features合约余额999932)
    @pytest.mark.p2
    def test_case18(self, input):
        print("\ntransfer,使用合约账户转账") 
        contract_account = "XC" + input.account + "@" + input.conf.name   
        #查余额
        self.trans_use("testAccount", input)       
        invokeArgs = {
            "to": "testAccount",
            "amount": self.amount
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "transfer", args,\
                          account = contract_account, fee = 100)
        assert err == 0, "使用合约账户转账失败： " + result
        print("转账后查询账户")
        err, after_account = input.test.xlib.Balance(account="testAccount")   
        assert err == 0 and int(after_account) == int(self.befor_account) + int(self.amount), \
                                                          "查询testAccount余额 失败" + after_account

        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(self.amount), \
                                                        "查询" + self.cname + "余额 失败" + after_cname

    # transfer,使用普通账户转账,(扣除70,features合约余额999862)
    @pytest.mark.p2
    def test_case19(self, input):
        print("\ntransfer,使用普通账户转账")   
        #查余额
        self.trans_use("testAccount", input)       
        invokeArgs = {
            "to": "testAccount",
            "amount": self.amount
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, \
                                "transfer", args, keys = "data/keys/", fee = 100)
        assert err == 0, "使用普通账户转账失败： " + result
        print("转账后查询账户")
        err, after_account = input.test.xlib.Balance(account="testAccount")   
        assert err == 0 and int(after_account) == int(self.befor_account) + int(self.amount), \
                                                          "查询testAccount余额 失败" + after_account

        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(self.amount), \
                                                        "查询" + self.cname + "余额 失败" + after_cname
    
    #transfer,自身转账
    @pytest.mark.p2
    def test_case20(self, input):
        print("\ntransfer,自身转账")   
        #查余额
        contract_account = "XC" + input.account + "@" + input.conf.name 
        self.trans_use(contract_account, input)       
        invokeArgs = {
            "to": contract_account,
            "amount": self.amount
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "transfer", \
                      args, account = contract_account, fee = 100)
        assert err == 0, "自身转账失败： " + result
        print("转账后查询合约账户")
        err, after_account = input.test.xlib.Balance(account=contract_account)   
        gitdiff=int(self.befor_account) - int(100) + int(self.amount)
        assert err == 0 and int(after_account) == gitdiff, \
                                                          "查询账户余额 失败" + after_account

        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(self.amount), \
                                                        "查询" + self.cname + "余额 失败" + after_cname

    #一次转账中有多个元素
    def test_case21(self, input):
        print("\n一次转账中有多个元素")   
        contract_account = "XC" + input.account + "@" + input.conf.name 
        self.trans_use("XC1111111178911114@xuper", input)     
        invokeArgs = {"to":"XC1111111178911112@xuper",
                       "amount":"60", "to":"XC1111111178911113@xuper",
                        "amount":"60", "to":"XC1111111178911114@xuper", "amount":"60"}
        
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "transfer", args,\
                     account = contract_account, fee = 100)
        assert err == 0, "一次转账中有多个元素 转账失败： " + result
        #合约方法
        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(60), \
                                                        "查询" + self.cname + "余额 失败" + after_cname
        #账户
        err, balance = input.test.xlib.Balance(account="XC1111111178911112@xuper") 
        assert err == 0 and balance == "0", "XC1111111178911112@xuper余额查询 失败： " + balance
        err, balance = input.test.xlib.Balance(account="XC1111111178911113@xuper") 
        assert err == 0 and balance == "0", "XC1111111178911113@xuper余额查询 失败： " + balance
        err, aft_balance = input.test.xlib.Balance(account="XC1111111178911114@xuper") 
        assert err == 0 and int(aft_balance) == int(self.befor_account) + int(60), \
                                                "XC1111111178911114@xuper余额查询 失败： " + balance
