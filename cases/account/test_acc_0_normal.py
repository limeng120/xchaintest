"""
说明: 账户相关测试用例
"""
import os
import pytest


class TestAccount:
    """
    账户相关测试用例
    """

    @pytest.mark.p0
    def test_acc1(self, input_args):
        """
        助记词强度:低
        """
        input_args.test.sh.exec_shell(input_args.conf.client_path, "rm -rf output")
        print("\n创建账户,中文助记词,助记词强度:低")
        output = "./output/data/zhangwei"
        err, result = input_args.test.xlib.create_account(
            output=output, lang="zh", strength="1"
        )
        assert err == 0, "创建账户失败：" + result

    @pytest.mark.p0
    def test_acc2(self, input_args):
        """
        助记词强度:中
        """
        print("\n创建账户,中文助记词,助记词强度:中")
        output = "./output/data/zhangwei2"
        err, result = input_args.test.xlib.create_account(
            output=output, lang="zh", strength="2"
        )
        assert err == 0, "创建账户失败： " + result

    @pytest.mark.p0
    def test_acc3(self, input_args):
        """
        助记词强度:高
        """
        print("\n创建账户,中文助记词,助记词强度:高")
        output = "./output/data/zhangwei3"
        err, result = input_args.test.xlib.create_account(
            output=output, lang="zh", strength="3"
        )
        assert err == 0, "创建账户失败： " + result

    @pytest.mark.p0
    def test_acc4(self, input_args):
        """
        助记词强度:低
        """
        print("\n创建账户,英文助记词,助记词强度:低")
        output = "./output/data/alice"
        err, result = input_args.test.xlib.create_account(
            output=output, lang="en", strength="1"
        )
        assert err == 0, "创建账户失败： " + result

    @pytest.mark.p0
    def test_acc5(self, input_args):
        """
        助记词强度:中
        """
        print("\n创建账户,英文助记词,助记词强度:中")
        output = "./output/data/alice2"
        err, result = input_args.test.xlib.create_account(
            output=output, lang="en", strength="2"
        )
        assert err == 0, "创建账户失败： " + result

    @pytest.mark.p0
    def test_acc6(self, input_args):
        """
        助记词强度:高
        """
        print("\n创建账户,英文助记词,助记词强度:高")
        output = "./output/data/alice3"
        err, result = input_args.test.xlib.create_account(
            output=output, lang="en", strength="3"
        )
        assert err == 0, "创建账户失败： " + result

    @pytest.mark.p0
    def test_acc7(self, input_args):
        """
        创建账户,不带助记词
        """
        print("\n创建账户,不带助记词")
        output = "./output/data/bob"
        err, result = input_args.test.xlib.create_account(output=output)
        assert err == 0, "创建账户失败： " + result

    @pytest.mark.p0
    def test_acc8(self, input_args):
        """
        强制覆盖已有密钥
        """
        output = "./output/data/alice4"
        abs_path = os.path.join(input_args.test.conf.client_path, output)
        # 第1次创建
        err, result = input_args.test.xlib.create_account(output=output)
        assert err == 0, "创建账户失败： " + result
        # 记录当前address
        err, address = input_args.test.sh.exec_shell(abs_path, "cat address")
        # 第2次创建，覆盖已有key
        err, result = input_args.test.xlib.create_account(force="", output=output)
        assert err == 0, "创建账户失败： " + result
        err, address2 = input_args.test.sh.exec_shell(abs_path, "cat address")
        assert address != address2, "覆盖创建account，操作前后address没改变"

    @pytest.mark.p0
    def test_acc9(self, input_args):
        """
        英文助记词
        """
        print("\n通过助记词生成私钥,英文助记词")
        if input_args.conf.crypto == "":
            # 非国密
            mnemonic = (
                '"course chef year noodle dumb safe curve gap huge van equal camera"'
            )
            address = "kxngcZC9vUgiM4bEHZh4pWDqFpSDWvw7L"
        else:
            # 国密
            mnemonic = '"hunt absent wedding upon close execute find length payment member addict double"'
            address = "tzWaB41mPduVL6jNioREZme5ZEPYj8Kqm"
        err, result = input_args.test.xlib.retrieve_account(
            mnemonic=mnemonic, lang="en"
        )
        assert err == 0, "根据助记词还原账户失败： " + result

        address2 = result.split(":")[1].split("\n")[0].replace(" ", "")
        assert address == address2, "根据助记词还原的address错误"

    @pytest.mark.p0
    def test_acc10(self, input_args):
        """
        通过助记词生成私钥,英文，输出指定输出目录
        """
        print("\n通过助记词生成私钥,英文助记词,指定输出目录")
        output = "./output/data/lucy9"
        if input_args.conf.crypto == "":
            # 非国密
            mnemonic = (
                '"course chef year noodle dumb safe curve gap huge van equal camera"'
            )
            address = "kxngcZC9vUgiM4bEHZh4pWDqFpSDWvw7L"
        else:
            # 国密
            mnemonic = '"hunt absent wedding upon close execute find length payment member addict double"'
            address = "tzWaB41mPduVL6jNioREZme5ZEPYj8Kqm"
        err, result = input_args.test.xlib.retrieve_account(
            mnemonic=mnemonic, lang="en", output=output
        )
        assert err == 0, "根据助记词还原账户失败： " + result

        abs_path = os.path.join(input_args.test.conf.client_path, output)
        err, address2 = input_args.test.sh.exec_shell(abs_path, "cat address")
        assert address == address2, "根据助记词还原的address错误"
