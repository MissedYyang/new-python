#http://yj1.b96dure93e9.rocks/pw/index.php?cateid=1
#1.小说下载
#2.图片下载
#3.视频下载
#----------------make   by   -Yyang------------------------------
import urllib.request
import urllib
import requests
import queue
import threading
import re
import os
import sys
import time

'''======================================小说========================================================='''
class Mythread_1(threading.Thread):
	"""线程1，用来爬取小说的具体网页的线程"""
	def __init__(self, page_queue,href_queue):
		super(Mythread_1, self).__init__()
		self.page_queue=page_queue#用来存放网页的页码的队列（即，爬取几页）
		self.href_queue=href_queue#用来存放每个小说的网页的队列
		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
		self.url="http://yj1.b96dure93e9.rocks/pw/thread.php?fid=17&page="

	def run(self):
		try:
			while not self.page_queue.empty():#判断页码队列是否为空
				print("开始线程1。。。。。。。。。。。。。。。。。。。")
				page=self.page_queue.get()#获取页码
				url=self.url+str(page)#构造完整的网址
				req=urllib.request.Request(url,headers=self.headers)
				result=urllib.request.urlopen(req).read().decode()#获取响应
				#print(result)#打印响应测试
				href='"打开新窗口" href="html_data/(.*?)" target="'#定义href的规律
				href_all=re.findall(href,result)#获取网页中所有的href信息
				#print(len(href_all))#打印测试
				#print(href_all,"\n")#打印测试
				for j in range(len(href_all)):
					self.href_queue.put(href_all[j])
			print("结束线程1。。。。。。。。。。。。。。。。。。。")
		except Exception as e:
			print("来自线程1，不要慌，小问题而已：",e)
			

class Mythread_2(threading.Thread):
	"""线程2，用来爬取"""
	def __init__(self,href_queue,titel_queue,text_queue):
		super(Mythread_2, self).__init__()
		self.href_queue=href_queue#用来存放每个小说的网页的队列
		self.titel_queue=titel_queue#用来存放每个小说标题的队列
		self.text_queue=text_queue#用来存放每个小说的内容的队列
		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
		self.url="http://yj1.b96dure93e9.rocks/pw/html_data/"

	def run(self):
		try:
			while not self.href_queue.empty():#用来判断获得的小说的网页是否为空
				print("开始线程2。。。。。。。。。。。。。。。。。。。")
				href=self.href_queue.get()#从存放每个小说的网页的队列取值
				url1=self.url+str(href)
				#print(url1)
				req1=urllib.request.Request(url1,headers=self.headers)
				result1=urllib.request.urlopen(req1).read().decode()#获取响应
				#print(result1)
				title='<span id="subject_tpc">(.*?)</span>'
				title_all=re.findall(title,result1)#获取响应中的所有标题信息
				text='<div class="f14" id="read_tpc">(.*?)</div>'#定义小说的文字的规律
				textall=re.findall(text,result1)#获取响应中的所有文字信息
				#print(textall,"\n")#打印测试
				#print(title_all[0],textall[0])
				self.titel_queue.put(title_all[0])
				self.text_queue.put(textall[0])
			print("结束线程2。。。。。。。。。。。。。。。。。。。")
		except Exception as e:
			print("来自线程2，不要慌，小问题而已：",e)



class Mythread_3(threading.Thread):
	"""线程3，用来保存文本"""
	def __init__(self,titel_queue,text_queue):
		super(Mythread_3, self).__init__()
		self.text_queue=text_queue#用来存放每个小说的内容的队列
		self.titel_queue=titel_queue#用来存放每个小说标题的队列

	def run(self):
		try:
			while not self.titel_queue.empty():
				print("开始线程3。。。。。。。。。。。。。。。。。。。")
				title=self.titel_queue.get()
				text=self.text_queue.get()
				#print(title,"\n",text,"\n")
				text1=text.replace("<br>","\n")
				text2=text1.replace("&nbsp","")
				#print(type(text2))
				#print(title,"\n",text,"\n")
				with open("mysider.txt","a",encoding='utf-8')as f:
					f.write("{},\n,{},\n,\n".format(title,text2))
					time.sleep(4)
				
			print("结束线程3。。。。。。。。。。。。。。。。。。。")
		except Exception as e:
			print("来自线程3，不要慌，小问题而已：",e)
			


'''=============================================图片=============================================================='''
class Mythread1_1(threading.Thread):
	"""线程1——1，用来爬取小说的具体网页的线程"""
	def __init__(self, page_queue,href_queue):
		super(Mythread1_1, self).__init__()
		self.page_queue=page_queue#用来存放网页的页码的队列（即，爬取几页）
		self.href_queue=href_queue#用来存放每个图片的网页的队列
		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
		self.url="http://yj1.b96dure93e9.rocks/pw/thread.php?fid=15&page="

	def run(self):
		try:
			while not self.page_queue.empty():#判断页码队列是否为空
				print("开始线程1——1。。。。。。。。。。。。。。。。。。。")
				page=self.page_queue.get()#获取页码
				url=self.url+str(page)#构造完整的网址
				req=urllib.request.Request(url,headers=self.headers)
				result=urllib.request.urlopen(req).read().decode()#获取响应
				#print(result)#打印响应测试
				href='"打开新窗口" href="html_data/(.*?)" target="'#定义href的规律
				href_all=re.findall(href,result)#获取网页中所有的href信息
				#print(href_all)#打印测试
				#print(href_all,"\n")#打印测试
				for j in range(len(href_all)):
					self.href_queue.put(href_all[j])
			print("结束线程1——1。。。。。。。。。。。。。。。。。。。")
		except Exception as e:
			print("来自线程1——1，不要慌，小问题而已：",e)
			

