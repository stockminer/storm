#!/usr/bin/env python
import ConfigParser
from Loger import Loger
import time
import re
import os

class JobConfig:
    def __init__(self):
        self.conf_name = "NULL"
        self.url = "NULL"
        self.host = "NULL"
        self.crawl_span = 0 #by second
        self.encode = "UTF-8"
        self.timeout = 10
        self.latest_craw_time = 0
        self.page_root = "../pages"
        self.save_file_name = self.page_root + "/default.html"
        self.url_exp_count = 0
        self.url_exps = []
        self.filter_url_exp_count = 0
        self.filter_url_exps = []
        
        self.title_exp = ""
        self.page_time_exp = ""
        self.abstract_exp = ""
        self.content_exp = ""
        self.site_name_exp = ""
        self.author_exp = ""

        self.valid = False
    def set_url(self, url):
        self.url = url
        host_t = re.compile('^(http://[^/]*)/.*').findall(self.url)
        if len(host_t) > 0:
            self.host = host_t[0]
    def set_span(self, span):
        self.crawl_span = span
    def set_encode(self,encode):
        self.encode = encode
    def set_conf_name(self,name):
        self.conf_name = name
    def set_filename(self,file_name):
        self.save_file_name = self.page_root + "/" + file_name
    def set_crawl_time(self,crawl_time):
        self.latest_craw_time = crawl_time
    def get_craw_time(self):
        return int(self.latest_craw_time + self.crawl_span)
    def set_url_exp_count(self, count):
        self.url_exp_count = count
    def set_filter_url_exp_count(self, count):
        self.filter_url_exp_count = count
    def set_title_exp(self,exp):
        self.title_exp = re.compile(exp)
    def set_page_time_exp(self,exp):
        self.page_time_exp = re.compile(exp)
    def set_craw_time_exp(self,exp):
        self.craw_time_exp = re.compile(exp)
    def set_abstract_exp(self,exp):
        self.abstract_exp = re.compile(exp)
    def set_content_exp(self,exp):
        self.content_exp = re.compile(exp)
    def set_site_name_exp(self,exp):
        self.site_name_exp = re.compile(exp)
    def set_author_exp(self,exp):
        self.author_exp = re.compile(exp)
    def set_valid(self, flag):
        if flag == 1:
            self.valid = True
        else:
            self.valid = False
class JobsConfig:
    def __init__(self, conf_file):
        self.job_configs = None 
        self.conf_file = conf_file
        self.last_mttime = 0
        self.latest_crawl_job = 0
        self.logger = Loger().get_loger()
        
    def __load_conf(self):
        self.logger.info('load craw_conf')
        self.job_configs = []
        self.latest_crawl_job = 0
        conf = ConfigParser.ConfigParser()
        conf.read(self.conf_file)
        for section in conf.sections():
            if 'MuluCrawlJob_' not in section:
                continue
            job = JobConfig()
            job.set_conf_name(section)
            url = conf.get(section, 'URL')
            if len(url) > 0  and url[-1] == '/':
                url = url[0:-1]
            job.set_url(url)
            job.set_span(conf.getint(section, 'Span'))
            job.set_encode(conf.get(section,'Encode'))
            job.set_filename(conf.get(section,'SaveFileName'))
            job.set_url_exp_count(conf.getint(section,'UrlExp_count'))
            for i in range(0,job.url_exp_count):
                exp = conf.get(section, 'UrlExp_%d' %(i))
                exp = exp[1:-1]
                self.logger.debug('get_url_exp:%s' %exp)
                job.url_exps.append(re.compile(exp))
            job.set_filter_url_exp_count(conf.getint(section,'FilterUrlExp_count'))
            for i in range(0,job.filter_url_exp_count):
                exp = conf.get(section, 'FilterUrlExp_%d' %i)
                exp = exp[1:-1]
                self.logger.debug('filter_url_exp:%s' %exp)
                job.filter_url_exps.append(re.compile(exp))
            job.set_valid(conf.getint(section, 'Is_valid'))
            self.job_configs.append(job)
    def get_next_job(self):
        new_time = os.stat(self.conf_file).st_mtime
        if new_time != self.last_mttime:
            self.last_mttime = new_time
            self.__load_conf()
        job = None
        all_cnf_cunt = len(self.job_configs)
        for i in range(0, all_cnf_cunt):
            crawl_time = self.job_configs[self.latest_crawl_job].get_craw_time()
            now_time = int(time.time())
            #self.logger.debug("item:%s crawl_time(%d),left(%d)" \
            #    %(self.job_configs[self.latest_crawl_job].conf_name, crawl_time, crawl_time-now_time))
            if crawl_time <= now_time and self.job_configs[self.latest_crawl_job].valid:
                job = self.job_configs[self.latest_crawl_job]
                self.job_configs[self.latest_crawl_job].set_crawl_time(now_time)
            self.latest_crawl_job = (self.latest_crawl_job + 1) % all_cnf_cunt
            if job != None:
                break
        return job
if __name__ == '__main__':
    
    jobconf = JobsConfig('../conf/craw-jobs.conf')
