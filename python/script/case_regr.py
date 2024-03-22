'''
	> File Name: case_regr.py
	> Author: rogerz
	> Mail: rogerzzt@163.com
	> Created Time: 三  6/ 7 17:41:11 2023
'''

#!/usr/bin/env python3
import os
import signal

# 定义一个空的命令列表和文件夹前缀
TEST = []

TEST.append("ttu_de1_smoke_test")
TEST.append("ttu_de2_smoke_test")
TEST.append("ttu_de3_smoke_test")
TEST.append("ttu_de4_smoke_test")
TEST.append("ttu_de5_smoke_test")

# 定义信号处理函数
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    exit(0)


# 生成8个不同名称的文件夹和相应的命令
for i in range(len(TEST)):
    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_handler)

    # 创建shell命令
    command = "make uvm TEST=" + TEST[i] + " WAVE=1 COV=1"

    # 执行命令
    os.system(command)

    # 检查是否接收到中断信号
    if signal.getsignal(signal.SIGINT) is not None:
        print('Task was interrupted by user!')
        break

