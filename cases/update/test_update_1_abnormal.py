"""
说明：共识升级的异常场景
"""
import json
import pytest
import time
import os

class TestUpdateConErr:

    # 【异常】向低版本升级
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n【异常】向低版本升级")
        validator = input.addrs
        err, version, _ = input.test.update.updateConsensus("tdpos", validator, version="0")
        assert err == 0, "提案和投票失败：" + version

         # 15个区块后触发升级，故等20个区块
        input.test.xlib.WaitNumHeight(20)
        # 检查升级后的参数、候选人、共识名称
        
        err, result = input.test.update.checkUpdate("tdpos", validator, version)
        assert err != 0
        print(result)

    # 【异常】向同版本升级
    @pytest.mark.abnormal
    def test_case02(self, input):
        print("\n【异常】向同版本升级")
        validator = input.addrs[0]

        # 查询当前共识版本
        err, result = input.test.xlib.ConsensusStatus()
        if err != 0:
            return err, result
        result = json.loads(result)
        version = result["version"]

        err, version, _ = input.test.update.updateConsensus("single", validator, version=version)
        assert err == 0, "提案和投票失败：" + version

        # 15个区块后触发升级，故等20个区块
        input.test.xlib.WaitNumHeight(20)
        # 检查升级后的参数、候选人、共识名称
        
        err, result = input.test.update.checkUpdate("single", validator, version)
        assert err != 0
        print(result)

    # 【异常】禁止升级到pow共识
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】升级到pow共识")
        err, version, id = input.test.update.updateConsensus("pow", input.addrs)
        assert err == 0, "提案和投票失败：" + version

        # 15个区块后触发升级，故等20个区块
        input.test.xlib.WaitNumHeight(20)

        # 提案状态预期是completed_failure
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "completed_failure" in result