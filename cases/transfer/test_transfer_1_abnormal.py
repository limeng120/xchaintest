"""
说明: 转账的异常场景
"""
import pytest


class TestTransferErr:
    """
    转账的异常场景
    """

    alice_key = "output/data/alice"
    alice_addr = ""

    def init_acc(self, input_args):
        """
        if alice or bob's key not exist, create it
        """
        _, self.alice_addr = input_args.test.xlib.get_address(self.alice_key)

    @pytest.mark.abnormal
    def test_create_account1(self, input_args):
        """
        转账为负数
        """
        print("\n【异常】转账金额为负数")
        self.init_acc(input_args)
        err, result = input_args.test.xlib.transfer(to=self.alice_addr, amount="-100")
        assert err != 0, "转账金额为负数，不合预期：" + result
        msg = "Amount in transaction can not be negative number"
        assert msg in result, "报错消息错误"

    @pytest.mark.abnormal
    def test_create_account2(self, input_args):
        """
        转账为小数
        """
        print("\n【异常】转账金额为小数")
        self.init_acc(input_args)
        err, result = input_args.test.xlib.transfer(to=self.alice_addr, amount="1.25")
        assert err != 0, "转账金额为小数，不合预期：" + result
        msg = "Invalid amount number"
        assert msg in result, "报错消息错误"

    @pytest.mark.abnormal
    def test_create_account3(self, input_args):
        """
        转账为0，有币环境报错，无币化环境转账成功
        """
        print("\n【异常】转账金额为0")
        self.init_acc(input_args)
        err, result = input_args.test.xlib.transfer(to=self.alice_addr, amount="0")
        if input_args.conf.nofee:
            assert err == 0, "无币化环境，转账金额为0，失败，不合预期:" + result
        else:
            assert err != 0, "转账金额为0，不合预期：" + result
            msg = "Err:500-50403-tx not enough"
            assert msg in result, "报错消息错误"

    @pytest.mark.abnormal
    def test_create_account4(self, input_args):
        """
        转账金额超出余额
        """
        print("\n【异常】转账金额超出余额")
        self.init_acc(input_args)
        err, result = input_args.test.xlib.transfer(
            to=self.alice_addr,
            amount="10000000000000000000000000000000",
            keys="./output/data/bob/",
        )
        assert err != 0, "转账金额超出余额，不合预期：" + result
        msg = "Select utxo error"
        assert msg in result, "报错消息错误"

    @pytest.mark.abnormal
    def test_create_account5(self, input_args):
        """
        转账者账户不存在
        """
        print("\n【异常】转账者账户不存在")
        err, result = input_args.test.xlib.transfer(
            to="XC1119991817716611@xuper", amount="10", keys="./output/data/bob123/"
        )
        assert err != 0, "转账者账户不存在，不合预期：" + result
        msg = "open output/data/bob123/address: no such file or directory"
        assert msg in result, "报错消息错误"

    @pytest.mark.abnormal
    def test_create_account6(self, input_args):
        """
        账户中使用冻结余额转账
        """
        print("\n【异常】账户中使用冻结余额转账")
        self.init_acc(input_args)
        err, result = input_args.test.xlib.transfer(
            to=self.alice_addr, amount="100000000000000", keys="./output/data/alice2/"
        )
        assert err != 0, "使用冻结余额转账，不合预期：" + result
        msg = "Select utxo error"
        assert msg in result, "报错消息错误"
