"""
说明: acl测试用例的前置步骤

"""
import os
import json
import pytest

class TestPreAcl:

    #权限用例依赖的前置步骤
    @pytest.mark.p0
    def test_preAcl(self, input, **kwargs):
        """
        运行acl用例的前置步骤：
        创建合约账户
        转账给合约账户
        部署go native合约
        """
        account = "2111111111111112"
        name = input.conf.name
        acl_account = "XC" + account + "@" + name

        file = "goTemplate/counter"
        cname = "gn_MultiSign"

        #创建合约账户
        aks = [input.conf.addrs[0], input.conf.addrs[1]]    
        err, result = input.test.xlib.CreateContractAccount2(aks, account_name=account)
        assert err == 0 or "already exists" in result, result
        
        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        # 3.检查合约账号余额，余额不足1000000000，转账
        amount=1000000000
        err, result = input.test.TranferWhenNotEnough(acl_account, amount, **kwargs)
        if err != 0:
            return err, result         
        
        input.test.xclient.WriteAddrs(acl_account, aks)               
        #多ak部署合约 
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)
        # 生成部署合约的tx
        err, result = input.test.xlib.DeployContract("native", "go", cname, file, acl_account, args, isMulti="")
        # 生成部署的tx失败，或者 合约已存在，直接返回
        if "already exists" in result:
            return 0, result
        if err != 0:
            return err, result
        # 对tx多签
        signkeys = [input.conf.keys[0], input.conf.keys[1]] 
        err, result = input.test.xlib.Multisign(keys=signkeys)
        assert err == 0, "tx多签失败： " + result
        #等tx上链
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result
