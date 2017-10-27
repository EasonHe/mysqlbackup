import os
import datetime
import time
import logging
import re
from shutil import copy2
user = 'root'
passwd='123456'
host='127.0.0.1'
path='/data/backup/'
tm=time.strftime( path +"/%Y-%m-%d.%H",time.localtime(time.time())) 
logpath = '/data/mydata/'
def get_dbname():
    cmd = "mysql -u" +user +' ' +"-h" +host +' '+"-p" +passwd+' '+ '-e'+' ' + "'show databases;'"
    database = os.popen(cmd)
    sdb=database.read()
    db=(sdb.split("\n"))
    db.remove('')
    db.remove('Database')
    db.remove('test')
    return db

def log(info):
    logging.basicConfig(filename='mybak.log', level=logging.INFO)
    logging.info(info)

def create():
   # tm=time.strftime( path +"/%Y-%m-%d.%H",time.localtime(time.time()))   
    if os.path.exists(tm) is not True:
        os.makedirs(tm)
    #else: 
    #    raise Exception('Permission denied or exist')

def senmail(c):
    summ=len(get_dbname())
    if c == summ:
       smail="curl http://172.18.13.191:4000/sender/mail"+' '+"-d" +' '+"'tos=hewei@raiyee.com&subject=mysqlbak&content=backups all successed'"
       os.system(smail)
    else:
       smail="curl http://172.18.13.191:4000/sender/mail"+' '+"-d" +' '+"'tos=hewei@raiyee.com&subject=mysqlbak&content=backups have false'"
       os.system(samil)
def dump():
    n=0
    for i in get_dbname():
        sqlcmd="mysqldump -u" +user +' '+ "-h"+host +' '+"--single-transaction"+' '+"--master-data=2" +' '+'-p'+passwd +' '+i +' ' "|" "gzip"  +' ' +'>'+ tm+'/'+i +'_'"$(date +%F).sql.gz"
        starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ret= os.system(sqlcmd)
        a=lambda x:'succeed'if ret ==0 else 'false'
        if a(ret) == 'succeed':
              n = n+1
        stoptime =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        inf= i+ ''+"at" +' '+ starttime +' '+ "starting"+' '+ "in"+' ' +stoptime+' '+ "bakup finishied"+' '+a(ret) 
        log(inf)
    return n    

def flushlog():
    cmdf="mysqladmin -u"+user +' ' +"-h"+host +' ' + "-p"+passwd + ' ' +"flush-logs"
    os.system(cmdf)
def loadfile(logpath):
    return os.listdir(logpath)

def cpfile():
    m=[]
    for  x in loadfile(logpath):
       regex=r'master-bin\..*'
       if re.match(regex,x):
          m.append(x)
    return m 

def action():
    for i in cpfile():
        path=logpath+i
        copy2(path,tm)
if __name__ == '__main__':
    create()
    senmail(dump())
    flushlog()
    action()
