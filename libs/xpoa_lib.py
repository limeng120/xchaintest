# !/usr/bin/env python3
"""
Xpoa测试lib
"""
from .poa_lib import Poa
from .xclient_libs import Xlibs


class Xpoa(Poa):
    """
    Xpoa功能库：继承Poa的所有方法，改写xlib的consensus invoke方法
    """

    def __init__(self, conf):
        super().__init__(conf)
        self.xlib = NewXlibs(conf)


class NewXlibs(Xlibs):
    """
    改写consensus invoke方法的type
    """

    def consensus_invoke(self, **kwargs):
        """
        调用共识合约
        type: 共识类型
        method：共识invoke的方法
        flag："--isMulti" 是否需要多签，可选配
        account: 发起人与候选人的acl账户，多签需要，可选配
        desc: 描述nominate或者vote的文件
        keys: key1（非多签） 或者[key1, key2]，（多签）; 如果不指定keys，则命令不会添加（使用默认data/keys)
        """

        res = ["consensus invoke"]
        args = ["type", "method", "account", "desc", "output"]

        # 将所有consensus invoke 的type改写为xpos
        kwargs["type"] = "xpoa"

        for arg in args:
            if arg in kwargs.keys():
                res.append("--" + arg)
                res.append(kwargs[arg])

        if "flag" in kwargs.keys():
            res.append(kwargs["flag"])

        cmd = " ".join(str(arg) for arg in res)

        # 打印desc文件
        if "desc" in kwargs.keys():
            self.sh.exec_shell(self.conf.client_path, "cat " + kwargs["desc"])

        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result
