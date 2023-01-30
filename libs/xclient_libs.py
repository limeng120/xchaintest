# !/usr/bin/env python3
"""
Libs for some common function of xchain
"""
import os
import time
import subprocess
import json
import math
import numpy as np

from .xclient_ops import Xclient
from .xclient_ops import Shell

class Xlibs(object):
    """
    xchain的常用lib库
    """

    def __init__(self, conf):
        super().__init__()
        self.xclient = Xclient(conf)
        self.conf = conf
        self.host = conf.default_host
        self.sh = Shell()

    #创建账户
    def CreateAccount(self, **kwargs):
        """
        在指定目录下创建账户
        output：为输出的目录
        可选参数：lang, strength
        """
        res = ["account", "newkeys"]
        argname = ["output", "lang", "strength", "force"]
        for key, value in kwargs.items():
            if key in argname:
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        
        #参数中设置了output，则检查output目录是否被创建
        if "output" in kwargs.keys():
            if os.path.exists((os.path.join(self.conf.client_path, kwargs["output"]))) is False:
                err = -1
                result = "after create account, check dir exist failed"

        return err, result
        
    # 【通过助记词，生成私钥】
    def RetrieveAccount(self, **kwargs):
        """
        mnemonic：助记词
        lang：助记词类型
        address：生成的私钥
        output：输出地址 /output/data/zhangwei5
        """    
        res = ["account", "restore"]
        argname = ["output", "lang", "mnemonic"]
        for key, value in kwargs.items():
            if key in argname:
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)    
        err, result = self.xclient.exec_host(cmd, **kwargs)

        #参数中设置了output，则检查output目录是否被创建
        if "output" in kwargs.keys():
            if os.path.exists((os.path.join(self.conf.client_path, kwargs["output"]))) is False:
                err = -1
                result = "after create account, check dir exist failed"
        return err, result

    def QueryContactAccount(self, **kwargs):
        """
        查询合约账户，2种方式
        1.可输入address
        2.可输入key的路径
        查询账户权重, 合约方法，根据address查账号
        type：acl，权重 contracts,合约方法 keys/address,根据address查账号
        name: 账号
        """  
        res = ["account", "query"]
        argname = ["address", "keys"]
        for key, value in kwargs.items():
            if key in argname:
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)    
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    def QueryAcl(self, **kwargs):
        """
        查询合约账号的acl或者合约方法的acl
        account：合约账号名
        contrct：合约名
        method：合法方法，与合约名同时使用
        """
        res = ["acl", "query"]
        argname = ["account", "contract", "method"]
        for key, value in kwargs.items():
            if key in argname:
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)    
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    def GetAddress(self, key_path):
        """
        根据key的路径，获取address
        """
        err, result = self.sh.exec_shell(self.conf.client_path, "cat " + key_path + "/address")
        return err, result

    #查询余额
    def Balance(self, **kwargs):
        """
        account：账户
        frozen：是否查询冻结余额
        """
        res = ["account", "balance"]
        for key, value in kwargs.items():
            #查询合约账户是./bin/xchain-cli account balance  XC1111111111111111@xuper
            if key == "account":
                res.append(value)
            elif key == "frozen":
                res.append("--" + key)
            elif key == "keys":
                res.append("--" + key)
                res.append(value)
        
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    def QueryBlockHeight(self, name="", **kwargs):
        """
        name是链名, 不填写则使用conf内定义的name
        host是节点端口，不填写则用查询全部node
        """
        if name == "":
            name = self.conf.name

        res = []
        hostList = [kwargs["host"]] if "host" in kwargs.keys() else self.conf.hosts.values()
        s = ["status", "-L", "--name", name]
        cmd = " ".join(s)
        for n in hostList:
            for i in range(5):
                err, result = self.xclient.exec_host(cmd, host=n, nolog=True)
                if err != 0:
                    print(name + "链, host:" + n + "，获取高度失败")
                    continue
                else:
                    break
            if result == "null" or "\"" + name +"\"" not in result:
                return 1, "not find chain " + name
            
            info = json.loads(result)
            height = -1
            for i in range(len(info)):
                if info[i]["name"] == name:
                    height = info[i]["ledger"]["trunkHeight"]
                    break
            res.append(height)
        print("ledger height " + str(res))
        if np.std(res) > 3:
            return 1, "节点高度不一致：" + str(res)
        return 0, res[0]
        
    #查询TX，返回值为tx所在的block
    def QueryTx(self, txid, name="xuper"):
        host = self.host
        s = ("tx", "query", txid, "--name", name, "-H", host)
        cmd = " ".join(s)
        err, result = self.xclient.exec(cmd, other="|grep \\\"blockid\\\":|awk -F '\"' '{print $4}'")
        return err, result.split("\n")[0]
    
    #查询block，返回值为bool
    def QueryBlock(self, blockid, name="xuper"):
        host = self.host
        s = ("block", blockid, "--name", name, "-H", host)
        cmd = " ".join(s)
        err, result = self.xclient.exec(cmd, other="|grep \\\"inTrunk\\\"|awk -F ' ' '{print $2}'|awk -F ',' '{print $1}'")
        return err, result
    
    #通过高度查询block，返回blockid
    def QueryBlockByH(self, height):
        host = self.host
        s = ("block", "-N", height, "-H", host)
        cmd = " ".join(s)
        err, result = self.xclient.exec(cmd, other="|grep \\\"blockid\\\":|head -n 1|awk -F '\"' '{print $4}'")
        return err, result

    def WaitNumHeight(self, num, name=""):
        # 获取当前区块高度
        err, height = self.QueryBlockHeight(name)
        assert err == 0, height
        h = int(height)

        # 可能出现节点停止出块，为防止死循环，增加最长等待时间=出块个数*出块间隔+60
        max_wait_time = num * 3 + 60
        start_time = 0

        # 等num个区块高度后继续执行
        while int(height) <= h + num and start_time < max_wait_time:
            #每3秒查询一次
            time.sleep(3)
            err, height = self.QueryBlockHeight(name)
            assert err == 0, height
            start_time = start_time + 3

        if start_time >= max_wait_time:
            print("fail !! 超过最大等待时间 " + str(max_wait_time))
            assert False
        return err, height

    #执行转账
    def Transfer(self, **kwargs):
        """
        to:收款地址
        amount:转账金额
        key:付款账户
        """
        res = ["transfer"]
        argname = ["to", "amount", "keys", "frozen"]
        for key, value in kwargs.items():
            if key in argname:
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    #创建合约账户  
    def CreateContractAccount(self, **kwargs):
        """
        简易方式创建
            key: 私钥
            account: 账户名称
        通过描述文件创建
            desc: 创建合约账户的acl描述文件
        """
        res = ["account", "new"]
        argname = ["account", "desc", "keys"]
        for key, value in kwargs.items():
            if key in argname:
                res.append("--" + key)
                res.append(value)
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        if err != 0:
            return err, result
        # account_name = result.split("\n")[-1]
        # account_name = account_name.split(":")[1]
        # return err, account_name
        return err, result             

    # 创建合约账户, 自动生成desc           
    def CreateContractAccount2(self, aks=[], **kwargs):
        """
        创建合约账户,通过json文件创建
        aks：列表，合约账户内的ak   
        account_name：账户名. 注意：desc方式，合约名使用参数account_name,防止跟简易模式时传入的account混淆
        """
        # 1.准备desc中的acl字符串
        acl = {
            "pm":{
                "rule": 1,
                "acceptValue": 1
            },
            "aksWeight":{
            }
        }
        weight = math.ceil(10/len(aks)) * 0.1
        for ak in aks:
            acl["aksWeight"][ak] = weight

        # 由于xchain-cli的要求, acl中的引号要转义
        acl_str = json.dumps(acl)
        
        # 2.准备desc文件
        desc_file = 'output/account.json'
        account_desc = {
                "module_name": "xkernel", 
                "method_name": "NewAccount", 
                "contract_name": "$acl", 
                "args": {
                "account_name": kwargs["account_name"], 
                "acl": acl_str
                }
        }              
        desc = os.path.join(self.conf.client_path, desc_file)
        if not os.path.exists(desc):
            file2 = open(desc, mode='a', encoding='UTF-8')
            file2.close()    
        with open(desc, "w") as f:
            json.dump(account_desc, f)
            f.close()  
        # 3.执行创建账户命令  
        err, result = self.CreateContractAccount(desc=desc_file, **kwargs) 
        return err, result 

    # 部署合约
    def DeployContract(self, type, lang, cname, file, acl_account, args, **kwargs):
        """
        type: wasm native evm
        lang: go, java
        cname: 合约名
        file: 合约文件
        acl_account: 部署合约的账户
        args: 合约初始化参数 -a 后的内容
        """
        args = "\'" + args + "\'"
        res = [type, "deploy", "--cname", cname, file, "--account", acl_account]
        if lang != "cpp" and lang != "" :
            res.extend(["--runtime", lang])
        if args != "'None'":
            res.extend(["-a", args])
        for key, value in kwargs.items():
            if key == "abi":
                res.append("--" + key)
                res.append(value)
            elif key == "isMulti":
                res.append("--" + key)    
        cmd = " ".join(str(a) for a in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    # 调用合约
    def InvokeContract(self, type, cname, method, args, **kwargs):
        """
        type: wasm native evm
        cname: 合约名
        method: 调用合约的方法名
        args: 合约的描述 -a 后的内容
        """
        methodtype = ["transfer", "send", "invoke"]
        args = "\'" + args + "\'"
        res = [type, "invoke", cname, "--method", method]
        if args != "'None'":
            res.extend(["-a", args])
        for key, value in kwargs.items():
            if key == "isMulti":
                res.append("--" + key)              
            elif key == "account" or key == "keys"  or key == "fee" or key == "amount":  
                res.append("--" + key) 
                res.append(value)


        cmd = " ".join(str(a) for a in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    # 从转账或者合约调用的回显，获取txid
    def GetTxidFromRes(self, result):
        """
        result: 
        合约调用的结果字符串，示例如下
            contract response: 19
            The gas you cousume is: 52
            The fee you pay is: 52
            Tx id: a21ad9aa612b3497b384c00e71a54536a2fdf4b61b93b45574634692685dead9
        转账的txid，xchain环境，直接回显
        返回txid
        """
        txid = ""
        lines = result.split("\n")
        if len(lines) == 1 and "Tx id:" not in result:
            txid = result
        else:
            for line in lines:
                if "Tx id:" in line:
                    txid = line.split()[2]
                    break
            assert txid != "", "结果中不含txid" 
        return txid 

    # 从合约调用的回显，获取value
    def GetValueFromRes(self, result):
        """
        result: 合约调用的结果字符串，示例如下
            contract response: 19
            The gas you cousume is: 52
            The fee you pay is: 52
            Tx id: a21ad9aa612b3497b384c00e71a54536a2fdf4b61b93b45574634692685dead9
        
        对于开放网络，结果如下
            contract response: success
            contract response: 19
            The gas you cousume is: 101
            The fee you pay is: 101
            ComplianceCheck txid: 2645062ccf41b37cdd860291055dbc2426578f787c811cc89d54720cec00e1e6
            Tx id: 2248b14a0dba03245f35c6ddd1acad3b47c50089c5b52a9575f1186f1da8b028
        返回value
        """
        value = ""
        lines = result.split("\n")
        for line in lines:
            if "contract response: " in line:
                value = line.split("contract response: ")[1] 
        assert value != "", "结果中不含value" 
        return value

    # 查询合约
    def QueryContract(self, type, cname, method, args, **kwargs):
        """
        type: wasm native evm
        cname: 合约名
        method: 查询合约的方法名
        args: 合约的描述 -a 后的内容
        """
        # 交易上链可验证更多场景，故改为invoke
        err, result = self.InvokeContract(type, cname, method, args, **kwargs)
        return err, result


    # 查询acl账户创建的合约
    def QueryAccContract(self, acl_account, cname):
        """
        acl_account: 合约账户
        cname: 合约账户下的合约名
        """
        res = ["account", "contracts", "--account", acl_account]
        cmd = " ".join(str(a) for a in res)
        err, result = self.xclient.exec_host(cmd)
        if err != 0:
            return err, result
        result = json.loads(result)
        for contract in result:
            if contract["contract_name"] == cname:
                return 0, contract
        return 1, "未找到合约：" + cname

    # 升级native合约
    def UpgradeContract(self, type, cname, file, acl_account, **kwargs):
        """
        type: wasm native evm
        cname: 合约名
        file: 用于更新合约的文件
        acl_account: 之前部署合约的合约账户
        """      
        res = [type, "upgrade", "--cname", cname, file, "--account", acl_account]

        cmd = " ".join(str(a) for a in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    #查询共识状态
    def ConsensusStatus(self, **kwargs):

        res = ("consensus", "status")
        cmd = " ".join(res)

        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

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

        # 判断是否多签--isMulti, 
        if "flag" in kwargs.keys() and kwargs["flag"] == "--isMulti":
            res.append(kwargs["flag"])
        # 非多签情况下，是否需要要指定keys（如果不加，默认使用client的data/keys）
        elif "keys" in kwargs.keys():
            args.append("keys")

        for a in args:
            if a in kwargs.keys():
                res.append("--"+a)
                res.append(kwargs[a])

        cmd = " ".join(str(a) for a in res)
        # 打印desc文件
        if "desc" in kwargs.keys():
            self.sh.exec_shell(self.conf.client_path, "cat " + kwargs["desc"])
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result
        
    # 对tx进行签名
    def Multisig(self, tx, output, key, **kwargs):
        tx = "--tx="+tx
        output = "--output="+output
        res = ("multisig", "sign", tx, "--keys", key, output)
        cmd = " ".join(res)

        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    #发送多签的签名
    def MultisigSend(self, tx, signs, **kwargs):
        res = ("multisig", "send", "--tx="+tx, signs, signs)
        cmd = " ".join(res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result

    # 前提：已生成tx.out
    # 用keys对其签名，并send到xchain
    def Multisign(self, **kwargs):
        """
        keys: 进行签名的私钥路径
        """
        #获取用来签名的key
        keys = kwargs["keys"]
        outputs = []
        tx = "./tx.out"

        #各自签名
        for key in keys:
            output = os.path.basename(key) + ".sign"
            
            err, result = self.Multisig(tx, output, key, **kwargs)
            if err != 0:
                return err, result
            outputs.append(output)
    
        #收集和发送签名
        signs = ",".join(str(x) for x in outputs)

        err, result = self.MultisigSend(tx, signs, **kwargs)
        return err, result

    # 发起多签名的tx, 适用于通过desc文件发起交易的操作
    def MultiSignTX(self, desc, acl_account, keys, addrs, **kwargs):
        """
        desc 定义交易内容的文件
        acl_account  发起请求的acl账户
        keys 签名阶段，用的私钥路径
        addrs 生成tx阶段，用的ak
        """
        self.xclient.WriteAddrs(acl_account, addrs)

        # 生成tx.out
        res = ["multisig", "gen", "--desc", desc, "--from", acl_account]
        cmd = " ".join(str(x) for x in res)

        err, result = self.xclient.exec_host(cmd, **kwargs)
        if err != 0:
            return err, result

        # 对tx签名，并将tx和签名发送到xchain
        err, result = self.Multisign(keys=keys, **kwargs)
        return err, result

    # 多签转账
    def MultiTransfer(self, signkeys, addrs, **kwargs): 
        self.xclient.WriteAddrs(kwargs.get("account"), addrs)  
        res = ["multisig", "gen"]   
        argname = ["to", "amount", "keys", "frozen"]
        for key, value in kwargs.items():
            if key == "account":
                res.append("--from")
                res.append(value) 
            elif key in argname and value != None:
                res.append("--" + key)
                res.append(value) 
        cmd = " ".join(str(x) for x in res)    
        err, result = self.xclient.exec_host(cmd, **kwargs)
        if err != 0:
            return err, result
            
        err, result = self.Multisign(keys=signkeys)
        return err, result

    #执行发起提案和多签流程
    def Propose(self, **kwargs):
        """
        type: 共识类型
        method：共识invoke的方法
        flag："--isMulti" 是否需要多签，可选配 
        account: 发起人与候选人的acl账户，多签需要，可选配
        desc: 描述nominate或者vote的文件
        keys: key1（非多签） 或者[key1, key2]，（多签）; 如果不指定keys，则命令不会添加（使用默认data/keys)

        """
        # 需要多签，修改data/acl/addrs
        if "flag" in kwargs.keys() and kwargs["flag"] == "--isMulti":
            acl_account = kwargs["account"]
            addrs = []
            for k in kwargs["keys"]:
                err, addr = self.GetAddress(k)
                addrs.append(addr)
            self.xclient.WriteAddrs(acl_account, addrs)

        err, result = self.ConsensusInvoke(**kwargs)
        if err != 0:
            return err, result

        #检查是否为需要多签的情况
        if "flag" in kwargs.keys() and kwargs["flag"] == "--isMulti":
            err, result = self.Multisign(**kwargs)
            if err != 0:
                return err, result

        return err, result

    def AddrTrans(self, type, from_addr, **kwargs):
        """
        evm地址转换
        type:      转换类型，x2e 或者 e2x
        from_addr: 转换前的地址
        """
        res = ["evm", "addr-trans", "--type", type, "--from", from_addr]
        cmd = " ".join(str(x) for x in res)
        err, result = self.xclient.exec_host(cmd, **kwargs)
        return err, result
    
    #代币分配相关操作
    def GovernToken(self, **kwargs):
        """
        type="init"
            key: 选填，用于支付手续费的账户，默认为xchain-cli对应的data/keys
        type="query"
            addr: 查询地址
        type="transfer"
            addr: 收款人地址
            amount: 转账金额
            key: 选填，转账付款的账户，默认为xchain-cli对应的data/keys
        """
        type = kwargs["type"]

        if type == "init":
            res = ["xkernel", "invoke", "'$govern_token'", "--method", "Init", "-a", "{}"]
            cmd = " ".join(res)  
            err, result = self.xclient.exec_host(cmd, **kwargs)
            return err, result

        elif type == "query":
            addr = kwargs["addr"]
            res = ("governToken", "query", "-a", addr)
            cmd = " ".join(res)
            err, result = self.xclient.exec_host(cmd, **kwargs)
            return err, result

        elif type == "transfer":
            addr = kwargs["addr"]
            amount = kwargs["amount"]

            res = ["governToken", "transfer", "--to", addr, "--amount", amount]
            if "key" in kwargs.keys():
                res.append("--keys")
                res.append(kwargs["key"])
                
            cmd = " ".join(res)
            err, result = self.xclient.exec_host(cmd, **kwargs)
            return err, result

        else:
            err, result = True, "Wrong type"
            return err, result

    # 获取代币总量
    def GetTotalToken(self, addr, **kwargs):
        err, result = self.GovernToken(type="query", addr=addr, **kwargs)
        if err != 0:
            return err, result
        result = result[result.index("{\"total_balance"):]
        money = json.loads(result)
        return err, money["total_balance"]

    # 获取冻结代币，注意，返回值为int类型
    def GetFrozenToken(self, addr, type="tdpos", **kwargs):
        """
        type： ordinary 或者tdpos，不配置则按tdpos
        """
        err, result = self.GovernToken(type="query", addr=addr, **kwargs)
        if err != 0:
            return err, result
        result = result[result.index("{\"total_balance"):]
        money = json.loads(result)
        if type == "tdpos":
            frozen = money["locked_balances"]["tdpos"]
        else:
            frozen = money["locked_balances"]["ordinary"]
        return err, frozen

    # 等待tx上链
    def WaitTxOnChain(self, txid, first_sleep=5, **kwargs):
        time.sleep(first_sleep)
        name = kwargs["name"] if "name" in kwargs.keys() else self.conf.name
        for i in range(60):
            print("查询tx " + txid)
            err, blockid = self.QueryTx(txid, name) 
            if err != 0 or blockid == "":
                print("查询tx " + txid + " 的blockid失败：再次查询")
                time.sleep(3)
                continue
        
            print("查询block " + blockid)
            err, result = self.QueryBlock(blockid, name) 
            if err != 0 or result == "":
                print("查询" + blockid + " 失败，再次查询")
                time.sleep(3)
            if result == "true":
                print("succ，tx已上链")
                return 0, txid + "已上链"
            
        return 1, txid + "未上链"
