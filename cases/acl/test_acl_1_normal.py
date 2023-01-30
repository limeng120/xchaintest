"""
说明: 合约账户权限的测试用例
"""
import json
import time
import pytest
import os

class TestAccounAcl(object):
    """
    合约账户权限的测试用例
    """
    # 合约账号的acl是node1 node2
    account = "2111111111111112"

    #被转账者
    to_account = "XC1111111111111211@xuper" 
    #合约调用
    cname = "gn_MultiSign"

    @pytest.mark.p0
    def test_transferToAddress(self, input):
        """
        多签名转账给普通账户
        """
        print("\n多签名转账给普通账户")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name

        #1.获取账户address, node3的address
        to_addr = input.addrs[2]
        # 2.查询被转账 账户 和 合约账户余额
        err, befor_balan = input.test.xlib.Balance(account=to_addr)
        #3.转账   
        keys = [input.keys[0], input.keys[1]] 
        addrs = [input.addrs[0], input.addrs[1]]   
        err, result= input.test.xlib.MultiTransfer(signkeys=keys, addrs=addrs, 
                                   to=to_addr, amount="200", account=account)
        assert err == 0, "转账给合约账户 失败： " + result
        #4.检查被转账余额
        err, after_balan = input.test.xlib.Balance(account=to_addr)
        assert int(after_balan) == int(befor_balan) + int(200), "转账给合约账户 失败： " + result

    @pytest.mark.p0
    def test_transferToAccount(self, input):
        """
        多签名转账给合约账户
        """
        print("\n多签名转账给合约账户")

        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name
        
        # 1.转账接收人地址是个acl账户
        to_addr = self.to_account
        # 2.查询被转账 账户余额
        err, befor_balan = input.test.xlib.Balance(account=to_addr)
        # 3.转账
        keys = [input.keys[0], input.keys[1]] 
        addrs = [input.addrs[0], input.addrs[1]]   
        err, result= input.test.xlib.MultiTransfer(signkeys=keys, addrs=addrs, 
                                   to=to_addr, amount="100", account=account)
        assert err == 0, "转账给合约账户 失败： " + result
        # 4.检查被转账余额
        err, after_balan = input.test.xlib.Balance(account=to_addr)
        assert int(after_balan) == int(befor_balan) + int(100), "转账给合约账户 失败： " + result

    @pytest.mark.p0
    def test_invoke(self, input, **kwargs):
        """
        调用goNative合约
        """
        print("\n调用goNative合约")
        # node3调用increase
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "increase", 
                                    args, keys=input.keys[1])
        assert err == 0, "调用go native合约失败： " + result
        
        #等tx上链
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

        # 合约账号调用get
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name

        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        signkeys = [input.keys[0], input.keys[1]] 
        addrs = [input.addrs[0], input.addrs[1]]  
        input.test.xclient.WriteAddrs(account, addrs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "get", 
                                    args, isMulti="", account=account)
        err, result = input.test.xlib.Multisign(keys=signkeys)
        assert err == 0, "调用go native合约失败： " + result
        
        #等tx上链
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result
   
    @pytest.mark.p0
    def test_updateACL(self, input, **kwargs):
        """
        修改账户acl
        """
        print("\n修改账户acl")

        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name

        #设置合约账户的acl
        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 1
            },
            "aksWeight": {
            }
        }
        #如果需要设成其他的ak，在这里做修改
        for ad in input.addrs:
            acl["aksWeight"][ad] = 0.6

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)
        #编辑合约账户描述文件
        #用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        set_desc = {
            "module_name": "xkernel", 
            "contract_name": "$acl",
            "method_name": "SetAccountAcl",
            "args": {
                "account_name": account, 
                "acl": acl_str
            }
        }
        #创建一个临时文件来保存desc文件
        desc = os.path.join(input.conf.client_path, "set.desc")
        with open(desc, "w") as f:
            json.dump(set_desc, f)
            f.close()

        #修改合约账户
        signkeys=[input.keys[0], input.keys[1]]
        addrs=[input.addrs[0], input.addrs[1]]

        err, result = input.test.xlib.MultiSignTX(desc="set.desc", acl_account=account,
                     keys=signkeys, addrs=addrs)
        assert err == 0, "修改合约账户失败" + result

        #等tx上链
        txid = input.test.xlib.GetTxidFromRes(result)
        err, result = input.test.xlib.WaitTxOnChain(txid)
        assert err == 0, result

        err, result = input.test.xlib.QueryAcl(account=account)
        assert err == 0, "查询合约账户acl失败：" + result  
        aksWeight = json.loads(result.strip('\nconfirmed'))["aksWeight"] 
        # 3.返回acl
        for key, value in aksWeight.items():
            assert value == acl["aksWeight"][key], "合约账号的acl修改结果,不符合预期"

