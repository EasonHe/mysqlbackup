#!/usr/bin/bash
python  /data/script/mysqlbak.py
date=`date  '+%Y-%m-%d.00'`
target=${date}'.tar.gz'
cd /data/backup
tar -zcf $target $date --remove-files
echo "压缩完成,$target"
scp $target  backup@172.20.3.121:/data/backup/ 
localdata=`date  '+%Y-%m-%d.00.tar.gz'  --date='-7 day'` 
if [ -f ./${localdata} ];then
echo "have in"
rm ./${localdata} -f
fi
#sto=`date  '+%Y-%m-%d.00.tar.gz'  --date='-10 day'`
#ssh  backup@172.20.3.121  "rm -f /data/backup/${sto}"
