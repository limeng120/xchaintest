"""
说明: 查询平行链信息
"""
import json
import pytest
import time
import os

class TestQueryWithG:

    # case01 共识状态: pow共识的平行链
    @pytest.mark.p1
    def test_case01(self, input):
        err, result = input.test.xlib.ConsensusStatus(name="hipow1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "pow", "共识类别有误"
    
    # case02 共识状态: single共识的平行链
    @pytest.mark.p1
    def test_case02(self, input):
        err, result = input.test.xlib.ConsensusStatus(name="hisingle1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "single", "共识类别有误"

    # case03 共识状态: tdpos共识的平行链
    @pytest.mark.p1
    def test_case03(self, input):
        err, result = input.test.xlib.ConsensusStatus(name="hitdpos1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "tdpos", "共识类别有误"
    
    # case04 共识状态: xpos共识的平行链
    @pytest.mark.p1
    def test_case04(self, input):
        err, result = input.test.xlib.ConsensusStatus(name="hixpos1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "xpos", "共识类别有误"
    
    # case05 共识状态: poa共识的平行链
    @pytest.mark.p1
    def test_case05(self, input):
        err, result = input.test.xlib.ConsensusStatus(name="hipoa1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "poa", "共识类别有误"

    # case06 共识状态: xpoa共识的平行链
    @pytest.mark.p1
    def test_case06(self, input):
        err, result = input.test.xlib.ConsensusStatus(name="hixpoa1")
        assert err == 0, "查询链共识状态失败：" + result
        result = json.loads(result)
        assert result["consensus_name"] == "xpoa", "共识类别有误"