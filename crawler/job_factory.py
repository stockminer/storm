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
import re

class JobTypeBase(object):
    def __init__(self, conf, is_test=False):
        self.conf = conf
        self.create_jobs_count_today = 0
        self.last_create_jobs_time = 0
        self.is_test = is_test
        self.db = DB(self.conf)
        
    def get_jobs(self):
        return None
    def is_kaishi(self):
        return self.conf.is_kaishi_today
    
class JobTypeCheckIsKaishi(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)

    def get_jobs(self):
        #周末不开市
        time_now = time.localtime(time.time())
        if time_now.tm_wday >= 5:
            self.conf.is_kaishi_today = False
            return None
        #不在正常开盘时间，设置为闭市
        if not 9 < time_now.tm_hour < 16:
            self.conf.is_kaishi_today = False
            return None

        if (time.time() - self.last_create_jobs_time) < 600:
            return None
        #每半小时检查一次
        jobs = []
        if time_now.tm_min == 30:
            self.last_create_jobs_time = time.time()
            jobs.append(JobCheckIsKaishi(self.conf))
        return jobs
class JobTypeUpConf(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)

    def get_jobs(self):
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 60 :
            return None
        self.last_create_jobs_time = time.time()
        jobs.append(JobUpConf(self.conf))
        return jobs
   
class JobTypeCrawlStockDeal(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)

    def get_jobs(self):
        if not self.is_kaishi():
            return None
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 1800 :
            return jobs
        if time.localtime(time.time()).tm_hour in (12, 15) \
                and time.localtime(time.time()).tm_min == 30:
            self.last_create_jobs_time = time.time()
            jobs.append(JobGetStockList(self.conf))
        return jobs
    
class JobTypeCrawlStockConception(JobTypeBase):
    def __init__(self, conf, is_test = False):
        JobTypeBase.__init__(self, conf, is_test)
    def get_jobs(self):
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 600 :
            return jobs
        #凌晨2点抓一次概念情况
        if (time.localtime(time.time()).tm_hour == 2 \
                and time.localtime(time.time()).tm_min == 0) or self.is_test:
            self.last_create_jobs_time = time.time()
            data = Client(self.conf.stock_conception_list_url_page).gvalue()
            save_to_file(data, self.conf.stock_concept_file + ".html")
            #获得token
            ret = re.compile("EM_Finance2014NumericApplication/JS.aspx[^\\s]+token=([0-9a-z]{30,32})\"").search(data)
            token = None
            if ret:
                token = ret.group(1)
            if not token:
                return None
            stock_list_url = self.conf.stock_conception_list_url + token
            list_data = Client(stock_list_url).gvalue()
            save_to_file(list_data, self.conf.stock_concept_file + ".json")
            rets = re.findall('"([^\"]+)"', list_data.decode('utf-8'))
            concep_data = {}
            for match in rets:
                parts = match.split(',')
                concep_data[parts[1]] = parts[2].encode('utf-8')
            stock_list = StockList()
            #初始化概念
            stock_list.up_classify(self.db, mtype='conceps', is_init = True)
            for key in concep_data:
                jobs.append(JobGetConceptionStock(self.conf, key, token, concep_data[key]))
                pass
                
            #js_data = Client(self.conf.stock_hangye_list_url).gvalue()
            #save_to_file(js_data, self.conf.stock_hangye_file + ".json")
            #json_data = ananlyse_json(js_data.decode('gb18030','ignore').encode('utf-8','ignore'))
            #初始化行业信息
            stock_list.up_classify(self.db, mtype='hangye', is_init = True)
            #for itm in json_data:
            #    
            jobs.append(JobGetHangyeStock(self.conf, 'tdx_key', 'tdx_name'))
        return jobs
class JobTypeCrawlMoneyFlow(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)
    def get_jobs(self):
        if not self.is_kaishi():
            return None
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 1800 :
            return jobs
        if time.localtime(time.time()).tm_hour in (10, 11, 14, 15) \
                and time.localtime(time.time()).tm_min == 31:
            self.last_create_jobs_time = time.time()
            jobs.append(JobGetMoneyFlow(self.conf))
        return jobs
    
class JobTypeCrawlHGTMoneyFlow(JobTypeBase):
    def __init__(self, conf):
        JobTypeBase.__init__(self, conf)
    def get_jobs(self):
        if not self.is_kaishi():
            return None
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 1800 :
            return jobs
        if time.localtime(time.time()).tm_hour == 15 \
                and time.localtime(time.time()).tm_min == 30:
            self.last_create_jobs_time = time.time()
            jobs.append(JobGetHGTMoneyFlow(self.conf))
        return jobs    
class JobTypeGetDetailDeal(JobTypeBase):
    def __init__(self, conf, is_test = False):
        JobTypeBase.__init__(self, conf, is_test)
    def get_jobs(self):
        if not self.is_kaishi():
            return None
        jobs = []
        if (time.time() - self.last_create_jobs_time) < 1800 and not self.is_test:
            return None
        
        if (time.localtime(time.time()).tm_hour == 19 \
                and time.localtime(time.time()).tm_min == 0) \
                or self.is_test:
            self.last_create_jobs_time = time.time()
        
            stock_list = self.get_stock_list()
            for (code, day) in stock_list:
                if not day or not code:
                    #log error
                    continue
                day = day.strftime("%Y-%m-%d")
                jobs.append(JobGetDetailDeal(self.conf, code, day))
        return jobs    
    def get_stock_list(self):
        stock_list = []
        conn = self.db.get_conn()
        cur = conn.cursor()
        cmd_sql = 'select `symbol`, `latest_deal_day` from stocks where `type`=2 and `can_deal`=1'
        count=cur.execute(cmd_sql)
        if count <= 0:
            return StateCode.GET_STOCK_NULL
        results = cur.fetchmany(5000)
        for ret in results:
            stock_list.append(ret)
        cur.close()
        conn.commit()
        self.db.close(conn)
        return stock_list
class JobFactory(object):
    '''
    classdocs
    '''

    def __init__(self, conf):
        self.conf = conf
        self.job_types = []
        self.job_types.append(JobTypeCheckIsKaishi(self.conf))
        self.job_types.append(JobTypeCrawlStockDeal(self.conf))
        self.job_types.append(JobTypeCrawlStockConception(self.conf))
        self.job_types.append(JobTypeCrawlMoneyFlow(self.conf))
        self.job_types.append(JobTypeCrawlHGTMoneyFlow(self.conf))
        self.job_types.append(JobTypeUpConf(self.conf))
        self.job_types.append(JobTypeGetDetailDeal(self.conf))
