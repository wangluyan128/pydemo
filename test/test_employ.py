#coding = utf-8
import unittest
from employ import Employee
class TestEmploy(unittest.TestCase):
    def setUp(self):
        self.people = Employee("ZHU","Fangya",2000)
        self.salary = [7000,12000]
    def test_give_default_raise(self):
        self.assertEqual(self.people.give_raise(),self.salary[0])
    def test_give_custome_raise(self):
        self.default = 10000
        self.assertEqual(self.people.give_raise(default=10000),self.salary[1])
'''
if __name__=="__main__":
    if __name__ == '__main__':
        unittest.main()
'''