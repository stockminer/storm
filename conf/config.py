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

class Config:
    def __init__(self):
        #程序根目录
        self.work_root = '/home/users/miaoyafei/project/gold-mine'
        #数据存储位置相关配置
        self.data_root = '/home/users/miaoyafei/project/data'
        self.stock_root = self.data_root + '/stock'
        self.mine_root = self.data_root + '/mine'
        self.gold_root = self.data_root + '/gold'
        
        #配置文件的路径
        self.conf_root = self.work_root + '/conf'
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
        self.stock_base_tagfile = self.stock_root + '/stock_base_tag'
        self.stock_base_data_file = self.stock_root + '/stocklist'
        self.stock_code_file = self.stock_root + '/codelist'
        self.stock_deal_day = self.stock_root + '/day/deal'
        
        
        
        #动态变量与配置
        self.stock_code_list_time_tag = None 
        
        #接口相关
        self.stock_list_url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=3000&sort=symbol&asc=1&symbol=&node='
        
        
