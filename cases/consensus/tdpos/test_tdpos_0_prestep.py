"""
说明：测试tdpos xpos共识的前置准备工作
1. 账户的基本准备：
    创建了合约账户（由3个节点的账户组成）
    给合约账户转账
    在data/acl/addrs文件中写入合约账户的地址信息
2. 代币的初始化：
    代币初始化及异常情况
    为合约账户及其对应的账户分配代币
"""
import os
import json
import pytest

class TestBasic:

    #查询共识状态测试
    @pytest.mark.p2
    def test_consensusStatus(self, input):
        """
        查询共识状态测试
        """
        err, result = input.test.xlib.ConsensusStatus()
        assert err == 0, "查询共识状态失败： " + result

    #查询Tdpos共识信息
    @pytest.mark.p2
    def test_getTdposInfos(self, input):
        err, result = input.test.GetTdposInfos()
        assert err == 0, "查询Tdpos共识信息失败： " + result
        
    # 创建合约账户
    @pytest.mark.p2
    def test_accountEnv(self, input):
        """
        为了测试tdpos共识功能的一些预部署
        """
        account_name = input.account_name
        acl_account = input.acl_account

        #创建合约账户
        err, result = input.test.xlib.CreateContractAccount2(input.addrs, account_name=account_name)
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        #转账给刚刚创建的合约账户
        amount = "10000000000"
        
        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        origin_balance = int(result)

        err, result = input.test.xlib.Transfer(to=acl_account, amount=amount)
        assert err == 0, "给合约账户转账失败"

        # 等三个块，让合约账户和转账被确认，再执行下面的测试
        input.test.xlib.WaitNumHeight(3)

        #查询
        err, result = input.test.xlib.Balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

        input.test.xclient.WriteAddrs(input.acl_account, input.addrs)
            
    #初始化代币，为pos case所需的账户转入治理代币
    @pytest.mark.p2
    def test_governToken(self, input):
        """
        为测试用账户，转入治理代币
        """
        acl_account = input.acl_account

        amount = "10000000000000"

        # 初始化代币
        input.test.xlib.GovernToken(type="init")

        # 查询代币
        err, result = input.test.xlib.GovernToken(type="query", addr=input.node1)
        assert err == 0, "代币查询失败" + result

        # 代币转账(后面投票时要保证acl或address的账户拥有代币)
        # 合约账户
        err, result = input.test.xlib.GovernToken(type="transfer", addr=acl_account, amount=amount)
        assert err == 0, "代币转账失败" + result
        # 各投票节点的地址账户
        for a in input.addrs:
            err, result = input.test.xlib.GovernToken(type="transfer", addr=a, amount=amount)
            assert err == 0, "代币转账失败" + result
