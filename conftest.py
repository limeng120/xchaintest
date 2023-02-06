"""
Auther：Ethan

pytest的测试配置文件（本文件不可以重命名）
"""
import pytest

from libs import config_lib as config

from libs.tdpos_lib import Tdpos
from libs.xpos_lib import Xpos
from libs.poa_lib import Poa
from libs.xpoa_lib import Xpoa
from libs.common_lib import Common


def pytest_addoption(parser):
    """
    给pytest命令添加--type字段，用于声明当前共识的类型
    """
    parser.addoption("--type", action="store", default="", help="consensus type_arg")


class PosTest:
    """
    tdpos xpos共识测试
    """

    file = "conf/conf.yaml"
    conf = config.Get(file)

    host = conf.default_host
    # 合约账户
    account_name = "1234432112344321"
    acl_account = "XC" + account_name + "@" + conf.name

    # 查看tdpos.json获取当前一个term的block_num, proposer_num
    block_num = 10
    proposer_num = 2

    # 一个term最多只可能有（block_num * proposer_num）个区块，可以取最值用来验证是否生效
    term_height = block_num * proposer_num

    # 各节点的keys和addrs数组
    keys = conf.keys
    addrs = conf.addrs
    node1, node2, node3 = addrs[0], addrs[1], addrs[2]
    key1, key2, key3 = keys[0], keys[1], keys[2]

    # 选取一个候选人，修改最后一位, 构造一个不存在的地址，用来验证一些异常情况
    wrong_candidate = node1[:-1] + str(ord(node1[-1]) + 1)

    # 当前client的默认账户地址，通过config读出
    client_addr = conf.client_addr
    client_key = conf.client_key

    # 用于投票的个人账户key，addr, 验证时需要（这里默认为client的data/keys)
    vote_addr = conf.client_addr
    key_addr = conf.client_key


class PoaTest:
    """
    poa xpoa共识测试
    """

    file = "conf/conf.yaml"
    conf = config.Get(file)

    host = conf.default_host
    hosts = conf.hosts

    # 各节点的keys和addrs数组
    keys = conf.keys
    addrs = conf.addrs
    node1, node2, node3 = addrs[0], addrs[1], addrs[2]
    key1, key2, key3 = keys[0], keys[1], keys[2]
    host1, host2, host3 = hosts["node1"], hosts["node2"], hosts["node3"]

    # 只包含node1的合约账户
    acc11 = {
        "account_name": "1111111111111111",
        "acl_account": "XC1111111111111111@" + conf.name,
        "keys": [key1],
        "addrs": [node1],
    }

    # 只包含node3的合约账户
    acc33 = {
        "account_name": "3333333333333333",
        "acl_account": "XC3333333333333333@" + conf.name,
        "keys": [key3],
        "addrs": [node3],
    }

    # node1与node2的合约账户
    acc12 = {
        "account_name": "1111222211112222",
        "acl_account": "XC1111222211112222@" + conf.name,
        "keys": [key1, key2],
        "addrs": [node1, node2],
    }

    # node2与node3的合约账户
    acc23 = {
        "account_name": "2222333322223333",
        "acl_account": "XC2222333322223333@" + conf.name,
        "keys": [key2, key3],
        "addrs": [node2, node3],
    }

    # node1与node3的合约账户
    acc13 = {
        "account_name": "1111333311113333",
        "acl_account": "XC1111333311113333@" + conf.name,
        "keys": [key1, key3],
        "addrs": [node1, node3],
    }

    # node1，node2，node3的合约账户
    acc123 = {
        "account_name": "1111222233331111",
        "acl_account": "XC1111222233331111@" + conf.name,
        "keys": [key1, key2, key3],
        "addrs": [node1, node2, node3],
    }


class BasicTest:
    """
    共识以外的其他case使用
    """

    file = "conf/conf.yaml"
    conf = config.Get(file)

    host = conf.default_host
    client_path = conf.client_path
    client_addr = conf.client_addr

    # 合约部署账户
    account = "2111111111111111"

    # 多签名账户
    account_aks = "2111111111111112"

    # 各节点的keys和addrs数组
    keys = conf.keys
    addrs = conf.addrs
    node1, node2, node3 = addrs[0], addrs[1], addrs[2]
    key1, key2, key3 = keys[0], keys[1], keys[2]

    # 使用gm或者默认加密
    crypto = conf.crypto


@pytest.fixture(scope="session")
def input_args(request):
    """
    指定scope为session，即所有测试文件共用一个input_args实例
    """
    # 获取共识类型
    type_arg = request.config.getoption("--type")

    if type_arg == "tdpos":
        # 配置测试的基本参数
        case = PosTest
        # 初始化一个tdpos的测试实例
        case.test = Tdpos(case.conf)

    elif type_arg == "xpos":
        case = PosTest
        case.test = Xpos(case.conf)

    elif type_arg == "poa":
        case = PoaTest
        case.test = Poa(case.conf)

    elif type_arg == "xpoa":
        case = PoaTest
        case.test = Xpoa(case.conf)

    else:
        case = BasicTest
        case.test = Common(case.conf)

    return case
