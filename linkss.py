from bs4 import BeautifulSoup
import requests
import re

url = 'https://stackoverflow.com/'
sitename="https://stackoverflow.com/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
links = []

for link in soup.findAll('a', attrs={'href': re.compile("^")}):
    links.append(link.get('href'))

for link in links:
    print(link)
    try:
        if(sitename in str(link)):
            f=open("inboundlinks.txt","a")
            f.write(str(link))
            f.write("\n")
            f.close()
        elif(str(link).startswith('/')):
            f=open("inboundlinks.txt","a")
            f.write(str(link))
            f.write("\n")
            f.close()
        elif(str(link).startswith('?')):
            f=open("inboundlinks.txt","a")
            f.write(str(link))
            f.write("\n")
            f.close()            
        else:
            g=open("outboundlinks.txt","a")
            if(str(link)=="#"):
                continue
            g.write(str(link))
            g.write("\n")
            g.close()
    except:
        pass
           
