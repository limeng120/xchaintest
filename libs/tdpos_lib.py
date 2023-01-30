# !/usr/bin/env python3
"""
tdpos共识常用的函数库
包括：
1. 共识状态查询
2. tdpos 提案、投票信息查询
3. 代币初始化
4. 执行多签
5. 提案发起（校验是否多签）
6. 提名多名候选人（默认需要多签，校验结果）
7. 给多个候选人投票（默认不需要多签名，采用访问节点的默认账户投票，校验结果）

由于提名，投票，撤销等操作，读取共识状态要等到三个区块之后，为了验证，在这些功能函数里都有等4个区块高度的操作
"""

import json
import os
import time
import numpy as np
from .common_lib import Common

class Tdpos(Common):
    """
    Tdpos的常用功能库
    """

    def __init__(self, conf):
        super().__init__(conf)

    # 获取候选人提名、投票、撤销的明细（返回字典类型数据，默认全部，可以指定类型）
    def GetTdposInfos(self, type="", **kwargs):
        """
        type: "nominate", "vote", "revoke"
        """
        #获取当前的共识状态
        err, result = self.xlib.ConsensusInvoke(type="tdpos", method="getTdposInfos", **kwargs)
        if err != 0:
            return err, result

        if result[result.index("{"):] == "{}":
            contract = {}
        else:
            contract = json.loads(result[result.index("{"):])

        # 如果是空白，增加对应的字段
        for i in ["nominate", "vote", "revoke"]:
            if i not in contract.keys():
                contract[i] = {}

        if type != "":
            return err, contract[type]
        else:
            return err, contract

    # 快速提名，不含结果校验(默认多签名，如不想多签，在测试case里调用底层propose函数)
    def QuickNominate(self, candidate, amount, proposer, keys, **kwargs):
        nominate_desc = {
            "candidate": candidate,
            "amount": str(amount)
        }

        desc = os.path.join(self.conf.client_path, "nominate.desc")
        with open(desc, "w") as f:
            json.dump(nominate_desc, f)
            f.close()
    
        err, result = self.xlib.Propose(type="tdpos", method="nominateCandidate", \
            flag="--isMulti", account=proposer, desc="nominate.desc", keys=keys, **kwargs)
        return err, result

    # 快速投票，不含结果校验(如不多签)
    def QuickVote(self, candidate, amount, proposer, keys, **kwargs):
        vote_desc = {
            "candidate": candidate,
            "amount": str(amount)
        }
        #创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "vote.desc")
        with open(desc, "w") as f:
            json.dump(vote_desc, f)
            f.close()

        # 判断是否和合约账户投票
        if "flag" in kwargs.keys() and kwargs["flag"] == "--isMulti":
            #执行投票
            err, result = self.xlib.Propose(type="tdpos", method="voteCandidate", \
                desc="vote.desc", account=proposer, keys=keys, **kwargs)
            return err, result
        else:
            #执行投票
            err, result = self.xlib.Propose(type="tdpos", method="voteCandidate", desc="vote.desc", keys=keys, **kwargs)
            return err, result

    # 快速撤销投票，不含结果校验
    def QuickRevokeVote(self, candidate, amount, proposer, keys, **kwargs):
        revoke_desc = {
            "candidate": candidate,
            "amount": str(amount)
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "revokeVote.desc")
        with open(desc, "w") as f:
            json.dump(revoke_desc, f)
            f.close()

        # 判断是否合约账户撤销投票
        if "flag" in kwargs.keys() and kwargs["flag"] == "--isMulti":
            #执行撤销
            err, result = self.xlib.Propose(type="tdpos", method="revokeVote", \
                desc="revokeVote.desc", account=proposer, keys=keys, **kwargs)
            return err, result
        else:
            err, result = self.xlib.Propose(type="tdpos", method="revokeVote", \
                desc="revokeVote.desc", keys=keys, **kwargs)
            return err, result

    # 快速撤销候选人，不含结果校验(默认多签名，如不想多签，在测试case里调用底层propose函数)
    def QuickRevokeNominate(self, candidate, proposer, keys, **kwargs):
        revoke_desc = {
            "candidate": candidate
        }

        #创建一个临时文件来保存desc文件
        desc = os.path.join(self.conf.client_path, "revokeNominate.desc")
        with open(desc, "w") as f:
            json.dump(revoke_desc, f)
            f.close()
            
        err, result = self.xlib.Propose(type="tdpos", method="revokeNominate", \
            account=proposer, desc="revokeNominate.desc", keys=keys, **kwargs)
        return err, result

    #提名候选人
    def Nominate(self, candidate, amount, proposer, keys, **kwargs):
        # 提名候选人前的冻结代币，共识状态
        err, frozen_before = self.xlib.GetFrozenToken(proposer)
        err, consensus_before = self.GetTdposInfos()

        err, result = self.QuickNominate(candidate, amount, proposer, keys, **kwargs)
        if err != 0:
            return err, result

        # 验证提名前后的冻结代币变化
        err, frozen_after = self.xlib.GetFrozenToken(proposer)
        if int(frozen_after) - int(frozen_before) != int(amount):
            err, result = 1, "提名前后 冻结代币变化不符合预期"

        # 验证提名前后的共识状态变化
        detail = {
            "type": "nominate",
            "candidate": candidate,
            "proposer": proposer,
            "amount": amount
        }
        err, result = self.CheckTdposInfos(consensus_before, detail)
        return err, result

    #投票
    def Vote(self, candidate, amount, proposer, keys, **kwargs):

        # 提名候选人前的冻结代币，共识状态
        err, frozen_before = self.xlib.GetFrozenToken(proposer)
        err, consensus_before = self.GetTdposInfos()

        err, result = self.QuickVote(candidate, amount, proposer, keys, **kwargs)
        if err != 0:
            return err, result

        # 验证投票前后的冻结代币变化
        err, frozen_after = self.xlib.GetFrozenToken(proposer)
        if frozen_after - frozen_before != amount:
            err, result = 1, "提名前后 冻结代币变化不符合预期" 

        # 验证提名前后的共识状态变化
        detail = {
            "type": "vote",
            "candidate": candidate,
            "proposer": proposer,
            "amount": amount
        }
        err, result = self.CheckTdposInfos(consensus_before, detail)
        return err, result

    #撤销投票
    def RevokeVote(self, candidate, amount, proposer, keys, **kwargs):
        # 撤销投票前的冻结代币
        err, frozen_before = self.xlib.GetFrozenToken(proposer)
        err, consensus_before = self.GetTdposInfos()

        err, result = self.QuickRevokeVote(candidate, amount, proposer, keys, **kwargs)
        if err != 0:
            return err, result

        # 验证撤销投票后的冻结代币
        err, frozen_after = self.xlib.GetFrozenToken(proposer)
        change = frozen_before - frozen_after
        if change != amount:
            err, result = 1, "撤销投票失败，账户的冻结代币没有解冻"

        # 验证共识状态
        detail = {
            "type": "revoke_vote",
            "candidate": candidate,
            "proposer": proposer,
            "amount": amount
        }
        err, result = self.CheckTdposInfos(consensus_before, detail)
        return err, result
        
    # 撤销候选人
    def RevokeNominate(self, candidate, proposer, keys, **kwargs):
        """
        candidate：被撤销的候选人
        proposer： 提案发起人
        keys：     签名用的key，支持单签、多签
        flag：     设为--isMulti,是多签，其他是单签
        """
        # 撤销候选人前的冻结代币
        err, frozen_before = self.xlib.GetFrozenToken(proposer)
        err, consensus_before = self.GetTdposInfos()

        err, result = self.QuickRevokeNominate(candidate, proposer, keys, **kwargs)
        if err != 0:
            return err, result

        # 获取候选人被提名时的冻结代币数量，用于校验冻结代币变化
        amount = consensus_before["nominate"][candidate][proposer]

        # 验证撤销候选人后的冻结代币
        err, frozen_after = self.xlib.GetFrozenToken(proposer)
        change = frozen_before - frozen_after
        if change != amount:
            err, result = 1, "撤销投票失败，账户的冻结代币没有解冻"

        # 验证共识状态
        detail = {
            "type": "revoke_nominate",
            "candidate": candidate,
            "proposer": proposer
        } 
        err, result = self.CheckTdposInfos(consensus_before, detail)     
        return err, result

    # 验证期望的validators与实际的是否一致
    def CheckValidators(self, validators, **kwargs):
        #获取当前的共识状态
        err, result = self.xlib.ConsensusStatus(**kwargs)
        if err != 0:
            return err, result

        #获取候选人状态，nominate在两层封装的json里，所以要loads两次
        consensus = json.loads(result)
        validators_info = json.loads(consensus["validators_info"])
        validators_now = validators_info["validators"]
        
        for v in validators:
            if v not in validators_now:
                err, result = 1, "票数TopK的候选人没有生效：" 

        for v in validators_now:
            if v not in validators:
                err, result = 1, "票数TopK的候选人没有生效："             

        return err, result

    # 验证执行一个操作前后共识状态
    def CheckTdposInfos(self, consensus_before, detail, **kwargs):

        candidate = detail["candidate"]
        err, consensus_after = self.GetTdposInfos(**kwargs) 

        # 如果没有进行过相关操作，初始化一个空字典
        if detail["type"] not in consensus_before.keys():
            consensus_before[detail["type"]] = {}

        # 提名状态验证
        if detail["type"] == "nominate":
            
            nominate1, nominate2 = consensus_before["nominate"], consensus_after["nominate"]

            proposer = detail["proposer"]
            amount = detail["amount"]

            if candidate in nominate1.keys():
                # 由于目前只支持一次提名，这里不会用到
                nominate1[candidate].append([{proposer:amount}])
            else:
                nominate1[candidate] = {proposer: amount}

            err = 1 if nominate1 != nominate2 else 0

        # 投票状态的验证
        elif detail["type"] == "vote":

            vote1, vote2 = consensus_before["vote"], consensus_after["vote"]
            amount = detail["amount"]
            proposer = detail["proposer"]

            if candidate in vote1.keys():
                if proposer in vote1[candidate].keys():
                    # 考虑票全被撤回的情况
                    if vote1[candidate][proposer] == "":
                        vote1[candidate][proposer] = 0
                    
                    vote1[candidate][proposer] += amount
                
                else:
                    vote1[candidate][proposer] = amount
           
            else:
                vote1[candidate] = {proposer: amount}

            err = 1 if vote1 != vote2 else 0

        # 撤销投票状态验证
        elif detail["type"] == "revoke_vote":
            
            # 校验撤销投票状态
            revoke1, revoke2 = consensus_before["revoke"], consensus_after["revoke"]
            amount = detail["amount"]
            proposer = detail["proposer"]    

            dict = {
                "RevokeType":"vote",
                "Ballot": amount,
                "TargetAddress": candidate
            }

            if proposer in revoke1.keys():
                revoke1[proposer].append(dict)
            else:
                revoke1[proposer] = [dict]

            err = 1 if revoke1 != revoke2 else 0 

            # 同时校验撤销导致的投票状态变更
            vote1, vote2 = consensus_before["vote"], consensus_before["vote"]
            amount = detail["amount"]
            proposer = detail["proposer"]

            vote1[candidate][proposer] -= amount
            if vote1 != vote2:
                err = 1
        
        # 撤销候选人状态验证
        elif detail["type"] == "revoke_nominate":

            proposer = detail["proposer"]    

            # 校验候选人的状态变更
            nominate1, nominate2 = consensus_before["nominate"], consensus_after["nominate"]

            amount = consensus_before["nominate"][candidate][proposer]
            
            err = 1 if candidate in nominate2.keys() else 0     

            # 校验撤销投票状态
            revoke1, revoke2 = consensus_before["revoke"], consensus_after["revoke"]

            dict = {
                "RevokeType":"nominate",
                "Ballot": amount,
                "TargetAddress": candidate
            }

            if proposer in revoke1.keys():
                revoke1[proposer].append(dict)
            else:
                revoke1[proposer] = [dict]

            if revoke1 != revoke2:
                err = 1
                
        result = "共识状态在操作后不符合预期" if err == 1 else "一致"
        return err, result

    # 验证链的状态，自定义对区块高度和分叉率的要求
    def CheckChainStatus(self, **kwargs):
        # 查询区块高度是否一致(标准差小于3)
        err, height = self.TrunkHeight(**kwargs)
        if np.std(height) > 3:
            err, result = 1, "区块高度不一致"
        else:
            result = " ".join(str(x) for x in height)
        
        # 查询分叉率
        err, br = self.BifurcationRatio(**kwargs)
        if err != 0:
            result = br
        else:
            result = " ".join(str(x) for x in br)
        
        return err, result

    # 清理所有vote和nominate
    # 由于前面用例用node1和合约账号发起提名和投票，只考虑revoke这两个账户
    def clearVoteNominate(self):
        err, vote = self.GetTdposInfos("vote") 
        if err != 0:
            return err, vote
       
        for addr, record in vote.items():
            for initiator, amount in record.items():
                if initiator == self.conf.addrs[0]:
                    key = self.conf.keys[0]
                    err, result = self.QuickRevokeVote(addr, amount, initiator, key)
                    if err != 0:
                        return err, result
                else:
                    key = self.conf.keys
                    err, result = self.QuickRevokeVote(addr, amount, initiator, key)
                    if err != 0:
                        return err, result
                # 等待tx上链
                txid = self.xlib.GetTxidFromRes(result)
                err, result = self.xlib.WaitTxOnChain(txid)
                if err != 0:
                        return err, result              

        err, vote = self.GetTdposInfos("vote")   
        if err != 0:
            return err, vote
        for v in vote.values():
            if v:
                return 1, "清理后，投票非空：" + str(vote)
        
        err, nominate = self.GetTdposInfos("nominate")   
        if err != 0:
            return err, nominate
        
        for addr, record in nominate.items():
            for initiator in record.keys():
                if initiator == self.conf.addrs[0]:
                    key = self.conf.keys[0]
                    err, result = self.QuickRevokeNominate(addr, initiator, key)
                    if err != 0:
                        return err, result
                else:
                    key = self.conf.keys
                    err, result = self.QuickRevokeNominate(addr, initiator, key, flag="--isMulti")
                    if err != 0:
                        return err, result
                # 等待tx上链
                txid = self.xlib.GetTxidFromRes(result)
                err, result = self.xlib.WaitTxOnChain(txid)
                if err != 0:
                    return err, result              

        err, nominate = self.GetTdposInfos("nominate") 
        if err != 0:
            return err, nominate
        if nominate:
            return 1, "清理后，提名非空"
        
        self.xlib.WaitNumHeight(1)
        return 0, ""

    def waitTermChange(self, targetTerm):
        """
        等待term变更到targetTerm
        """
        print("targetTerm: " + str(targetTerm))
        #获取当前的共识状态
        err, result = self.xlib.ConsensusStatus()
        if err != 0:
            return err, "查询consensus status 失败：" + result

        # 获取当前term，等待term改变
        consensus = json.loads(result)
        validators_info = json.loads(consensus["validators_info"])
        term = validators_info["curterm"]
        print("term: " + str(term)) 
        retry = 1
        while str(term) != str(targetTerm) and retry < 100:
            time.sleep(3)
            assert err == 0, result
            err, result = self.xlib.ConsensusStatus()
            assert err == 0, result
            consensus = json.loads(result)
            validators_info = json.loads(consensus["validators_info"])
            term = validators_info["curterm"]
            print("term: " + str(term))
            retry = retry + 1
        if retry == 100:
            return 1, "未等到term变更为" + str(targetTerm)
        else:
            print("已经进入targetTerm:" + str(targetTerm))
            return 0, ""
        
        