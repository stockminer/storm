#!encoding=utf-8
import threading
import time
import sys
from tools.loger import Loger
from base.spider_type import SpiderType
from base.state_code import StateCode

mylock = threading.RLock()
class Spider(threading.Thread):
    def __init__(self, level, id, conf, loger):
        threading.Thread.__init__(self)
        self.level = level
        self.id = id
        self.conf = conf
        self.loger = loger
        self.state = StateCode.SPIDER_OK
        self.job_list = []
    def info(self):
        return "spider_info:level-id[%d-%d],state[%d]" %(self.level, self.id, self.state)
    def add_job(self, job):
        self.loger.debug('spider[%d-%d] add a job:%s' %(self.level, self.id, job.info()))
        return self.modify_jobs('add', job)
        
    def del_job(self):
        return self.modify_jobs('del')
        
    def modify_jobs(self, type, job=None):
        ret = StateCode.SUCC
        mylock.acquire()
        if type == 'add':
            if job == None:
                ret = StateCode.PARAM_NULL
            elif len(self.job_list) > self.conf.spider_job_max_size:
                ret = StateCode.SPIDER_BUSY
            else:
                self.job_list.append(job)
        elif type == 'del':
            del self.job_list[0]
        mylock.release()
        return ret

    def run(self):        
        while self.state != StateCode.SPIDER_SICK:
            if len(self.job_list) == 0:
                time.sleep(5)
                continue
            a_job = self.job_list[0]
            ret = a_job.to_work()
            if ret != StateCode.SUCC:
                self.loger.warning('a job fail:%d,spider-info:%s, job-info:%s', ret, self.info(), a_job.info())
            self.del_job()
            time.sleep(1)
        if self.state == StateCode.SPIDER_SICK:
            self.loger.warning('spider sick, info:%s', self.info())
    def set_state(self, state):
        self.state = state
