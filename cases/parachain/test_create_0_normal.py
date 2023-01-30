"""
说明: 测试创建平行链
"""
import json
import pytest
import time
import os

class TestCreateChain:

    # case01 创建pow共识的平行链
    @pytest.mark.p1
    def test_case01(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("pow", "hipow1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err == 0, "创建平行链失败：" + result
    
    # case02 创建single共识的平行链
    @pytest.mark.p1
    def test_case02(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("single", "hisingle1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    # case03 创建tdpos共识的平行链
    @pytest.mark.p1
    def test_case03(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("tdpos", "hitdpos1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err == 0, "创建平行链失败：" + result
    
    # case04 创建xpos共识的平行链
    @pytest.mark.p1
    def test_case04(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("xpos", "hixpos1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    # case05 创建poa共识的平行链
    @pytest.mark.p1
    def test_case05(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("poa", "hipoa1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err == 0, "创建平行链失败：" + result

    # case06 创建xpoa共识的平行链
    @pytest.mark.p1
    def test_case06(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("xpoa", "hixpoa1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err == 0, "创建平行链失败：" + result
        input.test.xlib.WaitNumHeight(5)

    