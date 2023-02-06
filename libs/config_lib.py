# !/usr/bin/env python3
"""
Configuration
"""
import os
import subprocess
import yaml


class Get:
    """
    解析配置文件conf/conf.yaml
    """

    def __init__(self, file):

        stream = open(file, mode="r", encoding="utf-8")
        data = yaml.load(stream, Loader=yaml.FullLoader)
        stream.close()

        self.hosts = data["hosts"]
        self.default_host = data["default_host"]

        self.client_path = data["client_path"]
        self.cli = os.path.join(self.client_path, "bin/xchain-cli")

        # 节点账户路径
        self.accounts = data["accounts"]

        # 用于签名的key数组, addr数组(为了字典序考虑, 即node1、2、3的顺序，遍历key赋值)
        self.keys, self.addrs = [], []
        for node in self.accounts.keys():
            # 获取key
            self.keys.append(self.accounts[node])
            cmd = (
                "cd "
                + os.path.join(self.client_path, self.accounts[node])
                + " &&"
                + " ".join(("cat", "address"))
            )
            err, result = subprocess.getstatusoutput(cmd)
            assert err == 0, result
            # 为TestTdpos的类变量赋值，便于其他函数使用
            self.addrs.append(result)

        # 当前client的地址
        cmd = (
            "cd "
            + os.path.join(self.client_path, "data/keys")
            + " &&"
            + " ".join(("cat", "address"))
        )
        err, result = subprocess.getstatusoutput(cmd)
        assert err == 0, result
        self.client_addr = result
        self.client_key = "data/keys"

        assert isinstance(data["nofee"], bool), "nofee字段设置错误"
        self.nofee = data["nofee"]

        self.crypto = data["crypto"] if data["crypto"] in ["gm", "gm2"] else ""

        self.all_log = data["all_log"]

        self.name = data["name"]
