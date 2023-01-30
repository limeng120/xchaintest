"""
说明: 合约账户权限的异常测试用例
"""
import json
import time
import pytest
import os

class TestAccounAclErr(object):
    """
    合约账户权限的异常测试用例
    """
    # 合约账号的acl是node1 node2
    account = "2111111111111112" 
    #被转账者
    to_account = "XC1111111111111211@xuper"
    #合约部署，调用
    file = "goTemplate/counter"
    cname = "gn_nat_err"
  
    @pytest.mark.abnormal
    def test_transferToAccount(self, input):
        """
        多签名转账给合约账户，签名不足
        """
        print("\n【异常】多签转账，签名不足，失败")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name
        # 1. 转账，签名的账户权重不足acceptValue
        keys = [input.keys[0]]
        addrs = [input.addrs[0]]  
        err, result= input.test.xlib.MultiTransfer(signkeys=keys, addrs=addrs, 
                                        to=self.to_account, amount="100", account=account)
        assert err != 0, "多签名转账给合约账户成功，不合预期： " + result 
        msg = "the signature is invalid or not match the address"
        assert msg in result, "报错信息错误" 
    
    @pytest.mark.abnormal
    def test_transferNOAddr(self, input):
        """
        多签名转账给合约账户，data/acl/addrs配置错误
        """
        print("\n【异常】多签名转账给合约账户，data/acl/addrs配置错误")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name
        keys = [input.keys[0], input.keys[1]]
        addrs = ["123"]  

        # 1.转账
        err, result= input.test.xlib.MultiTransfer(signkeys=keys, addrs=addrs, 
                                        to=self.to_account, amount="100", account=account)        
        assert err != 0, "签名无效，多签名转账成功，不合预期： " + result 
        msg = "the signature is invalid or not match the address"
        assert msg in result, "报错信息错误" 

    @pytest.mark.abnormal
    def test_Deploy(self, input):
        """
        部署goNative合约，签名不足
        """
        print("\n【异常】部署goNative合约，签名不足")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name
        deploy = {
            "creator": "abc"
        }
        args = json.dumps(deploy)
        keys = [input.keys[0]]
        addrs = [input.addrs[0]]
        input.test.xclient.WriteAddrs(account, addrs)
        err, result = input.test.xlib.DeployContract("native", "go", self.cname, 
                           self.file, account, args, isMulti="")
        err, result = input.test.xlib.Multisign(keys=keys)
        assert err != 0, "部署go native合约成功，不合预期： " + result
        msg = "the signature is invalid or not match the address"
        assert msg in result, "报错信息错误" 
    
    @pytest.mark.abnormal
    def test_Invoke(self, input):
        """
        调用goNative合约，签名无效
        """
        print("\n【异常】调用goNative合约，签名无效")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name
        invokeArgs = {
            "key": "dudu"
        }
        args = json.dumps(invokeArgs)
        keys = [input.keys[0]]
        addrs = [input.addrs[0]]
        input.test.xclient.WriteAddrs(account, addrs)
        err, result = input.test.xlib.InvokeContract("native", self.cname, "increase", 
                                    args, isMulti="", account=account)
        err, result = input.test.xlib.Multisign(keys=keys)
        assert err != 0, "调用go native合约失败： " + result
        msg = "the signature is invalid or not match the address"
        assert msg in result, "报错信息错误" 

    @pytest.mark.abnormal
    def test_UpdateACL_1(self, input):
        """
        修改acl失败，签名无效
        """
        print("\n【异常】修改合约账号的acl，签名无效")

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
        acls = [input.addrs[0]]
        for ad in acls:
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
        err, result = input.test.xlib.MultiSignTX(desc="set.desc", acl_account=account,
                     keys=[input.keys[0]], addrs=[input.addrs[0]])
        assert err != 0, "修改合约账户失败" + result
        msg = "the signature is invalid or not match the address"
        assert msg in result, "报错信息错误"   
    
    @pytest.mark.abnormal
    def test_UpdateACL_2(self, input, **kwargs):
        """
        修改acl失败，合约账号不存在
        """
        print("\n【异常】修改不存在合约账号的acl")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input.conf.name

        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 1
            },
            "aksWeight": {
            }
        }
        acls = [input.addrs[0]]
        #如果需要设成其他的ak，在这里做修改
        for ad in acls:
            acl["aksWeight"][ad] = 1

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        #编辑合约账户描述文件
        #用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        set_desc = {
            "module_name": "xkernel", 
            "contract_name": "$acl",
            "method_name": "SetAccountAcl",
            "args": {
                "account_name": "XC111119876511112@xuper", 
                "acl": acl_str
            }
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(input.conf.client_path, "set.desc")
        with open(desc, "w") as f:
            json.dump(set_desc, f)
            f.close()

        #修改合约账户
        err, result = input.test.xlib.MultiSignTX(desc="set.desc", acl_account=account,
                     keys=[input.keys[0], input.keys[1]], addrs=[input.addrs[0], input.addrs[1]])
        assert err != 0, "修改合约账户失败" + result
        msg = "invoke failed+Key not found"
        assert msg in result, "报错信息错误" 

