"""
说明: 测试创建平行链的异常场景
"""
import json
import pytest
import time
import os

class TestCreateChainErr:

    # case01 创建平行链 name设为""
    @pytest.mark.abnormal
    def test_case01(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("pow", "")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "block chain name is empty"
        assert msg in result, "报错信息错误"
    
    # case02 创建同名平行链
    @pytest.mark.abnormal
    def test_case02(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("single", "hisingle1")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "blockchain exist"
        assert msg in result, "报错信息错误"

    # case03 创建名为xuper的平行链
    @pytest.mark.abnormal
    def test_case03(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("tdpos", "xuper")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "blockchain exist"
        assert msg in result, "报错信息错误"

    # case04 创建平行链带群组时，群组的name与链名不一致
    @pytest.mark.abnormal
    def test_case04(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("xpos", "badch", group=True, group_name="test")
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "group name should be same with the parachain name"
        assert msg in result, "报错信息错误"

    # case05 创建同名平行链带群组 
    @pytest.mark.abnormal
    def test_case05(self, input):
        err, chain_conf = input.test.pchain.GenChainConf("poa", "hipoa1", group=True)
        assert err == 0, "生成链配置失败：" + chain_conf
        err, result = input.test.pchain.CreateChain(chain_conf)
        assert err != 0, "创建平行链成功，不合预期：" + result
        msg = "blockchain exist"
        assert msg in result, "报错信息错误"

    # # case06 创建平行链，name为特殊字符
    # # Todo: 当前成功，需修改
    # @pytest.mark.abnormal
    # def test_case06(self, input):
    #     err, chain_conf = input.test.pchain.GenChainConf("xpoa", "!@#$%^&*()<>:qwe,,...//??")
    #     assert err == 0, "生成链配置失败：" + chain_conf
    #     err, result = input.test.pchain.CreateChain(chain_conf)
    #     assert err != 0, "创建平行链成功，不合预期：" + result