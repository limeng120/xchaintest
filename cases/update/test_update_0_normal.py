"""
说明：测试共识升级
两次升级直接需间隔20个block以上
其他共识不能升级到pow共识
1.测试tdpos与其他共识间 互相升级
tdpos->tdpos
tdpos->poa poa->tdpos
tdpos->xpoa xpoa->tdpos
tdpos->xpos xpos->tdpos
tdpos->single single->tdpos

2.测试xpos与其他共识间 互相升级(当前是tdpos，先执行tdpos升级xpos，在执行以下）
xpos->xpos
xpos->poa poa->xpos
xpos->xpoa xpoa->xpos
xpos->single single->xpos

3.测试poa与其他共识间 互相升级(当前是xpos，先执行xpos升级poa，在执行以下）
poa->poa
poa->xpoa xpoa->poa
poa->single single->poa

4.测试xpoa与其他共识间 互相升级(当前是poa，先执行poa升级xpoa，在执行以下）
xpoa->xpoa
xpoa->single single->xpoa

5.测试single与其他共识间 互相升级(当前是xpoa，先执行xpoa升级single，在执行以下）
single->single

"""
import pytest


class TestUpdateCons:
    """
    测试共识升级
    """

    def update(self, old_cons, new_cons, index, input_args):
        """
        old_cons: 原有共识名称
        new_cons: 升级的共识名称
        index： 判断奇偶，用于设置候选人，以便每次变更前后候选人也会变化
        """
        print(old_cons + "升级到" + new_cons)
        # 升级前后的候选人变化
        if index % 2 == 1:
            validator = [input_args.addrs[0], input_args.addrs[1]]
        else:
            validator = input_args.addrs

        err, version, propose_id = input_args.test.update.update_consensus(
            new_cons, validator
        )
        assert err == 0, "提案和投票失败：" + version

        input_args.test.xlib.wait_num_height(20)

        # 提案状态预期是completed_success
        err, result = input_args.test.update.query_propose(propose_id)
        assert err == 0, "查询提案失败：" + result
        assert "completed_success" in result

        # 检查升级后的参数、候选人、共识名称
        err, result = input_args.test.update.check_update(new_cons, validator, version)
        assert err == 0, result

        # 升级后，测试基本功能能否正常
        err, result = input_args.test.basic_function()
        assert err == 0, result

    @pytest.mark.p2
    def test_case01(self, input_args):
        """
        tdpos升级到tdpos
        """
        err, result = input_args.test.xlib.govern_token(method_type="init")
        assert err == 0 or "Govern tokens has been initialized" in result, (
            "初始化治理代币失败： " + result
        )
        print("tdpos升级到tdpos")
        self.update("tdpos", "tdpos", 1, input_args)

    @pytest.mark.p2
    def test_case02(self, input_args):
        """
        tdpos升级到poa
        """
        print("tdpos升级到poa")
        self.update("tdpos", "poa", 1, input_args)

    @pytest.mark.p2
    def test_case03(self, input_args):
        """
        poa升级到tdpos
        """
        print("poa升级到tdpos")
        self.update("poa", "tdpos", 0, input_args)

    @pytest.mark.p2
    def test_case04(self, input_args):
        """
        tdpos升级到xpoa
        """
        print("tdpos升级到xpoa")
        self.update("tdpos", "xpoa", 1, input_args)

    @pytest.mark.p2
    def test_case05(self, input_args):
        """
        xpoa升级到tdpos
        """
        print("xpoa升级到tdpos")
        self.update("xpoa", "tdpos", 0, input_args)

    @pytest.mark.p2
    def test_case06(self, input_args):
        """
        tdpos升级到xpos
        """
        print("tdpos升级到xpos")
        self.update("tdpos", "xpos", 1, input_args)

    @pytest.mark.p2
    def test_case07(self, input_args):
        """
        xpos升级到tdpos
        """
        print("xpos升级到tdpos")
        self.update("xpos", "tdpos", 0, input_args)

    @pytest.mark.p2
    def test_case08(self, input_args):
        """
        tdpos升级到single
        """
        print("tdpos升级到single")
        self.update("tdpos", "single", 1, input_args)

    @pytest.mark.p2
    def test_case09(self, input_args):
        """
        single升级到tdpos
        """
        print("single升级到tdpos")
        self.update("single", "tdpos", 0, input_args)

    @pytest.mark.p2
    def test_case10(self, input_args):
        """
        xpos升级到xpos
        """
        print("tdpos升级到xpos")
        self.update("tdpos", "xpos", 1, input_args)

        print("xpos升级到xpos")
        self.update("xpos", "xpos", 0, input_args)

    @pytest.mark.p2
    def test_case11(self, input_args):
        """
        xpos升级到poa
        """
        print("xpos升级到poa")
        self.update("xpos", "poa", 1, input_args)

    @pytest.mark.p2
    def test_case12(self, input_args):
        """
        poa升级到xpos
        """
        print("poa升级到xpos")
        self.update("poa", "xpos", 0, input_args)

    @pytest.mark.p2
    def test_case13(self, input_args):
        """
        xpos升级到xpoa
        """
        print("xpos升级到xpoa")
        self.update("xpos", "xpoa", 1, input_args)

    @pytest.mark.p2
    def test_case14(self, input_args):
        """
        xpoa升级到xpos
        """
        print("xpoa升级到xpos")
        self.update("xpoa", "xpos", 0, input_args)

    @pytest.mark.p2
    def test_case15(self, input_args):
        """
        xpos升级到single
        """
        print("xpos升级到single")
        self.update("xpos", "single", 1, input_args)

    @pytest.mark.p2
    def test_case16(self, input_args):
        """
        single升级到xpos
        """
        print("single升级到xpos")
        self.update("single", "xpos", 0, input_args)

    @pytest.mark.p2
    def test_case17(self, input_args):
        """
        poa升级到poa
        """
        print("xpos升级到poa")
        self.update("xpos", "poa", 1, input_args)

        print("poa升级到poa")
        self.update("poa", "poa", 0, input_args)

    @pytest.mark.p2
    def test_case18(self, input_args):
        """
        poa升级到xpoa
        """
        print("poa升级到xpoa")
        self.update("poa", "xpoa", 1, input_args)

    @pytest.mark.p2
    def test_case19(self, input_args):
        """
        xpoa升级到poa
        """
        print("xpoa升级到poa")
        self.update("xpoa", "poa", 0, input_args)

    @pytest.mark.p2
    def test_case20(self, input_args):
        """
        poa升级到single
        """
        print("poa升级到single")
        self.update("poa", "single", 1, input_args)

    @pytest.mark.p2
    def test_case21(self, input_args):
        """
        single升级到poa
        """
        print("single升级到poa")
        self.update("single", "poa", 0, input_args)

    @pytest.mark.p2
    def test_case22(self, input_args):
        """
        xpoa升级到xpoa
        """
        print("poa升级到xpoa")
        self.update("poa", "xpoa", 1, input_args)

        print("xpoa升级到xpoa")
        self.update("xpoa", "xpoa", 0, input_args)

    @pytest.mark.p2
    def test_case23(self, input_args):
        """
        xpoa升级到single
        """
        print("xpoa升级到single")
        self.update("xpoa", "single", 1, input_args)

    @pytest.mark.p2
    def test_case24(self, input_args):
        """
        single升级到single
        """
        print("single升级到single")
        self.update("single", "single", 0, input_args)

    @pytest.mark.p2
    def test_case25(self, input_args):
        """
        single升级到xpoa
        """
        print("single升级到xpoa")
        self.update("single", "xpoa", 1, input_args)

    @pytest.mark.p2
    def test_case26(self, input_args):
        """
        xpoa升级到tdpos
        """
        print("xpoa升级到tdpos")
        self.update("xpoa", "tdpos", 1, input_args)
