#!encoding=utf-8
'''
Created on 2015年10月12日

@author: Yafei
'''
import MySQLdb
import sys

class DB(object):
    '''
    classdocs
    '''


    def __init__(self, conf):
        '''
        Constructor
        '''
        self.db_host = conf.db_host
        self.db_port = conf.db_port
        self.db_user = conf.db_user
        self.db_pwd = conf.db_pwd
        self.db_name = conf.db_name
        self.db_charset = conf.db_charset

    def get_conn(self):
        conn = None
        try:
            conn=MySQLdb.connect(host=self.db_host, \
                             user=self.db_user,\
                             passwd=self.db_pwd,\
                             db=self.db_name,\
                             port=self.db_port,\
                             charset=self.db_charset)
        except MySQLdb.Error,e:
            conn = None
            print >>sys.stderr, "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return conn
    def close(self,conn):
         conn.close()
    
'''
        import MySQLdb
 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
    cur=conn.cursor()
    cur.execute('select * from user')
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
　　请注意修改你的数据库，主机名，用户名，密码。

下面来大致演示一下插入数据，批量插入数据，更新数据的例子吧：

import MySQLdb
 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
    cur=conn.cursor()
     
    cur.execute('create database if not exists python')
    conn.select_db('python')
    cur.execute('create table test(id int,info varchar(20))')
     
    value=[1,'hi rollen']
    cur.execute('insert into test values(%s,%s)',value)
     
    values=[]
    for i in range(20):
        values.append((i,'hi rollen'+str(i)))
         
    cur.executemany('insert into test values(%s,%s)',values)
 
    cur.execute('update test set info="I am rollen" where id=3')
 
    conn.commit()
    cur.close()
    conn.close()
 
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
　　请注意一定要有conn.commit()这句来提交事务，要不然不能真正的插入数据。

运行之后我的MySQL数据库的结果就不上图了。

import MySQLdb
 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
    cur=conn.cursor()
     
    conn.select_db('python')
 
    count=cur.execute('select * from test')
    print 'there has %s rows record' % count
 
    result=cur.fetchone()
    print result
    print 'ID: %s info %s' % result
 
    results=cur.fetchmany(5)
    for r in results:
        print r
 
    print '=='*10
    cur.scroll(0,mode='absolute')
 
    results=cur.fetchall()
    for r in results:
        print r[1]
     
 
    conn.commit()
    cur.close()
    conn.close()
 
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
　　运行结果就不贴了，太长了。

查询后中文会正确显示，但在数据库中却是乱码的。经过我从网上查找，发现用一个属性有可搞定：

在Python代码 

conn = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='python') 中加一个属性：
 改为：
conn = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8') 
charset是要跟你数据库的编码一样，如果是数据库是gb2312 ,则写charset='gb2312'。

 

下面贴一下常用的函数：

然后,这个连接对象也提供了对事务操作的支持,标准的方法
commit() 提交
rollback() 回滚

cursor用来执行命令的方法:
callproc(self, procname, args):用来执行存储过程,接收的参数为存储过程名和参数列表,返回值为受影响的行数
execute(self, query, args):执行单条sql语句,接收的参数为sql语句本身和使用的参数列表,返回值为受影响的行数
executemany(self, query, args):执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数
nextset(self):移动到下一个结果集

cursor用来接收返回值的方法:
fetchall(self):接收全部的返回结果行.
fetchmany(self, size=None):接收size条返回结果行.如果size的值大于返回的结果行的数量,则会返回cursor.arraysize条数据.
fetchone(self):返回一条结果行.
scroll(self, value, mode='relative'):移动指针到某一行.如果mode='relative',则表示从当前所在行移动value条,如果 mode='absolute',则表示从结果集的第一行移动value条.
'''