"""
说明: 合约方法权限的异常测试用例
"""
import json
import os
import pytest


class TestContractAclErr:
    """
    合约方法权限的异常测试用例
    """

    account = "2111111111111112"
    # 合约调用
    cname = "gn_MultiSign"

    @pytest.mark.abnormal
    def test_update_acl1(self, input_args):
        """
        修改账户acl, 合约名不存在
        """
        print("\n【异常】修改账户acl, 合约名不存在，修改失败")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        # 设置合约账户的acl
        addr = input_args.addrs[2]
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
                "contract_name": "go_natCon_err",
                "method_name": "increase",
                "acl": acl_str,
            },
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "set.desc")
        with open(desc, "w") as set_acl_file:
            json.dump(set_desc, set_acl_file)
            set_acl_file.close()

        # 修改合约方法的acl
        err, result = input_args.test.xlib.multi_sign_tx(
            desc="set.desc",
            acl_account=account,
            keys=input_args.keys,
            addrs=input_args.addrs,
        )
        assert err != 0, "修改method acl成功，不合预期" + result
        msg = "ACL not enough"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_update_acl2(self, input_args):
        """
        修改账户acl, 合约方法不存在
        """
        print("\n修改账户acl, 合约方法不存在，可以成功")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        # 设置合约账户的acl
        addr = input_args.addrs[2]
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
                "method_name": "XincreaseX",
                "acl": acl_str,
            },
        }

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(input_args.conf.client_path, "set.desc")
        with open(desc, "w") as desc_file:
            json.dump(set_desc, desc_file)
            desc_file.close()

        # 修改合约方法的acl
        err, result = input_args.test.xlib.multi_sign_tx(
            desc="set.desc",
            acl_account=account,
            keys=input_args.keys,
            addrs=input_args.addrs,
        )
        assert err == 0, result
        # msg = "ACL not enough"
        # assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_update_acl3(self, input_args):
        """
        修改账户acl, 发起人不是部署合约的合约账号
        """
        print("\n【异常】修改账户acl, 发起人不是部署合约的合约账号，修改失败")
        # 合约账号的acl是node1 node2
        account = "XC" + self.account + "@" + input_args.conf.name

        # 设置合约账户的acl
        addr = input_args.addrs[2]
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
        with open(desc, "w") as desc_file:
            json.dump(set_desc, desc_file)
            desc_file.close()

        # 修改合约方法的acl
        account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.multi_sign_tx(
            desc="set.desc",
            acl_account=account,
            keys=input_args.keys,
            addrs=input_args.addrs,
        )
        assert err != 0, "修改method acl成功，不合预期" + result
        msg1 = "ACL not enough"
        msg2 = "the signature is invalid"
        assert msg1 in result or msg2 in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_invoke(self, input_args):
        """
        合约increase方法的acl是node3，node1无权限调用increase方法，调用失败
        """
        print("\n【异常】合约increase方法的acl是node3，node1无权限调用increase方法，调用失败")
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "increase", args, keys=input_args.keys[0]
        )
        assert err != 0, "合约调用成功，不合预期： " + result
        msg = "ACL not enough"
        assert msg in result, "报错信息错误"
