``` python
# -*- coding: utf-8 -*-

import requests
import pymysql
import json
import time
import numpy as np

class fileLoader():
    def __init__(self):
        self.dbconn = pymysql.connect(
          host="localhost",
          database="database",
          user="user",
          password="password",
          port=3306,
          charset='utf8'
         )
        self.cursor = self.dbconn.cursor()
    
    
    
    def ReaderSource(self):   
        
        
        #sql语句
        sqlcmd="select data from tablename"
        
        
        self.cursor.execute(sqlcmd)
        arr=self.cursor.fetchall() 
        
        return arr
        self.dbconn.close()
    def spirder(self, source):
        headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        page_url = 'https://newsupport.lenovo.com.cn/api/drive/'+str(source)+'/drivesetinginfo'
        time.sleep(np.random.rand()*2)
        html = requests.get(page_url, headers=headers, timeout=20).text
        data = json.loads(html)
        data1 = data['data']
        dict1 = []
        if len(data1) > 0:          
            for i in range(len(data1)):
                data2 = data1[i]['Data']
                for j in range(len(data2)):
                    dict1.append(data2[j]['Notes'])
            return dict1
    def writemysql(self, info):

        try:
            
            values = info
            print (values)
            print (len(values))
            print ("--------")
            print (values[0])
            if len(values) == 41:
                values.append('null')
                print (len(values))
            self.cursor.execute("insert into prc_bom_info values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
            self.dbconn.commit()
            self.cursor.close()
            self.dbconn.close()
        except pymysql.Error as e:
            print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def run(self):
        sns = fileLoader().ReaderSource()
        for sn in sns:
            print (sn)
            print ("====================")
            info = fileLoader().spirder(sn)
            print(info)
            #print ','.join(info)
        #    if len(info) >= 41:
         #       fileLoader().writemysql(info)


if __name__ == "__main__":
    fileLoader().run()
    
```
