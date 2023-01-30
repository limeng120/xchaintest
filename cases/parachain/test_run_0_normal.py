"""
说明: 测试平行链上执行基本功能：转账、创建合约账户、合约部署调用升级
"""
import json
import pytest
import time
import os

class TestChainBasic:

    def basic(self, input, name):
        print(name + "共识的平行链，执行基本功能")
        # 最多失败重试3次
        for i in range(3):
            err, result = input.test.BasicFunction(name=name)
            if err == 0:
                break
        assert err == 0, name + "平行链上，基本功能执行失败：" + result

    # # case01 pow共识的平行链，执行基本功能
    # @pytest.mark.p1
    # def test_case01(self, input):
    #     self.basic(input, name="hipow1")
            
    # case02 创建single共识的平行链
    @pytest.mark.p1
    def test_case02(self, input):
        self.basic(input, name="hisingle1")
       
    # case03 创建tdpos共识的平行链
    @pytest.mark.p1
    def test_case03(self, input):
        self.basic(input, name="hitdpos1")
    
    # case04 创建xpos共识的平行链
    @pytest.mark.p1
    def test_case04(self, input):
        self.basic(input, name="hixpos1")

    # case05 创建poa共识的平行链
    @pytest.mark.p1
    def test_case05(self, input):
        self.basic(input, name="hipoa1")

    # case06 创建xpoa共识的平行链
    @pytest.mark.p1
    def test_case06(self, input):
        self.basic(input, name="hixpoa1")
