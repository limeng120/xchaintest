# !/usr/bin/env python3
"""
Execute client ops 
"""
import os
import subprocess
import time
from datetime import datetime
import pytz

# 打印日志
def record(cmd, result):
    logdir = "logs"
    logFile = logdir + "/execute.log"
    
    if not os.path.exists(logFile):
        if not os.path.isdir(logdir): 
            os.makedirs(logdir)
        file = open(logFile,'w')
        file.close()

    tz = pytz.timezone('Asia/Shanghai') #东八区
    current_time = datetime.fromtimestamp(int(time.time()),
        pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
   
    f = open(logFile, 'a', encoding='utf-8')
    msg = "\n" + current_time + "\n " + "  command: " + cmd + "\n" + "   result: " + result + "\n"
    f.write(msg)
    f.close()
    print(msg)

def check_fee(result):

    if "You need add fee" in result:
        fee = result[result.index("The gas you cousume is: "):]
        fee = fee[:fee.index("You need add fee")]
        fee = fee.replace("The gas you cousume is: ","")
        #这里有一个换行，返回值之前先去掉
        return fee[:-1]
    else:
        return 0


class Xclient(object):
    """
    xchain-cli的操作类，用于执行xchain-cli命令，fee会自动添加
    """

    def __init__(self, conf):
        super().__init__()
        self.conf = conf


    # 执行xchain-cli命令，eg: ./xchain-cli status|grep block
    # 用于xchain-cli的结果再次grep的场景
    def exec(self, cmd, **kwargs):
        """
        执行xchain-cli命令，eg: (./bin/xchain-cli) status -H:37101|grep trunkHeight|awk '{print $2}'
        那么cmd = "status -H:37101", other = "|grep trunkHeight|awk '{print $2}'"
        未指定时，other默认为空。
        """
        # 如果不在参数里指定，就设置为conf的配置
        other = kwargs["other"] if "other" in kwargs.keys() else ""
        nofee = kwargs["nofee"] if "nofee" in kwargs.keys() else self.conf.nofee
        crypto = kwargs["crypto"] if "crypto" in kwargs.keys() else self.conf.crypto
        name = kwargs["name"] if "name" in kwargs.keys() else self.conf.name
        res = ["cd", self.conf.client_path, "&&", "./bin/xchain-cli", cmd]
        # 判断是否指定了加密的方式
        if crypto != "":
            res.append("--crypto")
            res.append(crypto)
        # 如果设置了平行链，则命令带上链名
        if name != "xuper":
            res.append("--name")
            res.append(name)
        res.append(other)
        cli_cmd = " ".join(str(x) for x in res)

        err, result = subprocess.getstatusoutput(cli_cmd)
        if self.conf.all_log:
            record(cli_cmd, result)
        elif err != 0:
            record(cli_cmd, result)
        

        # 校验是否要付费
        fee = check_fee(result)
        if fee != 0 and nofee == False:
            res = ("cd", self.conf.client_path, "&&", "./bin/xchain-cli", cmd, "--fee", fee, other)
            cli_cmd = " ".join(res)
            err, result = subprocess.getstatusoutput(cli_cmd)
            if self.conf.all_log: 
                record(cli_cmd, result)
            elif err != 0:
                record(cli_cmd, result)
        
        return err, result


    #使用默认的端口执行xchain-cli命令，不必指定端口，eg: ./xchain-cli cmd -H default_host
    #default_host在配置文件中设置
    def exec_host(self, cmd, **kwargs):
        """
        执行xchain-cli命令，eg：(./xchain-cli) status (-H 127.0.0.1)
        可选配指定端口（如果缺省，默认为conf文件中的default_host）
        """
        #获取host，和是否无币化
        
        host = kwargs["host"] if "host" in kwargs.keys() else self.conf.default_host
        nofee = kwargs["nofee"] if "nofee" in kwargs.keys() else self.conf.nofee
        crypto = kwargs["crypto"] if "crypto" in kwargs.keys() else self.conf.crypto
        name = kwargs["name"] if "name" in kwargs.keys() else self.conf.name
        nolog = kwargs["nolog"] if "nolog" in kwargs.keys() else False

        res = ["cd",self.conf.client_path,"&&","./bin/xchain-cli", cmd, "-H", host]
        # 判断是否指定了加密的方式
        if crypto != "":
            res.append("--crypto")
            res.append(crypto)
        # 如果设置了平行链，则命令带上链名
        if name != "xuper":
            res.append("--name")
            res.append(name)
        cli_cmd = " ".join(str(x) for x in res)

        # 执行
        err, result = subprocess.getstatusoutput(cli_cmd)
        if self.conf.all_log and nolog is False:
            record(cli_cmd, result)
        elif err != 0:
            record(cli_cmd, result)

        # 判断是否要付费
        fee = check_fee(result)
        if fee != 0 and nofee == False:
            res.append("--fee")
            res.append(fee)
            cli_cmd = " ".join(str(x) for x in res)
            err, result = subprocess.getstatusoutput(cli_cmd)
            if self.conf.all_log:
                record(cli_cmd, result)
            elif err != 0:
                record(cli_cmd, result)
        
        return err, result

    #以后台运行的方式，用默认的端口执行xchain-cli命令，不必指定端口，eg: ./xchain-cli cmd -H default_host
    #default_host在配置文件中设置
    def exec_host_backend(self, cmd, logfile, **kwargs):
        """
        执行xchain-cli命令，eg：(./xchain-cli) status (-H 127.0.0.1)
        可选配指定端口（如果缺省，默认为conf文件中的default_host）
        """
        host = kwargs["host"] if "host" in kwargs.keys() else self.conf.default_host
        crypto = kwargs["crypto"] if "crypto" in kwargs.keys() else self.conf.crypto
        name = kwargs["name"] if "name" in kwargs.keys() else self.conf.name
        res = ["cd", self.conf.client_path, "&&", "rm -f", logfile, "&&", \
            "./bin/xchain-cli", cmd, "-H", host, ">", logfile, "2>&1"]
        # 判断是否指定了加密的方式
        if crypto != "":
            res.append("--crypto")
            res.append(crypto)
        # 如果设置了平行链，则命令带上链名
        if name != "xuper":
            res.append("--name")
            res.append(name)
        cli_cmd = " ".join(str(x) for x in res)
        # 执行
        subprocess.Popen(cli_cmd, shell=True)
        record(cli_cmd, "")

    # 写入data/acl/addrs （在使用合约账户多签时，会时常应用）
    def WriteAddrs(self, acl_account, addrs):

        client_path = self.conf.client_path
        addrs_file = os.path.join(self.conf.client_path, "data/acl/addrs")
        if not os.path.exists(addrs_file):
            acl_path = os.path.join(client_path, "data/acl")
            if not os.path.exists(acl_path):
                os.mkdir(acl_path)
            file = open(addrs_file,'w')
            file.close()

        with open(addrs_file, "w") as f:
            for addr in addrs:
                addr = (acl_account + "/" + addr)
                f.write(addr + "\n")
            f.close()


class Shell(object):
    """
    执行shell命令，与xchain-cli无关，需要指定path和命令
    """

    #在指定的path路径下，执行shell命令
    def exec_shell(self, path, cmd):
        sh_cmd = "cd " + path + " && " + cmd
        err, result = subprocess.getstatusoutput(sh_cmd)
        record(sh_cmd, result)
        return err, result

