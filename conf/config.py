#!encoding=utf-8

'''
Created on 2015年6月20日

@author: fanfeifei
'''
from base.spider_type import SpiderType

class JobLevel:
    VERY_LOW_SLOW = 1
    VERY_LOW = 2
    LOW = 3
    NORMAL = 4
    HIGH = 5
    VERY_HIGH = 6
    
class RootConf:
    def __init__(self, user):
        self.user = user
        self.confs = {}
        self.confs['yafei'] = {}
        self.confs['yafei']['bin_root'] = '/home/users/miaoyafei/project/gold-mine'
        self.confs['yafei']['data_root'] = '/home/users/miaoyafei/project/data'
        
        self.confs['yafei-pc'] = {}
        self.confs['yafei-pc']['bin_root'] = 'Z:/project/gold-mine'
        self.confs['yafei-pc']['data_root'] = 'Z:/project/data'
        
    def bin_root(self):
        return self.confs[self.user]['bin_root']
    def data_root(self):
        return self.confs[self.user]['data_root']
    
class Config:
    def __init__(self, root_conf = RootConf('yafei')):
        #方便多用户开发
        self.root_conf = root_conf
        #程序根目录
        self.bin_root = self.root_conf.bin_root()
        #数据存储位置相关配置
        self.data_root = self.root_conf.data_root()
        
        self.deal_root = self.data_root + '/deal'
        self.mine_root = self.data_root + '/mine'
        self.gold_root = self.data_root + '/gold'
        self.conception_root = self.data_root + '/conception'
        self.money_flow_root = self.data_root + '/money_flow'
        self.info_root = self.data_root + '/info'
        
        #配置文件的路径
        self.conf_root = self.bin_root + '/conf'
        self.conf_file_log = self.conf_root + '/logger.conf'
        
        #spider level and thread number
        self.spider_conf = {}
        #级别 ，线程数量，抓取间隔
        self.spider_conf[JobLevel.VERY_HIGH] = (6,1)
        self.spider_conf[JobLevel.HIGH] = (5,1)
        self.spider_conf[JobLevel.NORMAL] = (1,1)
        self.spider_conf[JobLevel.LOW] = (3,1)
        self.spider_conf[JobLevel.VERY_LOW] = (3,1)
        self.spider_conf[JobLevel.VERY_LOW_SLOW] = (1,2)
        #每个spider内部job队列的最大长度
        self.spider_job_max_size = 2000
        
        #文件路径相关配置
        self.stock_base_tagfile = self.deal_root + '/stock_base_tag'
        self.stock_base_data_file = self.deal_root + '/stocklist'
        self.stock_code_file = self.deal_root + '/codelist'
        
        self.stock_concept_file = self.conception_root + '/concp'
        self.stock_hangye_file = self.conception_root + '/hangye'
        self.stock_money_flow_file = self.money_flow_root + '/mflow'
        #沪股通资金流向
        self.hgt_mone_flow_file = self.money_flow_root + '/hgt-mflow'
        #分笔交易路径
        self.fenbi_deal_dir = self.data_root + '/fenbi_deal'
        #动态变量与配置
        self.stock_code_list_time_tag = None 
        
        #接口相关
        #获取股票交易信息接口，node=sh_a 或者node=sz_a
        self.stock_list_url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=3000&sort=symbol&asc=1&symbol=&node='
        #获得概念列表
        self.stock_conception_list_url_page = "http://data.eastmoney.com/bkzj/gn.html"
        self.stock_conception_list_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=DCFFPBFM&st=(BalFlowMain)&sr=-1&p=1&ps=10000&js=&token='
        #概念下包含的股票信息
        self.stock_concept_detail_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(Code)&sr=-1&p=1&ps=2000&sty=DCFFITA&token=%s&cmd=C.%s'
        #行业列表
        self.tdx_hangye_file = self.data_root + "/tdx/base/hushen-hangye.txt"
        self.stock_hangye_list_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_bk?page=1&num=1000&sort=netamount&asc=0&fenlei=0'
        #行业detail列表
        self.stock_hangye_detail_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_ssggzj?page=1&num=2000&sort=symbol&asc=1&bankuai=0%2F'
        #资金流向
        self.stock_money_flow_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_ssggzj?page=1&num=3000&sort=symbol&asc=1&bankuai=&shichang='
        #沪股通资金流向
        self.hugutong_money_flow_url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHT&sty=SHTHPS&mkt=1'
        #检查是否开市的数据接口
        self.check_is_kaishi_url = 'http://hq.sinajs.cn/?list=sz399006'
        #分笔交易记录接口
        #http://market.finance.sina.com.cn/downxls.php?date=2015-10-19&symbol=sh600750
        self.fenbi_deal_url = "http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s"
        #flydata集合
        #今天是否开市
        self.is_kaishi_today = False
        self.today = '19700101'
        
        #数据库相关配置
        self.db_host = '127.0.0.1'
        self.db_port = 11198
        self.db_user = 'root'
        self.db_pwd = 'rankfresh!!!'
        self.db_name = 'stock'
        self.db_charset = 'utf8'

        #feature dump
        #conf dump file
        self.conf_dump_file = self.info_root + "/conf.dump.json"
