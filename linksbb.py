import bs4 as bs
import urllib2
from threading import Thread
from Queue import Queue
import ssl
concurrent = 1200
s=1
def doWork():
    while True:
        url = q.get()
        urlstatus = getStatus(url)
        q.task_done()

def getStatus(myurl):
    context = ssl._create_unverified_context()
	myurl=(myurl.split("//"))[1]
    files=myurl.replace(".", "_")
    try:
        source = urllib2.urlopen(myurl,context=context,timeout=2).read()
        source=str(source)
        soup = BeautifulSoup(source, "html.parser")
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^")}):
            links.append(link.get('href'))
        for link in links:
            try:
                if(myurl in str(link)):
                    f=open(files+"inboundlinks.txt","a")
                    f.write(str(link))
                    f.write("\n")
                    f.close()
                elif(str(link).startswith('/')):
                    f=open(files+"inboundlinks.txt","a")
                    f.write(str(link))
                    f.write("\n")
                    f.close()
                elif(str(link).startswith('?')):
                    f=open(files+"inboundlinks.txt","a")
                    f.write(str(link))
                    f.write("\n")
                    f.close()            
                else:
                    g=open(files+"outboundlinks.txt","a")
                    if(str(link)=="#"):
                        continue
                    g.write(str(link))
                    g.write("\n")
                    g.close()
        except:
           pass
    except:
        t=open("fail.txt","a+")
        t.write(myurl)
        t.write('\n')
        t.close() 

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    with open("a.txt") as infile:
        for line in infile:
            lin="https://"+line
            q.put(lin.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
