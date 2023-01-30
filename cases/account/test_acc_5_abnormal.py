"""
说明: evm账户的异常测试用例
"""
import pytest
import os


class TestEVMAccountErr: 
    """
    evm账户的异常测试用例
    """
    # case01 非法合约名转evm地址，合约名不足4位
    @pytest.mark.abnormal
    def test_case01(self, input): 
        print("\n非法合约账号转evm地址，合约名不足4位")
        err, result = input.test.xlib.AddrTrans("x2e", "aaa")
        assert err != 0, "非法合约账号转evm地址成功，不合预期： " + result
        msg = "is not a valid address"
        assert msg in result, "报错信息错误"

    # case02 非法合约名转evm地址，合约名超16位
    @pytest.mark.abnormal
    def test_case02(self, input): 
        print("\n非法合约账号转evm地址，合约名不足4位")
        err, result = input.test.xlib.AddrTrans("x2e", "a1234567890123456")
        assert err != 0, "非法合约账号转evm地址成功，不合预期： " + result
        msg = "is not a valid address"
        assert msg in result, "报错信息错误"

    # case03 非法合约账户转evm地址，合约账户长度15
    @pytest.mark.abnormal
    def test_case03(self, input): 
        print("\n非法合约账户转evm地址，合约账户长度15")
        ca_addr = "XC111111111111111@xuper"
        err, result = input.test.xlib.AddrTrans("x2e", ca_addr)
        assert err != 0, "非法合约账户转evm地址成功，不合预期： " + result
        msg = "is not a valid address"
        assert msg in result, "报错信息错误"

    # case04 非法合约账户转evm地址，合约账户长度17
    @pytest.mark.abnormal 
    def test_case04(self, input): 
        print("\n非法合约账户转evm地址，合约账户长度17")
        ca_addr = "XC11111111111111111@xuper"
        err, result = input.test.xlib.AddrTrans("x2e", ca_addr)
        assert err != 0, "非法合约账户转evm地址成功，不合预期： " + result
        msg = "is not a valid address"
        assert msg in result, "报错信息错误"

    # case05 非法合约账户转evm地址，合约账户包含字母、下划线
    @pytest.mark.abnormal
    def test_case05(self, input): 
        print("\n非法合约账户转evm地址，合约账户包含字母、下划线")
        ca_addr = "XC11111111111111_a@xuper"
        err, result = input.test.xlib.AddrTrans("x2e", ca_addr)
        assert err != 0, "非法合约账户转evm地址成功，不合预期： " + result
        msg = "is not a valid address"
        assert msg in result, "报错信息错误"

    # case06 非法evm地址转换，evm地址比正常值少1位
    @pytest.mark.abnormal
    def test_case06(self, input): 
        print("\n非法evm地址转换，evm地址比正常值少1位")
        evm_addr = "313131323131313131313131313131313131313"
        err, result = input.test.xlib.AddrTrans("e2x", evm_addr)
        assert err != 0, "非法evm地址转换成功，不合预期： " + result
        msg = "odd length hex string"
        assert msg in result, "报错信息错误"

    # case07 普通账户转evm地址，缺少参数
    @pytest.mark.abnormal
    def test_case07(self, input): 
        print("\n普通账户转evm地址，缺少参数")
        err, result = input.test.xlib.AddrTrans("x2e", "")
        assert err != 0, "普通账户转evm地址，缺少参数，转换成功，不合预期： " + result
        msg = "not a valid address"
        assert msg in result, "报错信息错误"
        
    # case08 evm地址转普通账户，缺少参数
    @pytest.mark.abnormal
    def test_case08(self, input): 
        print("\nevm地址转普通账户，缺少参数")
        err, result = input.test.xlib.AddrTrans("e2x", "")
        assert err != 0, "evm地址转普通账户，缺少参数，转换成功，不合预期： " + result
        msg = "go-hex: invalid byte"
        assert msg in result, "报错信息错误"