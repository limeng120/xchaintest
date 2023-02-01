"""
说明：poa, xpoa共识节点网络的测试
"""
import pytest


class TestEdit:
    """
    poa, xpoa共识节点网络的测试
    """

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        变更前后，验证集无重合：node1、2变更为node3
        """
        print("\n变更前后，验证集无重合：node1、2变更为node3")
        nominates = [input_args.node3]
        acl_account = input_args.acc12["acl_account"]
        addrs = input_args.acc12["addrs"]
        keys = input_args.acc12["keys"]
        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        增加候选人：node3变更为node1、2、3
        """
        print("\n增加候选人：node3变更为node1、2、3")
        nominates = [input_args.node1, input_args.node2, input_args.node3]

        acl_account = input_args.acc33["acl_account"]
        addrs = input_args.acc33["addrs"]
        keys = input_args.acc33["keys"]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys, host=input_args.host3
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        减少候选人，且当前集合超半数的成员签名：node1、2、3变更为node1、2，node1、3签名
        """
        print("\n减少候选人，且当前集合超半数的成员签名：node1、2、3变更为node1、2")
        nominates = [input_args.node1, input_args.node2]
        acl_account = input_args.acc13["acl_account"]
        addrs = input_args.acc13["addrs"]
        keys = input_args.acc13["keys"]

        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        1个区块内，两次变更：node1、2变更为node2、3，变更为node1
        """
        print("1个区块内，两次变更：node1、2变更为node2、3，变更为node1")
        nominates = [input_args.node2, input_args.node3]
        acl_account = input_args.acc12["acl_account"]
        addrs = input_args.acc12["addrs"]
        keys = input_args.acc12["keys"]

        # 提名node2，node3
        err, result = input_args.test.quick_edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err == 0, result

        nominates = [input_args.node2, input_args.node3]
        err, result = input_args.test.check_validates(nominates)
        assert err == 0, result

        # 提名node1
        acl_account = input_args.acc23["acl_account"]
        addrs = input_args.acc23["addrs"]
        keys = input_args.acc23["keys"]
        nominates = [input_args.node1]
        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys, host=input_args.host2
        )
        assert err == 0, result

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        相邻的三个区块内，两次变更：node1变更为node2、3，node1变更为node1、2
        """
        print("相邻的三个区块内，两次变更：node1变更为node2、3，node1变更为node1、2")
        nominates = [input_args.node2, input_args.node3]

        acl_account = input_args.acc11["acl_account"]
        addrs = input_args.acc11["addrs"]
        keys = input_args.acc11["keys"]

        err, result = input_args.test.quick_edit_validates(
            nominates, acl_account, addrs, keys
        )
        assert err == 0, result

        nominates = [input_args.node2, input_args.node3]
        err, result = input_args.test.check_validates(nominates)
        assert err == 0, result

        # 1个区块后验证再修改, 修改为[node1, node2, node3]
        err, result = input_args.test.xlib.wait_num_height(1)

        acl_account = input_args.acc23["acl_account"]
        addrs = input_args.acc23["addrs"]
        keys = input_args.acc23["keys"]
        nominates = [input_args.node1, input_args.node2]
        err, result = input_args.test.edit_validates(
            nominates, acl_account, addrs, keys, host=input_args.host2
        )
        assert err == 0, result
