import urllib
import urllib2
import time
from bs4 import BeautifulSoup

topurl = 'http://opac.lib.ustc.edu.cn/opac/top100.php'
myRequest = urllib2.Request(url = topurl)
result = urllib2.urlopen(myRequest)
html = result.read()
#print html
soup = BeautifulSoup(html,"lxml")
daytime = time.strftime('%m-%d',time.localtime(time.time()))
writing = open(daytime+'.txt','w+')
#print soup.prettify()
#print soup.table.a.string
#for child in soup.table.children:
    #print child
#print soup.table.contents
for string in soup.table.stripped_strings:
    print(string)
    writing.write(string.encode('gb2312'))
    writing.write("\r\n")
writing.write(daytime)
writing.close
