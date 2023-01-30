"""
说明：测试 撤销提案
"""
import json
import pytest
import time
import os

class TestThaw:

    # 提案状态是voting，且无投票，撤销提案
    @pytest.mark.p2
    def test_case01(self, input):
        print("\n提案状态是voting，且无投票，撤销提案")
        validator = input.addrs
        err, version = input.test.update.genConsJson("tdpos", validator)
        assert err == 0, version
        err, id = input.test.update.proposeUpdate()
        assert err == 0, id
        
        # 预期提案状态为voting
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "voting" in result

        # 撤销提案
        err, result = input.test.update.thawPropose(id)
        assert err == 0, result

        # 预期提案状态为cancelled
        err, result = input.test.update.queryPropose(id)
        assert err == 0, "查询提案失败：" + result
        assert "cancelled" in result
        

  