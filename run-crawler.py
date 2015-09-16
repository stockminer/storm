#encoding=utf-8
import sys
from conf.config import Config
import time
import random
from crawler.spider import Spider
from tools.loger import Loger
from crawler.job_factory import JobFactory
class Crawler:
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        self.job_factory = JobFactory(self.conf)
        self.spiders = {}
        for level, thread_num in self.conf.spider_conf.iteritems():
            for i in range(thread_num):
                if level not in self.spiders:
                    self.spiders[level] = []
                self.spiders[level].append(Spider(level, i, self.conf, self.logger))

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
                        random.randint(0, self.conf.spider_conf[job.level] - 1)].add_job(job)
                have_job_todo = True
            if not have_job_todo:
                time.sleep(1)
                
if __name__ == '__main__':
    conf = Config()
    logger = Loger(conf.conf_file_log, "crawl").get_loger()
    crawler = Crawler(conf, logger)
    ret = crawler.begin_work()
    exit(ret)

    
