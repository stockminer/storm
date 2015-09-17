#encoding=utf-8
'''
Created on 2015年9月17日

@author: Yafei
'''
import sys
sys.path.append('..')
import unittest
from crawler.job_factory import *
from conf.config import *

class Test(unittest.TestCase):

    #初始化工作 
    def setUp(self):
        self.conf = Config()

    #退出清理工作 
    def tearDown(self):
        pass

    #具体的测试用例，一定要以test开头
    #测试抓取概念信息
    def testJobTypeCrawlStockConception(self):
        job_type = JobTypeCrawlStockConception(self.conf)
        jobs = job_type.get_jobs()
        self.assertEqual(len(jobs), 0, 'test JobTypeCrawlStockConception fail')  
    
    def testJobTypeCrawlMoneyFlow(self):
        job_type = JobTypeCrawlMoneyFlow(self.conf)
        jobs = job_type.get_jobs()
        self.assertEqual(len(jobs), 0, 'test JobTypeCrawlMoneyFlow fail')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
