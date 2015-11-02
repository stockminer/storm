#encoding=utf-8
from base.state_code import StateCode
#import tushare as ts
from tools.tools import *
from tools.client import *
from base.stock import *
from base.db import *
from conf.config import *
import code
import sys
import re
import demjson
import jsonpickle as jspk
import json

class JobBase(object):
    def __init__(self, conf, level):
        self.conf = conf
        self.level = level
        self.db = DB(self.conf)
    def to_work(self):
        return StateCode.SUCC
    def info(self):
        return self.__class__.__name__
    
class JobCheckIsKaishi(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.VERY_HIGH)
    def info(self):
        return 'JobCheckIsKaishi'
    
    def to_work(self):
        time_now = time.localtime(time.time())
        nowdate = "%d-%02d-%02d" %(time_now.tm_year, time_now.tm_mon, time_now.tm_mday)
        data = Client(self.conf.check_is_kaishi_url).gvalue()
        ret = re.compile("\d{4}-\d{2}-\d{2}").search(data)
        if ret:
            last_kaishi_date_real = ret.group(0)
            if last_kaishi_date_real == nowdate:
                self.conf.is_kaishi_today = True
                self.conf.today = "%d%02d%02d" %(time_now.tm_year, time_now.tm_mon, time_now.tm_mday)
                return StateCode.SUCC
        self.conf.is_kaishi_today = False
        return StateCode.SUCC
   
class JobUpConf(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.HIGH)
    def info(self):
        return 'JobUpConf'
    
    def to_work(self):
        conf_str = jspk.pickler.Pickler().flatten(self.conf)
        conf_str = json.dumps(conf_str,indent=4)
        conf_str_out = open(self.conf.conf_dump_file,'w')
        print >>conf_str_out, conf_str
        conf_str_out.close()
        return StateCode.SUCC

class JobGetStockList(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.VERY_HIGH)
    def info(self):
        return 'JobGetStockList'
    
    def to_work(self):
        time_tag = get_time_tag()
        time_now = time.localtime(time.time())
        sh_a = Client(self.conf.stock_list_url + 'sh_a').gvalue()
        time.sleep(2)
        sz_a = Client(self.conf.stock_list_url + 'sz_a').gvalue()
        
        hs_data = "%s,%s" %(sh_a[:-1], sz_a[1:])
        save_to_file(hs_data, self.conf.stock_base_data_file + "-" + time_tag)

        js_data = ananlyse_json(hs_data.decode('gb18030','ignore').encode('utf-8','ignore'))
        stock_list = StockList()
        deal_days = self.get_latest_deal_day()
        for itm in js_data:
            stock = Stock()
            stock.code = itm['code']
            stock.symbol = itm['symbol']
            stock.name = itm['name']
            stock.type = StockType.GEGU
            one_deal = DealRecord()
            one_deal.d_time = "%s" %(self.conf.today)
            one_deal.zuoshou = itm['settlement'] #昨日收盘
            one_deal.open = itm['open']
            one_deal.close = itm['trade']
            one_deal.high = itm['high']
            one_deal.low = itm['low']
            one_deal.volume = itm['volume']
            one_deal.amount = itm['amount']
            one_deal.price_change = itm['pricechange']
            one_deal.p_change_rate = itm['changepercent']
            one_deal.turnover = itm['turnoverratio']
            one_deal.zong_shizhi = itm['mktcap']
            one_deal.liutong_shizhi = itm['nmc']
            stock.deals_day.append(one_deal)
            stock.can_deal = True if one_deal.volume > 0 else False
            if stock.can_deal:
                one_deal.d_time = "%d-%02d-%02d %02d:%02d:%02d" \
                    %(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, \
                    time_now.tm_hour, time_now.tm_min, time_now.tm_sec)
            else:
                one_deal.d_time = "0000-00-00" if stock.code not in deal_days else deal_days[stock.code]
            stock.latest_deal_day = one_deal.d_time
            stock_list.add(stock)
        stock_list.save_base_data(self.db)
        return StateCode.SUCC
    def get_latest_deal_day(self):
        days = {}
        conn = self.db.get_conn()
        cur=conn.cursor()
        select_sql = "select code, latest_deal_day from stocks"
        cur.execute(select_sql)
        results=cur.fetchall()
        for r in results:
            days[r[0]] = "0000-00-00" if not r[1] else r[1].strftime("%Y-%m-%d %H:%M:%S")
        cur.close()
        conn.commit()
        self.db.close(conn)
        return days
