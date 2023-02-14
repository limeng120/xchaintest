"""
说明: 测试java合约sdk
"""
import json
import pytest


class TestCall:
    """
    测试java合约sdk
    """

    c1File = "javaTemplate/c1-0.1.0-jar-with-dependencies.jar"
    c2File = "javaTemplate/c2-0.1.0-jar-with-dependencies.jar"
    c1name = "callc1"
    c2name = "callc2"
    test_befor = ""

    def trans_use(self, account, amount, input_args):
        """
        转账
        """
        # 1.查询账户余额
        err, befor_account = input_args.test.xlib.get_balance(account=account)
        assert err == 0, "查询" + account + "余额 失败" + befor_account
        # 2.先给合约账户转账
        err, result = input_args.test.xlib.transfer(to=account, amount=amount)
        assert err == 0 and result != "Select utxo error", "转账给合约账户 失败： " + result
        # 3.查询转账后的账户余额
        err, after_account = input_args.test.xlib.get_balance(account=account)
        assert err == 0, "查询" + account + "余额 失败" + after_account
        assert int(after_account) == int(befor_account) + int(amount)

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case01(self, input_args):
        """
        部署callc1 callc2合约
        """
        print("\n合约部署callc1 callc2合约")
        account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.deploy_contract(
            "native", "java", self.c1name, self.c1File, account, "None"
        )
        assert err == 0 or "exist" in result, "部署" + self.c1name + "合约失败： " + result
        err, result = input_args.test.xlib.deploy_contract(
            "native", "java", self.c2name, self.c2File, account, "None"
        )
        assert err == 0 or "exist" in result, "部署" + self.c2name + "合约失败： " + result

    @pytest.mark.skip("虚拟机部署native合约会超时")
    def test_case02(self, input_args):
        """
        给合约callc1 callc2充值，调用callc1合约invoke方法，实现跨合约调用
        """
        print("\n调用callc1合约invoke方法，实现跨合约调用")
        self.trans_use(self.c1name, 1, input_args)
        self.trans_use(self.c2name, 1000, input_args)

        print("\n 调用callc1合约invoke方法，实现跨合约调用")
        err, self.test_befor = input_args.test.xlib.get_balance(account="test")
        invoke_args = {"to": "test"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.c1name, "invoke", args, fee=30
        )
        assert err == 0, "调用callc1合约invoke方法，实现跨合约调用 失败" + result

        err, c1_balance = input_args.test.xlib.get_balance(account=self.c1name)
        assert err == 0, "查询" + self.c1name + "余额 失败" + c1_balance
        assert c1_balance == "0", self.c1name + "账户不为0 " + c1_balance

        err, c2_balance = input_args.test.xlib.get_balance(account=self.c2name)
        assert err == 0, "查询" + self.c1name + "余额 失败" + c2_balance
        assert c2_balance == "0", self.c2name + "账户不为0 " + c2_balance

        err, test_after = input_args.test.xlib.get_balance(account="test")
        assert err == 0, "查询" + self.c1name + "余额 失败" + test_after
        assert int(test_after) == int(self.test_befor) + int(1001), (
            "test账户余额没有增加, 失败" + test_after
        )
