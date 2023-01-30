"""
说明: 测试java合约sdk       
"""
import json
import pytest
import time

txid = None
blockid = None
class TestBuiltin():

    file = "javaTemplate/builtin-types-0.1.0-jar-with-dependencies.jar"
    cname = "builtin_types_j"
    #合约余额
    amount="70"
    befor_account=""
    befor_cname =""    
    widthCount = "".zfill(1024)
    
    def getList_use(self, invokeArgs, input):
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "getList", args)
        assert err == 0, "调getList方法，传入start 失败" + result 
   
    def trans_use(self, input):
        #1.先给合约账户转账
        err, cname_balan = input.test.xlib.Balance(account=self.cname)   
        if int(cname_balan)  < int(self.amount):
            err, result = input.test.xlib.Transfer(to=self.cname, amount= "1000000")
            assert err == 0 and  result != "Select utxo error", "转账给合约账户 失败： " + result

        #2.查询账户余额
        err, self.befor_account = input.test.xlib.Balance(account="testAccount")
        assert err == 0, "查询testAccount余额 失败" + self.befor_account
        err, self.befor_cname = input.test.xlib.Balance(account=self.cname)     
        assert err == 0, "查询" + self.cname + "余额 失败" + self.befor_cname 

    # 合约部署builtin-types合约
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n合约部署builtin-types合约")
        contract_account = "XC" + input.account + "@" + input.conf.name        
        err, result = input.test.xlib.DeployContract("native", "java", self.cname, self.file, contract_account, "None")
        assert err == 0 or "exist" in result, "部署builtin-types合约失败： " + result

    #getTx，查询交易
    @pytest.mark.p2
    def test_case02(self, input):
        print("\ngetTx,查询交易")
        err, result = input.test.xlib.Transfer(to="abc", amount= "1")
        assert err == 0
        global txid
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result
 
        invokeArgs = {
            "txid": txid
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "getTx", args)
        assert err == 0, "查询getTx交易失败： " + result

    #getBlock，查询区块
    @pytest.mark.p2
    def test_case03(self, input):
        print("\ngetBlock，查询区块")
        global blockid
        err, blockid = input.test.xlib.QueryTx(txid) 
        assert err == 0, "查询block失败：" + blockid
        assert blockid != " "         
        invokeArgs = {
            "blockid": blockid
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "getBlock", args)
        assert err == 0, "查询getBlock区块失败： " + result

    #transfer，转账xuper
    @pytest.mark.p2
    def test_case04(self, input):
        print("\ntransfer，转账xuper")   
        #查余额
        self.trans_use(input)       
        invokeArgs = {
            "to": "testAccount",
            "amount": self.amount
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "transfer", args, fee = 1)
        assert err == 0, "转账失败： " + result
        print("转账后查询账户")
        err, after_account = input.test.xlib.Balance(account="testAccount")   
        assert err == 0 and int(after_account) == int(self.befor_account) + int(self.amount), \
                                                          "查询testAccount余额 失败" + after_account

        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) - int(self.amount), \
                                                        "查询" + self.cname + "余额 失败" + after_cname

    #调put方法,写入1个kv，记录个数
    @pytest.mark.p2
    def test_case05(self, input):
        print("\n调put方法,写入1个kv")
        invokeArgs = {
            "key": "test1",
            "value":"value1"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法,写入210个kv 失败" + result 
    
    #调get方法,查询1个kv，记录个数
    @pytest.mark.p2
    def test_case06(self, input):
        print("\n调get方法,查询1个kv")
        invokeArgs = {
            "key": "test1"
            }
        args = json.dumps(invokeArgs)            
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,查询210个kv 失败" + result 
        
    #调getList方法，传入start，start后有超过100条
    @pytest.mark.p2
    def test_case07(self, input):
        print("\n调getList方法，传入start,start后有超过100条")
        invokeArgs = {
             "start": "test1"
            }
        self.getList_use(invokeArgs, input)
    
    #调getList方法，传入start，start后有超过200条
    @pytest.mark.p2
    def test_case08(self, input):
        print("\n调getList方法，传入start,start后有超过200条")
        invokeArgs = {
             "start": "test"
            }
        self.getList_use(invokeArgs, input)
      
    #调getList方法，传入start，start后有超过10条
    @pytest.mark.p2
    def test_case09(self, input):
        print("\n调getList方法，传入start,start后有超过10条")
        invokeArgs = {
             "start": "test10"
            }
        self.getList_use(invokeArgs, input)
      
    #调getList方法，传入start, start后无数据
    @pytest.mark.p2
    def test_case10(self, input):
        print("\n调getList方法，传入start,start后无数据")
        invokeArgs = {
             "start": "key"
            }
        self.getList_use(invokeArgs, input)
    
    #调put方法，key含特殊字符,value含特殊字符
    @pytest.mark.p2
    def test_case11(self, input):
        print("\n调put方法，key含特殊字符,value含特殊字符")
        invokeArgs = {
                "key": "test$",
                "value":"value$"
                }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法:key和value含特殊字符 失败" + result 
    
    #调get方法,key含特殊字符
    @pytest.mark.p2
    def test_case12(self, input):
        print("\n调get方法,key含特殊字符")
        invokeArgs = {
                "key": "test$"
                }
        args = json.dumps(invokeArgs)                     
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,key含特殊字符 失败" + result 

    #调put方法,key长度1k,value长度1k
    @pytest.mark.p2
    def test_case13(self, input):
        print("\n调put方法,key长度1k,value长度1k")
        invokeArgs = {
            "key": "test" + self.widthCount,
            "value": "value" + self.widthCount
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法：key和value长度1K, 失败" + result 
    
    #调get方法，key长度1k
    @pytest.mark.p2
    def test_case14(self, input):
        print("\n调get方法,key长度1k")
        invokeArgs = {
            "key": "test" + self.widthCount
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,key长度1k 失败" + result 
        result = input.test.xlib.GetValueFromRes(result)
        #value值长度是1024
        assert result == "value" + self.widthCount
    
    #authRequire，查询合约方法的调用者
    @pytest.mark.p2
    def test_case15(self, input):
        print("\nauthRequire,查询合约方法的调用者")
        err, result = input.test.xlib.QueryContract("native", self.cname, "authRequire", "None")
        assert err == 0, "authRequire,查询合约方法的调用者 失败" + result 
    
    #transferAndPrintAmount，给合约转账，合约内部查询转账金额
    @pytest.mark.p2
    def test_case16(self, input):
        print("\ntransferAndPrintAmount,给合约转账,合约内部查询转账金额")
        #查余额
        self.trans_use(input)
        err, result = input.test.xlib.InvokeContract("native", self.cname, 
                                "transferAndPrintAmount", "None", amount = 10)
        assert err == 0, "合约内部转账失败： " + result
        print("转账后查询合约")       
        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(10), "查询" + self.cname + "余额 失败" \
                                                                                 + after_cname     
    
    #调put方法，写入kv，并给合约转账
    @pytest.mark.p2
    def test_case17(self, input):
        print("\n调put方法，写入kv，并给合约转账")
        #查余额
        self.trans_use(input)
        invokeArgs = {
                "key": "test$",
                "value":"value$"
                }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args, amount = 1)
        assert err == 0, "调put方法，写入kv,并给合约转账 失败" + result 
        print("转账后查询合约")       
        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(1), "查询" + self.cname + "余额 失败" \
                                                                                 + after_cname     

    #调get方法，读取key，并给合约转账()
    @pytest.mark.p2
    def test_case18(self, input):
        print("\n调get方法,写入kv,并给合约转账,(合约余额999942)")
        #查余额
        self.trans_use(input)
        invokeArgs = {
                "key": "test$"
                }
        args = json.dumps(invokeArgs)  
        err, result = input.test.xlib.InvokeContract("native", self.cname, "get", args, amount=1)
        assert err == 0, "调get方法,写入kv,并给合约转账 失败" + result 
        print("转账后查询合约")       
        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(1), "查询" + self.cname + "余额 失败" \
                                                                                 + after_cname 
