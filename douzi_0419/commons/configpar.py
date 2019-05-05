# encoding=utf_8
# @Author   ： 豆子
# @Function :  config文件解析

from configparser import ConfigParser
from douzi_0419.commons import filepath
import os


class ConfigPar:
    def __init__(self):
        self.cp = ConfigParser()
        filename = os.path.join(filepath.configs_dir, 'global.conf')
        self.cp.read(filenames=filename, encoding='utf-8')
        if self.cp.getboolean('switch', 'on'):
            self.filename = os.path.join(filepath.configs_dir, 'online.conf')
            self.cp.read(filenames=self.filename, encoding='utf-8')
        else:
            self.filename = os.path.join(filepath.configs_dir, 'test.conf')
            self.cp.read(filenames=self.filename, encoding='utf-8')

    def has_section(self, section):
        if self.cp.has_section(section):
            return True
        else:
            return False

    def get(self, section, option):
        return self.cp.get(section, option)

    def getint(self, section, option):
        return self.cp.getint(section, option)

    def getboolean(self, section, option):
        return self.cp.getboolean(section, option)

    def add_section(self, section):
        self.cp.add_section(section)
        self.write(self.filename)

    def set(self, section, option, value):
        self.cp.set(section, option, value)
        self.write(self.filename)

    def write(self, filename):
        with open(filename, 'w') as f:
            self.cp.write(f)


if __name__ == '__main__':
    # constant_dir = os.path.join(constant.configs_dir, 'test.conf')
    # ConfigPar().get('api', 'url')
    a = ConfigPar().get('api', 'url')
    print(a)
    print(type(a))
