"""
说明: 测试创建平行链
"""
import pytest


class TestCreateChain:
    """
    测试创建平行链
    """

    # case01
    @pytest.mark.p1
    def test_case01(self, input_args):
        """
        创建pow共识的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "pow", "hipow1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    @pytest.mark.p1
    def test_case02(self, input_args):
        """
        创建single共识的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "single", "hisingle1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    @pytest.mark.p1
    def test_case03(self, input_args):
        """
        创建tdpos共识的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "tdpos", "hitdpos1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    @pytest.mark.p1
    def test_case04(self, input_args):
        """
        创建xpos共识的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "xpos", "hixpos1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    @pytest.mark.p1
    def test_case05(self, input_args):
        """
        创建poa共识的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "poa", "hipoa1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    @pytest.mark.p1
    def test_case06(self, input_args):
        """
        创建xpoa共识的平行链
        """
        err, chain_conf = input_args.test.pchain.gen_chain_conf(
            "xpoa", "hixpoa1", group=True
        )
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input_args.test.pchain.create_chain(chain_conf)
        assert err == 0, "创建平行链失败：" + result
        input_args.test.xlib.wait_num_height(5)
