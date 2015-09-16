#encoding=utf-8
'''
Created on 2015年6月20日

@author: fanfeifei
'''
#from pandas import Series,DataFrame
import time

def get_a():
    return 'a'

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
    f = open(dest_file,'w')
    print >>f, data
    f.close()