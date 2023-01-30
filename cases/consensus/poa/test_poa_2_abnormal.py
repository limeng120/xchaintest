"""
说明：更新候选人的异常场景
"""
import numpy as np
import pytest
import json
import os

class TestEditErr:

    # case01:【异常】初始验证集为node1，node2，变更候选人为node1，node2, node3，只有node1签名
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n【异常】变更候选人，签名不足1/2")
        nominates = [input.node1, input.node2]
        
        acl_account = input.acc11["acl_account"]
        addrs = input.acc11["addrs"]
        keys = [input.key1]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"
        
    # 【异常】合约账户acceptValue较小，不超过过半数节点的ak之和（假设当前为node1，node2）
    @pytest.mark.abnormal
    def test_case02(self, input):
        print("\n【异常】合约账号acceptValue较小，不超过过半数节点的ak之和")
        addrs = input.acc123["addrs"]
        keys = input.acc123["keys"]
        account_name = "1111222233335555"
        acl_account = "XC" + account_name + "@" + input.conf.name 

        #设置合约账户的acl
        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 0.3
            },
            "aksWeight": {
            }
        }

        #如果需要设成其他的ak，在这里做修改
        for ad in addrs:
            acl["aksWeight"][ad] = 0.3

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        account_desc = {
            "module_name": "xkernel", 
            "method_name": "NewAccount", 
            "contract_name": "$acl", 
            "args": {
                "account_name": account_name, 
                "acl": acl_str
            }
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(input.conf.client_path, "account.desc")
        with open(desc, "w") as f:
            json.dump(account_desc, f)
            f.close()

        #创建合约账户
        err, result = input.test.xlib.CreateContractAccount(desc="account.desc")
        assert err == 0 or "already exist" in result, "创建合约账户失败" + result

        # 等三个块，让合约账户和转账被确认，再执行下面的测试
        input.test.xlib.WaitNumHeight(3) 

        # 执行修改
        nominates = [input.node2, input.node3]
        keys = [input.key1, input.key3]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"

    # 【异常】合约账户acceptValue较大，超过全部节点的ak之和（假设当前为node1，node2）
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】合约账户acceptValue较大，超过全部节点的ak之和")
        addrs = input.acc12["addrs"]
        keys = input.acc12["keys"]
        account_name = "1111222233336666"
        acl_account = "XC" + account_name + "@" + input.conf.name 

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
        for ad in addrs:
            acl["aksWeight"][ad] = 0.3

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        account_desc = {
            "module_name": "xkernel", 
            "method_name": "NewAccount", 
            "contract_name": "$acl", 
            "args": {
                "account_name": account_name, 
                "acl": acl_str
            }
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(input.conf.client_path, "account.desc")
        with open(desc, "w") as f:
            json.dump(account_desc, f)
            f.close()

        #创建合约账户
        err, result = input.test.xlib.CreateContractAccount(desc="account.desc")
        assert err == 0 or "already exist" in result, "创建合约账户失败" + result
        
        err, result = input.test.xlib.Transfer(to=acl_account, amount= "1000")
        assert err == 0, "转账失败:" + result

        # 等三个块，让合约账户和转账被确认，再执行下面的测试
        input.test.xlib.WaitNumHeight(3) 

        # 执行修改
        nominates = [input.node2, input.node3]
        keys = [input.key1, input.key3]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "the signature is invalid or not match the address" in result, "报错信息错误"

    # 【异常】使用不存在的合约账户发起修改（假设当前为node1，node2）
    @pytest.mark.abnormal
    def test_case04(self, input):  
        print("\n【异常】使用不存在的合约账户发起修改")
        acl_account = "XC0000000000000000@xuper"
        nominates = [input.node1, input.node2]
        addrs = input.acc12["addrs"]
        keys = [input.key1, input.key3]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "xpoa query acl error. pls check" in result, "报错信息错误"

    # 【异常】使用普通账户发起修改（假设当前为node1，node2）
    @pytest.mark.abnormal
    def test_case05(self, input):
        print("\n【异常】使用普通账户发起修改")
        acl_account = input.node1
        nominates = [input.node1, input.node2]
        addrs = input.acc12["addrs"]
        keys = [input.key1, input.key2]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "xpoa query acl error. pls check" in result, "报错信息错误"

    # case06:【异常】验证acl的账户地址：合约账户地址包含不在验证集合的address(当前为node1，node2)
    @pytest.mark.abnormal
    def test_case06(self, input):
        print("\n【异常】验证acl的账户地址：合约账户地址包含不在验证集合的address\
            (当前为node1，node2)")
        nominates = [input.node1, input.node2, input.node3]
        acl_account = input.acc123["acl_account"]
        addrs = input.acc123["addrs"]
        keys = [input.key1, input.key3]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"
       
    # case07:【异常】验证acl的账户地址：合约账户地址是当前验证集的子集(当前为node1，node2)，且不满足>1/2
    @pytest.mark.abnormal
    def test_case07(self, input):
        print("\n【异常】验证acl的账户地址:合约账户地址是当前验证集的子集(当前为node1,node2),\
            且不满足>1/2")
        nominates = [input.node1, input.node2, input.node3]

        acl_account = input.acc11["acl_account"]
        addrs = input.acc11["addrs"]
        keys = input.acc11["keys"]

        err, result = input.test.EditValidates(nominates, acl_account, addrs, keys)
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"