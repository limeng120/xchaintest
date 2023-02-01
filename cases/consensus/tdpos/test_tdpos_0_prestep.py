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
import pytest


class TestBasic:
    """
    测试tdpos xpos共识的前置准备工作
    """

    @pytest.mark.p2
    def test_consensus_status(self, input_args):
        """
        查询共识状态测试
        """
        err, result = input_args.test.xlib.consensus_status()
        assert err == 0, "查询共识状态失败： " + result

    @pytest.mark.p2
    def test_get_tdpos_infos(self, input_args):
        """
        查询Tdpos共识信息
        """
        err, result = input_args.test.get_tdpos_infos()
        assert err == 0, "查询Tdpos共识信息失败： " + result

    @pytest.mark.p2
    def test_account_env(self, input_args):
        """
        为了测试tdpos共识功能的一些预部署
        """
        account_name = input_args.account_name
        acl_account = input_args.acl_account

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account2(
            input_args.addrs, account_name=account_name
        )
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(to=acl_account, amount=amount)
        assert err == 0, "给合约账户转账失败"

        # 等三个块，让合约账户和转账被确认，再执行下面的测试
        input_args.test.xlib.wait_num_height(3)

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

        input_args.test.xclient.write_addrs(input_args.acl_account, input_args.addrs)

    @pytest.mark.p2
    def test_govern_token(self, input_args):
        """
        为测试用账户，转入治理代币
        """
        acl_account = input_args.acl_account

        amount = "10000000000000"

        # 初始化代币
        input_args.test.xlib.govern_token(method_type="init")

        # 查询代币
        err, result = input_args.test.xlib.govern_token(
            method_type="query", addr=input_args.node1
        )
        assert err == 0, "代币查询失败" + result

        # 代币转账(后面投票时要保证acl或address的账户拥有代币)
        # 合约账户
        err, result = input_args.test.xlib.govern_token(
            method_type="transfer", addr=acl_account, amount=amount
        )
        assert err == 0, "代币转账失败" + result
        # 各投票节点的地址账户
        for addr in input_args.addrs:
            err, result = input_args.test.xlib.govern_token(
                method_type="transfer", addr=addr, amount=amount
            )
            assert err == 0, "代币转账失败" + result
