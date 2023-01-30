# !/usr/bin/env python3
"""
Poa类共识测试lib
"""
import os
import json


from .common_lib import Common
from .xclient_libs import Xlibs


class Poa(Common):
    """
    Poa功能库：继承Common的所有方法
    """
    def __init__(self, conf):
        super().__init__(conf)

    # 通过合约查询候选人，在变更后立即可查
    def GetValidates(self, **kwargs):
        err, result = self.xlib.ConsensusInvoke(type="poa", method="getValidates", **kwargs)
        return err, result

    # 编辑验证集
    def EditValidates(self, nominates, acl_account, addrs, keys, **kwargs):  
        # 写入合约账户的addrs
        self.xclient.WriteAddrs(acl_account, addrs)

        validates = ";".join(str(x) for x in nominates)
        edit_desc = {
            "validates": validates
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "editValidates.desc")
        with open(desc, "w") as f:
            json.dump(edit_desc, f)
            f.close()

        #发起提名
        err, result = self.xlib.Propose(type="poa", method="editValidates", account=acl_account, \
            flag="--isMulti", desc="editValidates.desc", keys=keys, **kwargs)
        if err != 0:
            return err, result
        txid = result.split("Tx id: ")[1]
        print(txid)

        err, result = self.CheckValidates(nominates)
        if err != 0:
            return err, result

        # 等待tx上链
        err, result = self.xlib.WaitTxOnChain(txid)
        if err != 0:
            return err, result

        # tx上链后，在等三个区块后验证  
        err, result = self.xlib.WaitNumHeight(4)
        if err != 0:
            return err, result
        err, result = self.CheckConsensusVal(nominates)
        return err, result

    def QuickEditValidates(self, nominates, acl_account, addrs, keys, **kwargs):

        # 写入合约账户的addrs
        self.xclient.WriteAddrs(acl_account, addrs)

        validates = ";".join(str(x) for x in nominates)
        edit_desc = {
            "validates": validates
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "editValidates.desc")
        with open(desc, "w") as f:
            json.dump(edit_desc, f)
            f.close()

        #发起提名
        err, result = self.xlib.Propose(type="poa", method="editValidates", account=acl_account, \
            flag="--isMulti", desc="editValidates.desc", keys=keys, **kwargs)
        return err, result

    # 检查合约中的验证集
    def CheckValidates(self, nominates, **kwargs): 
        err, result = self.GetValidates(**kwargs)
        if err != 0:
            return err, result
        result = result[result.index("{\"address"):]
        validators = json.loads(result)
        address = validators["address"]

        for v in nominates:
            if v not in address:
                err, result = 1, "验证集合与提名不符"
        for v in address:
            if v not in nominates:
                err, result = 1, "验证集合与提名不符"

        return err, result

    # 通过共识状态中的验证集，需在修改后3个区块后才能查到
    def CheckConsensusVal(self, nominates, **kwargs):
        err, result = self.xlib.ConsensusStatus()
        if err != 0:
            return err, result
        validators_info = json.loads(result)["validators_info"]
        validators_info = json.loads(validators_info)
        address = validators_info["validators"]
        err = 0
        result = ""
        if sorted(address) != sorted(nominates):
            err = 1
            result = "验证集不符合预期，real: " + str(address) + " expect: " + str(nominates)
        return err, result

        
    