# ===========
# 已部署好tdpos 2节点矿工的xchain
# ===========
basepath=$(cd $(dirname $0); pwd)
cd $basepath

type=$1
args=$2
chain=$3 # case是在xuper还是平行链执行

[ -z "$chain" ] && chain="xuper"

result_dir=${WORKSPACE}/result
[ -z "${WORKSPACE}" ] && result_dir=$basepath/result
rm -rf $result_dir
mkdir -p $result_dir
mkdir -p ./client/output

function showlog()
{
    echo "run failed, logs"
    cat xuperchain/testnet/node1/logs/nohup.out
    tail xuperchain/testnet/node1/logs/xchain.log.wf
}

function checkhealth()
{
    pytest -m "not abnormal" $args cases/test_env.py::TestEnv::test_trunk_height
    if [ $? -ne 0 ];then
        showlog
        exit 1
    fi
}
function basic()
{
    echo "=======账号测试 ======="
    rm ./client/output/* -rf
    pytest -m "not abnormal" $args cases/account --junit-xml=$result_dir/test_account.xml
    checkhealth

    echo "=======acl测试 ======="
    pytest -m "not abnormal" $args cases/acl --junit-xml=$result_dir/test_acl.xml
    checkhealth

    echo "=======转账测试 ======="
    pytest -m "not abnormal" $args cases/transfer --junit-xml=$result_dir/test_transfer.xml
    checkhealth

    echo "=======合约测试 ======="
    pytest -m "not abnormal" $args cases/contract --junit-xml=$result_dir/test_contract.xml
    checkhealth

    echo "=======事件测试 ======="
    pytest -m "not abnormal" $args cases/event --junit-xml=$result_dir/test_event.xml
    checkhealth

    echo "=======基本功能测试完成======="
}

function pchain_test()
{
    # 平行链测试，如果在平行链执行，跳过下面的case
    if [ "$chain" == "xuper" ];then
        echo "=======平行链测试======="
        pytest -m "not abnormal" $args cases/parachain --junit-xml=$result_dir/test_parachain.xml
        checkhealth
        echo "=======平行链测试完成======="
    fi
}

function update_test()
{
    echo "=======共识升级测试======="
    pytest -m "not abnormal" $args cases/update --junit-xml=$result_dir/test_update.xml
    checkhealth
}

function tdpos_test()
{
    echo "=======升级共识：tdpos 2矿工 ======="
    pytest -m "not abnormal" cases/update/test_update_0_normal.py::TestUpdateCons::test_case01
    checkhealth
    echo "=======tdpos共识测试 ======="
    pytest -m "not abnormal" $args cases/consensus/tdpos --type tdpos --junit-xml=$result_dir/test_tdpos.xml
    checkhealth
}

function xpos_test()
{
    echo "=======升级共识：xpos 2矿工 ======="
    pytest -m "not abnormal" cases/update/test_update_0_normal.py::TestUpdateCons::test_case06
    checkhealth
    echo "=======xpos共识测试 ======="
    pytest -m "not abnormal" $args cases/consensus/tdpos --type xpos --junit-xml=$result_dir/test_xpos.xml
    checkhealth
}

function poa_test()
{
    echo "=======升级共识：poa 2矿工 ======="
    pytest -m "not abnormal" cases/update/test_update_0_normal.py::TestUpdateCons::test_case02
    checkhealth
    echo "=======poa共识测试 ======="
    pytest -m "not abnormal" $args cases/consensus/poa --type poa --junit-xml=$result_dir/test_poa.xml
    checkhealth
}

function xpoa_test()
{
    echo "=======升级共识：xpoa 2矿工 ======="
    pytest -m "not abnormal" cases/update/test_update_0_normal.py::TestUpdateCons::test_case04
    checkhealth
    echo "=======xpoa共识测试 ======="
    pytest -m "not abnormal" $args cases/consensus/poa --type xpoa --junit-xml=$result_dir/test_xpoa.xml
    checkhealth
}

function single_test()
{
    echo "=======升级共识：single ======="
    pytest -m "not abnormal" cases/update/test_update_0_normal.py::TestUpdateCons::test_case08
    checkhealth
    echo "=======single共识测试 ======="
    pytest -m "not abnormal" $args cases/consensus/single --junit-xml=$result_dir/test_single.xml
    checkhealth
}

function contractsdk_test()
{
    echo "=======合约sdk测试 ======="
    pytest -m "not abnormal" $args cases/contractsdk --junit-xml=$result_dir/test_contractsdk.xml
    checkhealth
}

echo "=======测试环境准备======="
pytest -m "not abnormal" $args cases/test_env.py --junit-xml=$result_dir/test_env.xml
checkhealth

if [ "$type" == "basic" ];then
    basic
elif [ "$type" == "middlelevel" ];then
    update_test
elif [ "$type" == "highlevel" ];then
    contractsdk_test
    pchain_test
    single_test
    poa_test
    xpoa_test
    tdpos_test
    xpos_test
else
    echo "please input args: basic or highlevel"
fi

err=$(cat result/*|grep "failure message"|wc -l)
if [ $err -ne 0 ];then
    showlog
fi
exit $err
