#电影爬取  http://www.yy6080.cn/vodtypehtml/1.html
#加入了多线程下载ts文件
#加入每个小视频  单独放入各自的文件夹里面  避免混乱
#合并ts时  记得改名字

import re
import requests
import time
import os
from multiprocessing import Pool


#获取电影的名称和链接
def get_url1():
	#伪装浏览器浏览
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
	#打开网址并获取回应http://www.yy6080.cn/vodtypehtml/1.html
	res1=requests.get('http://www.yy6080.cn/vodtypehtml/1.html',headers=headers,cookies=cookiesoen)
	
	
	#打印回应测试
	#print(res1.text)
	#title标题正则表达式，src链接正则表达式
	#标题这里获取不是“utf-8”的格式  ，  原因未知
	#title='<a style="position:relative;display:block;" title="(.*?)" target="_blank" href="'
	src='" target="_blank" href="(.*?)"'

	#获取全部title   src
	#title_all=re.findall(title,res1.text)
	src_all=re.findall(src,res1.text)
	#print(len(title_all),len(src_all))
	#返回值，有两个,x
	#修改后这里只有一返回值
	return src_all
	
#获取电影播放链接
def get_play_url(src_all):
	play_url_all=[]
	for i in src_all:
		#网址拼接
		url2='http://www.yy6080.cn'+i
		#打印网址测试
		#print(url2)
		#伪装浏览器浏览
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		#打开网址并获取回应
		res2=requests.get(url=url2,headers=headers,cookies=cookiesoen)
		
		
		#打印回应测试
		#print(res2.text)
		#播放地址规律
		play_url='href="(.*?)" target="_blank"'
		#获取全部地址
		play_url_all1=re.findall(play_url,res2.text)
		#获取播放地址的第一个（有些有多个播放地址）
		#print(play_url_all[0])
		play_url_all.append(play_url_all1)
	#函数结束后，返回值
	return play_url_all

#获取电影名，电影播放地址 （链接：有其他资料     地址：只包括电影资料）
def down(play_url_all):
	title_all=[] #电影名字
	play_all=[]  #电影播放地址
	for i in range(0,len(play_url_all)):
		#print(i)
		#悬案密码2野鸡杀手 (2014)  测试地址http://www.yy6080.cn/vodhtml/31734.html
		#url3='http://www.yy6080.cn/vod-play-id-31740-src-1-num-1.html'
		url3='http://www.yy6080.cn'+play_url_all[i][0]
		#print(url3)
		#伪装浏览器浏览
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		#打开网址并获取回应http://www.yy6080.cn/vodtypehtml/1.html
		res3=requests.get(url=url3,headers=headers)
		#获取当前cookies
		cookiesoen=res3.cookies
		
		#获取cookies
		#Cookies=res3.Cookies
		#打印回应测试
		#time.sleep(5)
		#print(res3.text)
		#https://zy.aoxtv.com/m3u8.php?url=https://v3.szjal.cn/20200309/PqOI9DHP/index.m3u8
		# https://v3.szjal.cn/20200309/PqOI9DHP/hls/index.m3u8
		# https://v3.szjal.cn/20200309/PqOI9DHP/hls/2J5DNaKp.ts
		# https://v3.szjal.cn/20200309/PqOI9DHP/hls/3qje9Qsn.ts
		# 
		# 视频名字，获取
		title='<h3 class="movie-title">(.*?)</h3>'
		title_a1=re.findall(title,res3.text)
		#获取播放地址的最后后缀  https://hls.aoxtv.com/v3.szjal.cn/share/pyCcHYmuVCLBZWzb，
		m3u8_1="<script>(.*?)</script>"
		m3u8_2=re.findall(m3u8_1,res3.text)
		#打印测试
		#print(m3u8_2)
		#print(m3u8_2[1].split(',')[-1].split('.')[-1][-20:-4])
		#截取字符串
		j=m3u8_2[1].split(',')[-1].split('.')[-1][-20:-4]
		#构造播放地址
		url4='https://hls.aoxtv.com/v3.szjal.cn/share/'+j

		#print(title_a1[0])
		#print("电影链接：",url4)
		#电影名字，链接加入对应列表
		title_all.append(title_a1[0])
		play_all.append(url4)
	#多个返回值   电影名，地址
	return title_all,play_all


