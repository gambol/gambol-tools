#!/usr/bin/env python
#coding=utf-8 

# author:zhenbao.zhou
# usage: ./alert.py subject content

import sys
import smtplib  
from email.mime.text import MIMEText  
import logging

import urllib2
import urllib
import json
import pytz
import datetime

_user = "xxx@aaa.com"  
_pwd  = "Axxxxe"  
_to   = "zxxxxx@aaa.com"   # 要改成 ba@alphayee.com

#_xignite_url = "http://globalholidays.xignite.com/xGlobalHolidays.json/IsExchangeOpenOnDate?Exchange=XNYS&Date=08/22/2016&_Token=DBEC7AE6E4C04ECEAE8F3F5F002D3C80&Username=jiawei.bao@jimu.com"
_xignite_url = "http://globalholidays.xignite.com/xGlobalHolidays.json/IsExchangeOpenOnDate?Exchange=XNYS&_Token=DBEC7AE6E4C04ECEAE8F3F5F002D3C80&Username=jiawei.bao@jimu.com&Date="


logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')

def send_mail(subject,content):
    #使用MIMEText构造符合smtp协议的header及body  
    msg = MIMEText(content)  
    msg["Subject"] = subject 
    msg["From"]    = _user  
    msg["To"]      = _to  

    if not need_alert(subject):
        logging.info("no need alert. let it go")
        return

    logging.info("send mail alert. subject:" + subject)

    s = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465, timeout=30)#连接smtp邮件服务器,端口默认是25  
    # s.set_debuglevel(1) # 开启调试
    s.login(_user, _pwd)#登陆服务器  
    s.sendmail(_user, _to, msg.as_string())#发送邮件  
    s.close()  

# 判断是否需要发送报警
# 如果subject 以 [exchangeOpenAlert]开头,说明这个指标只有在开始期间才需要报警
def need_alert(subject):
    if not subject.startswith("[exchangeOpenAlert]"):
        return True

    tz = pytz.timezone('America/New_York')
    now = datetime.datetime.now(tz)
    
    # 判断当前时间点
    if now.hour >= 16:
        return False

    ## 改成 9点
    if now.hour < 9: 
        return False

    if now.hour == 9 and now.minute < 30:
        return False

    dateStr = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
    url = _xignite_url + dateStr
    
    return  is_open_day(url)

def is_open_day(url):
    html = urllib.urlopen(url).read()
    if html is None:
        html = urllib.urlopen(url).read()  # 如果为空, 说明网络异常. 那么再来一次吧

    if html is None:
        logging.warn("html is None. url:" + url)
        return True

    jsonObj = json.loads(html)
    if jsonObj is None:
        logging.warn("无法解释html. html:" + html)
        return True    ## 如果无法解释成json, 说明xignite接口挂了, 那么还是先认为为true吧. 多报警
       
    return jsonObj["Open"]

if __name__ == "__main__":
    send_mail(sys.argv[1], sys.argv[2])
