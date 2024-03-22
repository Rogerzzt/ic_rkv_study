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
import subprocess

# 定义一个测试命令列表和文件夹前缀
macro = []
test = []
timeout = 10

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

# 设置信号处理函数，用于超时后终止子进程
def kill_process(signum, frame):
    global current_command
    print(f"{current_command} timeout")
    results["timeout"].append(current_command)
    current_command = None
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

for i in range(len(macro)):
    for j in range(len(test)):
        command = "make uvm TEST=" + test[j] + " COV=1 MACRO=" + macro[i]

        # 在子进程中异步执行测试命令，并将其输出显示到终端上
        process = subprocess.Popen(command, shell=True, universal_newlines=True,
                                   stdout=subprocess.PIPE, preexec_fn=os.setsid)

        # 注册SIGALRM信号及处理函数
        signal.signal(signal.SIGALRM, kill_process)

        current_command = command
        signal.alarm(timeout)

        while True:
            # 从管道中读取子进程输出并打印到终端上
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

            # 如果输出中包含"TEST PASSED"，记录测试结果并取消超时定时器
            if check_output(output):
                results["passed"].append(current_command)
                print(f"{current_command} passed")
                signal.alarm(0)
                current_command = None
                break

            # 如果当前测试命令已经超时，检查是否还有下一条测试命令
            if current_command is None:
                if len(test) > j+1:
                    j += 1
                    current_command = "make uvm TEST=" + test[j] + " COV=1 MACRO=" + macro[i]
                    signal.alarm(timeout)
                elif len(macro) > i+1:
                    i += 1
                    j = 0
                    current_command = "make uvm TEST=" + test[j] + " COV=1 MACRO=" + macro[i]
                    signal.alarm(timeout)
                else:
                    # 所有测试命令都已执行完毕
                    break

        # 取消超时定时器
        signal.alarm(0)

        # 如果进程没有输出"TEST PASSED"，记录测试结果
        if check_output(output) is False:
            results["failed"].append(current_command)
            print(f"{current_command} failed: {output}")
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

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

