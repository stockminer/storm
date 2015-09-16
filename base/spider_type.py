#!encoding=utf-8
'''
Created on 2015年9月3日

@author: miaoyafei
'''

class SpiderType(object):
    '''
    抓取任务的类型信息
    '''
    TYPE_STOCK = 'TYPE_STOCK'
    TYPE_NEWS = 'TYPE_NEWS'
    def __init__(self, tp, t_num, jb_span, max_jobs):
        self.type = tp #spider 类型
        self.thread_num = t_num  #抓取股票信息的线程数
        self.job_span = jb_span #单个线程抓取过程中任务间隔时间
        self.max_jobs = max_jobs
        