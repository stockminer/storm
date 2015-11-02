#encoding=utf-8
'''
Created on 2015年6月20日

@author: fanfeifei
'''
#from pandas import Series,DataFrame
import os
import time
import json
import re

def data_frame_to_dict(df):
    index = df.index
    columns = df.columns
    data = {}
    for idx in index:
        data[idx] = {}
        for col in columns:
            data[idx][col] = df.at[idx, col]
    return data

def get_time_tag(format="%Y%m%d-%H-%M"):
    time_now = int(time.time())
    return "%s-%d" %(time.strftime(format, time.localtime(time_now)), time_now)

def save_to_file(data, dest_file):
    f_dir, f_name = os.path.split(dest_file)
    if len(f_dir) > 0 and not os.path.exists(f_dir):
        os.makedirs(f_dir)
    f = open(dest_file,'w')
    print >>f, data
    f.close()
    
def ananlyse_json(data):
    '''
    解析json数据，返回dict格式数据
    '''
    output = re.sub('([a-zA-Z]\w+):', '"\\1":',data)
    return json.loads(output)
