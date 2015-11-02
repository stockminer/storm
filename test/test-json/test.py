#!/usr/bin/env python
#encoding=utf-8
import sys
import json
import time
import re

if __name__ == "__main__":
    data = ""
    for line in open("data.txt"):
        data += line.strip()
#ticktime:"15:03:03"
    output = re.sub('([a-zA-Z]\w+):', '"\\1":',data).decode('gb18030')
    print json.loads(output)

    #demjson.decode(output.decode('gb2312','ignore'))
