#!encoding=utf-8
'''
Created on 2015年9月3日

@author: fanfeifei
'''
from tools.tools import *
from crawler.jobs import *

class JobTypeBase(object):
    def __init__(self, conf):
        self.conf = conf
        self.last_work_time = None
        self.has_worked_times_today = 0
    def get_jobs(self):
        return None

class JobTypeCrawlStockList(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)
        self.last_update_time = 0
    def get_jobs(self):
        jobs = []
        if (time.time() - self.last_update_time) < 1800 :
            return jobs
        if time.localtime(time.time()).tm_hour in (9, 10, 11, 13, 14, 15) \
                and time.localtime(time.time()).tm_min == 30:
            self.last_update_time = time.time()
            jobs.append(JobGetStockList(self.conf))
        return jobs
    
class JobTypeCrawlStockDayDeal(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)
    def get_jobs(self):
        return None
        stock_list_time_tag = self.conf.stock_code_list_time_tag
        if stock_list_time_tag == None:
            return None
        now_hour_minute = "%02d:%02d" %(time.localtime(time.time()).tm_hour, \
                                        time.localtime(time.time()).tm_min)
        if now_hour_minute < '10:30':
            self.has_worked_times_today = 0
            return None
        if self.has_worked_times_today > 0:
            return None
        self.has_worked_times_today += 1
         
        jobs = []
        
        for code in open(self.conf.stock_code_file + "-" + stock_list_time_tag):
            code = code.strip()
            if code.startswith('300'):
                continue
            jobs.append(JobGetStockDeal(self.conf, code))
        return jobs if len(jobs) else None
    
class JobFactory(object):
    '''
    classdocs
    '''

    def __init__(self, conf):
        self.conf = conf
        self.job_types = []
        self.job_types.append(JobTypeCrawlStockList(self.conf))
        self.job_types.append(JobTypeCrawlStockDayDeal(self.conf))

