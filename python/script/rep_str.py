##########################################################################
	#  > File Name: rep_str.py
	#  > Author: rogerz
	#  > Mail: rogerzzt@163.com
	#  > Created Time: 五  4/28 08:59:35 2023
 ##########################################################################

#!/usr/bin/env python3

import os
import re

# 设置要查找和替换的字段
old_field = 'rogerz'
new_field = 'rogerzzt'

# 遍历指定目录下的所有子目录和文件
for root, dirs, files in os.walk('/Users/zhangzhitao1/Documents/script/python/script'):
    for file in files:
        # 拼接完整文件路径
        file_path = os.path.join(root, file)
        # 处理文件类型
        if file_path.endswith('.py'):
            # 打开文件，并读取内容
            with open(file_path, 'r') as f:
                text = f.read()
            # 替换字段
            new_text = re.sub(old_field, new_field, text)
            # 生成新文件
            new_file_path = file_path.replace('.py', '_new.py')
            with open(new_file_path, 'w') as f:
                f.write(new_text)
