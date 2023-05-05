##########################################################################
	#  > File Name: req_str1.py
	#  > Author: rogerz
	#  > Mail: rogerzzt@163.com
	#  > Created Time: 五  4/28 11:27:27 2023
 ##########################################################################

#!/usr/bin/env python3

import argparse
import os
import re

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='在指定目录下批量替换文件中的某个字段')
parser.add_argument('directory', type=str, help='要处理的目录路径')
parser.add_argument('old_field', type=str, help='要查找的旧字段')
parser.add_argument('new_field', type=str, help='要替换成的新字段')
args = parser.parse_args()

# 遍历指定目录下的所有子目录和文件
for root, dirs, files in os.walk(args.directory):
    for file in files:
        # 拼接完整文件路径
        file_path = os.path.join(root, file)
        # 只处理txt文件
        if file_path.endswith('.py'):
            # 打开文件，并读取内容
            with open(file_path, 'r') as f:
                text = f.read()
            # 替换字段
            new_text = re.sub(args.old_field, args.new_field, text)
            # 输出结果
            print(f'Replaced {args.old_field} with {args.new_field} in {file_path}')
            # 生成新文件
            new_file_path = file_path.replace('.py', '_new.py')
            with open(new_file_path, 'w') as f:
                f.write(new_text)
