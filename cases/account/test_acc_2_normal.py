"""
说明: 合约账户的测试用例
"""
import json
import pytest


class TestContractAccount:
    """
    合约账户的测试用例
    """

    alice_key = "output/data/alice"
    bob_key = "output/data/bob"
    alice_addr = ""
    bob_addr = ""

    def init_acc(self, input_args):
        """
        if alice or bob's key not exist, create it
        """
        err, self.alice_addr = input_args.test.xlib.get_address(self.alice_key)
        if err != 0:
            err, result = input_args.test.xlib.initAccount(output=self.alice_key)
            assert err == 0 or "exist" in result, "创建账户失败：" + result
        err, self.bob_addr = input_args.test.xlib.get_address(self.bob_key)
        if err != 0:
            err, result = input_args.test.xlib.initAccount(output=self.bob_key)
            assert err == 0 or "exist" in result, "创建账户失败：" + result

    @pytest.mark.p0
    def test_case01(self, input_args):
        """
        创建合约账户,单ak
        """
        print("\n1.创建合约账户,通过json文件创建,单ak")
        self.init_acc(input_args)
        account = "1111111111111211"
        aks = [
            self.alice_addr,
        ]
        err, result = input_args.test.xlib.create_contract_account2(
            aks, account_name=account
        )
        assert err == 0 or "already exist" in result, "创建合约账户失败：" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 查询合约账号acl，预期只有alice addr
        account = "XC" + account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.query_acl(account=account)
        assert err == 0, "查询合约账户失败：" + result
        aks_weight = json.loads(result.strip("\nconfirmed"))["aksWeight"]
        # 3.返回acl
        assert sorted(aks_weight) == sorted(aks), "合约账号的acl,不符合预期"

    @pytest.mark.p0
    def test_case02(self, input_args):
        """
        创建合约账户,多ak
        """
        print("\n【2.创建合约账户,通过json文件创建,多ak】")
        self.init_acc(input_args)
        account = "1111111111111212"
        aks = [self.alice_addr, self.bob_addr]
        err, result = input_args.test.xlib.create_contract_account2(
            aks, account_name=account
        )
        assert err == 0 or "already exist" in result, "创建合约账户失败：" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 查询合约账号acl，预期有alice 和bob addr
        account = "XC" + account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.query_acl(account=account)
        assert err == 0, "查询合约账户失败：" + result
        aks_weight = json.loads(result.strip("\nconfirmed"))["aksWeight"]
        assert sorted(aks_weight) == sorted(aks), "合约账号的acl,不符合预期"

    @pytest.mark.p0
    def test_case03(self, input_args):
        """
        创建简易合约账户
        """
        print("\n【3.创建简易合约账户】")
        account = "1111111111111213"
        aks = [
            input_args.addrs[0],
        ]
        err, result = input_args.test.xlib.create_contract_account(account=account)
        assert err == 0 or "already exist" in result, "创建合约账户失败：" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 查询合约账号acl，预期只有alice addr
        account = "XC" + account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.query_acl(account=account)
        assert err == 0, "查询合约账户失败：" + result
        aks_weight = json.loads(result.strip("\nconfirmed"))["aksWeight"]
        assert sorted(aks_weight) == sorted(aks), "合约账号的acl,不符合预期"

    @pytest.mark.p0
    def test_case04(self, input_args):
        """
        查询包含特定地址的合约账号列表，通过传入account
        """
        print("\n【4.查询包含特定地址的合约账号列表,通过address查询】")
        self.init_acc(input_args)
        err, result = input_args.test.xlib.query_contact_account(
            address=self.alice_addr
        )
        assert err == 0, "通过address查询合约账户失败：" + result

    @pytest.mark.p0
    def test_case05(self, input_args):
        """
        查询包含特定地址的合约账号列表
        """
        print("\n【5.查询包含特定地址的合约账号列表,通过key查询】")
        err, result = input_args.test.xlib.query_contact_account(keys=self.alice_key)
        assert err == 0, "通过key查询合约账户失败：" + result
