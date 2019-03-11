# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import mysql.connector
import datetime
from bs4 import BeautifulSoup 
import subprocess
import requests
import whois
from datablogger_scraper.items import DatabloggerScraperItem
pages = set()
internalpages = set()
count=0
crawl=0
domain="http://novelupdates.com"
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

class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    global l
    global t
    name = "datablogger"
    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["novelupdates.com"]

    # The URLs to start with
    start_urls = ["http://novelupdates.com"]

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse_items(self, response):
        global d
        global l
        global t
        global crawl
        global pages
        global count
        global domain
        p={}
        d['domain']=domain
        count=count+1
        d['iurls_crawled']=count
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            ttt=[]
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            d['last_updated']=(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            if is_allowed:
                item = DatabloggerScraperItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)
                internalpages.add(link.url)
                internalpages.add(response.url)
                r=requests.get(link.url)
                soup = BeautifulSoup(r.text)
                imgs = soup.findAll("img",{"src":True})
                for img in imgs:
                    img_url = img["src"]
                    ttt.append(img_url)
                for tt in ttt:
                    r=requests.get(tt)
                    try:
                        if((int(r.status_code)!=200) and (int(r.status_code)!=301) and (int(r.status_code)!=302)):
                            p={"url" :tt,
                              "domain":dt,
                              "found on":response.url,
                              "found time":(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                              }
                            if tt not in list(pages):
                                t.append(p)
                    except:
                        pass
                    pages.add(dt)     
                #crawl=crawl+len(items)
                d['iurls_found']=len(internalpages)
            else:
                try:
                    li=((link.url).split("//"))[1]
                    li=((li).split("www."))[1]
                    li=(li.split("/"))[0]
                except:
                    li=(li.split("/"))[0]
                dt=li
                r=requests.get(link.url)
                if((int(r.status_code)!=200) and (int(r.status_code)!=301) and (int(r.status_code)!=302)):
                    p={"url" :link.url,
                        "domain":dt,
                        "found on":response.url,
                        "found time":(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                      }
                    if dt not in list(pages):
                        t.append(p)
                        #d['total external urls found']=len(pages)
                        d['eurls_found']=t
                        #f=open("urls.out","w+")
                        l.append(d)
                        #f.write(str(l))
                        #f.close()
                        sqlwrite(l,"projects")
                pages.add(dt)     
        # Return all the found items
        #sqlwrite(l,"projects")
        return d
