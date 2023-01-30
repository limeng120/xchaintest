"""
说明: 测试go合约 部署、调用、查询、升级的异常场景
"""
import json
import pytest
import time

class TestGoNative():

    file = "goTemplate/counter"
    cname = "gn_counter"
    # 1个不存在的合约账户
    ca = "XC9876543210987654@xuper"
    deploy = {"creator": "abc"}

    @pytest.mark.abnormal
    def test_case01(self, input):        
        """
        重复部署
        """    
        print("\n重复部署") 
        contract_account = "XC" + input.account + "@" + input.conf.name
        args = json.dumps(self.deploy)
        err, result = input.test.xlib.DeployContract("native", "go", self.cname, self.file, contract_account, args)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "already exists"
        assert msg in result, "报错信息错误"
  
    @pytest.mark.abnormal
    def test_case02(self, input):
        """使用普通账号部署合约"""
        print("\n使用普通账号部署合约") 
        args = json.dumps(self.deploy)
        err, address = input.test.xlib.GetAddress("data/keys")
        err, result = input.test.xlib.DeployContract("native", "go", self.cname, self.file, address, args)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "Key not found"   
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input):
        """使用不存在的合约账号，部署合约"""
        print("\n使用不存在的合约账号，部署合约") 
        args = json.dumps(self.deploy)
        err, result = input.test.xlib.DeployContract("native", "go", self.cname, self.file, self.ca, args)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input):
        """升级合约，用非部署账号"""
        print("\n升级合约，用非部署账号") 
        err, result = input.test.xlib.UpgradeContract("native", self.cname, self.file, self.ca)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "verify contract owner permission failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input):
        """升级合约，用部署账号对应的普通账号"""
        print("\n升级合约，用部署账号对应的普通账号") 
        err, address = input.test.xlib.GetAddress("data/keys")
        err, result = input.test.xlib.UpgradeContract("native", self.cname, self.file, address)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "verify contract owner permission failed"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case06(self, input):
        """升级不存在的合约"""
        print("\n升级不存在的合约")
        contract_account = "XC" + input.account + "@" + input.conf.name
        err, result = input.test.xlib.UpgradeContract("native", self.cname + "err", self.file, contract_account)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "contract for account not confirmed"
        assert msg in result, "报错信息错误"
