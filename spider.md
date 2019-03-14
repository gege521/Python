``` Python
# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

# -*- coding: utf-8 -*-
import xlrd, re, csv
from selenium import webdriver
from bs4 import BeautifulSoup
import PyMySQL
import json

class fileLoader():
    def __init__(self):
        self.souFileName = "/Users/zhangge/Desktop/prc_sn_02.181.xlsx"



    def ReaderSource(self):  #read sn
        workbook = xlrd.open_workbook(self.souFileName)
        booksheet = workbook.sheet_by_name('prc_sn_02.18')
        arr = []
        for row in range(booksheet.nrows):
            for col in range(booksheet.ncols):
                cel = booksheet.cell(row, col)
                val = cel.value
                arr.append(val)

        return arr

    def spirder(self, source): 
        page_url = 'https://newsupport.lenovo.com.cn/api/drive/'+source+'/drivesetinginfo'
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
            conn = PyMySQL.connect(host='localhost', user='root', passwd='root', db='sn_info', port=3306, charset="utf8")
            cur = conn.cursor()
            values = info
            print (values)
            print (len(values))
            print ("--------")
            print (values[0])
            if len(values) == 41:
                values.append('null')
                print (len(values))
            cur.execute("insert into sn_info_sec values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
            conn.commit()
            cur.close()
            conn.close()
        except PyMySQL.Error as e:
            print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def run(self):
        sns = fileLoader().ReaderSource()
        for sn in sns:
            print (sn)
            print ("====================")
            info = fileLoader().spirder(sn)
            print(info)

            if len(info) >= 41:
                fileLoader().writemysql(info)


if __name__ == "__main__":
    #fileLoader().spirder("M702QU6Z")
    fileLoader().run()
```