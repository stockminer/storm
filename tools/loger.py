#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import logging
import logging.config

class Loger:
    def __init__(self, conf_file, log_name):
        logging.config.fileConfig(conf_file)
        self.logger = logging.getLogger(log_name)
    def get_loger(self):
        return self.logger

if __name__ == '__main__':
    loger = Loger('../conf/logger.conf',"crawl").get_loger()
    loger.critical('abc:50')
    loger.error('abc:40')
    loger.warning('abc:30')
    loger.info('abc:20')
    loger.debug('abc:10')