class JobGetConceptionStock(JobBase):
    def __init__(self, conf, key, token, concep_name):
        JobBase.__init__(self, conf, JobLevel.VERY_LOW_SLOW)
        self.key = key
        self.token = token
        self.concep_name = concep_name

    def info(self):
        return 'JobGetConceptionStock:%s' %(self.concep)
    def to_work(self):
        cep_url = self.conf.stock_concept_detail_url %(self.token, self.key) + "1"
        stock_list_json = Client(cep_url).gvalue()
        
        save_to_file(stock_list_json, self.conf.stock_concept_file + '-' + self.key)
        #获得概念股票对应关系
        rets = re.findall('"([^\"]+)"', stock_list_json.decode('utf-8'))
        stock_list = StockList()
        for match in rets:
            parts = match.split(',')
            stock = Stock()
            stock.code = parts[1]
            stock.conceps.append(self.concep_name.encode('utf-8'))
            stock_list.add(stock)
        stock_list.up_classify(self.db, mtype='conceps')
        return StateCode.SUCC

class JobGetHangyeStock(JobBase):
    def __init__(self, conf, key, name):
        JobBase.__init__(self, conf, JobLevel.VERY_LOW_SLOW)
        self.key = key
        self.name = name

    def info(self):
        return 'JobGetHangyeStock:%s' %(self.concep)
    def to_work(self):
        
        #cep_url = self.conf.stock_hangye_detail_url + self.key
        #stock_list_json = Client(cep_url).gvalue()
        #优先使用通达信的行业数据
        hangye_tdx = self.get_tdx_hangye()
        old_stocks = {}
        #获得行业股票对应关系
        #js_data = ananlyse_json(stock_list_json.decode('gb18030','ignore').encode('utf-8','ignore'))
        stock_list = StockList()
        #for itm in js_data:
        #    stock = Stock()
        #    stock.code = itm['symbol'][2:]
        #    if stock.code in hangye_tdx:
        #        self.name = hangye_tdx[stock.code]
        #        old_stocks[stock.code] = 1
        #    stock.hangye = [self.name]
        #    stock_list.add(stock)
        for code, name in hangye_tdx.iteritems():
            if code not in old_stocks:
                stock = Stock()
                stock.code = code
                stock.hangye = [name]
                stock_list.add(stock)
        #save_to_file(stock_list_json, self.conf.stock_hangye_file + '-' + self.key)
        stock_list.up_classify(self.db, mtype='hangye')
        return StateCode.SUCC
    def get_tdx_hangye(self):
        hy_tdx = {}
        try:
            lines = []
            line_cnt = 0
            hy_index = 0
            dm_index = 0
            for line in open(self.conf.tdx_hangye_file):
                parts = line.strip().split('\t')
                lines.append(parts)
                if line_cnt == 0:
                    for i in range(0,len(parts)):
                        if parts[i].strip().decode('gb18030').encode('utf-8') == '代码':
                            dm_index = i
                        if parts[i].strip().decode('gb18030').encode('utf-8') == '细分行业':
                            hy_index = i
                line_cnt += 1
                            
            for line in lines[1:-1]:
                hy_tdx[line[dm_index]] = line[hy_index].decode('gb18030').encode('utf-8')
        except:
            print >>sys.stderr, 'load tongdaxin data error'
            return {}
        return hy_tdx
class JobGetMoneyFlow(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.NORMAL)

    def to_work(self):
        time_tag = get_time_tag()
        money_flow_json = Client(self.conf.stock_money_flow_url).gvalue()
        save_to_file(money_flow_json, self.conf.stock_money_flow_file + "-" + time_tag)
        return StateCode.SUCC
    
class JobGetHGTMoneyFlow(JobBase):
    def __init__(self, conf):
        JobBase.__init__(self, conf, JobLevel.NORMAL)

    def to_work(self):
        time_tag = get_time_tag()
        money_flow_json = Client(self.conf.hugutong_money_flow_url).gvalue()
        save_to_file(money_flow_json, self.conf.hgt_mone_flow_file + "-" + time_tag)
        return StateCode.SUCC

class JobGetDetailDeal(JobBase):
    '''
     获得分笔交易记录
     '''
    def __init__(self, conf, code, day):
        JobBase.__init__(self, conf, JobLevel.HIGH)
        self.code = code
        self.day = day
    def to_work(self):
        fenbi_data_url = self.conf.fenbi_deal_url %(self.day, self.code)
        print fenbi_data_url
        data = Client(fenbi_data_url).gvalue()
        save_to_file(data, "%s/%s/%s" %(self.conf.fenbi_deal_dir, self.day, self.code))
        deal_record = DealRecord()
        conn = self.db.get_conn()
        cur=conn.cursor()
        deal_record.add_detail(self.code, self.day, data, cur)
        cur.close()
        conn.commit()
        self.db.close(conn)
        return StateCode.SUCC
