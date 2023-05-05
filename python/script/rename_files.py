'''
	> File Name: rep_str2.py
	> Author: rogerz
	> Mail: rogerzzt@163.com
	> Created Time: 五  5/ 5 11:33:35 2023
'''

#!/usr/bin/env python3

import argparse
import os
import re

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='在指定目录下批量替换文件中的某个字段')
parser.add_argument('directory', type=str, help='要处理的目录路径')
parser.add_argument('old_field', type=str, help='要查找的旧字段')
parser.add_argument('new_field', type=str, help='要替换成的新字段')
parser.add_argument('--rename-dir', action='store_true', default=False, help='是否修改文件夹名称')
parser.add_argument('--rename-file', action='store_true', default=False, help='是否修改内部文件名称')
args = parser.parse_args()

# 修改文件夹名称
if args.rename_dir:
    # 获取目录所在的上级目录路径
    parent_dir = os.path.dirname(args.directory)
    # 拼接重命名后的目录路径
    new_directory_path = os.path.join(
        parent_dir, args.directory.replace(os.path.basename(args.directory), args.new_field))
    # 重命名目录
    os.rename(args.directory, new_directory_path)
    print(f"Renamed directory {args.directory} to {os.path.basename(new_directory_path)}")

# 遍历指定目录下的所有子目录和文件
for root, dirs, files in os.walk(args.directory):
    for file in files:
        # 拼接完整文件路径
        file_path = os.path.join(root, file)
        # 替换内部文件名称
        if args.rename_file:
            # 拼接重命名后的文件路径
            new_file_path = os.path.join(
                root, file.replace(args.old_field, args.new_field))
            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"Renamed file {file} to {os.path.basename(new_file_path)}")
            file_path = new_file_path

        # 只处理txt文件
        if file_path.endswith('.txt'):
            # 打开文件，并读取内容
            with open(file_path, 'r') as f:
                text = f.read()
            # 替换字段
            new_text = re.sub(args.old_field, args.new_field, text)
            # 输出结果
            print(f'Replaced {args.old_field} with {args.new_field} in {file_path}')
            # 生成新文件
            new_file_path = file_path.replace('.txt', '_new.txt')
            with open(new_file_path, 'w') as f:
                f.write(new_text)

            # 替换内部文件名称及其内容
            if args.rename_file:
                # 拼接重命名后的文件路径
                new_file_path = os.path.join(
                    root, file.replace(args.old_field, args.new_field))
                # 生成重命名后的新文件路径
                new_file_path = new_file_path.replace('.txt', '_new.txt')
                # 重命名文件
                os.rename(new_file_path, new_file_path.replace('_new.txt', '.txt'))
                print(f"Renamed file {os.path.basename(new_file_path)} to {os.path.basename(new_file_path).replace('_new.txt', '.txt')}")
