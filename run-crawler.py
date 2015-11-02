#encoding=utf-8
import sys
from conf.config import Config
import time
import random
from crawler.spider import Spider
from tools.loger import Loger
from crawler.job_factory import JobFactory
from base.monitor import *
from base.server import SocketServer

reload(sys)
sys.setdefaultencoding('utf8')

class Crawler:
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        self.job_factory = JobFactory(self.conf)
        self.spiders = {}
        for level, s_conf in self.conf.spider_conf.iteritems():
            for i in range(s_conf[0]):
                if level not in self.spiders:
                    self.spiders[level] = []
                self.spiders[level].append(Spider(level, i, s_conf[1], self.conf, self.logger))

    def begin_work(self):
        #let all spiders ready
        for level, sp_list in self.spiders.iteritems():
            for spider in sp_list:
                spider.setDaemon(True)
                spider.start()
                self.logger.info('start thread info:%s' %(spider.info()))
        while True:
            have_job_todo = False
            for jobtype in self.job_factory.job_types:
                jobs = jobtype.get_jobs()
                if jobs == None or len(jobs) == 0:
                    #print 'jobs is none'
                    continue
                for job in jobs:
                    self.spiders[job.level][\
                        random.randint(0, self.conf.spider_conf[job.level][0] - 1)].add_job(job)
                have_job_todo = True
            if not have_job_todo:
                time.sleep(1)
                
if __name__ == '__main__':
    
    monitor = Monitor()
    monitor_server = SocketServer(monitor)
    monitor_server.setDaemon(True)
    monitor_server.start()
    
    conf = Config()
    logger = Loger(conf.conf_file_log, "crawl").get_loger()
    crawler = Crawler(conf, logger)
    ret = crawler.begin_work()
    exit(ret)

    
