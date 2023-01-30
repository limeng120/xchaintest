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

    def __init__(self, conf):
        super().__init__(conf)

    def ConsensusInvoke(self, **kwargs):
        """
        type: 共识类型
        method: 调用方法
        flag: 
        account:
        desc:
        host:
        """
        
        res = ["consensus invoke"]
        args = ["type", "method", "account", "desc", "output"]

        # 将所有consensus invoke 的type改写为xpos
        kwargs["type"] = "xpoa"

        for a in args:
            if a in kwargs.keys():
                res.append("--" + a)
                res.append(kwargs[a])

        res.append(kwargs["flag"]) if "flag" in kwargs.keys() else res

        cmd = " ".join(str(a) for a in res)

        # 打印desc文件
        if "desc" in kwargs.keys():
            self.sh.exec_shell(self.conf.client_path, "cat " + kwargs["desc"])
            
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result
        
