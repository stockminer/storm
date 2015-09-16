#!/usr/bin/env python
import time
class AnalyseResult:
    def __init__(self, page_data):
        self.page_data = page_data
        self.url = "None"
        self.title = "None"
        self.page_time = "1970-01-01"
        self.craw_time = "1970-01-01"
        self.abstract = "None"
        self.content = "None"
        self.site_name = "None"
        self.author = "None"
        self.sub_urls = []
        self.sub_page_result = []
        self.analyse_success = False
    def get_format_dat(self):
        pass
    def get_data(self):
        if self.analyse_success:
            return self.get_format_data()
        else:
            return self.page_data
        
