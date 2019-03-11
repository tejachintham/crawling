# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import mysql.connector
import datetime
import bs4
import requests
import whois
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request

DOMAIN = 'example.com'
URL = 'http://%s' % DOMAIN
class MySpider(BaseSpider):
    name = DOMAIN
    allowed_domains = []
    start_urls = [
        URL
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            if not ( url.startswith('http://') or url.startswith('https://') ):
                url= URL + url 
            print(url)
            yield Request(url, callback=self.parse)

pages = set()
internalpages = set()
count=0
crawl=0
domain="wuxiaworld.com"
d={}
d['started_at']=datetime.datetime.now()
l=[]
t=[]
def sqlwrite(data,tablename):
    global domain
    for ll in data:
        print(data)
        keys=[]
        value=[]
        values=ll.items()
        for v,x in values:
            if(x==None):
                x="0"
            keys.append(str(v))
            value.append(str(x))
        mydb = mysql.connector.connect(
               host="localhost",
               user="root",
               passwd="",
               database="domains_expiry",
                )
        mycursor = mydb.cursor()
        string=""
        vvv=""
        sql_Delete_query = "DELETE FROM "+tablename+" WHERE domain = '"+domain+"'"
        mycursor.execute(sql_Delete_query)
        for k in keys:
            string=string+k+","
        for i in range(len(keys)):
            vvv=vvv+"%s,"
        vvv=vvv[:-1]    
        string=string[:-1]   
        sql = "INSERT INTO "+tablename+" ("+string+") VALUES ("+str(vvv)+")"
        #val = (id_val,user_id,serverid,sername,ipadrress,serverprovider)
        val=value
        print(val)
        mycursor.execute(sql,val)
        mydb.commit()
        mydb.close()
