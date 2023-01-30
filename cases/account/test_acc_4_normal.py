"""
说明: evm账户的测试用例
"""
import pytest
import os


class TestEVMAccount: 
    """
    evm账户的测试用例
    """
    addr = "jjjKPPGeqYkFxYp2zCP17o8AdWwAXBk6q"
    evm_addr = "D4CA13E87044275C8BA7A7217286868E2C2F357A"
    ca_addr = "XC1111111111111112@xuper"
    ca_evm_addr = "3131313231313131313131313131313131313132"
    cname = "storagetest"
    evm_cname = "313131312D2D2D2D2D73746F7261676574657374"
    cname4 = "test"
    evm_cname4 = "313131312D2D2D2D2D2D2D2D2D2D2D2D74657374"
    cname16 = "test012345678901"
    evm_cname16 = "3131313174657374303132333435363738393031"
    
    # case01 普通地址转evm地址
    @pytest.mark.p0
    def test_case01(self, input): 
        err, result = input.test.xlib.AddrTrans("x2e", self.addr)
        assert err == 0, "普通地址转evm地址失败： " + result
        address = result.split()[1]
        assert address == self.evm_addr, "地址转换结果不合预期"

    # case02 evm地址转普通地址
    @pytest.mark.p0
    def test_case02(self, input): 
        err, result = input.test.xlib.AddrTrans("e2x", self.evm_addr)
        assert err == 0, "evm地址转普通地址失败： " + result
        address = result.split()[1]
        assert address == self.addr, "地址转换结果不合预期"

    # case03 合约账户转evm地址
    @pytest.mark.p0
    def test_case03(self, input): 
        err, result = input.test.xlib.AddrTrans("x2e", self.ca_addr)
        assert err == 0, "合约账户转evm地址失败： " + result
        address = result.split()[1]
        assert address == self.ca_evm_addr, "地址转换结果不合预期"

    # case04 evm地址转合约账户
    @pytest.mark.p0
    def test_case04(self, input): 
        err, result = input.test.xlib.AddrTrans("e2x", self.ca_evm_addr)
        assert err == 0, "evm地址转合约账户失败： " + result
        address = result.split()[1]
        assert address in self.ca_addr, "地址转换结果不合预期"

    # case05 合约名转evm地址
    @pytest.mark.p0
    def test_case05(self, input): 
        err, result = input.test.xlib.AddrTrans("x2e", self.cname)
        assert err == 0, "合约名转evm地址失败： " + result
        address = result.split()[1]
        assert address == self.evm_cname, "地址转换结果不合预期"

    # case06 evm地址转合约名
    @pytest.mark.p0
    def test_case06(self, input): 
        err, result = input.test.xlib.AddrTrans("e2x", self.evm_cname)
        assert err == 0, "evm地址转合约名失败： " + result
        address = result.split()[1]
        assert address == self.cname, "地址转换结果不合预期"

    # case07 合约名转evm地址，合约名长度4
    @pytest.mark.p2
    def test_case07(self, input): 
        
        err, result = input.test.xlib.AddrTrans("x2e", self.cname4)
        assert err == 0, "合约名转evm地址失败： " + result
        address = result.split()[1]
        assert address == self.evm_cname4, "地址转换结果不合预期"

    # case08 evm地址转合约名，合约名长度4
    @pytest.mark.p2
    def test_case08(self, input): 
        err, result = input.test.xlib.AddrTrans("e2x", self.evm_cname4)
        assert err == 0, "evm地址转合约名失败： " + result
        address = result.split()[1]
        assert address == self.cname4, "地址转换结果不合预期"

    # case09 合约名转evm地址，合约名长度16
    @pytest.mark.p2
    def test_case09(self, input): 
        err, result = input.test.xlib.AddrTrans("x2e", self.cname16)
        assert err == 0, "合约名转evm地址失败： " + result
        address = result.split()[1]
        assert address == self.evm_cname16, "地址转换结果不合预期"

    # case10 evm地址转合约名，合约名长度16
    @pytest.mark.p2
    def test_case10(self, input): 
        err, result = input.test.xlib.AddrTrans("e2x", self.evm_cname16)
        assert err == 0, "evm地址转合约名失败： " + result
        address = result.split()[1]
        assert address == self.cname16, "地址转换结果不合预期"
