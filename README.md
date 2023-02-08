# Test Xchain
使用pytest框架，搭建xchain的自动化测试用例，覆盖账户、转账、权限、合约、平行链、共识、共识升级、事件订阅等功能点。

## 环境配置
- 操作系统：支持Linux、macos
- 开发语言：Python 3.x
- 依赖包：pytest pyyaml numpy pytz
- 版本控制工具：Git
- 其他：jdk1.8+ go1.13+

## 部署网络，执行测试用例
### 1.部署3节点xchain网络，编译go合约文件
参考文档 https://github.com/xuperchain/xuperchain#run-multi-nodes-blockchain
部署的xchain网络默认使用端口37101、37102、37103，所以自动化用例默认使用的端口也是这三个。
```
git clone https://github.com/xuperchain/xuperchain.git
cd xuperchain && make && make testnet && cd testnet/ && sh control_all.sh start
pwd
cd ../.. && cp xuperchain/output/bin/xchain-cli client/bin/
sleep 15

git clone https://github.com/xuperchain/contract-sdk-go.git
cd contract-sdk-go/example
go build -o ../../client/goTemplate/counter counter/main.go
go build -o ../../client/goTemplate/features features/main.go
```

### 2.配置说明
1. `hosts`和`default_host`是xchain网络各节点的rpcPort端口，按测试的xchain网络修改
2. `account`为xchain网络3节点的公私玥，`data/keys`为node1的公私玥，按测试的xchain网络修改

### 3.运行用例
```
sh run_case.sh basic   # 执行基本功能用例，运行时间约10min
sh run_case.sh highlevel # 执行高阶功能的用例，运行时间约75min
```

### 4.调试用例
```
pytest [-s] cases/***/test_***.py [cases/***/test_***.py] [--type $consensus_type] [-m p0]
```
* --type 在运行共识用例时需配置，支持`tdpos`, `xpos`, `poa`, `xpoa`, `single`. 如不填默认tdpos
* -m 执行特定tag的用例

注意：环境部署成功后，先执行环境检查用例，后调试用例
```
pytest -s case/test_env.py
```

### 5.新增用例
文件命名规范 test_[module]\_[id]\_[用例类别].py，例如test_acc_0_normal.py
