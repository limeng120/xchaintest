"""
说明: 测试cpp合约sdk
"""
import json
import pytest
import time
import os



class TestFeatures1():

    file = "cppTemplate/features.wasm"
    cname = "features"

    widthCount = "".zfill(1024)

    # 合约部署features合约
    @pytest.mark.p2
    def test_case01(self, input):
        print("部署features合约") 
        contract_account = "XC" + input.account + "@" + input.conf.name             
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)  
        err, result = input.test.xlib.DeployContract("wasm", "cpp", self.cname, self.file, contract_account, args)
        assert err == 0 or "exist" in result, "部署features合约失败： " + result
  
    #调put方法,写入1个kv，记录个数
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n调put方法,写入1个kv")
        invokeArgs = {
            "key": "test1",
            "value":"value1"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法,写入1个kv 失败" + result 
           
    
    #调get方法,查询1个kv，记录个数
    @pytest.mark.p2
    def test_case03(self, input):
        print("\n调get方法,查询210个kv")
        invokeArgs = {
            "key": "test1"
            }
        args = json.dumps(invokeArgs)            
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,查询1个kv 失败" + result     
    
    #调put方法，写入key长度1k,value长度1K
    @pytest.mark.p2
    def test_case04(self, input):
        print("\n调put方法,key长度1k,value长度1k")
        invokeArgs = {
            "key": "test" + self.widthCount,
            "value": "value" + self.widthCount
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法：key和value长度1K, 失败" + result 
    
    #调get方法，key长度1k,value长度1K
    @pytest.mark.p2
    def test_case05(self, input):
        print("\n调get方法,key长度1k,value长度1K")
        invokeArgs = {
            "key": "test" + self.widthCount
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,key和value长度1k 失败" + result 
        #value值长度是1024
        assert "value" + self.widthCount in result
    
    #调put方法，写入key长度1k
    @pytest.mark.p2
    def test_case06(self, input):
        print("\n调put方法,key长度1k")
        invokeArgs = {
            "key": "admin" + self.widthCount,
            "value": "adminvalue"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法：key长度1K, 失败" + result 
    
    #调get方法，key长度1k
    @pytest.mark.p2
    def test_case07(self, input):
        print("\n调get方法,key长度1k")
        invokeArgs = {
            "key": "admin" + self.widthCount
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,key长度1k 失败" + result 

    #调put方法，写入value长度1k
    @pytest.mark.p2
    def test_case08(self, input):
        print("\n调put方法,value长度1k")
        invokeArgs = {
            "key": "case1",
            "value": "lkvalue" + self.widthCount
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法,vaue长度1k 失败" + result 
    
    #调get方法,查询value长度1k
    @pytest.mark.p2
    def test_case09(self, input):
        print("\n调get方法,value长度1k")
        invokeArgs = {
            "key": "case1"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", args)
        assert err == 0, "调get方法,vaue长度1k 失败" + result 
    
    #put已经加入的值
    @pytest.mark.p2
    def test_case10(self, input):
        print("\nput已经加入的值")
        invokeArgs = {
            "key": "case1",
            "value":"qatestval1"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "put已经加入的值 失败" + result 
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", json.dumps({"key":"case1"}))
        assert err == 0 and "qatestval1" in result, "调get方法,查询已经加入的值 失败" + result 

    #调put方法,value值为" "
    @pytest.mark.p2
    def test_case11(self, input):
        print("\nput的value值为")
        invokeArgs = {
            "key": "dudu",
            "value":" "
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "put的value值为 失败" + result 
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", json.dumps({"key":"dudu"}))
        assert err == 0, "调get方法,查询已经加入的值 失败" + result 

    #调put方法,key为空字符串" "
    @pytest.mark.p2
    def test_case12(self, input):
        print("\n调put方法,key为空字符串" "")
        invokeArgs = {
            "key": " ",
            "value":"value2"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "调put方法,key为空字符串" " 失败" + result 
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", json.dumps({"key":" "}))
        assert err == 0, "调get方法,key为空字符串" " 失败" + result 

    #调get方法,key,value都为空
    @pytest.mark.p2
    def test_case13(self, input):
        print("\n调用get方法,key,value都为空")
        invokeArgs = {
            "key": " ",
            "value":" "
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "get方法,key,value都为空 失败" + result 
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", json.dumps({"key":" "}))
        assert err == 0, "调get方法,key为空失败" + result 
   
    #key,value为特殊字符
    @pytest.mark.p2
    def test_case14(self, input):
        print("\nput的key,value为特殊字符")
        invokeArgs = {
            "key": "!)(%^&*()O:@_-></!#$^",
            "value":"!@#$%^&*()_+=?><|"
            }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "put", args)
        assert err == 0, "put的key,value为特殊字符 失败" + result 
        err, result = input.test.xlib.QueryContract("native", self.cname, "get", \
              json.dumps({"key":"!)(%^&*()O:@_-></!#$^"}))
        assert err == 0, "调get方法,查询特殊字符 失败" + result 
