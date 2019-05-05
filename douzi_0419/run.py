# encoding=utf_8
# @Author  ： 豆子

import sys
import time
import unittest
import os
from HTMLTestRunner import HTMLTestRunner
from douzi_0419.commons import filepath

# a = sys.path
# print(a)
sys.path.append('./')

discover = unittest.defaultTestLoader.discover(filepath.case_dir, 'test*.py')
now = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
report_name = 'report' + '_' + now + '.html'
report_path = os.path.join(filepath.report_dir, report_name)
with open(report_path, 'wb+') as file:
    runner = HTMLTestRunner(stream=file, title='测试报告', description='api测试')
    runner.run(discover)
