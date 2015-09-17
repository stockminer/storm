#!encoding=utf-8
'''
Created on 2015年9月3日

@author: fanfeifei
'''
from tools.tools import *
from crawler.jobs import *
from tools.client import *
import json
import demjson

class JobTypeBase(object):
    def __init__(self, conf):
        self.conf = conf
        self.create_jobs_count_today = 0
        self.last_create_jobs_time = 0
    def get_jobs(self):
        return None

class JobTypeCrawlStockDeal(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)

    def get_jobs(self):
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 1800 :
            return jobs
        if time.localtime(time.time()).tm_hour in (9, 10, 11, 13, 14, 15) \
                and time.localtime(time.time()).tm_min == 30:
            self.last_create_jobs_time = time.time()
            jobs.append(JobGetStockList(self.conf))
        return jobs
    
class JobTypeCrawlStockConception(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)
    def get_jobs(self):
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 86400 :
            return jobs
        #凌晨2点抓一次概念情况
        if time.localtime(time.time()).tm_hour == 2 \
                and time.localtime(time.time()).tm_min == 0:
            self.last_create_jobs_time = time.time()
            data = Client(self.conf.stock_conception_list_url).gvalue()
            concep_data = self.ananlyse_json(data)
            for key in concep_data:
                jobs.append(JobGetConcetiopnStock(self.conf, key))
            
        return jobs
    def ananlyse_json(self, data):
        js_data = demjson.decode(data.decode('gb2312','ignore'))
        #js_data = json.loads(js_data_str)
        out = {}
        for item in js_data:
            key = item['category']
            out[key] = item
        return out
class JobTypeCrawlMoneyFlow(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)
    def get_jobs(self):
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 1800 :
            return jobs
        if time.localtime(time.time()).tm_hour in (9, 10, 11, 13, 14, 15) \
                and time.localtime(time.time()).tm_min == 31:
            self.last_create_jobs_time = time.time()
            jobs.append(JobGetMoneyFlow(self.conf))
        return jobs
    
class JobFactory(object):
    '''
    classdocs
    '''

    def __init__(self, conf):
        self.conf = conf
        self.job_types = []
        self.job_types.append(JobTypeCrawlStockDeal(self.conf))
        self.job_types.append(JobTypeCrawlStockConception(self.conf))
        self.job_types.append(JobTypeCrawlMoneyFlow(self.conf))

