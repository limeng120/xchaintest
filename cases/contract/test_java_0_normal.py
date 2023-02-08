"""
说明: 测试java native合约 部署、调用、查询、升级
"""
import json
import time
import pytest


class TestJavaNative:
    """
    测试java native合约 部署、调用、查询、升级
    """

    file = "javaTemplate/counter-0.1.0-jar-with-dependencies.jar"
    cname = "java_counter"

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case01(self, input_args):
        """
        部署java合约
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        deploy = {"creator": "abc"}
        args = json.dumps(deploy)
        err, result = input_args.test.xlib.deploy_contract(
            "native", "java", self.cname, self.file, contract_account, args
        )
        assert err == 0 or "already exist" in result, "部署java合约失败： " + result
        if err == 0:
            # 等待tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case02(self, input_args):
        """
        升级java合约，不带数据
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.upgrade_contract(
            "native", self.cname, self.file, contract_account
        )
        assert err == 0, "升级java合约失败： " + result

        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result
        time.sleep(2)
        err, result_query = input_args.test.xlib.query_acc_contract(
            contract_account, self.cname
        )
        assert err == 0, "查询账户下的合约失败： " + result_query
        assert txid == result_query["txid"], "升级后，检查合约txid，不一致"

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case03(self, input_args):
        """
        调用java合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "increase", args
        )
        assert err == 0, "调用java合约失败： " + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case04(self, input_args):
        """
        查询java合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "get", args
        )
        assert err == 0, "查询java合约失败： " + result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case05(self, input_args):
        """
        升级java合约，带数据
        """
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.upgrade_contract(
            "native", self.cname, self.file, contract_account
        )
        assert err == 0, "升级java合约失败： " + result

        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result
        time.sleep(2)
        err, result_query = input_args.test.xlib.query_acc_contract(
            contract_account, self.cname
        )
        assert err == 0, "查询账户下的合约失败： " + result_query
        assert txid == result_query["txid"], "升级后，检查合约txid，不一致"

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case06(self, input_args):
        """
        调用java合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "increase", args
        )
        assert err == 0, "调用java合约失败： " + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

    @pytest.mark.skip("虚拟机部署java合约资源不足")
    def test_case07(self, input_args):
        """
        查询java合约
        """
        invoke_args = {"key": "dudu"}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "get", args
        )
        assert err == 0, "查询java合约失败： " + result
