"""
说明：测试治理代币
"""
import json
import pytest
import time
import os

class TestGToken:

    alice_key = "output/data/alice"

    # 初始化代币
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n初始化代币")
        err, result = input.test.xlib.GovernToken(type="init")
        assert err == 0 or "Govern tokens has been initialized" in result, "初始化治理代币失败： " + result

    # 代币转账
    @pytest.mark.p2
    def test_case02(self, input):
        print("\n代币转账")
        err, alice_addr = input.test.xlib.GetAddress(self.alice_key)

        err, balance1 = input.test.xlib.GetTotalToken(addr=alice_addr)
        if err != 0:
            balance1 = 0
        
        err, result = input.test.xlib.GovernToken(type="transfer", addr=alice_addr, amount="1")
        assert err == 0, "代币转账失败:" + result

        err, balance2 = input.test.xlib.GetTotalToken(addr=alice_addr)
        assert err == 0, "代币查询失败"
        assert int(balance1) + 1 == int(balance2)
       
    # 【异常】重复初始化代币
    @pytest.mark.abnormal
    def test_case03(self, input):
        print("\n【异常】重复初始化代币")
        err, result = input.test.xlib.GovernToken(type="init")
        assert err != 0, result

    # 【异常】转账金额超过余额
    @pytest.mark.abnormal
    def test_case04(self, input):
        print("\n【异常】转账金额超过余额")
        err, alice_addr = input.test.xlib.GetAddress(self.alice_key)
        err, balance1 = input.test.xlib.GetTotalToken(addr=alice_addr)

        amount = str(int(balance1) + 1)
        err, result = input.test.xlib.GovernToken(type="transfer", addr=input.node1, amount=amount, key=self.alice_key)
        assert err != 0, result
        assert "sender's insufficient balance" in result, "报错信息错误"

    # 转账金额等于余额
    @pytest.mark.p2
    def test_case05(self, input):
        print("\n转账金额等于余额")
        _, alice_addr = input.test.xlib.GetAddress(self.alice_key)
        err, balance1 = input.test.xlib.GetTotalToken(addr=alice_addr)
        amount = str(balance1)

        # 给alice转账xuper，转代币需要gas
        err, result = input.test.xlib.Transfer(to=alice_addr, amount=1)
        assert err == 0, result

        err, result = input.test.xlib.GovernToken(type="transfer", \
            addr=input.node1, amount=amount, key=self.alice_key)
        assert err == 0, result

    # 转账金额等于0
    @pytest.mark.p2
    def test_case06(self, input):
        print("\n转账金额等于0")
        err, result = input.test.xlib.GovernToken(type="transfer", addr=input.node1, amount="0")
        assert err == 0, "代币转账失败:" + result

    # 【异常】转账：代币数为浮点类型
    @pytest.mark.abnormal
    def test_case07(self, input):
        print("\n【异常】转账：代币数为浮点类型")
        err, result = input.test.xlib.GovernToken(type="transfer", \
            addr=input.node1, amount="1.0")
        assert err != 0, result
    
    # 【异常】转账：代币数为负数
    @pytest.mark.abnormal
    def test_case08(self, input):
        print("\n【异常】转账：代币数为负数")
        err, result = input.test.xlib.GovernToken(type="transfer", \
            addr=input.node1, amount="-1")
        assert err != 0, result

    # 【异常】转账：代币数为字符串
    @pytest.mark.abnormal
    def test_case09(self, input):
        print("\n【异常】转账：代币数为字符串")
        err, result = input.test.xlib.GovernToken(type="transfer", \
            addr=input.node1, amount="aaa")
        assert err != 0, result

    # 【异常】转账：代币数为特殊字符
    @pytest.mark.abnormal
    def test_case10(self, input):
        print("\n【异常】转账：代币数为特殊字符")
        err, result = input.test.xlib.GovernToken(type="transfer", \
            addr=input.node1, amount="!!!")
        assert err != 0, result

    # 查询账户的代币余额
    @pytest.mark.p2
    def test_case11(self, input):
        print("\n查询账户的代币余额")
        err, result = input.test.xlib.GovernToken(type="query", \
            addr=input.node1)
        assert err == 0, result

    # 【异常】查询没有代币的账户的代币余额
    @pytest.mark.abnormal
    def test_case12(self, input):
        print("\n查询没有代币的账户的代币余额")
        err, result = input.test.xlib.GovernToken(type="query", \
            addr="aaa")
        assert err != 0, result