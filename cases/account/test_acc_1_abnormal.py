"""
说明: 账户相关的异常测试用例
"""
import pytest
import os
import json

class TestAccountErr(object):
    """
    账户相关的异常测试用例
    """
    @pytest.mark.abnormal
    def test_createAccount_1(self, input): 
        """
        助记词，生成私钥无效不存在
        """
        print("\n【异常】通过助记词生成私钥,助记词无效不存在")   
        mnemonic = "\"spare ready law cotton mean license lend orphan decorate network infant camera\""
        err, result = input.test.xlib.RetrieveAccount(mnemonic=mnemonic, lang="en")
        assert err != 0, "根据助记词还原账户成功，不合预期： " + result
        msg = "The checksum within the Mnemonic sentence incorrect"
        assert msg in result, "报错信息错误" 

    @pytest.mark.abnormal
    def test_createAccount_2(self, input):     
        """
        助记词，生成私钥英文在中文环境下/中文在英文环境下执行导致
        """
        print("\n【异常】通过助记词生成私钥,英文在中文环境下/中文在英文环境下执行导致")   
        mnemonic = "\"olive detect whip impact fog seminar bicycle science \
            melody sausage lake lemon will ribbon unfold wall wrap loop\""
        err, result = input.test.xlib.RetrieveAccount(mnemonic=mnemonic, lang="zh")
        assert err != 0, "根据助记词还原账户成功，不合预期： " + result
        msg = "Mnemonic word [olive] is not valid"
        assert msg in result, "报错信息错误" 

    @pytest.mark.abnormal
    def test_createAccount_3(self, input):
        """
        助记词，没有用""包围
        """
        print("\n【异常】通过助记词生成私钥,助记词没有用""包围")    
        mnemonic = "course chef year noodle dumb safe curve gap huge van equal camera"
        err, result = input.test.xlib.RetrieveAccount(mnemonic=mnemonic, lang="zh")
        assert err != 0, "根据助记词还原账户成功，不合预期： " + result
        msg = "The number of words in the Mnemonic sentence is not valid"
        assert msg in result, "报错信息错误" 

    @pytest.mark.abnormal
    def test_createAccount_4(self, input):  
        """
        输出目录存在，失败
        """
        print("\n【异常】通过助记词生成私钥,输出目录存在，中止")  
        output = "./output/data/zhangwei9"
        input.test.xlib.sh.exec_shell(input.test.conf.client_path, "mkdir -p " + output)
        if input.conf.crypto == "gm":
            mnemonic =  "\"hunt absent wedding upon close execute find length payment member addict double\""
        else:
            mnemonic =  "\"course chef year noodle dumb safe curve gap huge van equal camera\""
        err, result = input.test.xlib.RetrieveAccount(mnemonic=mnemonic, lang="en", output=output)
        assert err != 0, "根据助记词还原账户成功，不合预期： " + result   
        msg = "output directory exists, abort"
        assert msg in result, "报错信息错误" 