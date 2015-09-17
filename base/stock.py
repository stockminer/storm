#!encoding=utf-8
'''
Created on 2015年6月20日

@author: miaoyafei
'''

class Classify(object):
    '''
    分类相关属性
    '''
    def __init__(self):
        self.industry = {} #所属行业
        self.concept = {} #所属概念
        self.area = {} #所属地域
        
class Detail(object):
    '''
    分笔交易记录
    '''
    def __init__(self):
        self.d_time = 0 #交易时间，时间为具体交易时间
        self.price = 0 #成交价格
        self.change = 0 #价格变动
        self.volume = 0 #成交量
        self.amount = 0 #成交金额
        self.type = 0 #买卖类型 0中性盘 1买盘 2卖盘
        
class DealRecord(object):
    '''
    交易记录
    '''
    def __init__(self):
        self.d_time = 0 #记录时间
        self.open = 0 #开盘价
        self.close = 0 #收盘价
        self.high = 0 #最高价
        self.low = 0 #最低价
        self.volume = 0 #成交量
        self.amount = 0 #成交金额
        self.price_change = 0 #价格变动
        self.p_change_rate = 0 #价格变化率
        self.turnover = 0 #换手率
        self.detail = [] #分笔交易记录

class StockType:
    ZHISHU = 1
    GEGU_SH = 2
    GEGU_SZ = 3
    JIJIN = 4
class Stock(object):
    '''
    包含一只股票的所有属性
    '''
    ZHISHU = 1
    GEGU = 2
    def __init__(self, df):
        self.type = None #类型 指数、个股、基金等
        self.code = '' #代码
        self.name = '' #名字
        self.classify = Classify() #所属类型属性
        self.time_to_market = 0 #上市时间
        self.deals_day = [] #天级交易记录
        self.deals_hour = [] #小时级交易记录
        self.can_deal = 0 #是否暂停上市
