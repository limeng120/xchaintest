"""
说明：修改平行链群组
"""
import json
import pytest


class TestGroup:
    """
    修改平行链群组
    """

    def edit_query_group(self, name, admin, input_args):
        """
        修改群组
        """
        err, result = input_args.test.pchain.edit_chain_group(name=name, admin=admin)
        assert err == 0, "修改群组失败：" + result

        err, result = input_args.test.pchain.query_chain_group(name=name)
        assert err == 0, "查询群组失败：" + result
        tmp = result.split("\n")[0]
        result = tmp.split(": ")[1]
        result = json.loads(result)
        assert sorted(result["admin"]) == sorted(admin), "修改后 群组不符合预期"

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        创建平行链时群组成员是3个，修改群组，减少成员，3->2
        """
        print("\n 创建平行链时群组成员是3个，修改群组，减少成员，3->2")
        admin = [input_args.addrs[0], input_args.addrs[1]]
        self.edit_query_group("hipow1", admin, input_args)

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        修改平行链群组时,admin不存在，可以修改成功
        """
        print("\n修改平行链群组时,admin不存在，可以修改成功")
        admin = [input_args.addrs[0], "121212121212122121"]
        self.edit_query_group("hixpoa1", admin, input_args)

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        给不同链，设置不同权限
        """
        print("\n 给不同链，设置不同权限")
        groups = [
            {"name": "hisingle1", "admin": input_args.addrs},
            {
                "name": "hipow1",
                "admin": [input_args.addrs[0], input_args.addrs[1]],
            },
        ]
        for group in groups:
            self.edit_query_group(group["name"], group["admin"], input_args)

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        连续更新链的群组
        """
        print("\n连续更新hitdpos1链群组：node123-->node1,3 --->node1,2--->node2,3-->node123")
        addrs = input_args.addrs
        keys = input_args.keys
        change_array = [[0], [0, 2], [0, 1], [1, 2], [1, 0, 2]]

        before_admin = change_array[0][0]
        for value in change_array:
            admin = []
            query_person = value[0]
            for node_index in value:
                admin.append(addrs[node_index])
            # 修改候选人
            err, result = input_args.test.pchain.edit_chain_group(
                name="hitdpos1", admin=admin, keys=keys[before_admin]
            )
            assert err == 0, "修改hitdpos1群组失败：" + result
            err, result = input_args.test.pchain.query_chain_group(
                name="hitdpos1", keys=keys[query_person]
            )
            assert err == 0, "查询hitdpos1群组失败：" + result
            before_admin = query_person

            tmp = json.loads(result.split("\n")[0].split(": ")[1])
            assert sorted(tmp["admin"]) == sorted(admin), "修改后 hitdpos1群组不符合预期"

    # @pytest.mark.p2
    # def test_case05(self, input_args):
    #     """
    #     修改已停用的链的群组
    #     """
    #     print("\n 修改已停用的链的群组")
    #     err, result = input_args.test.pchain.stop_chain(name="hipow1")
    #     assert err == 0, "停用链失败：" + result
    #     # 等2个区块，链停用
    #     input_args.test.xlib.wait_num_height(2)
    #     err, result = input_args.test.xlib.query_height(name="hipow1")

    #     assert "not find chain hipow1" in result, "停用链后,查看链的区块高度不合预期 ：" + result
    #     admin = [input_args.addrs[0], input_args.addrs[1]]
    #     self.edit_query_group("hipow1", admin, input_args)
