"""
说明：停用平行链群组的异常场景
"""
import pytest


class TestStopChainErr:
    """
    停用平行链群组的异常场景
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        普通节点无停用权限"
        """
        print("\n 普通节点停用权限，非admin节点")
        output = "./output/data/alice"
        input_args.test.xlib.create_account(output=output, lang="en", strength="1")
        err, result = input_args.test.pchain.stop_chain(
            name="hixpoa1", keys="output/data/alice"
        )
        assert err != 0, "非admin节点停用链成功，不符合预期：" + result
        msg = "invoke failed+unAuthorized"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        停用name为空字符串的链
        """
        print("\n停用name为空字符串的链")
        err, result = input_args.test.pchain.stop_chain(name="")
        assert err != 0, "停用name为空字符串的链成功，不符合预期：" + result
        msg = "chain name is empty"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        停用不存在的链
        """
        print("\n停用不存在的链")
        err, result = input_args.test.pchain.stop_chain(name="notexit")
        assert err != 0, "停用不存在的链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        停用xuper链
        """
        print("\n停用xuper链")
        err, result = input_args.test.pchain.stop_chain(name="xuper")
        assert err != 0, "停用xuper链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"
