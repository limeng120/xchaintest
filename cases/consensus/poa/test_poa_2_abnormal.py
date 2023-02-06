"""
说明：更新候选人的异常场景
"""
import json
import os
import pytest


class TestEditErr:
    """
    更新候选人的异常场景
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        【异常】初始验证集为node1，node2，变更候选人为node1，node2, node3，只有node1签名
        """
        print("\n【异常】变更候选人，签名不足1/2")
        nominates = [input_args.node1, input_args.node2]

        acl_account = input_args.acc11["acl_account"]
        addrs = input_args.acc11["addrs"]
        keys = [input_args.key1]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        【异常】合约账户acceptValue较小，不超过过半数节点的ak之和（假设当前为node1，node2）
        """
        print("\n【异常】合约账号acceptValue较小，不超过过半数节点的ak之和")
        addrs = input_args.acc123["addrs"]
        keys = input_args.acc123["keys"]
        account_name = "1111222233335555"
        acl_account = "XC" + account_name + "@" + input_args.conf.name

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 0.3}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        for addr in addrs:
            acl["aksWeight"][addr] = 0.3

        # 由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        account_desc = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {"account_name": account_name, "acl": acl_str},
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "account.desc")
        with open(desc, "w") as desc_file:
            json.dump(account_desc, desc_file)
            desc_file.close()

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account(desc="account.desc")
        assert err == 0 or "already exist" in result, "创建合约账户失败" + result

        # 等三个块，让合约账户和转账被确认，再执行下面的测试
        input_args.test.xlib.wait_num_height(3)

        # 执行修改
        nominates = [input_args.node2, input_args.node3]
        keys = [input_args.key1, input_args.key3]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】合约账户acceptValue较大，超过全部节点的ak之和（假设当前为node1，node2）
        """
        print("\n【异常】合约账户acceptValue较大，超过全部节点的ak之和")
        addrs = input_args.acc12["addrs"]
        keys = input_args.acc12["keys"]
        account_name = "1111222233336666"
        acl_account = "XC" + account_name + "@" + input_args.conf.name

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 1}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        for addr in addrs:
            acl["aksWeight"][addr] = 0.3

        # 由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        account_desc = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {"account_name": account_name, "acl": acl_str},
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "account.desc")
        with open(desc, "w") as desc_file:
            json.dump(account_desc, desc_file)
            desc_file.close()

        # 创建合约账户
        err, result = input_args.test.xlib.create_contract_account(desc="account.desc")
        assert err == 0 or "already exist" in result, "创建合约账户失败" + result

        err, result = input_args.test.xlib.transfer(to=acl_account, amount="1000")
        assert err == 0, "转账失败:" + result

        # 等三个块，让合约账户和转账被确认，再执行下面的测试
        input_args.test.xlib.wait_num_height(3)

        # 执行修改
        nominates = [input_args.node2, input_args.node3]
        keys = [input_args.key1, input_args.key3]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "the signature is invalid or not match the address" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        【异常】使用不存在的合约账户发起修改（假设当前为node1，node2）
        """
        print("\n【异常】使用不存在的合约账户发起修改")
        acl_account = "XC0000000000000000@xuper"
        nominates = [input_args.node1, input_args.node2]
        addrs = input_args.acc12["addrs"]
        keys = [input_args.key1, input_args.key3]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "xpoa query acl error. pls check" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        【异常】使用普通账户发起修改（假设当前为node1，node2）
        """
        print("\n【异常】使用普通账户发起修改")
        acl_account = input_args.node1
        nominates = [input_args.node1, input_args.node2]
        addrs = input_args.acc12["addrs"]
        keys = [input_args.key1, input_args.key2]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "xpoa query acl error. pls check" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case06(self, input_args):
        """
        【异常】验证acl的账户地址：合约账户地址包含不在验证集合的address(当前为node1，node2)
        """
        print(
            "\n【异常】验证acl的账户地址：合约账户地址包含不在验证集合的address\
            (当前为node1，node2)"
        )
        nominates = [input_args.node1, input_args.node2, input_args.node3]
        acl_account = input_args.acc123["acl_account"]
        addrs = input_args.acc123["addrs"]
        keys = [input_args.key1, input_args.key3]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case07(self, input_args):
        """
        【异常】验证acl的账户地址：合约账户地址是当前验证集的子集(当前为node1，node2)，且不满足>1/2
        """
        print(
            "\n【异常】验证acl的账户地址:合约账户地址是当前验证集的子集(当前为node1,node2),\
            且不满足>1/2"
        )
        nominates = [input_args.node1, input_args.node2, input_args.node3]

        acl_account = input_args.acc11["acl_account"]
        addrs = input_args.acc11["addrs"]
        keys = input_args.acc11["keys"]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err != 0, result
        assert "Xpoa needs valid acl account" in result, "报错信息错误"
