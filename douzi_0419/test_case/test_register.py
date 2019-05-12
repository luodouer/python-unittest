# encoding=utf_8
# @Author   ： 豆子
# @Function :  账号注册

import unittest
from ddt import ddt, data
from douzi_0419.commons.configpar import ConfigPar
from douzi_0419.commons.context import Replace
from douzi_0419.commons.page import RandomChoice
from douzi_0419.commons.logprase import Logger
from douzi_0419.commons.mysqlconnect import MySqlConnect
from douzi_0419.commons import constant
from douzi_0419.commons.excelparse import ExcelParse
from douzi_0419.commons.testrequest import TestHttpRequest

ep = ExcelParse(constant.data_dir)
cases = ep.get_cases('register')
pwd_length_case_id = 1


@ddt
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = TestHttpRequest()
        cls.mysql_connect = MySqlConnect()
        cls.section_name = 'data'
        cls.cp = ConfigPar(constant.basedata_dir)
        if not cls.cp.has_section(cls.section_name):
            cls.cp.add_section(cls.section_name)
        cls.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        cls.logger = Logger(__name__)

    def setUp(self):
        global pwd_length_case_id
        p = True
        while p:
            phone_sql = 'SELECT MobilePhone FROM future.member  WHERE MobilePhone !="" ORDER BY MobilePhone LIMIT 1'
            self.mobile_phone = self.mysql_connect.fetch_one(phone_sql)['MobilePhone']
            self.phone = int(self.mobile_phone) + RandomChoice.random_choice_one(1, 1000)
            self.count_sql = 'SELECT COUNT(*) count FROM future.member WHERE MobilePhone="{}"'.format(self.phone)
            p = self.mysql_connect.fetch_one(self.count_sql)['count']

        self.logger.info('注册用例执行之前，{} 手机号尚未注册'.format(self.phone))
        if pwd_length_case_id == 4:
            self.pwd = RandomChoice.random_more_str(5)
        elif pwd_length_case_id == 5:
            self.pwd = RandomChoice.random_more_str(19)
        elif pwd_length_case_id == 6:
            self.pwd = RandomChoice.random_more_str(6)
        elif pwd_length_case_id == 7:
            self.pwd = RandomChoice.random_more_str(18)
        else:
            self.pwd = RandomChoice.random_more_str(8)

        option_user = 'register_user'
        option_pwd = 'register_pwd'
        self.cp.set(self.section_name, option_user, str(self.phone))
        self.cp.set(self.section_name, option_pwd, self.pwd)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.mysql_connect.close()
        cls.logger.clear_handler()

    @data(*cases)
    def test_register(self, case):
        global pwd_length_case_id
        case.data = Replace.find_str(self.section_name, case.data)

        try:
            self.session.request(url=case.url, method=case.method, data=case.data, headers=self.headers)
            self.assertEqual(str(case.expected), self.session.get_json_code())
            new_user = self.mysql_connect.fetch_one(self.count_sql)['count']
            if self.session.get_json()['msg'] == '注册成功':
                self.cp.set(self.section_name, 'register_user_s', str(self.phone))
                self.cp.set(self.section_name, 'register_pwd_s', self.pwd)
                self.assertEqual(1, new_user)
                self.logger.info('手机号码 {} 注册成功，对应手机号的登陆密码是：{}'.format(self.phone, self.pwd))
            else:
                self.assertEqual(0, new_user)
            result = 'Pass'
        except AssertionError as a:
            self.logger.exception()
            result = 'Fail'
            raise a
        finally:
            self.logger.info('测试模块：{}，测试用例id：{}，测试目的：{}，请求响应结果：{}，执行结果：{}'.
                             format(case.sheet_name, case.case_id, case.title, self.session.get_text(), result))
            ep.back_write_by_excel(case.sheet_name, case.case_id, self.session.get_text(), result)
            pwd_length_case_id = case.case_id + 1


if __name__ == '__main__':
    unittest.main()
