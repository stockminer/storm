#!encoding=utf-8
'''
Created on 2015年6月20日

@author: miaoyafei
'''
from base.state_code import StateCode

class Detail(object):
    '''
    分笔交易记录
    '''
    BUY_STR = '买盘'.decode('utf-8').encode('gb18030')
    SELL_STR = '卖盘'.decode('utf-8').encode('gb18030')
    def __init__(self):
        self.d_time = 0 #交易时间，时间为具体交易时间
        self.price = 0 #成交价格
        self.change = 0 #价格变动
        self.volume = 0 #成交量
        self.amount = 0 #成交金额
        self.type = 0 #买卖类型 0中性盘 1买盘 2卖盘
    def set(self, data_str):
        data = data_str.strip().split('\t')
        if len(data) != 6:
            return StateCode.DETAIL_LINE_ERROR
        self.d_time = data[0]
        self.price = float(data[1])
        self.change = 0 if data[2] == '--' else float(data[2])
        self.volume = int(data[3])
        self.amount = int(data[4])
        self.type = 0
        if data[5] == '1' or data[5] == Detail.BUY_STR:
            self.type = 1
        elif data[5] == '2' or data[5] == Detail.SELL_STR:
            self.type = 2
        return StateCode.SUCC
    def get_str(self):
        str_out = "%s\t%.3f\t%.2f\t%d\t%d\t%d" \
                %(self.d_time, self.price, self.change, self.volume, self.amount, self.type)
        return str_out
class DealRecord(object):
    '''
    交易记录
    '''
    def __init__(self):
        self.d_time = 0 #记录时间
        self.zuoshou = 0 #昨日收盘
        self.open = 0 #开盘价
        self.close = 0 #收盘价
        self.high = 0 #最高价
        self.low = 0 #最低价
        self.volume = 0 #成交量
        self.amount = 0 #成交金额
        self.price_change = 0 #价格变动
        self.p_change_rate = 0 #价格变化率
        self.turnover = 0 #换手率
        self.zong_shizhi = 0 #总市值
        self.liutong_shizhi = 0 #流通市值
        self.detail = [] #分笔交易记录
        self.zhuli_in = 0 #主力买入
        self.zhuli_out = 0 #主力卖出
        self.sanhu_in = 0 #散户买入
        self.sanhu_out = 0 #散户卖出
    def add_detail(self, code, day, file_data, cur):
        code = code[2:]
        parts = file_data.strip().split('\n')
        #成交时间    成交价  价格变动    成交量(手)  成交额(元)  性质
        if len(parts) <= 2 or len(parts[0].split('\t')) != 6:
            return StateCode.DETAIL_FILE_NULL
        details = []
        for line in parts[1:]:
            one_d = Detail()
            if one_d.set(line) != StateCode.SUCC:
                continue
            details.append(one_d.get_str())
        data_str = "\n".join(details).strip()
        save_sql = 'insert into deal_detail(`code`,`time`,`data`) values(%s,%s,%s)'
        count=cur.execute(save_sql, [code, day, data_str])
        if count <= 0:
            return StateCode.INSERT_DATA_FAIL
        return StateCode.SUCC
        
class StockType:
    ZHISHU = 1 #指数
    GEGU = 2 #个股
    JIJIN = 3 #基金
    GAINIAN = 4 #概念
    
class Stock(object):
    '''
    包含一只股票的所有属性
    '''
    def __init__(self):
        self.type = None #类型 指数、个股、基金等
        self.code = '' #代码
        self.symbol = '' #带标记的代码
        self.name = '' #名字
        self.conceps = [] #所属概念
        self.hangye = [] #所属行业
        self.time_to_market = 0 #上市时间
        self.deals_day = [] #天级交易记录
        self.can_deal = 0 #是否暂停上市
        self.latest_deal_day = '0000-00-00' #最近交易时间
    def save_base_data(self, cur):
        save_sql = 'insert into stocks(`code`, `symbol`, `type`, `name`, `can_deal`, `latest_deal_day`) values("%s","%s",%d,"%s",%d, "%s")' \
                %(self.code, self.symbol, self.type, self.name, self.can_deal, self.latest_deal_day)
        
        count=cur.execute('select code from stocks where code=%s',self.code)
        if count > 0:
            save_sql = 'update stocks set `symbol`="%s", `type`=%s, `name`="%s",`can_deal`=%d, `latest_deal_day`="%s" WHERE `code`="%s"' \
                %(self.symbol, self.type, self.name, self.can_deal, self.latest_deal_day, self.code)
        cur.execute(save_sql)
        
    def save_deals_day(self, cur):
        datas = []
        for dl in self.deals_day:
            datas.append((self.code, dl.d_time, dl.zuoshou, dl.open, dl.close, dl.high, dl.low, dl.volume,\
                          dl.amount, dl.price_change, dl.p_change_rate, dl.turnover,dl.zong_shizhi, dl.liutong_shizhi, \
                          dl.zhuli_in, dl.zhuli_out, dl.sanhu_in, dl.sanhu_out))
        insert_sql = "insert into deal_record(`code`, `deal_time`, `zuoshou`, `open`, `close`, `high`, `low`, `volume`,\
            `amount`, `price_change`, `p_change_rate`, `turnover`, `zong_shizhi`,`liutong_shizhi`,`zhuli_in`, `zhuli_out`, `sanhu_in`, `sanhu_out`) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(insert_sql, datas)
    
    def up_classify(self, cur, mtype):
        '''
        更新个股的概念和行业信息
        '''
        cmd_sql = 'select ' + mtype + ' from stocks where code=%s'
        count=cur.execute(cmd_sql, self.code)
        if count <= 0:
            return StateCode.GET_STOCK_NULL
        result = cur.fetchone()
        values = result[0].strip().split('\t') if len(result[0].strip()) != 0 else []
        class_types = self.conceps if mtype == 'conceps' else self.hangye
        for val in class_types:
            if val not in values:
                values.append(val)
        new_cep = "\t".join(values).strip()
        cmd_base = 'update stocks set %s' %(mtype)
        cmd_sql = cmd_base + '=%s where code=%s'
        if cur.execute(cmd_sql,(new_cep, self.code)):
            return StateCode.SUCC
        return StateCode.UP_STOCK_ERR

class StockList(object):
    '''
    股票集合
    '''
    def __init__(self):
        #key为股票编号，value为Stock对象
        self.list = {} 
        
    def add(self, stock):
        self.list[stock.code] = stock
    def get(self, code = None):
        if code:
            if code in self.list:
                return self.list[code]
            else:
                return None
        return self.list
    def save_base_data(self, db):
        conn = db.get_conn()
        cur=conn.cursor()
        for stock in self.list.itervalues():
            stock.save_base_data(cur)
            if stock.can_deal:
                stock.save_deals_day(cur)
        cur.close()
        conn.commit()
        db.close(conn)
    def up_classify(self, db, mtype, is_init = False):
        conn = db.get_conn()
        cur = conn.cursor()
        if is_init:
            cmd_sql = "update stocks set %s='' where 1" %(mtype)
            cur.execute(cmd_sql)
            return StateCode.SUCC
        for stock in self.list.itervalues():
            stock.up_classify(cur, mtype)
        cur.close()
        conn.commit()
        db.close(conn)
            