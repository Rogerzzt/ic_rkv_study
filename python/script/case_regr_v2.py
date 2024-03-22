'''
	> File Name: case_regr_v2.py
	> Author: rogerz
	> Mail: rogerzzt@163.com
	> Created Time: 四  6/ 8 10:04:37 2023
'''

#!/usr/bin/env python3
import os
import re
import signal
import datetime
import subprocess

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
    # 检查命令的输出是否包含"TEST PASSED"
    return re.search("TEST PASSED", output) is not None

# 定义一个函数用于执行测试命令
def run_command(command, timeout):
    try:
        # 使用 subprocess.run 执行命令并指定超时时间
        result = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        output = result.stdout.decode('utf-8')

        # 检查命令的返回值，记录测试结果
        if result.returncode == 0 and check_output(result.stdout):
            results["passed"].append(command)
        else:
            results["failed"].append(command)

    except subprocess.TimeoutExpired:
        # 如果命令执行超时，则记录测试结果
        results["timeout"].append(command)
        print(f"Command '{command}' timed out.")

    except Exception as e:
        # 如果命令执行过程中发生其他异常，则记录测试结果
        results["failed"].append(command)
        print(f"Command '{command}' failed with error: {e}")


# 循环执行测试命令列表中的每条命令
for i in range(len(macro)):
    for j in range(len(test)):
        # 将命令拆分成一个由字符串组成的列表
        command_list = ["make", "uvm", "TEST=" + test[j], "COV=1", "MACRO=" +
                        macro[i]]

run_command(command_list, timeout=60)  # 设置每个命令的超时时间为60秒

# 输出测试结果
print("Test results:")
print(f"Passed: {len(results['passed'])}")
print("\n".join("- " + c for c in results["passed"]))
print()
print(f"Timeout: {len(results['timeout'])}")
print("\n".join("- " + c for c in results["timeout"]))
print()
print(f"Failed: {len(results['failed'])}")
print("\n".join("- " + c for c in results["failed"]))


# 获取当前时间并格式化为字符串
now = datetime.datetime.now()
time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# 建立日志目录
log_dir = f"test_result_{time_str}"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# 建立日志文件名
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
