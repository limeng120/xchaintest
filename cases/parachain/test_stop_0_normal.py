"""
说明：测试停用平行链
"""

import pytest


class TestStopChain:
    """
    测试停用平行链
    """

    def stop_query_chain(self, name, input_args):
        """
        停用链
        """
        err, result = input_args.test.pchain.stop_chain(name=name)
        assert err == 0, result
        # 当node1不是admin时，需用node2重试stopChain
        if "failed+unAuthorized" in result:
            err, result = input_args.test.pchain.stop_chain(
                name=name, keys=input_args.keys[1]
            )
        assert err == 0, "停用链失败：" + result
        # 等2个区块，链停用
        input_args.test.xlib.wait_num_height(2)
        err, result = input_args.test.xlib.query_height(name=name)
        assert "not find chain " + name in str(result), "停用链后,查看链的区块高度不合预期 ：" + str(
            result
        )

    def get_all_chain(self, input_args):
        """
        组装启用着的平行链
        """
        chain_list = []
        for _, v in input_args.conf.hosts.items():
            err, result = input_args.test.pchain.query_chain(host=v)
            assert err == 0, "查询所有启用着的平行链失败：" + result
            for element in result:
                if element not in chain_list:
                    chain_list.append(element)

        return chain_list

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        停用所有链
        """
        print("\n停用所有链,查询不到平行链")
        # 组装启用着的平行链
        stop_list = self.get_all_chain(input_args)
        # 停用链
        for chain in stop_list:
            self.stop_query_chain(chain, input_args)
        # 检查平行链是否全停止
        result = self.get_all_chain(input_args)
        assert len(result) == 0, "还有未停用的平行链，失败：" + str(result)

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        停用已经停用的链
        """
        print("\n停用已经停用的链")
        self.stop_query_chain("hisingle1", input_args)
