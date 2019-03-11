# -*- coding: utf-8 -*-
import scrapy
import mysql.connector
from bs4 import BeautifulSoup
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
               database="imdb",
                )
        mycursor = mydb.cursor()
        string=""
        vvv=""
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

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/title/tt7294534/']
    def parse(self, response):
        d={}
        soup = BeautifulSoup(response.text,'html.parser')
        ax = soup.find("div", {"class": "title_wrapper"})
        title = ax.find("h1")
        year = ax.find("a")
        su = soup.find("div", {"class": "subtext"})
        pos=soup.find("div", {"class": "poster"})
        idl=pos.find('a')
        idl=idl['href']
        sa=str(su.getText())  
        poster=pos.find('img')
        poster=poster['src']
        sa=str(su.getText())           
        rating = soup.find("div", {"class": "imdbRating"})
        plot_short = soup.find("div", {"class": "summary_text"}) 
        ratecount = rating.find("span", {"class": "small"})    
        ss=sa.split("|")
        similar = soup.find("div", {"class": "rec_slide"})
        ttt=similar.find_all("a")
        t=[]
        for tt in ttt:
            try:
                y=tt['href']
                y=y.split("/")
                y=y[2]
                t.append(y)
            except:
                pass
        cre = soup.find_all("div", {"class": "credit_summary_item"})       
        credit=[]
        for c in cre:
            i=1
            cred=c.find_all('a')
            val=""
            for cc in cred:
                if(len(cred)>2):
                    if(i<4):
                        val=val+(cc.getText())+","
                        i=i+1
                else:
                    val=val+(cc.getText())
            val=val[0:-1]        
            credit.append(val)     
        plot = soup.find("div", {"class": "inline canwrap"})
        trailer = soup.find("div", {"class": "slate"})
        pshort=trailer.find("a")
        rate=soup.find("div", {"class": "ratingValue"})
        f=open("uu.txt","w",encoding="utf-8")       
        f.write(str(title.getText()))
        d["title"]=str(title.getText())
        f.write("|")
        f.write(str(year.getText()))
        d["year"]=str(year.getText())
        deta = soup.find_all("div", {"class": "txt-block"})
        for det in deta:
            if "Country:" in str(det):
                country=det.find("a")
            if "Language:" in str(det):
                lang=det.find("a")
            if "Production Co:" in str(det):
                p=1
                de=det.find_all("a")
                val=""
                for cc in de:
                    if(len(cred)>2):
                        if(p<4):
                            val=val+(cc.getText())+","
                            p=p+1
                    else:
                        val=val+(cc.getText())
                production=val[0:-1]
        if(len(ss)>4):
            f.write("-")
            f.write("|")
            d["certified"]="-"
            d["time"]=str((ss[0]).replace("\n",""))
            d["Genres"]=str((ss[1]).replace("\n",""))
            d["releasedate"]=str((ss[2]).replace("\n",""))
        else:
            d["certified"]=str((ss[0]).replace("\n",""))
            d["time"]=str((ss[1]).replace("\n",""))
            d["Genres"]=str((ss[2]).replace("\n",""))
            d["releasedate"]=str((ss[3]).replace("\n",""))
        for s in ss:
            s=s.strip()
            f.write("|")
            f.write(str(s.replace("\n","")))
        for s in credit:
            '''if "," in str(s):
                s=s.split(",")
                s=s[0:-1]
                for'''
            s=s.strip()
            f.write("|")
            f.write(str(s.replace("\n","")))
        d["director"]=str((credit[0]).replace("\n",""))
        d["writer"]=str((credit[1]).replace("\n",""))
        d["actor"]=str((credit[2]).replace("\n",""))    
        f.write("|")
        f.write(str((plot.getText()).strip()))
        d["plot"]=str((plot.getText()).strip())
        f.write("|")
        f.write(str((lang.getText()).strip()))
        d["lang"]=str((lang.getText()).strip())
        f.write("|")
        f.write(str((country.getText()).strip()))
        d["country"]=str((country.getText()).strip())
        f.write("|")
        f.write(str(production))
        d["production"]=str(production)
        f.write("|")
        try:
            f.write(str((rate.getText()).strip()))
            d["rating"]=str((rate.getText()).strip())
        except:
            f.write("-")
            d["rating"]="-"
        f.write("|")    
        try:
            f.write(str((ratecount.getText()).strip()))
            d["voters"]=str((ratecount.getText()).strip())
        except:
            f.write("-")
            d["voters"]="-"
        f.write("|")    
        try:
            f.write(str((poster).strip()))
            d["poster"]=str((poster).strip())
        except:
            f.write("-")
            d["poster"]="-"
        f.write("|")    
        try:
            f.write(str((idl.split("/"))[2]))
            d["titleid"]=str((idl.split("/"))[2])
        except:
            f.write("-")
            d["titleid"]="-"
        f.write("|")    
        try:
            #f.write(str(("https://www.imdb.com"+pshort['href']))
            li=str(pshort['href'])
            d["trailer"]="https://www.imdb.com"+li
        except:
            f.write("-")
            d["trailer"]="-"
        f.write("|")    
        try:
            f.write(str((plot_short.getText()).strip()))
            d["plot_short"]=str((plot_short.getText()).strip())
        except:
            f.write("-")
            d["plot_short"]="-"
        f.write("|")    
        try:
            f.write(str(t))
            d["simliar_movies"]=str(t)
        except:
            f.write("-")
            d["simliar_movies"]="-"                      
        f.close()
        l=[]
        l.append(d)
        sqlwrite(l,"data")
