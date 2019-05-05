# encoding=utf_8
# @Author  ： 豆子

import unittest
from ddt import ddt, data
from douzi_0419.commons.configpar import ConfigPar
from douzi_0419.commons.context import Context
from douzi_0419.commons.mysqlconnect import MySqlConnect
from douzi_0419.commons import filepath
from douzi_0419.commons.excelparse import ExcelParse
from douzi_0419.commons.testrequest import TestHttpRequest

ep = ExcelParse(filepath.data_dir)
cases = ep.get_cases('register')


@ddt
class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = TestHttpRequest()
        cls.mysql_connect = MySqlConnect()
        cls.section_name = 'register'
        cls.cp = ConfigPar()
        if not cls.cp.has_section(cls.section_name):
            cls.cp.add_section(cls.section_name)
        cls.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def setUp(self):
        sql = 'SELECT MobilePhone FROM future.member  WHERE MobilePhone !="" ORDER BY MobilePhone DESC LIMIT 1'
        self.mobile_phone = self.mysql_connect.fetch_one(sql)[0]
        self.phone = int(self.mobile_phone) + 1
        option_name = 'register'
        self.cp.set(self.section_name, option_name, str(int(self.mobile_phone) + 1))

    def tearDown(self):
        self.mysql_connect.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.mysql_connect.close()

    @data(*cases)
    def test_register(self, case):
        case.data = Context.find_str(self.section_name, case.data)
        try:
            self.session.request(url=case.url, method=case.method, data=case.data, headers=self.headers)
            self.assertEqual(str(case.expected), self.session.get_json_code())
            if self.session.get_json()['msg'] == '注册成功':
                self.cp.set(self.section_name, 'register_s', str(int(self.mobile_phone) + 1))
            result = 'Pass'
        except AssertionError as a:
            result = 'Fail'
            raise a
        finally:
            ep.back_write_by_excel(case.sheet_name, case.case_id, self.session.get_text(), result)


if __name__ == '__main__':
    unittest.main()