#用来下载视频的m3u8大地址
def get_m3u8_1(title_all,play_all):
	#用来下载视频的m3u8大地址---------->小地址
	big=[]#用来储存第一层m3u8文件
	#print(play_all)
	for i in range(0,len(play_all)):
		#异常捕获
		try:
				#url5='https://hls.aoxtv.com/v3.szjal.cn/share/jB887b3nevU3VjLV'
			url5=play_all[i]
			#print(url5)
			#伪装浏览器浏览
			headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

			#打开网址并获取回应
			res5=requests.get(url=url5,headers=headers,cookies=cookiesoen)
			#print(res5.text)
		
			
			#正则表达式获取响应里面的m3u8地址
			#这个位置需注意  昨天的今天用不了  可能需要修改
			m3u8='type:"hls",url:"(.*?)"'
			m3u8_one=re.findall(m3u8,res5.text)

			#打印测试
			#print(m3u8_one)
			#获取相响应
			res6=requests.get(url=m3u8_one[0],headers=headers,cookies=cookiesoen)
			#把文件保存为first_m3u8   路径为："C:\Users\admin\Desktop\yy6080\first_m3u8"
			#文件名字
			mm=title_all[i]+"one.m3u8"
			#先  以写入的方式创建一个文件
			f=open(mm,mode='wb')
			#写入文件
			f.write(res6.content)
			#文件关闭
			f.close()
			#再次打开文件
			f=open(mm,mode="r",encoding="utf-8")
			#读取文件第一行
			f.readline()
			#读取文件第二行
			f.readline()
			#读取文件第三行，赋值给url7
			url7=f.readline()
			#打印测试
			#print(url7)
			#关闭文件
			f.close()
			#把大m3u8加入列表
			big.append(url7)
		except Exception as e:
			#如果报错，忽略错误继续工作
			big.append("no")
			continue
	#返回值
	return big

#用来下载视频的m3u8小地址
def get_m3u8_2(title_all,big):
	for i in range(0,len(big)):
		try:
				#伪装浏览器浏览
			headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
			#打开网址并获取回应
			#print(big[i])
			res8=requests.get(big[i],headers=headers,cookies=cookiesoen)

			#打印测试发现，很多都是加密的，只能拿到大m3u8地址
			#print(res8.text)
			
			#先  以写入的方式创建一个文件
			mn=title_all[i]+'two.m3u8'
			f=open(mn,mode='wb')
			#写入文件
			f.write(res8.content)
			#文件关闭
			f.close()

		except Exception as e:
			continue

#用来获取视频的每个ts视频文件
def get_movie(title_all,big):
	#pool=Pool(10)
	down_url=[]#每个小视频链接
	dy_all=[]#电影名字
	#遍历每一个电影名字
	for x in range(0,len(title_all)):
		#异常捕获
		try:
			#取值，赋值
			name=title_all[x]
			#拼接 文件的名字：电影名two.m3u8  ()，此名字和保存文件名必须一致
			name1=title_all[x]+'two.m3u8'
			#打开文件  电影名two.m3u8
			f=open(name1,mode='r',encoding="utf-8")
			#变量
			i=1
			#对 电影名two.m3u8 文件的每一行进行遍历
			for line in f:
				#文件每一行 开头 判断 是否 为 # {{ e 是就直接继续下一行
				if line.startswith("#"or "{"or "e"):
					continue
				#如不是则执行
				else:
					#https://hls.aoxtv.com/v3.szjal.cn/20200309/HpEY7O50/index.m3u8
					#https://v3.szjal.cn/20200309/HpEY7O50/hls/Sez1qBoC.ts
					#https://v3.szjal.cn/20200309/HpEY7O50/Sez1qBoC.ts
					#拼接下载的url
					down_u='https://v3.szjal.cn/'+big[x].split('/')[3]+"/"+big[x].split('/')[4]+"/"+big[x].split('/')[5]+"/"+line.strip()
					down_url.append(down_u)
					dy_all.append(name)
					  

		except Exception as e:
			continue
	#返回值
	return down_url,dy_all


#用来下载 每一个ts视频文件
def down_dy(y,dyname,filename):
	try:
		os.chdir(r'C:\Users\admin\Desktop\yy6080')

		os.chdir(filename)
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		res9=requests.get(y,headers=headers)
		#dyname=y.split("/")[-1]
		f=open(dyname,mode="wb")
		f.write(res9.content)
		f.close()
		#print(y,"下载完成。。。。。。")

	except Exception as e:
		print("未知错误",e)
		pass








