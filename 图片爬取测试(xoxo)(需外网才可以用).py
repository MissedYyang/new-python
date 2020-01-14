import re
import os
import urllib.request
import urllib


headers={"User-Agent":"Mozilla/5.0 (Windows NT 8.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
url1="http://s1.sesemp4.com/art/Zpic/"
req1=urllib.request.Request(url1,headers=headers)
res1=urllib.request.urlopen(req1).read().decode("utf-8")
#print(res1)
page=r'<li><a href="/art/html/(.*?).html" target="_blank">'
name=r'</span>(.*?)</a></li>'

page=re.findall(page,res1)
name=re.findall(name,res1)
#print(page,name)

path1="knows"
if not os.path.exists(path1):
    os.mkdir(path1)

os.chdir(path1)

for i in range(len(name)):
    url2="http://s1.sesemp4.com/art/html/"+page[i]+".html"
    osname=name[i]
    if not os.path.exists(osname):
        os.mkdir(osname)

    os.chdir(osname)

    
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 8.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    req2=urllib.request.Request(url2,headers=headers)
    res2=urllib.request.urlopen(req2).read().decode("utf-8")
    #print(res2)
    src=r'<p><img src="(.*?)" /><br /></p>'
    src1=re.findall(src,res2)
    #print(src1)
    for j in range(len(src1)):
        
        trueurl=src1[j]
        print(trueurl)
        filename=trueurl.split(r"/")[-1]
        print(filename)
        
        #urllib.request.urlretrieve(trueurl,filename,None)
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 8.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        req3=urllib.request.Request(trueurl,headers=headers)
        res3=urllib.request.urlopen(req3).read()
        
        with open(filename,"wb")as  f:
            f.write(res3)




        
