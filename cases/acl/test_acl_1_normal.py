"""
说明: 合约账户权限的测试用例
"""
import json
import os
import pytest


class TestAccounAcl:
    """
    合约账户权限的测试用例
    """

    # 合约账号的acl是node1 node2
    account = "2111111111111112"

    # 被转账者
    to_account = "XC1111111111111211@xuper"
    # 合约调用
    cname = "gn_MultiSign"

    @pytest.mark.p0
    def test_transfer1(self, input_args):
        """
        多签名转账给普通账户
        """
        print("\n多签名转账给普通账户")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        # 1.获取账户address, node3的address
        to_addr = input_args.addrs[2]
        # 2.查询被转账 账户 和 合约账户余额
        err, befor_balan = input_args.test.xlib.get_balance(account=to_addr)
        # 3.转账
        keys = [input_args.keys[0], input_args.keys[1]]
        addrs = [input_args.addrs[0], input_args.addrs[1]]
        err, result = input_args.test.xlib.multi_transfer(
            signkeys=keys, addrs=addrs, to=to_addr, amount="200", account=account
        )
        assert err == 0, "转账给合约账户 失败： " + result
        # 4.检查被转账余额
        err, after_balan = input_args.test.xlib.get_balance(account=to_addr)
        assert int(after_balan) == int(befor_balan) + int(200), "转账给合约账户 失败： " + result

    @pytest.mark.p0
    def test_transfer2(self, input_args):
        """
        多签名转账给合约账户
        """
        print("\n多签名转账给合约账户")

        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        # 1.转账接收人地址是个acl账户
        to_addr = self.to_account
        # 2.查询被转账 账户余额
        err, befor_balan = input_args.test.xlib.get_balance(account=to_addr)
        # 3.转账
        keys = [input_args.keys[0], input_args.keys[1]]
        addrs = [input_args.addrs[0], input_args.addrs[1]]
        err, result = input_args.test.xlib.multi_transfer(
            signkeys=keys, addrs=addrs, to=to_addr, amount="100", account=account
        )
        assert err == 0, "转账给合约账户 失败： " + result
        # 4.检查被转账余额
        err, after_balan = input_args.test.xlib.get_balance(account=to_addr)
        assert int(after_balan) == int(befor_balan) + int(100), "转账给合约账户 失败： " + result

    @pytest.mark.p0
    def test_invoke(self, input_args):
        """
        调用goNative合约
        """
        print("\n调用goNative合约")
        # node3调用increase
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "increase", args, keys=input_args.keys[1]
        )
        assert err == 0, "调用go native合约失败： " + result

        # 等tx上链
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        # 合约账号调用get
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        signkeys = [input_args.keys[0], input_args.keys[1]]
        addrs = [input_args.addrs[0], input_args.addrs[1]]
        input_args.test.xclient.write_addrs(account, addrs)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "get", args, isMulti="", account=account
        )
        err, result = input_args.test.xlib.multi_sign(keys=signkeys)
        assert err == 0, "调用go native合约失败： " + result

        # 等tx上链
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

    @pytest.mark.p0
    def test_update_acl(self, input_args):
        """
        修改账户acl
        """
        print("\n修改账户acl")

        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 1}, "aksWeight": {}}
        # 如果需要设成其他的ak，在这里做修改
        for addr in input_args.addrs:
            acl["aksWeight"][addr] = 0.6

        # 编辑合约账户描述文件
        # 用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        set_desc = {
            "module_name": "xkernel",
            "contract_name": "$acl",
            "method_name": "SetAccountAcl",
            "args": {"account_name": account, "acl": json.dumps(acl)},
        }
        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "set.desc")
        with open(desc, "w") as set_acl_file:
            json.dump(set_desc, set_acl_file)
            set_acl_file.close()

        # 修改合约账户
        err, result = input_args.test.xlib.multi_sign_tx(
            desc="set.desc",
            acl_account=account,
            keys=[input_args.keys[0], input_args.keys[1]],
            addrs=[input_args.addrs[0], input_args.addrs[1]],
        )
        assert err == 0, "修改合约账户失败" + result

        # 等tx上链
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        err, result = input_args.test.xlib.query_acl(account=account)
        assert err == 0, "查询合约账户acl失败：" + result
        aks_weight = json.loads(result.strip("\nconfirmed"))["aksWeight"]
        # 3.返回acl
        for key, value in aks_weight.items():
            assert value == acl["aksWeight"][key], "合约账号的acl修改结果,不符合预期"
