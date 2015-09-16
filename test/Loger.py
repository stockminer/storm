#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import logging
import logging.config

log_conf = '../conf/logger.conf'
logging.config.fileConfig(log_conf)
logger = logging.getLogger("crawl")
class Loger:
    def get_loger(self):
        return logger

if __name__ == '__main__':
    loger = Loger().get_loger()
    loger.critical('abc:50')
    loger.error('abc:40')
    loger.warning('abc:30')
    loger.info('abc:20')
    loger.debug('abc:10')
