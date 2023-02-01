"""
说明: 测试evm合约 部署、调用、查询的异常场景
"""
import json
import pytest


class TestEVMErr:
    """
    测试evm合约 部署、调用、查询的异常场景
    """

    file = "evmTemplate/Counter.bin"
    cname = "e_counter"
    abi = "evmTemplate/Counter.abi"
    # 1个不存在的合约账户
    ca = "XC9876543210987654@xuper"
    deploy = {"creator": "abc"}

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        重复部署
        """
        print("\n重复部署")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        args = json.dumps(self.deploy)
        input_args.test.xlib.deploy_contract(
            "evm", "", self.cname, self.file, contract_account, args, abi=self.abi
        )
        err, result = input_args.test.xlib.deploy_contract(
            "evm", "", self.cname, self.file, contract_account, args, abi=self.abi
        )
        assert err != 0, "部署evm合约成功，不合预期： " + result
        msg = "already exists"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        使用普通账号部署合约
        """
        print("\n使用普通账号部署合约")
        args = json.dumps(self.deploy)
        err, address = input_args.test.xlib.get_address("data/keys")
        err, result = input_args.test.xlib.deploy_contract(
            "evm", "", self.cname + "new", self.file, address, args, abi=self.abi
        )
        assert err != 0, "部署evm合约成功，不合预期： " + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        使用不存在的合约账号，部署合约
        """
        print("\n使用不存在的合约账号，部署合约")
        args = json.dumps(self.deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "evm", "", self.cname, self.file, self.ca, args, abi=self.abi
        )
        assert err != 0, "部署evm合约成功，不合预期： " + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"
