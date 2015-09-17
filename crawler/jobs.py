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
        
        save_to_file("%s,%s" %(sh_a[:-1], sz_a[1:]), self.conf.stock_base_data_file + "-" + time_tag)
        return StateCode.SUCC

class JobGetConcetiopnStock(JobBase):
    def __init__(self, conf, conception):
        JobBase.__init__(self, conf, JobLevel.NORMAL)
        self.concep = conception
    def info(self):
        return 'JobGetConcetiopnStock:%s' %(self.concep)
    def to_work(self):
        time_tag = get_time_tag()
        stock_list_json = Client(self.conf.stock_concept_detail_url + self.concep).gvalue()
        save_to_file(stock_list_json, self.conf.stock_concept_detail_file + "-" + time_tag + '-' + self.concep)
        return StateCode.SUCC
    
class JobGetMoneyFlow(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.NORMAL)

    def to_work(self):
        time_tag = get_time_tag()
        money_flow_json = Client(self.conf.stock_money_flow_url).gvalue()
        save_to_file(money_flow_json, self.conf.stock_money_flow_file + "-" + time_tag)
        return StateCode.SUCC