class Mythread1_2(threading.Thread):
	"""线程1——2，用来爬取每一个图片的集合大标题的的网址"""
	def __init__(self,href_queue,titel_queue,image_queue):
		super(Mythread1_2, self).__init__()
		self.href_queue=href_queue#用来存放每个图片的网页的队列
		self.titel_queue=titel_queue#用来存放每个图片标题的队列
		self.image_queue=image_queue#用来存放每个图片的网址的队列
		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
		self.url="http://yj1.b96dure93e9.rocks/pw/html_data/"

	def run(self):
		try:
			while not self.href_queue.empty():#用来判断获得的图片的网页是否为空
				print("开始线程1——2。。。。。。。。。。。。。。。。。。。")
				href=self.href_queue.get()#从存放每个图片的网页的队列取值
				url1=self.url+str(href)
				#print(url1)
				req1=urllib.request.Request(url1,headers=self.headers)
				result1=urllib.request.urlopen(req1).read().decode()#获取响应
				#print(result1)
				title='<span id="subject_tpc">(.*?)</span>'
				title_all=re.findall(title,result1)#获取响应中的所有标题信息
				image='<img src="(.*?)" border="'#定义图片的网页的规律
				imageall=re.findall(image,result1)#获取响应中的所有图片链接
				#print(title_all,imageall)
				self.titel_queue.put(title_all[0])
				for k in range(len(imageall)):
					self.image_queue.put(imageall[k])

			print("结束线程1——2。。。。。。。。。。。。。。。。。。。")
		except Exception as e:
			print("来自线程1——2，不要慌，小问题而已：",e)



class Mythread1_3(threading.Thread):
	"""线程1_3，用来保存文本"""
	def __init__(self,titel_queue,image_queue):
		super(Mythread1_3, self).__init__()
		self.image_queue=image_queue#用来存放每个图片的网址的队列
		self.titel_queue=titel_queue#用来存放每个小说标题的队列
		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}

	def run(self):
		try:
			#title=self.titel_queue.get()
			#os.mkdir(title)
			while not self.image_queue.empty():
				print("开始线程1——3。。。。。。。。。。。。。。。。。。。")
				image_url=self.image_queue.get()
				#print(image_url)
				name=image_url.split("/")[-1]
				#urllib.request.urlretrieve(image_url,name,None)
				req2=urllib.request.Request(image_url,headers=self.headers)
				result2=urllib.request.urlopen(req2).read()#获取响应
				with open(name,"wb")as f:
					f.write(result2)

			print("结束线程1——3。。。。。。。。。。。。。。。。。。。")
		except Exception as e:
			print("来自线程1——3，不要慌，小问题而已：",e)



'''============================================================================================================='''			



#主函数，存放程序运行的主要逻辑思维
def main():
	print("==================================感谢您使用本程序=-By-Yyang=========================")
	page_queue=queue.Queue()#用来存放网页的页码的队列（即，爬取几页）
	href_queue=queue.Queue()#用来存放每个小说的网页的队列
	text_queue=queue.Queue()#用来存放每个小说的内容的队列
	titel_queue=queue.Queue()#用来存放每个小说标题的队列
	image_queue=queue.Queue()#用来存放每个图片网址的队列
	for i in range(1,4):
		page_queue.put(i)
	path="novel"
	if not os.path.exists(path):
		os.mkdir(path)
	os.chdir(path)

	print("1:小说                  2：图片                     3：视屏")
	num=str(input("请输入对应的数字："))
	if num=="1":
		t1=Mythread_1(page_queue,href_queue)#实例化线程1，并传入参数
		t1.start()   #开始执行线程1
		t2=Mythread_2(href_queue,titel_queue,text_queue)#实例化线程2，并传入参数
		time.sleep(10)
		t2.start()   #开始执行线程2
		t3=Mythread_3(titel_queue,text_queue)#实例化线程3，并传入参数
		time.sleep(15)
		t3.start()   #开始执行线程3
		t1.join()
		t2.join()
		t3.join()
		print("保存完毕。。。。。。。。。。。")
		sys.exit()

	elif num=="2":
		
		t1_1=Mythread1_1(page_queue,href_queue)#实例化线程1——1，并传入参数
		t1_1.start()   #开始执行线程1——1
		t1_2=Mythread1_2(href_queue,titel_queue,image_queue)#实例化线程1——2，并传入参数
		time.sleep(10)
		t1_2.start()   #开始执行线程1——2
		t1_3=Mythread1_3(titel_queue,image_queue)#实例化线程1——3，并传入参数
		time.sleep(15)
		t1_3.start()   #开始执行线程1——3
		t1_1.join()
		t1_2.join()
		t1_3.join()
		print("保存完毕。。。。。。。。。。。")
		sys.exit()

	elif num=="3":
		print("心情好的时候在做这个。。。。。。。。。。。")


	else:
		print("输入有误！！！！！！！")



#程序执行开始位置
if __name__ == '__main__':
	main()
			
#小说
#主页：http://yj1.b96dure93e9.rocks/pw/index.php?cateid=1
#小说：http://yj1.b96dure93e9.rocks/pw/thread.php?fid=17&page=1 #第一页
#小说内容：http://yj1.b96dure93e9.rocks/pw/html_data/17/2001/4541550.html
#
#相片
#主页：http://yj1.b96dure93e9.rocks/pw/thread.php?fid=15&page=1
#相片：http://yj1.b96dure93e9.rocks/pw/html_data/15/2001/4543048.html
#相片内容：http://p8.urlpic.club/pic20190701/upload/image/20200110/11006105197.jpg
