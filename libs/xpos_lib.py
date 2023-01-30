# !/usr/bin/env python3
"""
Xpos测试lib类
"""
from .tdpos_lib import Tdpos
from .xclient_libs import Xlibs


class Xpos(Tdpos):
    """
    Xpos功能库：继承Tdpos的所有方法，改写xlib的consensus invoke方法
    """

    def __init__(self, conf):
        super().__init__(conf)
        self.xlib = NewXlibs(conf)


class NewXlibs(Xlibs):
    """
    改写consensus invoke方法的type
    """

    def __init__(self, conf):
        super().__init__(conf)
        
    #调用共识合约
    def ConsensusInvoke(self, **kwargs):
        """
        type: 共识类型
        method: 调用方法
        flag: 
        account:
        desc:
        """
        
        res = ["consensus invoke"]

        args = ["type", "method", "account", "desc", "output"]

        if "flag" in kwargs.keys() and kwargs["flag"] == "--isMulti":
            res.append(kwargs["flag"])
        elif "keys" in kwargs.keys():
            args.append("keys")

        # 将所有consensus invoke 的type改写为xpos
        kwargs["type"] = "xpos"

        for a in args:
            if a in kwargs.keys():
                res.append("--" + a)
                res.append(kwargs[a])

        cmd = " ".join(str(a) for a in res)

        # 打印desc文件
        if "desc" in kwargs.keys():
            self.sh.exec_shell(self.conf.client_path, "cat " + kwargs["desc"])

        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

        