#!/usr/bin/env python

import tushare as ts
from tools.tools import *
import json
df = ts.get_stock_basics()
#index, col =  df.axes()
#print index
#print col
print "get data ok"
json_data = df.to_json(orient='index')

for code in json.loads(json_data).keys():
    print code