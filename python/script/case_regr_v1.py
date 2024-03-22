'''
	> File Name: case_regr_v1.py
	> Author: rogerz
	> Mail: rogerzzt@163.com
	> Created Time: 四  6/ 8 08:40:07 2023
'''

#!/usr/bin/env python3
import os
import re
import signal
import datetime

# 定义一个测试命令列表和文件夹前缀
macro = []
test = []

macro.append("DEF_TCC_TTU_AT")
test.append("ttu_de1_smoke_test")

# 定义测试结果
results = {
    "passed": [],
    "timeout": [],
    "failed": []
}

# 定义一个函数用于检查shell输出是否包含"TEST PASSED"
def check_output(output):
    return re.search("TEST PASSED", output) is not None

# 定义一个函数用于执行测试命令
def run_command(command):
    # 使用 os.system 执行命令
    return_code = os.system(command)

    # 检查命令的返回值，记录测试结果
    if return_code == 0:
        results["passed"].append(command)
    elif return_code < 0:
        results["timeout"].append(command)
    else:
        results["failed"].append(command)


# 循环执行测试命令列表中的每条命令
for i in range(len(macro)):
    for j in range(len(test)):
        command = "make uvm TEST=" + test[j] + " COV=1 MACRO=" + macro[i]
        run_command(command)

# 输出测试结果
print("Test results:")
print("Passed: %d" % len(results["passed"]))
print("\n".join("- " + c for c in results["passed"]))
print()
print("Timeout: %d" % len(results["timeout"]))
print("\n".join("- " + c for c in results["timeout"]))
print()
print("Failed: %d" % len(results["failed"]))
print("\n".join("- " + c for c in results["failed"]))


# 获取当前时间并格式化为字符串
now = datetime.datetime.now()
time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# ���建日志目录
log_dir = f"test_result_{time_str}"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# ���建日志文件名
log_file = os.path.join(log_dir, f"test_result_{time_str}.log")

# 打开文件并写入测试结果
with open(log_file, "w") as f:
    f.write("Test results:\n")
    f.write(f"Passed: {len(results['passed'])}\n")
    f.write("\n".join(f"- {c}" for c in results["passed"]))
    f.write("\n\n")
    f.write(f"Timeout: {len(results['timeout'])}\n")
    f.write("\n".join(f"- {c}" for c in results["timeout"]))
    f.write("\n\n")
    f.write(f"Failed: {len(results['failed'])}\n")
    f.write("\n".join(f"- {c}" for c in results["failed"]))

print(f"测试结果已保存到文件 '{log_file}' 中。")
