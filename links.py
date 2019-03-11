import re
import requests
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument( '-s',"--sitename",type=str)
args = parser.parse_args()

concurrent = 256

pages = set()

def get_links(page_url):
  time.sleep(1)
  global pages
  pattern = re.compile("^(/)")
  try:
      html = requests.get(page_url).text # fstrings require Python 3.6+
      soup = BeautifulSoup(html, "html.parser")
      for link in soup.find_all("a", href=pattern):
          if "href" in link.attrs:
              if link.attrs["href"] not in pages:
                  new_page = link.attrs["href"]
                  #new_page ="https://www.wuxiaworld.com"+new_page
                  f=open("foundlinks.txt","a+")
                  f.write(new_page)
                  f.write("\n")
                  f.close()
                  if "apiajax" in str(new_page):
                    f=open("sitelinks.txt","a+")
                    f.write(new_page)
                    f.write("\n")
                    f.close()
                  pages.add(new_page)
                  get_links(args.sitename+new_page)
  except:
      pass     
   
def doWork():
    while True:
        url = q.get()
        urlstatus = get_links(url)
        q.task_done()
q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for i in range(1,40):
        q.put(args.sitename)
    q.join()
except KeyboardInterrupt:
    sys.exit(1)        
