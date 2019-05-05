# encoding=utf_8
# @Author   ： 豆子
# @Function :  文件路径

import os

# 上2级目录
base_dir = os.path.dirname(os.path.dirname(__file__))

# configs目录
configs_dir = os.path.join(base_dir, 'configs')

# common文件目录
commons_dir = os.path.join(base_dir, 'commons')

# 测试结果目录
result_dir = os.path.join(base_dir, r'results')
# logs目录
log_dir = os.path.join(result_dir, 'logs')
# 测试报告目录
report_dir = os.path.join(result_dir, 'reports')

# 测试用例目录
case_dir = os.path.join(base_dir, 'test_case')

# 测试数据目录
data_dir = os.path.join(base_dir, 'test_data', 'cases.xlsx')

