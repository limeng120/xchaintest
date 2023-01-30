"""
说明：发起提案返失败的case，正常用例在升级case中已验证。
"""
import json
import pytest
import time
import os

class TestProposeErr:

    # 【异常】min_vote_percent设为50
    @pytest.mark.abnormal
    def test_case01(self, input):
        print("\n【异常】min_vote_percent设为50")
        validator = input.addrs
        err, version = input.test.update.genConsJson("tdpos", validator, percent="50")
        assert err == 0, version
        err, result = input.test.update.proposeUpdate()
        assert err != 0 and "min_vote_percent err" in result, result
        
    # 【异常】 stop_vote_height 小于当前区块高度
    @pytest.mark.abnormal
    def test_case02(self, input):
        print("\n【异常】stop_vote_height 小于当前区块高度")
        validator = input.addrs
        err, version = input.test.update.genConsJson("tdpos", validator, stop_vote_height="1")
        assert err == 0, version
        err, result = input.test.update.proposeUpdate()
        assert err != 0, result
        assert "stop voting height must be larger than current trunk height" in result 
        
    # 【异常】 stop_vote_height 大于trigger
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】stop_vote_height 大于trigger")
        validator = input.addrs
        # 获取当前区块高度
        err, height = input.test.xlib.QueryBlockHeight()
        assert err == 0, height
        stop = int(height) + 20
        trigger = int(height) + 10
        
        err, version = input.test.update.genConsJson("tdpos", validator, \
        stop_vote_height=stop, trigger_height=trigger)
        assert err == 0, version
        err, result = input.test.update.proposeUpdate()
        assert err != 0, result
        assert "trigger_height must be bigger than stop_vote_height" in result, result