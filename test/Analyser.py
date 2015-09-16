#!/usr/bin/env python
import re
from AnalyseResult import AnalyseResult
from Loger import Loger
import time

class UrlAnalyser:
    def __init__(self):
        self.url_exp = re.compile("^http://")
        self.logger = Loger().get_loger()
    def analyze(self, job, page_data):
        analyse_result = AnalyseResult(page_data)
        urls = {}
        for rex in job.url_exps:
            t_urls = rex.findall(page_data)
            for url in t_urls:
                urls[url] = 1
        for url in urls:
            url = self.process(job, url)
            analyse_result.sub_urls.append(url)
            self.logger.debug("job(%s) get url(%s)" %(job.conf_name, url))
        return analyse_result
    def process(self,job,url):
        
        if len(self.url_exp.findall(url)) > 0:
            return url
        url = job.url + '/' + url
        return url
class PageAnalyser:
    def __init__(self):
        self.logger = Loger().get_loger()
    def analyze(self,job,page_data, url):
        page_data = page_data.decode(job.encode,'ignore').encode('utf-8','ignore')
        page_data = page_data.replace('\r','').replace('\n','')
        analyse_result = AnalyseResult(page_data)
        analyse_result.url = url
        analyse_result.craw_time = time.strftime("%Y%m%d %H:%M:%S")
        analyse_result.analyse_success = 1
        return analyse_result
if __name__ == '__main__':
    analyser = UrlAnalyser()
    analyser.analyse_result = AnalyseResult("")
    analyser.analyse_result.sub_urls.append('http://it.21cn.com/a.html')
    analyser.analyse_result.sub_urls.append('http://it.21cn.com/b.html')
