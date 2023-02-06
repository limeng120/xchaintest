"""
说明：共识升级的异常场景
"""
import json
import pytest


class TestUpdateConErr:
    """
    共识升级的异常场景
    """

    @pytest.mark.abnormal
    def test_case01(self, input_args):
        """
        【异常】向低版本升级
        """
        print("\n【异常】向低版本升级")
        validator = input_args.addrs
        err, version, _ = input_args.test.update.update_consensus(
            "tdpos", validator, version="0"
        )
        assert err == 0, "提案和投票失败：" + version

        # 15个区块后触发升级，故等20个区块
        input_args.test.xlib.wait_num_height(20)
        # 检查升级后的参数、候选人、共识名称

        err, result = input_args.test.update.check_update("tdpos", validator, version)
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case02(self, input_args):
        """
        【异常】向同版本升级
        """
        print("\n【异常】向同版本升级")
        validator = input_args.addrs[0]

        # 查询当前共识版本
        err, result = input_args.test.xlib.consensus_status()
        assert err != 0, result
        result = json.loads(result)
        version = result["version"]

        err, version, _ = input_args.test.update.update_consensus(
            "single", validator, version=version
        )
        assert err == 0, "提案和投票失败：" + version

        # 15个区块后触发升级，故等20个区块
        input_args.test.xlib.wait_num_height(20)
        # 检查升级后的参数、候选人、共识名称

        err, result = input_args.test.update.check_update("single", validator, version)
        assert err != 0, result

    @pytest.mark.abnormal
    def test_case03(self, input_args):
        """
        【异常】禁止升级到pow共识
        """
        print("\n【异常】升级到pow共识")
        err, version, propose_id = input_args.test.update.update_consensus(
            "pow", input_args.addrs
        )
        assert err == 0, "提案和投票失败：" + version

        # 15个区块后触发升级，故等20个区块
        input_args.test.xlib.wait_num_height(20)

        # 提案状态预期是completed_failure
        err, result = input_args.test.update.query_propose(propose_id)
        assert err == 0, "查询提案失败：" + result
        assert "completed_failure" in result
