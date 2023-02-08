# !/usr/bin/env python3
"""
Poa类共识测试lib
"""
import os
import json

from .common_lib import Common


class Poa(Common):
    """
    Poa功能库：继承Common的所有方法
    """

    def get_validates(self, **kwargs):
        """
        通过合约查询候选人，在变更后立即可查
        """
        err, result = self.xlib.consensus_invoke(
            type="poa", method="getValidates", **kwargs
        )
        return err, result

    def edit_validates(self, nominates, acl_account, addrs, keys, **kwargs):
        """
        变更候选人，等待3个区块后变更生效，检查矿工是按新的候选人集合选出
        """
        # 写入合约账户的addrs
        self.xclient.write_addrs(acl_account, addrs)

        validates = ";".join(str(x) for x in nominates)
        edit_desc = {"validates": validates}

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "editValidates.desc")
        with open(desc, "w") as edit_val_file:
            json.dump(edit_desc, edit_val_file)
            edit_val_file.close()

        # 发起提名
        err, result = self.xlib.propose(
            type="poa",
            method="editValidates",
            account=acl_account,
            flag="--isMulti",
            desc="editValidates.desc",
            keys=keys,
            **kwargs
        )
        if err != 0:
            return err, result
        txid = result.split("Tx id: ")[1]
        print(txid)

        err, result = self.check_validates(nominates)
        if err != 0:
            return err, result

        # 等待tx上链
        err, result = self.xlib.wait_tx_on_chain(txid)
        if err != 0:
            return err, result

        # tx上链后，在等三个区块后验证
        err, result = self.xlib.wait_num_height(4)
        if err != 0:
            return err, result
        err, result = self.check_consensus_val(nominates)
        return err, result

    def quick_edit_validates(self, nominates, acl_account, addrs, keys, **kwargs):
        """
        快速变更候选人，不等待变更生效
        """
        # 写入合约账户的addrs
        self.xclient.write_addrs(acl_account, addrs)

        validates = ";".join(str(x) for x in nominates)
        edit_desc = {"validates": validates}

        # 创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "editValidates.desc")
        with open(desc, "w") as desc_file:
            json.dump(edit_desc, desc_file)
            desc_file.close()

        # 发起提名
        err, result = self.xlib.propose(
            type="poa",
            method="editValidates",
            account=acl_account,
            flag="--isMulti",
            desc="editValidates.desc",
            keys=keys,
            **kwargs
        )
        return err, result

    def check_validates(self, nominates, **kwargs):
        """
        检查合约中存储的候选人集合
        """
        err, result = self.get_validates(**kwargs)
        if err != 0:
            return err, result
        result = result[result.index('{"address') :]
        validators = json.loads(result)
        address = validators["address"]

        for v in nominates:
            if v not in address:
                err, result = 1, "候选人集合与提名不符"
        for v in address:
            if v not in nominates:
                err, result = 1, "候选人集合与提名不符"

        return err, result

    def check_consensus_val(self, nominates):
        """
        查询共识状态结果中的候选人集合
        """
        err, result = self.xlib.consensus_status()
        if err != 0:
            return err, result
        validators_info = json.loads(result)["validators_info"]
        validators_info = json.loads(validators_info)
        address = validators_info["validators"]
        err = 0
        result = ""
        if sorted(address) != sorted(nominates):
            err = 1
            result = "候选人集合不符合预期，real: " + str(address) + " expect: " + str(nominates)
        return err, result
