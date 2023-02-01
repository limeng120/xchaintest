"""
说明: 测试go合约sdk
"""
import json
import pytest


class TestGoFeatures:
    """
    测试go合约sdk
    """

    file = "goTemplate/features"
    cname = "features_go"
    amount = "100"

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        部署features合约
        """
        print("部署features合约")
        contract_account = "XC" + input_args.account + "@" + input_args.conf.name
        err, result = input_args.test.xlib.deploy_contract(
            "native", "go", self.cname, self.file, contract_account, "None"
        )
        assert err == 0 or "exist" in result, "部署features合约失败： " + result

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        通过合约查询txid和block信息
        """
        # 1.先给合约账户转账
        err, result = input_args.test.xlib.transfer(to=self.cname, amount="1000000")
        assert err == 0, "转账失败：" + result
        txid = input_args.test.xlib.get_txid_from_res(result)
        # 等待tx上链
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        print("\n根据txid 查询交易信息")
        args = json.dumps({"txid": txid})
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "query_tx", args
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        blockid = json.loads(result.split()[-1])["blockid"]
        err, blockid_cli = input_args.test.xlib.query_tx(txid)
        assert err == 0 and blockid_cli == blockid, "blockid 错误"

        print("\n根据block 查询区块信息")
        args = json.dumps({"block_id": blockid})
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "query_block", args
        )
        assert err == 0, result
        result = input_args.test.xlib.get_value_from_res(result)
        assert err == 0 and json.loads(result.split()[-1])["in_trunk"] is True, (
            "查询区块 失败" + result
        )

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        通过合约进行转账
        """
        # 查余额
        err, befor_account = input_args.test.xlib.get_balance(account="123456")
        assert err == 0, "查询 " + "123456" + " 余额 失败" + befor_account
        err, befor_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0, "查询 " + self.cname + " 余额 失败" + befor_cname

        invoke_args = {"to": "123456", "amount": self.amount}
        args = json.dumps(invoke_args)
        err, result = input_args.test.xlib.invoke_contract(
            "native", self.cname, "transfer", args, fee=100
        )
        assert err == 0, "使用普通账户转账失败： " + result
        print("转账后查询账户")
        err, after_account = input_args.test.xlib.get_balance(account="123456")
        assert err == 0 and int(after_account) == int(befor_account) + int(
            self.amount
        ), ("查询123456余额 失败" + after_account)

        err, after_cname = input_args.test.xlib.get_balance(account=self.cname)
        assert err == 0 and int(after_cname) == int(befor_cname) - int(self.amount), (
            "查询" + self.cname + "余额 失败" + after_cname
        )

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        logging 从合约内写一条日志
        """
        print("\nlogging 从合约内写一条日志")
        # 写入logs/xchain.log文件中 自动化没有 cat logs/xchain.log |grep "log from contract"
        err, result = input_args.test.xlib.query_contract(
            "native", self.cname, "Logging", "None"
        )
        assert err == 0, "从合约内写一条日志 失败" + result
