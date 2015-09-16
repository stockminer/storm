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
        self.sme = 0 #是否中小板
        self.gem = 0 #是否创业板
        self.st = 0 #是否风险警示板
        self.is_sz50 = 0 #是否上证50成分股
        self.is_zz50 = 0 #是否深圳50成分股
        
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
        self.d_time = 0 #记录时间，以粒度开盘时间为准
        self.open = 0 #开盘价
        self.close = 0 #收盘价
        self.high = 0 #最高价
        self.low = 0 #最低价
        self.volume = 0 #量能
        self.price_change = 0 #价格变动
        self.p_change_rate = 0 #价格变化率
        self.ma5 = 0 #5单位均线
        self.ma10 = 0 #10单位均线
        self.ma20 = 0 #20单位均线
        self.v_ma5 = 0 #5单位均量
        self.v_ma10 = 0 #10单位均量
        self.v_ma20 = 0 #20单位均量
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
        self.classify = None #所属类型属性
        self.pe = 0 #市盈率
        self.pb = 0 #市净率
        self.liquid_stock = 0 #流通股本
        self.all_stock = 0 #总股本
        self.total_assets = 0 #总资产
        self.liquid_assets = 0 #流动资产
        self.fixed_assets = 0 #固定资产
        self.reserved = 0 #公积金
        self.reserved_per_share = 0 #每股公积金
        self.eps = 0 #每股收益
        self.bvps = 0 #每股净资产
        self.time_to_market = 0 #上市时间
        self.hs_300_weight = 0
        self.deals_day = [] #天级交易记录
        self.is_delisted = 0 #是否退市
        self.lock_time = 0 #暂停上市时间
