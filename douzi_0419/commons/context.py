# encoding=utf-8
# @Author   ： 豆子
# @Function ：  上下文管理，正则替换

import re
from douzi_0419.commons.configpar import ConfigPar


class Context:
    @staticmethod
    def find_str(section, target):
        pattern = '#(.*?)#'
        while re.search(pattern, target):
            key = re.search(pattern, target).group(1)
            value = ConfigPar().get(section, key)
            target = re.sub(pattern, value, target, count=1)
        return target
