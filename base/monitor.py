#!encoding=utf-8
'''
Created on 2015年6月20日

@author: miaoyafei
'''
import jsonpickle as jspk
class Info(object):
    '''
    状态监控
    '''
    def __init__(self):
        self.id = 0 #监控id
        self.group = 0 #所在组
        self.up_time = '0000-00-00 00:00:00' #更新时间
        self.state_info = '' #状态信息
    def get_value(self):
        return "%d\t%d\t%s\t%s" %(self.id, self.group, self.up_time, self.state_info)
class Monitor(object):
    def __init__(self):
        self.infos = {}
    def up_info(self, id, info):
        self.infos[id] = info
    def get_info(self, id):
        return self.infos[id] if id in self.infos else None
    def get_all_infos(self):
        return self.infos
    def get_group(self, g_id):
        out = []
        for info in self.infos.itervalues():
            if info.group == g_id:
                out.append(info)
        return jspk.encode(out)
