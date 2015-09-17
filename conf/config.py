#!encoding=utf-8

'''
Created on 2015年6月20日

@author: fanfeifei
'''
from base.spider_type import SpiderType

class JobLevel:
    VERY_LOW = 1
    LOW = 2
    NORMAL = 3
    HIGH = 4
    VERY_HIGH = 5
class RootConf:
    def __init__(self, user):
        self.user = user
        self.confs = {}
        self.confs['yafei'] = {}
        self.confs['yafei']['bin_root'] = '/home/users/miaoyafei/project/gold-mine'
        self.confs['yafei']['data_root'] = '/home/users/miaoyafei/project/data'
        
        self.confs['yafei-pc'] = {}
        self.confs['yafei-pc']['bin_root'] = 'Z:/project/gold-mine'
        self.confs['yafei-pc']['data_root'] = 'Z:/project/data'
        
    def bin_root(self):
        return self.confs[self.user]['bin_root']
    def data_root(self):
        return self.confs[self.user]['data_root']
    
class Config:
    def __init__(self):
        #方便多用户开发
        self.root_conf = RootConf('yafei')
        #程序根目录
        self.bin_root = self.root_conf.bin_root()
        #数据存储位置相关配置
        self.data_root = self.root_conf.data_root()
        
        self.deal_root = self.data_root + '/deal'
        self.mine_root = self.data_root + '/mine'
        self.gold_root = self.data_root + '/gold'
        self.conception_root = self.data_root + '/conception'
        self.money_flow_root = self.data_root + '/money_flow'
        #配置文件的路径
        self.conf_root = self.bin_root + '/conf'
        self.conf_file_log = self.conf_root + '/logger.conf'
        
        #spider level and thread number
        self.spider_conf = {}
        self.spider_conf[JobLevel.VERY_HIGH] = 6
        self.spider_conf[JobLevel.HIGH] = 5
        self.spider_conf[JobLevel.NORMAL] = 1
        self.spider_conf[JobLevel.LOW] = 3
        self.spider_conf[JobLevel.VERY_LOW] = 3
        
        #每个spider内部job队列的最大长度
        self.spider_job_max_size = 2000
        
        #文件路径相关配置
        self.stock_base_tagfile = self.deal_root + '/stock_base_tag'
        self.stock_base_data_file = self.deal_root + '/stocklist'
        self.stock_code_file = self.deal_root + '/codelist'
        
        self.stock_concept_detail_file = self.conception_root + '/concp'
        self.stock_money_flow_file = self.money_flow_root + '/mflow'
        #动态变量与配置
        self.stock_code_list_time_tag = None 
        
        #接口相关
        #获取股票交易信息接口，node=sh_a 或者node=sz_a
        self.stock_list_url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=3000&sort=symbol&asc=1&symbol=&node='
        #获得概念列表
        self.stock_conception_list_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_bk?page=1&num=1000&sort=netamount&asc=0&fenlei=1'
        #概念下包含的股票信息, like &bankuai=1%2Fgn_xtyc
        self.stock_concept_detail_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_ssggzj?page=1&num=2000&sort=symbol&asc=1&shichang=&bankuai=1%2F'
        #资金流向
        self.stock_money_flow_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_ssggzj?page=1&num=3000&sort=symbol&asc=1&bankuai=&shichang='
    
        
