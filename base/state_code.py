#!encoding=utf-8
'''
Created on 2015年9月3日

@author: fanfeifei
'''

class StateCode(object):
    '''
    程序状态码
    '''
    SUCC = 0 #正常返回
    FAIL = 1 #异常返回
    SPIDER_OK = 2 #爬虫正常
    SPIDER_SICK = 3 #爬虫异常
    SPIDER_SLEEP = 4 #爬虫休眠
    SPIDER_BUSY = 5 #爬虫满载
    PARAM_NULL = 6 #参数为空
    GET_STOCK_NULL = 7 #未获得stock
    UP_STOCK_ERR = 8 #更新股票信息error
    DETAIL_FILE_NULL = 9 #分笔交易文件记录为空
    DETAIL_LINE_ERROR = 10 #分笔记录错误
    INSERT_DATA_FAIL = 11 #插入数据错误