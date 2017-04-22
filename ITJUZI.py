# -*- coding: utf_8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import time
import MySQLdb
import json
from lxml import etree

from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def getHTMLdata(comId):
    driver.get("http://www.itjuzi.com/company/" + str(comId))
    pageSource = driver.page_source
 
    selector = etree.HTML(pageSource)
    companyId = comId
    companyName=''
    financingTime=''
    financingRound=''
    financingAmount=''
    investorList=''
    try:
        companyName = selector.xpath('//div[@class="line-title"]/span/b/text()')[0].strip()
        # 融资时间
        financingTime = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/span[1]/text()')[0]#selector.xpath('//table[@class="list-round-v2"]/tr[1]/td[1]/span[1]/text()').strip()

        # 轮次  class="round"
        financingRound = selector.xpath('//span[@class="round"]/a/text()')[0]#'TEST'  # selector.xpath('//span[@class="round"]/text()')[0].strip()

        # 融资额
        financingAmount= selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/span/a/text()')[0] #selector.xpath('//table[@class="list-round-v2"] ')
        # 投资方
        investorList=selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/child::a/text()')
        investorList=",".join(list(investorList))

    except:
        print(' error meet')
        pass
    print companyId
    print companyName
    print financingTime
    print financingRound
    print financingAmount
    print  investorList

    conn = MySQLdb.connect(
        host='#',
        port=3306,
        user='#',
        passwd='#',
        db='spider',
        charset="utf8"
    )
    cur = conn.cursor()
    insertSQL = "INSERT INTO ITJUZI \
                      (`companyId`,`companyName`,`financingTime`,`financingRound`,`financingAmount`,`investor`,`creatTime`)VALUES \
                      (%d,'%s','%s','%s','%s','%s','%s')" % \
                (int(companyId),companyName  ,financingTime,financingRound,financingAmount,investorList,
                 time.strftime('%Y-%m-%d %H:%M:%S') )
    cur.execute(insertSQL)
    conn.commit()

    cur.close()
    conn.close()




# Here put your chromedriver path.
driver = webdriver.Chrome('/Users/scottxiao/Downloads/chromedriver')
username = "666666@qq.com"  # your username
password = "666666"   # your password
driver.get('https://www.itjuzi.com/user/login')
cookie1 = driver.get_cookies()
elem = driver.find_element_by_xpath("/html/body")
elem.send_keys(Keys.ENTER)

time.sleep(1)
elem = driver.find_element_by_xpath("//*[@id='create_account_email']")
elem.send_keys(username)
elem = driver.find_element_by_xpath("//*[@id='create_account_password']")
elem.send_keys(password)
elem.send_keys(Keys.ENTER) 

for companyId in range(2681, 52302):
    getHTMLdata(companyId)
driver.close()



