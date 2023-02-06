"""
说明: acl测试用例的前置步骤

"""
import json
import pytest


class TestPreAcl:
    """
    权限用例依赖的前置步骤
    """

    @pytest.mark.p0
    def test_pre_acl(self, input_args, **kwargs):
        """
        运行acl用例的前置步骤：
        创建合约账户
        转账给合约账户
        部署go native合约
        """
        account = "2111111111111112"
        name = input_args.conf.name
        acl_account = "XC" + account + "@" + name

        file = "goTemplate/counter"
        cname = "gn_MultiSign"

        # 创建合约账户
        aks = [input_args.conf.addrs[0], input_args.conf.addrs[1]]
        err, result = input_args.test.xlib.create_contract_account2(
            aks, account_name=account
        )
        assert err == 0 or "already exists" in result, result

        if err == 0:
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result

        # 3.检查合约账号余额，余额不足1000000000，转账
        err, result = input_args.test.tranfer_when_not_enough(
            acl_account, 1000000000, **kwargs
        )
        assert err == 0, result

        input_args.test.xclient.write_addrs(acl_account, aks)
        # 多ak部署合约
        args = json.dumps({"creator": "abc"})
        # 生成部署合约的tx
        err, result = input_args.test.xlib.deploy_contract(
            "native", "go", cname, file, acl_account, args, isMulti=""
        )
        # 生成部署的tx失败，或者 合约已存在，直接返回
        if "already exists" not in result:
            assert err == 0, result
            # 对tx多签
            signkeys = [input_args.keys[0], input_args.keys[1]]
            err, result = input_args.test.xlib.multi_sign(keys=signkeys)
            assert err == 0, "tx多签失败： " + result
            # 等tx上链
            txid = input_args.test.xlib.get_txid_from_res(result)
            err, result = input_args.test.xlib.wait_tx_on_chain(txid)
            assert err == 0, result
