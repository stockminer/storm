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
import time

reload(sys)  
sys.setdefaultencoding('utf8')  

class Test(unittest.TestCase):

    #初始化工作 
    def setUp(self):
        self.conf = Config(RootConf('yafei'))

    #退出清理工作 
    def tearDown(self):
        pass

    #具体的测试用例，一定要以test开头
    #测试抓取概念信息
    def a_testJobTypeCrawlStockConception(self):
        job_type = JobTypeCrawlStockConception(self.conf, True)
        jobs = job_type.get_jobs()
        print len(jobs)
        for job in jobs:
            job.to_work()
            time.sleep(1)
        #self.assertEqual(len(jobs), 0, 'test JobTypeCrawlStockConception fail')  
    def a_testJobGetHangyeStock(self):
        job = JobGetHangyeStock(self.conf, 'test_key', 'test_name')
        out = job.get_tdx_hangye()
        print out
    def a_testJobTypeCrawlMoneyFlow(self):
        job_type = JobTypeCrawlMoneyFlow(self.conf)
        jobs = job_type.get_jobs()
        self.assertEqual(len(jobs), 0, 'test JobTypeCrawlMoneyFlow fail')
    def a_testJobGetStockList(self):
        JobGetStockList(self.conf).to_work()
    def a_testJobGetDetailDeal(self):
        JobGetDetailDeal(self.conf, 'sh600750', '2015-10-21').to_work()
    def testJobTypeGetDetailDeal(self):
        job_type = JobTypeGetDetailDeal(self.conf, True)
        jobs = job_type.get_jobs()
        print jobs
        for job in jobs:
            job.to_work()
            time.sleep(1)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
