"""
说明: 测试evm合约sdk的异常场景
"""
import json
import pytest
import time

class TestStoragetErr():

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

    def transfer_NotEnough(self, toArgs, file, input):
        contract_account = "XC" + input.account + "@" + input.conf.name                
        args = json.dumps(toArgs)        
        err, result = input.test.xlib.InvokeContract("evm", file, "transfer", args,\
                        account = contract_account)

        key_err, key_result = input.test.xlib.InvokeContract("evm", file, "transfer", args)
        assert err != 0 or key_err != 0, "代币余额不足,转账成功,不符合预期：" + result + key_result
        msg = "contract invoke failed" 
        assert msg in result or msg in key_result, "报错信息错误"

    @pytest.mark.abnormal
    def transfer_use(self, file, input):
        invokeArgs = ["-1", "a", "0"]
        if (file == self.tokeName):
            contract_account = "XC" + input.account + "@" + input.conf.name  
            # #转账数额为0 
            toArgs = {"_to":self.tokenAddr, "_value":"0"}        
            args = json.dumps(toArgs)        
            err, result = input.test.xlib.InvokeContract("evm", file, "transfer", args,\
                            account = contract_account)
            assert err == 0, "代币数为0 转账失败,不符合预期：" + result
            #[异常]转账数额为-1
            invokeArgs = ["-1", "a"]
        for i in range(len(invokeArgs)):
                getArgs = json.dumps({"_to":self.tokenAddr, "_value":invokeArgs[i]})
                err, result = input.test.xlib.InvokeContract("evm", file, "transfer", getArgs)
                assert err != 0, "转账数额为" + invokeArgs[i] \
                                                  + " 转账成功,不符合预期：" + result 
                msg = "contract invoke failed" 
                assert msg in result, "报错信息错误"
    
    def balanceOf(self, file, input):
        err, result = input.test.xlib.QueryContract("evm", file, "balanceOf", \
                              '{"_owner":"313131312D2D2D2D2D2D2D2D2D2D616263646566"}')        
        assert err == 0, "查询不存在的账户 失败, 不符合预期： " + result

    #【异常】uint数据类型的增删改查，传入非uint值
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\nuint数据类型的增删改查,传入非uint值")
        invokeArgs = [
                      {"x":"-10"},
                      {"x":"aaaa"},
                      {"x":"!@#$%^&*_+"}
                    ]
        for i in range(len(invokeArgs)):
                args = json.dumps(invokeArgs[i]) 
                err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", args) 
                assert err != 0, "传入uint边界值成功，不符合预期" + result 
                msg = "invoke failed"
                assert msg in result, "报错信息错误"
        
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", '{"x":}') 
        assert err != 0, "传入uint边界值成功，不符合预期" + result 
        msg = "invalid character '}' looking for beginning of value"
        assert msg in result, "报错信息错误"

        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", \
          json.dumps({"x":"111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"}))
        assert err == 0, "数据溢出出错 不符合预期" + result 
        err, getRes = input.test.xlib.QueryContract("evm", self.cname, "getUint", "None")         
        msg = '[{"0":"25870071517096625434027777777777777777777777777777777777777777777777777777777"},\
                      {"1":"25870071517096625434027777777777777777777777777777777777777777777777777777778"},\
                        {"2":"25870071517096625434027777777777777777777777777777777777777777777777777777779"}]'
        assert msg.replace(" ", "") in getRes, "报错信息错误" 

    #【异常】bool数据类型的增删改查，传入非bool值
    @pytest.mark.abnormal
    def test_case04(self, input):
        print("\nuint数据类型的增删改查,传入uint边界值")
        invokeArgs = [
                      {"x":"-1"},
                      {"x":"qqqq"},
                      {"x":"+!@"}     
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps(invokeArgs[i]) 
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBool", args) 
            assert err != 0, "传入非bool值成功,不符合预期" + result 
            msg = "invoke failed"
            assert msg in result, "报错信息错误"

        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBool", '{"x":}') 
        assert err != 0, "传入非bool值成功,不符合预期" + result 
        msg = "invalid character '}' looking for beginning of value"
        assert msg in result, "报错信息错误"
    
    #【异常】address数据类型的增删改查，传入非法address
    #1.设置address数据，比合法地址少1位 
    #2.设置address数据为xchain普通账号、合约账号、合约名
    @pytest.mark.abnormal
    def test_case05(self, input):
        print("\n address数据类型的增删改查,传入非法address")
        invokeArgs = [                      
                      {"x":"313131323131313131313131313131313131313"},
                      {"x":"TeyyPLpp9L7QAcxHangtcHTu7HUZ6iydY"},
                      {"x":"XC2111111111111111@xuper"},
                      {"x":self.cname}   
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps(invokeArgs[i]) 
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setAddress", args) 
            assert err != 0, "传入address值成功,不符合预期" + result 
            msg = "invoke failed"
            assert msg in result, "报错信息错误"
    
    #【异常】uint array数据类型的增删改查，传入非数组格式
    @pytest.mark.abnormal
    def test_case06(self, input):
        print("\n address数据类型的增删改查,传入非法address")
        invokeArgs = [                      
                      "[1,]",
                      "1",
                      "[-10]",
                      "[aaa]",
                      "[!@#$%^&]"
                    ]
        for i in range(len(invokeArgs)):
            args = json.dumps({"uintArrays":invokeArgs[i]}) 
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUints", args) 
            assert err != 0, "传入非uint arrayl值成功,不符合预期" + result 
            msg = "invoke failed"
            assert msg in result, "报错信息错误"
        
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUints", '{"uintArrays":}') 
        assert err != 0, "传入非uint arrayl值成功,不符合预期" + result 
        msg = "invalid character '}' looking for beginning of value"
        assert msg in result, "报错信息错误"

        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUints", json.dumps({"uintArrays":\
          "[111111111111111111111111111111111111111111111111111111111111111111111111111111111111111]"}))
        assert err == 0, "数据溢出出错 不符合预期" + result 
        err, getRes = input.test.xlib.QueryContract("evm", self.cname, "getUints", "None")         
        msg = "25870071517096625434027777777777777777777777777777777777777777777777777777777"
        assert msg.replace(" ", "") in getRes, "报错信息错误" 

    #【异常】原生代币转账，调evm合约同时给合约转账
    @pytest.mark.abnormal
    def test_case07(self, input):
        print("\n【异常】原生代币转账，调evm合约同时给合约转账")
        contract_account = "XC" + input.account + "@" + input.conf.name 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", json.dumps({"x":"-10"}),\
                     account = contract_account, amount= 100)
        assert err != 0, "调evm合约同时给合约,转账为负数 成功,不符合预期" + result
        msg = "negative value not allowed for uint256" 
        assert msg in result, "报错信息错误"

        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setUint", json.dumps({"x":"10"}),\
                     account = contract_account, amount= 1000000000000000000000000)
        assert err != 0, "给合约自身转账,当前账户余额不足成功,不符合预期" + result
        msg = "enough money(UTXO) to start this transaction" 
        assert msg in result, "报错信息错误"

    #【异常】原生代币转账，evm合约向外转账
    @pytest.mark.abnormal
    def test_case08(self, input):
        print("\n【异常】原生代币转账，evm合约向外转账")
        #【异常】原生代币转账，evm合约给自己转账
        err, result = input.test.xlib.AddrTrans("x2e", self.cname)
        assert err == 0, "合约名转evm地址失败： " + result
        address = result.split()[1]
        invokeArgs=[
                    {"receiver":"XC2111111111111111@xuper", "amount":"1"},
                    {"receiver":"gq2sEvq1ijTtpnGfcSrGXCztKtq31rgDZ", "amount":"1"},
                    {"receiver":"aaaa", "amount":"1"},
                    {"receiver":address, "amount":"1"}
                   ]
        for i in range(len(invokeArgs)):
                args = json.dumps(invokeArgs[i])
                err, result = input.test.xlib.InvokeContract("evm", self.cname, "send", args)
                assert err != 0, "evm合约向外转账成功,不符合预期" + result
                msg = "contract invoke failed" 
                assert msg in result, "报错信息错误"

    #直接调用原生合约方法做erc20代币转账，转出账户余额不足
    @pytest.mark.abnormal
    def test_case09(self, input):
        print("\n直接调用原生合约方法做erc20代币转账，转出账户余额不足")
        toArgs = {"_to":"313131312D2D2D2D2D746573746E657374313030", "_value":"19999999999999999999999999999"} 
        self.transfer_NotEnough(toArgs, self.tokeName, input)

    #直接调用原生合约方法做erc20代币转账，转账数额非正整数
    @pytest.mark.abnormal
    def test_case10(self, input):
        print("\n 直接调用原生合约方法做erc20代币转账，转账数额非正整数")
        self.transfer_use(self.tokeName, input)

    #直接调用原生合约方法做erc20代币余额查询,查询不存在的账户
    @pytest.mark.abnormal
    def test_case11(self, input):
        print("\n直接调用原生合约方法做erc20代币余额查询,查询不存在的账户")
        self.balanceOf(self.tokeName, input)
    
    #跨合约调用原生合约方法做erc20代币转账，转出账户余额不足
    @pytest.mark.abnormal
    def test_case12(self, input):
        print("\n跨合约调用原生合约方法做erc20代币转账，转出账户余额不足")
        toArgs = {"_to":"D4CA13E87044275C8BA7A7217286868E2C2F357A", "_value":"5000000000000000000"} 
        self.transfer_NotEnough(toArgs, self.testNest, input)    

    #跨合约调用原生合约方法做erc20代币转账，转账数额非正整数
    @pytest.mark.abnormal
    def test_case13(self, input):
        print("\n跨合约调用原生合约方法做erc20代币转账，转账数额非正整数")
        self.transfer_use(self.testNest, input) 
    
    #跨合约调用原生合约方法做erc20代币余额查询，查询不存在的账户
    @pytest.mark.abnormal
    def test_case14(self, input):
        print("\n跨合约调用原生合约方法做erc20代币余额查询，查询不存在的账户")
        self.balanceOf(self.testNest, input)

    #int数据类型的增删改查,传入非法int
    @pytest.mark.abnormal
    def test_case15(self, input):
        print("\nint数据类型的增删改查,传入非法int")
        value = ["-57896044618658097711785492504343953926634992332820282019728792003956564819968",\
            "57896044618658097711785492504343953926634992332820282019728792003956564819968"]
        for v in value:
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setInt", json.dumps({"x": str(v)}))
            assert err != 0 and "value to large for int256" in result
        value = ["aaa", "!"]
        for v in value:
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setInt", json.dumps({"x": str(v)}))
            assert err != 0 and "failed to parse" in result
    
    @pytest.mark.abnormal
    def test_case16(self, input):
        print("\nint数组数据类型的增删改查,传入非法int值")
        value = ["-57896044618658097711785492504343953926634992332820282019728792003956564819968",\
            "57896044618658097711785492504343953926634992332820282019728792003956564819968"]
        for v in value:
            args = json.dumps({"x": "[" + v + "]"})
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setIntArr", args)
            assert err != 0 and "value to large for int256" in result
        value = ["aaa", "!"]
        for v in value:
            args = json.dumps({"x": "[" + v + "]"})
            err, result = input.test.xlib.InvokeContract("evm", self.cname, "setIntArr", args)
            assert err != 0 and "failed to parse" in result

    @pytest.mark.abnormal
    def test_case17(self, input):
        print("\nint数组数据类型的增删改查,传入非数组类型")
        args = json.dumps({"x": "10"})
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setIntArr", args)
        assert err != 0 and "argument 0 should be array or slice" in result
       
    #address数据类型的增删改查，传入非数组
    @pytest.mark.abnormal
    def test_case18(self, input):
        print("\naddress数组数据类型的增删改查，传入非数组")
        invokeArgs = "3131313231313131313131313131313131313133"
        args = json.dumps({"x":invokeArgs})
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setAddrArr", args)
        assert err != 0 and "argument 0 should be array or slice" in result

    #address数据类型的增删改查，传入非数组
    @pytest.mark.abnormal
    def test_case19(self, input):
        print("\naddress数组数据类型的增删改查，传入非法address")
        invokeArgs = [                      
                      "[1,]",
                      "1",
                      "[-10]",
                      "[aaa]",
                      "[!@#$%^&]"
                    ]
        for a in invokeArgs:
            err, _ = input.test.xlib.InvokeContract("evm", self.cname, "setAddrArr", a)
            assert err != 0
       
    @pytest.mark.abnormal
    def test_case20(self, input):
        print("\nbytes32数据类型的增删改查,传入非法bytes32") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytesAuto", json.dumps({"x":\
                "0x111"}))
        assert err != 0 and "cannot map from" in result

    @pytest.mark.abnormal
    def test_case21(self, input):
        print("\nbytes32数据类型的增删改查,传入非法bytes32,值是2个byte32") 
        err, result = input.test.xlib.InvokeContract("evm", self.cname, "setBytes", json.dumps({"x":\
                "0xe4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd\
e4d1c5c1b7273da2a327d26541fb3e99a9a53923ae3dae0103ef8516554099bd"}))
        assert err != 0 and "byte to long for bytes32" in result
