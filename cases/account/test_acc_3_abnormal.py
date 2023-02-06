"""
说明: 合约账户的异常测试用例
"""

import os
import json
import pytest


class TestCAErr:
    """
    合约账户的异常测试用例
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        合约账户名字超过16位
        """
        print("\n【异常】创建合约账户,合约账户名字超过16位")
        account = "1111111111111112222222"
        err, result = input_args.test.xlib.create_contract_account(account=account)
        assert err != 0, "创建合约账户成功，不合预期：" + result
        msg = "invoke NewAccount failed, account number length expect 16, actual: 22"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        合约账户名字不足16位
        """
        print("\n【异常】创建合约账户,合约账户名字不足16位")
        account = "111111111111"
        err, result = input_args.test.xlib.create_contract_account(account=account)
        assert err != 0, "创建合约账户成功，不合预期：" + result
        msg = "invoke NewAccount failed, account number length expect 16, actual: 12"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        合约账户名字不是纯数字
        """
        print("\n【异常】创建合约账户,合约账户名字不是纯数字")
        account = "test111111111111"
        err, result = input_args.test.xlib.create_contract_account(account=account)
        assert err != 0, "创建合约账户成功，不合预期：" + result
        msg = "expect continuous 16 digits"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        json文件配置有误
        """
        print("\n【异常】创建合约账户,json文件配置有误")
        # 1.获取data/keys/address
        err, address = input_args.test.xlib.get_address("./data/keys")
        assert err == 0, "获取address失败：" + address
        # 2.修改account.json文件ak
        basic_accountconf = {
            "module_name": "xkernel",
            "method_name": "NewAccount",
            "contract_name": "$acl",
            "args": {
                "account_name": "9111111111111111",
                "acl": '{"pm": {"rule": 1,"acceptValue": 0.6},"Weight": "'
                + address
                + '": 0.6}',
            },
        }

        accfile = "output/account.json"
        desc = os.path.join(input_args.test.conf.client_path, accfile)
        if not os.path.exists(desc):
            file2 = open(desc, mode="a", encoding="UTF-8")
            file2.close()
        with open(desc, "w") as desc_file:
            json.dump(basic_accountconf, desc_file)
            desc_file.close()
        # 3.执行创建账户命令
        err, result = input_args.test.xlib.create_contract_account(desc=accfile)
        assert err != 0, "创建合约账户成功，不合预期：" + result
        msg = "unmarshal args acl error"
        assert msg in result, "报错信息错误"
