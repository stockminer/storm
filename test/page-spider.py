#!/usr/bin/env python
import time
from JobsConfig import JobsConfig
from JobsConfig import JobConfig
from Spider import Spider
from Loger import Loger

class PageSpider:
    def __init__(self, conf_file, thread_count):
        self.jobs_config = JobsConfig(conf_file)
        self.spider_list = []
        self.thread_count = thread_count
        for i in range(0,self.thread_count):
            self.spider_list.append(Spider(i))        
        self.latest_used_spider = 0
        self.state = 1 # 1:run,2:sleep,3:exit
        
        self.logger = Loger().get_loger()

    def run(self):
        for spider in self.spider_list:
            spider.setDaemon(True)
            spider.start()
            self.logger.info('start thread %d' %(spider.id))
        while True:
            a_job = self.jobs_config.get_next_job()
            if a_job == None:
                time.sleep(5)
                continue
            self.spider_list[self.latest_used_spider].add_job(a_job)
            self.latest_used_spider = (self.latest_used_spider + 1) % self.thread_count

             
if __name__ == '__main__':
    conf_file = '../conf/craw-jobs.conf'
    mulu_spider = PageSpider(conf_file,5)
    mulu_spider.run()
    exit(1)
