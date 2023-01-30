"""
说明：poa, xpoa用例执行前的准备工作
"""
import numpy as np
import pytest
import json
import os

# 为后面的测试准备，合约账户的创建
class TestBasic:

    #查询共识状态测试
    @pytest.mark.p2
    def test_consensusStatus(self, input):
        """
        查询共识状态测试
        """
        err, result = input.test.xlib.ConsensusStatus(host=input.host)
        assert err == 0, "查询共识状态失败： " + result
    
    #查询Poa共识信息
    @pytest.mark.p2
    def test_getValidates(self, input):
        err, result = input.test.GetValidates(host=input.conf.default_host)
        assert err == 0, "查询Poa共识信息失败： " + result

    # 构建一个node1， node2， node3的合约账户, akWeight分配
    @pytest.mark.p2
    def test_case01(self, input):
        addrs = input.acc123["addrs"]
        account_name = input.acc123["account_name"]
        acl_account = input.acc123["acl_account"]

        #设置合约账户的acl
        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 0.5
            },
            "aksWeight": {
            }
        }

        #如果需要设成其他的ak，在这里做修改
        acl["aksWeight"][addrs[0]] = 0.3
        acl["aksWeight"][addrs[1]] = 0.4
        acl["aksWeight"][addrs[2]] = 0.3

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        #编辑合约账户描述文件
        #用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
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
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        #转账给刚刚创建的合约账户
        amount="10000000000"
        key = "data/keys"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount, key=key)
        assert err == 0, "给合约账户转账失败"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    # 构建一个node1，node2的合约账户，每个账户ak为0.5，value要求为0.8
    @pytest.mark.p2
    def test_case02(self, input):
        addrs = input.acc12["addrs"]
        account_name = input.acc12["account_name"]
        acl_account = input.acc12["acl_account"]

        #设置合约账户的acl
        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 0.8
            },
            "aksWeight": {
            }
        }

        #如果需要设成其他的ak，在这里做修改
        for ad in addrs:
            acl["aksWeight"][ad] = 0.5

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        #编辑合约账户描述文件
        #用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
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
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        #转账给刚刚创建的合约账户
        amount="10000000000"
        key = "data/keys"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount, key=key)
        assert err == 0, "给合约账户转账失败"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    # 构建一个node2，node3的合约账户，每个账户ak为0.5，value要求为0.8
    @pytest.mark.p2
    def test_case03(self, input):
        addrs = input.acc23["addrs"]
        account_name = input.acc23["account_name"]
        acl_account = input.acc23["acl_account"]

        #设置合约账户的acl
        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 0.8
            },
            "aksWeight": {
            }
        }

        #如果需要设成其他的ak，在这里做修改
        for ad in addrs:
            acl["aksWeight"][ad] = 0.5

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        #编辑合约账户描述文件
        #用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
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
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        #转账给刚刚创建的合约账户
        amount="10000000000"
        key = "data/keys"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount, key=key)
        assert err == 0, "给合约账户转账失败"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    # 构建一个node1，node3的合约账户，每个账户ak为0.5，value要求为0.8
    @pytest.mark.p2
    def test_case04(self, input):
        addrs = input.acc13["addrs"]
        account_name = input.acc13["account_name"]
        acl_account = input.acc13["acl_account"]
        
        #设置合约账户的acl
        acl = {
            "pm": {
                "rule": 1,
                "acceptValue": 0.8
            },
            "aksWeight": {
            }
        }

        #如果需要设成其他的ak，在这里做修改
        for ad in addrs:
            acl["aksWeight"][ad] = 0.5

        #由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        #编辑合约账户描述文件
        #用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
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
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        #转账给刚刚创建的合约账户
        amount="10000000000"
        key = "data/keys"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount, key=key)
        assert err == 0, "给合约账户转账失败"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    # 构建一个只有node1的合约账户，使用快速创建的方式
    @pytest.mark.p2
    def test_case05(self, input):

        account_name = input.acc11["account_name"]
        acl_account = input.acc11["acl_account"]

        #创建合约账户测试
        err, result = input.test.xlib.CreateContractAccount(account=account_name, keys="data/keys")
        assert err == 0 or "already exists" in result, result
        
        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result

        #转账给刚刚创建的合约账户
        amount="10000000000"
        key = "data/keys"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount, key=key)
        assert err == 0, "给合约账户转账失败"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    # 构建一个只有node3的合约账户，使用快速创建的方式
    @pytest.mark.p2
    def test_case06(self, input):
        # 给node3转账
        err, result = input.test.xlib.Transfer(to=input.node3, amount="1000")
        assert err == 0, "给合约账户转账失败"
        
        account_name = input.acc33["account_name"]
        acl_account = input.acc33["acl_account"]

        #创建合约账户测试
        err, result = input.test.xlib.CreateContractAccount(account=account_name, keys=input.key3)
        assert err == 0 or "already exists" in result, result

        if err == 0:
            #等tx上链
            txid = input.test.xlib.GetTxidFromRes(result)
            err, result = input.test.xlib.WaitTxOnChain(txid)
            assert err == 0, result
                
        #转账给刚刚创建的合约账户
        amount="10000000000"
        key = "data/keys"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount, key=key)
        assert err == 0, "给合约账户转账失败"

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"