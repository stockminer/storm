import threading
import time
import sys
import urllib2
import Analyser as anly
import urllib
from Mysql import Mysql

from Loger import Loger
import gzip
import StringIO
mylock = threading.RLock()
class Spider(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id = id
        self.thread_state = 0
        self.job_list = []
        self.url_analyser = anly.UrlAnalyser()
        self.page_analyser = anly.PageAnalyser()
        self.logger = Loger().get_loger()
        self.white_site_dict = {}
        for site in open("/home/work/spider/conf/white_site_list.conf"):
            self.white_site_dict[site.strip()] = 1
    def down_load(self, job, page_url=None):
        page_data = None
        craw_url = job.url
        if page_url != None:
            craw_url = page_url
        try:
            request = urllib2.Request(craw_url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
            response = urllib2.urlopen(request,timeout=job.timeout)
            #response.status,response.reason
            isGzip = response.headers.get('Content-Encoding')
            if isGzip:
                compresseddata = response.read()
                compressedstream = StringIO.StringIO(compresseddata)
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                page_data = gzipper.read()
            else:
                page_data = response.read()
            response.close()
        except:
            self.logger.warning(sys.exc_info())
            page_data = None
        return page_data

    def save_page_to_db(self, analyse_result):
        if analyse_result == None:
            return
        mysql = Mysql()
        for page in analyse_result.sub_page_result:
            select = "select count(url) from pages where url=%s"
            ret = mysql.getOne(select,[page.url])
            if ret[0] == 1:
                continue
            insert = "insert into pages(url,allpage) values(%s,%s)"
            id = mysql.insertOne(insert,[page.url, page.page_data])
        mysql.dispose()
    def is_in_db(self,url):
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        if host not in self.white_site_dict:
            return True
        mysql = Mysql()
        flag = False

        select = "select count(url) from pages where url=%s"
        ret = mysql.getOne(select,[url])
        if ret[0] == 1:
            flag = True
        mysql.dispose()
        return flag
         
    def save(self, result, job):
        if result == None:
            return
        fp = open(job.save_file_name,'wb')
        fp.write(result.get_data())
        fp.flush()
        fp.close()
        self.save_page_to_db(result)
    
    def add_job(self, job):
        self.modify_jobs('add', job)
        
    def del_job(self):
        self.modify_jobs('del')
        
    def modify_jobs(self, type, job=None):
        mylock.acquire()
        if type == 'add' and job != None:
            self.job_list.append(job)
        elif type == 'del':
            del self.job_list[0]
        mylock.release()
        
    def to_crawl(self, job):
        self.logger.info('spider %d: crawl:%s' %(self.id, job.url[0:40]))
        #download the page
        page_data = self.down_load(job)
        #analyser the page
        analyse_result = self.url_analyser.analyze(job, page_data)

        for url in analyse_result.sub_urls:
            in_db = self.is_in_db(url)
            if in_db:
                continue
            sub_page_data = self.down_load(job,url)
            page_analyse_result = self.page_analyser.analyze(job, sub_page_data,url)
            if page_analyse_result == None:
                continue
            analyse_result.sub_page_result.append(page_analyse_result)
        #save the data to db or file
        self.save(analyse_result, job)

    def run(self):        
        while self.thread_state == 0:
            if len(self.job_list) == 0:
                time.sleep(2)
                continue
            a_job = self.job_list[0]
            self.del_job()
            self.to_crawl(a_job)
            
    def set_state(self, state):
        self.thread_state = state