#程序运行开始位置
if __name__ == '__main__':
		path="yy6080"
		if not os.path.exists(path):
			os.mkdir(path)
		os.chdir(path)

		
		global cookiesoen
		cookiesoen={"Cookie":"UM_distinctid=1711090d62c1f7-00883e3311c229-376b4502-100200-1711090d62d465; CNZZDATA1255998158=329059389-1585116799-http%253A%252F%252Fwww.yy6080.cn%252F%7C1585116799; Hm_lvt_4fe4f15f2d34a35d754b16b692969673=1585120860"}
		
		#获取电影的名称和链接
		src_all=get_url1()#0,代表取第一个返回值  #修改后这里只有一返回值
		#title_all=get_url1()[1]#0,代表取第一个返回值
		#
		#获取电影播放链接
		play_url_all=get_play_url(src_all)

		#获取电影名，电影播放地址
		title_all,play_all=down(play_url_all) 
		#打印测试。ok
		#print(title_all)
		#print(play_all)
		#
		#用来下载视频的m3u8大地址
		big=get_m3u8_1(title_all,play_all)
		#用来下载视频的m3u8小文件地址
		get_m3u8_2(title_all,big)
		#用来读取每个m3u8小视频里面的每个ts链接  保存并返回
		down_url,dy_all=get_movie(title_all,big)

		#print(len(dy_all),len(down_url))

		pool=Pool(20)#创建进程池

		#丢进进程池  下载
		#
		
		

		#对dy_all 进行遍历
		for x in range(0,len(dy_all)):

			dyname=dy_all[x]
			os.chdir(r'C:\Users\admin\Desktop\yy6080')
			if not os.path.exists(dyname):
				os.mkdir(dyname)
		
			y=down_url[x]
			xy=y.split("/")[-1]
			dyname1=dyname+str(x)+".ts"
			xy1=xy[0:1]
			#print(y)
			if xy1=="{":
				print("舍去")
				continue
			else:
				print("保留")
				#加入线程池中
				pool.apply_async(down_dy,(y,dyname1,dyname))
		#关闭线程，即不再加入其他工作
		pool.close()
		#等待线程完成
		pool.join()
		print('全部完成。。。。。')







		#悬案密码2野鸡杀手 (2014)
		#	 http://www.yy6080.cn/vodhtml/31734.html
		#	 http://www.yy6080.cn/vod-play-id-31734-src-1-num-1.html
		##   https://hls.aoxtv.com/v3.szjal.cn/share/pyCcHYmuVCLBZWzb
		#    https://zy.aoxtv.com/m3u8.php?url=https://v3.szjal.cn/20200309/PqOI9DHP/index.m3u8
		
		#野火春风斗古城
		#	http://www.yy6080.cn/vodhtml/31740.html
		#	http://www.yy6080.cn/vod-play-id-31740-src-1-num-1.html
		#	https://hls.aoxtv.com/v3.szjal.cn/share/4NZSatz4ZQi509bq
		#	https://zy.aoxtv.com/m3u8.php?url=https://v3.szjal.cn/20200308/5ICf1yFI/index.m3u8
		#
		#
		#
		#
		#https://v3.szjal.cn/20200309/HpEY7O50/hls/oIBWGsfo.ts
		#https://v3.szjal.cn/20200309/2qzvFI1M/hls/gx8ujI30.ts
		#
		#
		#
		#视频名称：亚瑟
		#http://www.yy6080.cn/vod-play-id-31735-src-1-num-1.html
		#https://hls.aoxtv.com/v3.szjal.cn/share/5eiHlolCOcqC1wqo
		#https://hls.aoxtv.com/v3.szjal.cn/20200309/HpEY7O50/index.m3u8
		#https://v3.szjal.cn/20200309/HpEY7O50/hls/Sez1qBoC.ts
		#https://v3.szjal.cn/20200309/HpEY7O50/hls/wd2hHpVr.ts
		#
		#
		#《亚当的苹果》
		#http://www.yy6080.cn/vod-play-id-2420-src-2-num-1.html
		#https://hls.aoxtv.com/v3.szjal.cn/share/FyEQcUhD35jkG1TL
		#https://hls.aoxtv.com/v3.szjal.cn/20200309/2qzvFI1M/index.m3u8
		#https://v3.szjal.cn/20200309/2qzvFI1M/hls/sI4ToVPX.ts
		#https://v3.szjal.cn/20200309/2qzvFI1M/hls/DVvJjlPB.ts
		#
		#
		#
		#


