"""
说明: 合约方法权限的测试用例
"""
import json
import os
import pytest


class TestContractAcl:
    """
    合约方法权限的测试用例
    """

    # 多签
    account = "2111111111111112"
    # 合约调用
    cname = "gn_MultiSign"

    @pytest.mark.p0
    def test_update_acl(self, input_args):
        """
        设置合约方法acl，ak为node2的address
        """
        print("\n设置合约方法acl，ak为node2的address")

        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name
        addr = input_args.addrs[1]
        # 设置合约账户的acl
        acl = {"pm": {"rule": 1, "acceptValue": 1}, "aksWeight": {}}

        # 如果需要设成其他的ak，在这里做修改
        acl["aksWeight"][addr] = 1

        # 由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)

        # 编辑合约账户描述文件
        # 用json.dumps直接转讲字典转换为json格式, 注意这里要用account_name，不含XC和@xuper
        set_desc = {
            "module_name": "xkernel",
            "contract_name": "$acl",
            "method_name": "SetMethodAcl",
            "args": {
                "contract_name": self.cname,
                "method_name": "increase",
                "acl": acl_str,
            },
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "set.desc")
        with open(desc, "w") as acl_set_file:
            json.dump(set_desc, acl_set_file)
            acl_set_file.close()

        # 修改合约方法的acl
        err, result = input_args.test.xlib.multi_sign_tx(
            desc="set.desc",
            acl_account=account,
            keys=input_args.keys,
            addrs=input_args.addrs,
        )
        assert err == 0, "修改合约方法acl失败" + result

        # 等tx上链
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        err, result = input_args.test.xlib.query_acl(
            contract=self.cname, method="increase"
        )
        assert err == 0, "查询合约方法acl失败：" + result
        aks_weight = json.loads(result.strip("\nconfirmed"))["aksWeight"]
        print(aks_weight)
        # 2.检查acl是否修改
        for ak, value in aks_weight.items():
            assert ak == addr and value == 1, "合约方法acl设置结果，不符合预期"

    @pytest.mark.p0
    def test_invoke(self, input_args):
        """
        调用goNative合约，node2可调用成功
        """
        print("\n调用goNative合约")
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
