"""
说明: 合约账户的测试用例
"""
import pytest
import os
import json
import yaml

class TestContractAccount(object):
    """
    合约账户的测试用例
    """
    alice_key = "output/data/alice"
    bob_key = "output/data/bob"
    alice_addr = ""
    bob_addr = ""

    def initAcc(self, input):
        """
        if alice or bob's key not exist, create it
        """
        err, self.alice_addr = input.test.xlib.GetAddress(self.alice_key)
        if err != 0:
            err, result = input.test.xlib.initAccount(output=self.alice_key)
            assert err == 0 or "exist" in result, "创建账户失败：" + result
        err, self.bob_addr = input.test.xlib.GetAddress(self.bob_key)
        if err != 0:
            err, result = input.test.xlib.initAccount(output=self.bob_key)
            assert err == 0 or "exist" in result, "创建账户失败：" + result

    @pytest.mark.p0   
    def test_createCA_1(self, input):
        """
        创建合约账户,单ak
        """
        print("\n1.创建合约账户,通过json文件创建,单ak")
        self.initAcc(input)
        account = "1111111111111211"
        aks=[self.alice_addr,]
        err, result = input.test.xlib.CreateContractAccount2(aks, account_name=account)
        assert err == 0 or "already exist" in result, "创建合约账户失败：" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        # 查询合约账号acl，预期只有alice addr
        account="XC" + account + "@" + input.conf.name
        err, result = input.test.xlib.QueryAcl(account=account)
        assert err == 0, "查询合约账户失败：" + result
        aksWeight = json.loads(result.strip('\nconfirmed'))["aksWeight"] 
        # 3.返回acl
        assert sorted(aksWeight) == sorted(aks), "合约账号的acl,不符合预期"

    @pytest.mark.p0   
    def test_createCA_2(self, input):
        """
        创建合约账户,多ak
        """
        print("\n【2.创建合约账户,通过json文件创建,多ak】")
        self.initAcc(input)
        account = "1111111111111212"
        aks=[self.alice_addr, self.bob_addr]
        err, result = input.test.xlib.CreateContractAccount2(aks, account_name=account)
        assert err == 0 or "already exist" in result, "创建合约账户失败：" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        # 查询合约账号acl，预期有alice 和bob addr
        account="XC" + account + "@" + input.conf.name
        err, result = input.test.xlib.QueryAcl(account=account)
        assert err == 0, "查询合约账户失败：" + result
        aksWeight = json.loads(result.strip('\nconfirmed'))["aksWeight"] 
        assert sorted(aksWeight) == sorted(aks), "合约账号的acl,不符合预期"

    @pytest.mark.p0   
    def test_createCA_3(self, input):  
        """
        创建简易合约账户
        """
        print("\n【3.创建简易合约账户】")
        account = "1111111111111213"
        aks=[input.addrs[0],]
        err, result = input.test.xlib.CreateContractAccount(account=account)
        assert err == 0 or "already exist" in result, "创建合约账户失败：" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        # 查询合约账号acl，预期只有alice addr
        account="XC" + account + "@" + input.conf.name
        err, result = input.test.xlib.QueryAcl(account=account)
        assert err == 0, "查询合约账户失败：" + result
        aksWeight = json.loads(result.strip('\nconfirmed'))["aksWeight"] 
        assert sorted(aksWeight) == sorted(aks), "合约账号的acl,不符合预期"
       
    @pytest.mark.p0    
    def test_queryCA_1(self, input):   
        """
        查询包含特定地址的合约账号列表，通过传入account
        """ 
        print("\n【4.查询包含特定地址的合约账号列表,通过address查询】")   
        self.initAcc(input)     
        err, result = input.test.xlib.QueryContactAccount(address=self.alice_addr)  
        assert err == 0, "通过address查询合约账户失败：" + result

    @pytest.mark.p0 
    def test_queryCA_2(self, input): 
        """
        查询包含特定地址的合约账号列表
        """ 
        print("\n【5.查询包含特定地址的合约账号列表,通过key查询】")        
        err, result = input.test.xlib.QueryContactAccount(keys=self.alice_key)  
        assert err == 0, "通过key查询合约账户失败：" + result


