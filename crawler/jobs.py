#encoding=utf-8
from base.state_code import StateCode
#import tushare as ts
from tools.tools import *
from tools.client import *
from base.stock import *
from conf.config import *
import code

class JobBase(object):
    def __init__(self, conf, level):
        self.conf = conf
        self.level = level
    def to_work(self):
        return StateCode.SUCC
    def info(self):
        return self.__class__.__name__
    
class JobGetStockList(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.VERY_HIGH)
    def info(self):
        return 'JobGetStockList'
    
    def to_work(self):
        time_tag = get_time_tag()
        sh_a = Client(self.conf.stock_list_url + 'sh_a').gvalue()
        time.sleep(2)
        sz_a = Client(self.conf.stock_list_url + 'sz_a').gvalue()
        
        save_to_file(sh_a, self.conf.stock_base_data_file + "-" + time_tag + 'sh_a')
        save_to_file(sz_a, self.conf.stock_base_data_file + "-" + time_tag + 'sz_a')
        
#        stock_codes = df.index
#        stock_code_file = open(self.conf.stock_code_file + "-" + time_tag, 'w')
#        for code in stock_codes:
#            print >>stock_code_file, code
#        stock_code_file.close()
#        self.conf.stock_code_list_time_tag = time_tag
#        tag_file = open(self.conf.stock_base_tagfile, 'w')
#        print >>tag_file, time_tag
#        tag_file.close()
        return StateCode.SUCC

class JobGetStockDeal(JobBase):
    def __init__(self, conf, code):
        JobBase.__init__(self, conf, JobLevel.NORMAL)
        self.code = code
    def info(self):
        return 'JobGetStockDeal:%s' %(self.code)
    def to_work(self):
        df = None
        try:
            df = ts.get_h_data(self.code)
        except :
            print "error:%s" %(self.info())
            return StateCode.FAIL
        df.to_json(self.conf.stock_deal_day + "-" + self.code, orient='index')
        print 'finish %s crawl' %self.code
        return StateCode.SUCC