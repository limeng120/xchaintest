"""
说明: 转账
"""
import time
import pytest


class TestTransfer:
    """
    转账
    """

    @pytest.mark.p0
    def test_transfer1(self, input_args):
        """
        转账给普通账户
        """
        print("\n转账给普通账户")
        addr = "./output/data/alice/"
        # 查询账户余额
        err, befor_balan = input_args.test.xlib.get_balance(keys=addr)
        err, to = input_args.test.xlib.get_address(addr)
        # 转账
        err, result = input_args.test.xlib.transfer(to=to, amount="10000")
        assert err == 0 and result != "Select utxo error", "转账给合约账户 失败： " + result
        time.sleep(4)
        # 对比余额
        err, after_balan = input_args.test.xlib.get_balance(keys=addr)
        assert int(after_balan) == int(befor_balan) + int(10000)

    @pytest.mark.p0
    def test_transfer2(self, input_args):
        """
        指定被转账人,转账给账户
        """
        print("\n指定被转账人,转账给账户")
        addr = "./output/data/bob/"
        # 查询账户余额
        err, befor_balan = input_args.test.xlib.get_balance(keys=addr)
        err, to = input_args.test.xlib.get_address(addr)
        # 转账
        err, result = input_args.test.xlib.transfer(
            to=to, amount="1000", keys="./output/data/alice"
        )
        assert err == 0 and result != "Select utxo error", "被转账人,转账给账户 失败： " + result
        time.sleep(4)
        # 对比余额
        err, after_balan = input_args.test.xlib.get_balance(keys=addr)
        assert int(after_balan) == int(befor_balan) + int(1000)

    @pytest.mark.p0
    def test_transfer3(self, input_args):
        """
        转账给合约账户
        """
        print("\n转账给合约账户")
        account = "XC1111111111111111@" + input_args.conf.name
        # 查询账户余额
        err, befor_balan = input_args.test.xlib.get_balance(account=account)
        # 转账并获取 TX
        err, txid = input_args.test.xlib.transfer(to=account, amount="100000000000")
        assert err == 0 and txid != "Select utxo error", "转账给合约账户 失败： " + txid
        time.sleep(4)
        # 对比余额
        err, after_balan = input_args.test.xlib.get_balance(account=account)
        assert int(after_balan) == int(befor_balan) + int(100000000000)

    @pytest.mark.p0
    def test_transfer4(self, input_args):
        """
        带有冻结高度的转账给账户
        """
        print("\n带有冻结高度,转账给账户")
        # 查询账户余额
        addr = "./output/data/alice2"
        err, befor_balan = input_args.test.xlib.get_balance(keys=addr, frozen=True)
        # 查询区块高度
        err, getheight = input_args.test.xlib.query_height()
        assert err == 0, getheight
        err, to = input_args.test.xlib.get_address(addr)
        assert err == 0, to
        # 转账
        err, result = input_args.test.xlib.transfer(
            to=to, amount="100", frozen=(int(getheight) + 500)
        )
        assert err == 0 and result != "Select utxo error", "冻结转账给账户 失败： " + result
        time.sleep(4)
        # 对比 高度和余额
        err, after_balan = input_args.test.xlib.get_balance(keys=addr, frozen=True)
        assert err == 0, after_balan
        err, after_height = input_args.test.xlib.query_height()
        assert err == 0, after_height
        if int(after_height) < (int(getheight) + int(500)):
            assert int(after_balan) == int(befor_balan) + int(100)
        else:
            assert after_balan == befor_balan

    @pytest.mark.p0
    def test_transfer5(self, input_args):
        """
        带有冻结高度的转账给合约账户
        """
        print("\n带有冻结高度的转账给合约账户")
        account = "XC1111111111111111@" + input_args.conf.name
        # 查询账户余额
        err, befor_balan = input_args.test.xlib.get_balance(
            account=account, frozen=True
        )
        # 查询区块高度
        err, getheight = input_args.test.xlib.query_height()
        assert err == 0, getheight
        # 转账
        err, result = input_args.test.xlib.transfer(
            to=account, amount="100", frozen=(int(getheight) + 500)
        )
        assert err == 0 and result != "Select utxo error", "冻结转账给 合约账户 失败：" + result
        time.sleep(4)
        # 对比 高度和余额
        err, after_balan = input_args.test.xlib.get_balance(
            account=account, frozen=True
        )
        assert err == 0, after_balan
        err, after_height = input_args.test.xlib.query_height()
        assert err == 0, after_height
        if int(after_height) < (int(getheight) + int(500)):
            assert int(after_balan) == int(befor_balan) + int(100)
        else:
            assert after_balan == befor_balan

    @pytest.mark.p0
    def test_balance1(self, input_args):
        """
        查询账户余额,余额
        """
        print("\n查询账户余额")
        err, result = input_args.test.xlib.get_balance(keys="./output/data/alice")
        assert err == 0, "查询账户余额 失败" + result

    @pytest.mark.p0
    def test_balance2(self, input_args):
        """
        查询账户余额,冻结余额
        """
        print("\n查询账户冻结余额")
        err, result = input_args.test.xlib.get_balance(
            keys="./output/data/alice", frozen=True
        )
        assert err == 0, "查询账户冻结余额 失败" + result

    @pytest.mark.p0
    def test_balance3(self, input_args):
        """
        查询合约账户余额
        """
        print("\n查询合约账户余额")
        account = "XC1111111111111111@" + input_args.conf.name
        err, result = input_args.test.xlib.get_balance(account=account)
        assert err == 0, "查询合约账户余额 失败" + result

    @pytest.mark.p0
    def test_balance4(self, input_args):
        """
        查询合约账户余额,冻结余额
        """
        print("\n查询合约账户冻结余额")
        account = "XC1111111111111111@" + input_args.conf.name
        err, result = input_args.test.xlib.get_balance(account=account, frozen=True)
        assert err == 0, "查询合约账户冻结余额 失败" + result

    @pytest.mark.p0
    def test_query_tx_block(self, input_args):
        """
        根据txid 查询交易信息
        """
        # 获取转账的txid
        account = "XC1111111111111111@" + input_args.conf.name
        err, result = input_args.test.xlib.transfer(to=account, amount="1")
        assert err == 0, "转账失败：" + result

        txid = input_args.test.xlib.get_txid_from_res(result)

        print("\n根据txid 查询交易信息")
        # 等待tx上链
        err, result = input_args.test.xlib.wait_tx_on_chain(txid)
        assert err == 0, result

        err, blockid = input_args.test.xlib.query_tx(txid)
        assert err == 0, "查询tx失败：" + blockid
        assert blockid != " "

        print("根据blockid，查询区块信息")
        err, result = input_args.test.xlib.query_block(blockid)
        assert err == 0 and result == "true", "查询block失败：" + blockid

    @pytest.mark.p0
    def test_query_block(self, input_args):
        """
        根据高度查询区块
        """
        print("\n根据高度查询区块")
        err, result = input_args.test.xlib.query_block_by_height("5")
        assert err == 0, "查询block失败：" + result
