"""
说明: 测试创建平行链的异常场景
"""
import pytest


class TestCreateChainErr:
    """
    测试创建平行链的异常场景
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        创建平行链 name设为""
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf("pow", "")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "block chain name is empty"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        创建同名平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf("single", "hisingle1")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "blockchain exist"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        创建名为xuper的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf("tdpos", "xuper")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "blockchain exist"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        创建平行链带群组时，群组的name与链名不一致
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "xpos", "badch", group=True, group_name="test"
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "group name should be same with the parachain name"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        创建同名平行链带群组
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "poa", "hipoa1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "blockchain exist"
        assert msg in result, "报错信息错误"
