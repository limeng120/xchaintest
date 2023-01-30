"""
说明: 测试evm合约sdk     
"""
import json
import pytest
import time

class TestStoraget():

    abi = "evmTemplate/StorageBasicData.abi"
    file = "evmTemplate/StorageBasicData.bin"
    cname = "storagetest"

    tokenAbi = "evmTemplate/TESTToken.abi"
    tokenFile = "evmTemplate/TESTToken.bin"
    tokeName = "testtoken100"
    tokenAddr = "313131312D2D2D2D74657374746F6B656E313030"
    
    TESTNesTokenbin = "evmTemplate/TESTNestToken.bin"
    TESTNesTokenAbi = "evmTemplate/TESTNestToken.abi"
    testNest="testnest100"

    #合约余额
    amount="100"
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

    # 合约部署storagetest合约
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n部署storagetest合约") 
        contract_account = "XC" + input.account + "@" + input.conf.name 
        err, result = input.test.xlib.DeployContract("evm", "", self.cname, \
            self.file, contract_account, "None", abi = self.abi)         
        assert err == 0 or "already exist" in result, "部署storagetest合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

    #uint数据类型的增删改查,传入合法uint
    @pytest.mark.p2
    def test_case02(self, input):
        print("\nuint数据类型的增删改查,传入合法uint")
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", json.dumps({"x": "10"}))
        assert err == 0, "uint数据类型的增删改查,传入合法uint 失败： " + result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getUint", "None")
        assert err == 0, result
        result = input.test.xlib.GetValueFromRes(result)
        assert result == '[{"0":"10"},{"1":"11"},{"2":"12"}]',\
                     "查询Uint设置后的数据 有误" + result

        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", json.dumps({"x":"01234567"}))
        assert err == 0, "uint数据类型的增删改查,传入合法uint 失败： " + result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getUint", json.dumps({"x":"01234567"}))                
        assert err == 0, result
        result = input.test.xlib.GetValueFromRes(result)
        assert result == '[{"0":"342391"},{"1":"342392"},{"2":"342393"}]',\
                     "查询Uint设置后的数据 有误" + result

    #uint数据类型的增删改查，传入uint边界值
    @pytest.mark.p2
    def test_case03(self, input):
        print("\nuint数据类型的增删改查,传入uint边界值")
        invokeArgs = [
                      {"x":"0"},
                      {"x":"11111111111111111111111111111111111111111111111111111111111111111111111111111"}
                    ]
        getResults = ['[{"0":"0"},{"1":"1"},{"2":"2"}]', 
               '[{"0":"11111111111111111111111111111111111111111111111111111111111111111111111111111"},\
               {"1":"11111111111111111111111111111111111111111111111111111111111111111111111111112"},\
               {"2":"11111111111111111111111111111111111111111111111111111111111111111111111111113"}]']
        for i in range(len(invokeArgs)):
            args = json.dumps(invokeArgs[i]) 
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", args) 
            assert err == 0, "传入uint边界值 失败" + result 
            err, result = input.test.xlib.QueryContract("evm", self.cname, "getUint", "None")  
            assert err == 0, result
            result = input.test.xlib.GetValueFromRes(result)              
            assert result == getResults[i].replace(' ', ''),\
                    "查询Uint设置后的数据 有误" + result
        
    #bool数据类型的增删改查，传入合法bool值
    @pytest.mark.p2
    def test_case04(self, input):
        print("\nbool数据类型的增删改查，传入合法bool值")
        invokeArgs = [                      
                      {"x":"true"},
                      {"x":"1"},
                      {"x":"false"},              
                      {"x":"0"}
                     ]
        for i in range(len(invokeArgs)):
                args = json.dumps(invokeArgs[i]) 
                err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBool", args) 
                assert err == 0, "传入合法bool值 失败" + result 
                err, result = input.test.xlib.QueryContract("evm", self.cname, "getBool", "None")
                assert err == 0, result
                result = input.test.xlib.GetValueFromRes(result)
                if invokeArgs[i] == {'x':'false'}   or invokeArgs[i]  == {'x':'0'}:
                    assert result == '[{"retBool":"false"}]',\
                     "查询bool数据 有误" + result
                else:
                    assert result == '[{"retBool":"true"}]',\
                     "查询bool数据 有误" + result
    
    #string数据类型的增删改查，传入合法string
    @pytest.mark.p2
    def test_case05(self, input):
        print("\nstring数据类型的增删改查，传入合法string")
        invokeArgs = ["hello", " hello world_! ", ""]
        for i in range(len(invokeArgs)):
                args = json.dumps({"x":invokeArgs[i]})
                err, result = input.test.xlib.InvokeContract("evm", self.cname, "setString", args)
                assert err == 0, "传入合法string值 失败" + result
                err, getResult = input.test.xlib.QueryContract("evm", self.cname, "getString", "None")
                assert err == 0, getResult
                result = input.test.xlib.GetValueFromRes(getResult)
                retStr ='[{"retString":"' + invokeArgs[i] + '"}]'       
                assert result == retStr, "查询string数据 有误" + getResult

    #address数据类型的增删改查，传入合法address
    @pytest.mark.p2
    def test_case06(self, input):
        print("\naddress数据类型的增删改查，传入合法address")
        invokeArgs = "3131313231313131313131313131313131313133"
        args = json.dumps({"x":invokeArgs})
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setAddress", args)
        assert err == 0, "设置address数据 失败" + result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getAddress", "None")
        assert err == 0, result
        result = input.test.xlib.GetValueFromRes(result)
        assert result == '[{"retAddress":"' + invokeArgs + '"}]', \
                                  "查询address数据 有误" + result

    #uint array数据类型的增删改查，传入uint
    @pytest.mark.p2
    def test_case07(self, input):
        print("\n uint array数据类型的增删改查,传入uint")
        invokeArgs = [
                     "[1,2,3,4]",
                     "[0]",
                     "[11111111111111111111111111111111111111111111111111111111111111111111111111111]"
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps({"uintArrays":invokeArgs[i]})
            #获取旧数组
            err, result = input.test.xlib.QueryContract("evm", self.cname, "getUints", "None")
            result = input.test.xlib.GetValueFromRes(result)
            oldResult =  json.loads(json.loads(result)[0]["0"])

            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUints", args) 
            assert err == 0, "传入uint array 失败" + result 
            err, result = input.test.xlib.QueryContract("evm", self.cname, "getUints", "None")    
            assert err == 0, result
            result = input.test.xlib.GetValueFromRes(result)

            #数组追加
            oldResult.extend(json.loads(invokeArgs[i]))           
            assert result == '[{"0":"' + \
                    str(oldResult).replace(' ', '') + '"}]', "查询uint array数据 有误" + result

    #原生代币转账，调evm合约同时给合约账号转账, 余额 1000100
    @pytest.mark.p2
    def test_case08(self, input):
        print("\n 原生代币转账,调evm合约同时给合约账号转账")
        #查余额
        contract_account = "XC" + input.account + "@" + input.conf.name 
        self.trans_use(contract_account, input)
        args = json.dumps({"x":"10"})
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", args,\
                     account = contract_account, amount=self.amount)
        assert err == 0, "调evm合约同时给合约账号转账 失败： " + result    

        err, after_cname = input.test.xlib.Balance(account=self.cname)   
        assert err == 0 and int(after_cname) == int(self.befor_cname) + int(self.amount), \
                                                "查询" + self.cname + "余额 失败" + after_cname
    
    # 部署erc20合约
    @pytest.mark.p2
    def test_case09(self, input):
        print("\n部署erc20合约") 
        contract_account = "XC" + input.account + "@" + input.conf.name 
        err, result = input.test.xlib.DeployContract("evm", "", self.tokeName, \
            self.tokenFile, contract_account, "None", abi = self.tokenAbi)         
        assert err == 0 or "already exist" in result, "部署erc20合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

    # 部署调用合约
    @pytest.mark.p2
    def test_case10(self, input):
        print("\n部署调用合约")  
        args = json.dumps({"token":self.tokenAddr})
        contract_account = "XC" + input.account + "@" + input.conf.name 
        err, result = input.test.xlib.DeployContract("evm", "", self.testNest, \
            self.TESTNesTokenbin, contract_account, args, abi = self.TESTNesTokenAbi)         
        assert err == 0 or "already exist" in result, "部署调用合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

    #跨合约调用，跨合约查询原始合约的合约名
    @pytest.mark.p2
    def test_case11(self, input):
        print("\n跨合约调用,跨合约查询原始合约的合约名")
        err, result = input.test.xlib.QueryContract("evm", self.testNest, "getTokenAddress", "None")        
        assert err == 0, "跨合约查询原始合约失败：" + result
        result = input.test.xlib.GetValueFromRes(result)
        assert json.loads(result)[0]['0']   == self.tokenAddr, "跨合约查询合约名有误" + result

    #跨合约调用，跨合约调用原始合约的方法做erc20代币转账
    @pytest.mark.p2
    def test_case12(self, input):
        print("\n 跨合约调用,跨合约调用原始合约的方法做erc20代币转账")
        contract_account = "XC" + input.account + "@" + input.conf.name  
        invokeArgs = [
                     "B4E26DF80E3F548455634ABE87937FC0E1368225",
                     "313131312D2D2D2D2D746573746E657374313030",
                     "D4CA13E87044275C8BA7A7217286868E2C2F357A"
                    ]
        for i in range(len(invokeArgs)):   
                getArgs = json.dumps({"_owner":invokeArgs[i]})
                err, oldResult = input.test.xlib.QueryContract("evm", self.tokeName, "balanceOf", getArgs)        
                assert err == 0, "查询 代币余额失败： " + oldResult
                oldResult = input.test.xlib.GetValueFromRes(oldResult)
                oldResult = json.loads(oldResult)[0]['0']
                #转账
                toArgs = {"_to":invokeArgs[i], "_value":"10"}        
                args = json.dumps(toArgs)        
                err, result = input.test.xlib.InvokeContract("evm", self.tokeName, "transfer", args,\
                        account = contract_account)
                assert err == 0, "直接调用原始合约的方法做erc20代币转账 转账失败： " + result

                err, NewResult = input.test.xlib.QueryContract("evm", self.tokeName, "balanceOf", getArgs)        
                assert err == 0, "直接调用原始合约的方法做erc20代币转账 转账失败： " + NewResult
                NewResult = input.test.xlib.GetValueFromRes(NewResult)
                assert int(json.loads(NewResult)[0]['0']) == int(oldResult) + int(10), \
                                    "转账后查询代币 余额有误" + NewResult
    
    @pytest.mark.p2
    def test_case13(self, input):
        print("\n原生代币转账,evm合约向外转账")
        invokeArgs = [
                     "3131313231313131313131313131313131313132",
                     "D4CA13E87044275C8BA7A7217286868E2C2F357A",
                     "313131312D2D2D2D2D2D2D2D2D636F756E746572"
                    ]
        for i in range(len(invokeArgs)):                   
                err, result = input.test.xlib.AddrTrans("e2x", invokeArgs[i])
                assert err == 0, "evm地址转合约名失败： " + result

                if i == 0:
                    address = "XC" + result.split()[1] + "@" + input.conf.name
                else:
                    address = result.split()[1]
                #查询合约余额
                self.trans_use(address, input)
                #转账
                toArgs = {"receiver":invokeArgs[i], "amount":"1"}        
                args = json.dumps(toArgs)        
                err, result = input.test.xlib.InvokeContract("evm", self.cname, "send", args, fee=10)
                assert err == 0, "evm合约向外转账 失败： " + result
                #查询转账后的余额                                
                err, NewResult = input.test.xlib.Balance(account=self.cname) 
                assert err == 0, "转账后查询合约余额 失败： " + NewResult
                assert int(NewResult) == int(self.befor_cname) - int(1), \
                                    "转账后查询合约 余额有误" + NewResult

                err, NewAclResult = input.test.xlib.Balance(account=address) 
                assert err == 0, "转账后查询evm账户余额 失败： " + NewResult
                assert int(NewAclResult) == int(self.befor_account) + int(1), \
                                    "转账后查询evm账户 余额有误" + NewAclResult
                if err == 0:
                    # 等待tx上链
                    txid = input.test.xlib.GetTxidFromRes(result)
                    err, result = input.test.xlib.WaitTxOnChain(txid)
                    assert err == 0, result

    #uint数据类型的增删改查,传入合法int
    @pytest.mark.p2
    def test_case14(self, input):
        print("\nint数据类型的增删改查,传入合法int")
        value = [10, -10, 0]
        for v in value:
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setInt", json.dumps({"x": str(v)}))
            assert err == 0, result
            err, result = input.test.xlib.QueryContract("evm", self.cname, "getInt", "None") 
            result = input.test.xlib.GetValueFromRes(result)       
            assert err == 0 and  '[{"retInt":"' + str(v) + '"}]' in result

    #uint数据类型的增删改查,传入int边界值
    @pytest.mark.p2
    def test_case15(self, input):
        print("\nint数据类型的增删改查,传入int边界值")
        value = [-57896044618658097711785492504343953926634992332820282019728792003956564819967, \
                57896044618658097711785492504343953926634992332820282019728792003956564819967]
        for v in value:
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setInt", json.dumps({"x": str(v)}))
            assert err == 0, result
            err, result = input.test.xlib.QueryContract("evm", self.cname, "getInt", "None") 
            result = input.test.xlib.GetValueFromRes(result)
            assert err == 0 and '[{"retInt":"' + str(v) + '"}]' in result

    @pytest.mark.p2
    def test_case16(self, input):
        print("\nint数组数据类型的增删改查,传入合法int数组")
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setIntArr", json.dumps({"x": "[10,-10,0]"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getIntArr", "None")                
        assert err == 0 and '10,-10,0' in result

    @pytest.mark.p2
    def test_case17(self, input):
        print("\nint数组数据类型的增删改查,传入int边界值") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setIntArr", json.dumps({"x":\
                "[-57896044618658097711785492504343953926634992332820282019728792003956564819967,\
57896044618658097711785492504343953926634992332820282019728792003956564819967]"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getIntArr", "None")                
        assert err == 0 and '-57896044618658097711785492504343953926634992332820282019728792003956564819967,\
57896044618658097711785492504343953926634992332820282019728792003956564819967' in result

    #address数据类型的增删改查，传入合法address
    @pytest.mark.p2
    def test_case18(self, input):
        print("\naddress数组数据类型的增删改查，传入合法address数组")
        invokeArgs = "[3131313231313131313131313131313131313133,3131313231313131313131313131313131313133]"
        args = json.dumps({"x":invokeArgs})
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setAddrArr", args)
        assert err == 0, "设置address数据 失败" + result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getAddrArr", "None")
        assert err == 0 and \
            "3131313231313131313131313131313131313133,3131313231313131313131313131313131313133" in result
       
    @pytest.mark.p2
    def test_case19(self, input):
        print("\nbytes数据类型的增删改查,传入合法byte，值是1个byte32") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytesAuto", json.dumps({"x":\
                "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getBytesAuto", "None")                
        assert err == 0 

    @pytest.mark.p2
    def test_case20(self, input):
        print("\nbytes数据类型的增删改查,传入合法byte，值是2个byte32") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytesAuto", json.dumps({"x":\
                "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd\
e4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getBytesAuto", "None")                
        assert err == 0 

    @pytest.mark.p2
    def test_case21(self, input):
        print("\nbytes数据类型的增删改查,传入合法byte，值是0x1111") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytesAuto", json.dumps({"x":\
                "0x1111"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getBytesAuto", "None")                
        assert err == 0 

    @pytest.mark.p2
    def test_case22(self, input):
        print("\nbytes32数据类型的增删改查,传入合法bytes32") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytes", json.dumps({"x":\
                "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getBytes", "None")                
        assert err == 0

    @pytest.mark.p2
    def test_case23(self, input):
        print("\nbytes32数据类型的增删改查,传入合法bytes32") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytes", json.dumps({"x":\
                "0x1111"}))
        assert err == 0, result
        err, result = input.test.xlib.QueryContract("evm", self.cname, "getBytes", "None")                
        assert err == 0
