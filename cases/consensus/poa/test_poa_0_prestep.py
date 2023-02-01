"""
说明：poa, xpoa用例执行前的准备工作
"""
import json
import os
import pytest


class TestBasic:
    """
    创建合约账户为，后面的测试准备
    """

    @pytest.mark.p2
    def test_consensus_status(self, input_args):
        """
        查询共识状态测试
        """
        err, result = input_args.test.xlib.consensus_status(host=input_args.host)
        assert err == 0, "查询共识状态失败： " + result

    @pytest.mark.p2
    def test_get_validates(self, input_args):
        """
        查询Poa共识信息
        """
        err, result = input_args.test.get_validates(host=input_args.conf.default_host)
        assert err == 0, "查询Poa共识信息失败： " + result

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        构建一个node1， node2， node3的合约账户, akWeight分配
        """
        acc = input_args.acc123
        acl_account = acc["acl_account"]

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 0.5}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        acl["aksWeight"][acc["addrs"][0]] = 0.3
        acl["aksWeight"][acc["addrs"][1]] = 0.4
        acl["aksWeight"][acc["addrs"][2]] = 0.3

        # 编辑合约账户描述文件
        # 用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        account_desc = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {"account_name": acc["account_name"], "acl": json.dumps(acl)},
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "account.desc")
        with open(desc, "w") as new_account_file:
            json.dump(account_desc, new_account_file)
            new_account_file.close()

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account(desc="account.desc")
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(
            to=acl_account, amount=amount, key="data/keys"
        )
        assert err == 0, "给合约账户转账失败"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        构建一个node1，node2的合约账户，每个账户ak为0.5，value要求为0.8
        """
        acc = input_args.acc12
        acl_account = acc["acl_account"]

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 0.8}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        for addr in acc["addrs"]:
            acl["aksWeight"][addr] = 0.5

        # 编辑合约账户描述文件
        # 用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        account_desc = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {"account_name": acc["account_name"], "acl": json.dumps(acl)},
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "account.desc")
        with open(desc, "w") as new_account_file:
            json.dump(account_desc, new_account_file)
            new_account_file.close()

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account(desc="account.desc")
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(
            to=acl_account, amount=amount, key="data/keys"
        )
        assert err == 0, "给合约账户转账失败"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        构建一个node2，node3的合约账户，每个账户ak为0.5，value要求为0.8
        """
        acc = input_args.acc23
        acl_account = acc["acl_account"]

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 0.8}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        for addr in acc["addrs"]:
            acl["aksWeight"][addr] = 0.5

        # 编辑合约账户描述文件
        # 用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        account_desc = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {"account_name": acc["account_name"], "acl": json.dumps(acl)},
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "account.desc")
        with open(desc, "w") as desc_file:
            json.dump(account_desc, desc_file)
            desc_file.close()

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account(desc="account.desc")
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"
        key = "data/keys"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(
            to=acl_account, amount=amount, key=key
        )
        assert err == 0, "给合约账户转账失败"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        构建一个node1，node3的合约账户，每个账户ak为0.5，value要求为0.8
        """
        acc = input_args.acc13
        acl_account = acc["acl_account"]

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 0.8}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        for addr in acc["addrs"]:
            acl["aksWeight"][addr] = 0.5

        # 编辑合约账户描述文件
        # 用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        account_desc = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {"account_name": acc["account_name"], "acl": json.dumps(acl)},
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "account.desc")
        with open(desc, "w") as desc_file:
            json.dump(account_desc, desc_file)
            desc_file.close()

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account(desc="account.desc")
        assert err == 0 or "already exists" in result, "创建合约账户失败" + result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"
        key = "data/keys"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(
            to=acl_account, amount=amount, key=key
        )
        assert err == 0, "给合约账户转账失败"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        构建一个只有node1的合约账户，使用快速创建的方式
        """
        acc = input_args.acc11
        acl_account = acc["acl_account"]

        # 创建合约账户测试
        err, result = input_args.test.xlib.create_contract_account(
            account=acc["account_name"], keys="data/keys"
        )
        assert err == 0 or "already exists" in result, result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(
            to=acl_account, amount=amount, key="data/keys"
        )
        assert err == 0, "给合约账户转账失败"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        构建一个只有node3的合约账户，使用快速创建的方式
        """
        acc = input_args.acc33
        acl_account = acc["acl_account"]
        # 给node3转账
        err, result = input_args.test.xlib.transfer(to=input_args.node3, amount="1000")
        assert err == 0, "给合约账户转账失败"

        # 创建合约账户测试
        err, result = input_args.test.xlib.create_contract_account(
            account=acc["account_name"], keys=input_args.key3
        )
        assert err == 0 or "already exists" in result, result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 转账给刚刚创建的合约账户
        amount = "10000000000"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        origin_balance = int(result)

        err, result = input_args.test.xlib.transfer(
            to=acl_account, amount=amount, key="data/keys"
        )
        assert err == 0, "给合约账户转账失败"

        # 查询
        err, result = input_args.test.xlib.get_balance(account=acl_account)
        assert origin_balance + int(amount) == int(result), "转账后金额不符合要求"
