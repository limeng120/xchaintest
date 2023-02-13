"""
说明：修改平行链群组的异常场景
"""
import pytest


class TestGroupErr:
    """
    修改平行链群组的异常场景
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        非管理员修改平行链群组信息
        """
        print("\n 非管理员修改平行链群组信息")
        output = "./output/data/alice"
        input_args.test.xlib.create_account(output=output, lang="en", strength="1")
        admin = [input_args.addrs[0], input_args.addrs[1]]
        err, result = input_args.test.pchain.edit_chain_group(
            name="hixpoa1", admin=admin, keys="output/data/alice"
        )
        assert err != 0, "非管理员修改平行链群组信息成功，不符合预期：" + result
        msg = "invoke failed+unAuthorized"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        single共识：修改平行链群组时,矿工不是群组成员
        """
        print("\nsingle共识：修改平行链群组时,矿工不是群组成员")
        # 群组成员初始是node1~3、设置群组成员为node2
        admin = [input_args.addrs[1]]
        err, result = input_args.test.pchain.edit_chain_group(
            name="hisingle1", admin=admin, keys=input_args.keys[1]
        )
        assert err == 0, "修改hisingle的群组失败，不符合预期" + result

        height1 = []
        height2 = []
        # 查看区块高度，node2，3不涨块
        # 等2个区块，链停用
        input_args.test.xlib.wait_num_height(2)
        # 查询node2的平行链高度
        err, height1 = input_args.test.xlib.query_height(
            name="hisingle1", host=input_args.conf.hosts["node2"]
        )
        assert err == 0, height1

        # 等xuper出2个区块后，hisingle1 区块高度不变化
        input_args.test.xlib.wait_num_height(2)

        # 查询node2的平行链高度
        err, height2 = input_args.test.xlib.query_height(
            name="hisingle1", host=input_args.conf.hosts["node2"]
        )
        assert err == 0, height2

        assert height1 == height2, (
            "矿工不在群组内，节点涨块,不符合预期 height1=" + str(height1) + "height2=" + str(height2)
        )

        # 还原群组成员为node1~3
        admin = [
            input_args.addrs[0],
            input_args.addrs[1],
            input_args.addrs[2],
        ]
        err, result = input_args.test.pchain.edit_chain_group(
            name="hisingle1", admin=admin, keys=input_args.keys[1]
        )
        assert err == 0, "修改hisingle的群组失败，不符合预期" + result

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        修改xuper链群组
        """
        print("\n修改xuper链群组")
        admin = [input_args.addrs[1], input_args.addrs[2]]
        err, result = input_args.test.pchain.edit_chain_group(name="xuper", admin=admin)
        assert err != 0, "修改xuper链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case04(self, input_args):
        """
        查看xuper链群组
        """
        print("\n查看xuper链群组")
        err, result = input_args.test.pchain.query_chain_group(name="xuper")
        assert err != 0, "查看xuper链成功，不符合预期：" + result
        msg = "Key not found"
        assert msg in result, "报错信息错误"

    @pytest.mark.abnormal
    def test_case05(self, input_args):
        """
        非管理员，查看群组
        """
        print("\n非管理员，查看群组")
        err, result = input_args.test.pchain.query_chain_group(
            name="hixpoa1", keys="output/data/alice"
        )
        assert err != 0, "非管理员，查看群组链成功，不符合预期：" + result
        msg = "unAuthorized"
        assert msg in result, "报错信息错误"
