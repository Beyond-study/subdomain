#encoding:utf-8
__author__ = 'Beyond'
import sys
import httplib
import threading
import Queue
import string
import getopt



#结果存放文件
r = open('./result.txt','w')
#多线程锁
lock = threading.Lock()
#默认线程数
nThread = 20
def conn_test(site):
	global r,lock
	try:
		conn = httplib.HTTPConnection(site,80,timeout=5)
		conn.request("GET","/")
		re = conn.getresponse()
		if re.status == 301:
			pass
		else:
			lock.acquire()	
			r.writelines(site + '---' + str(re.status) + '\n')
			print '[+] ' + site + '____exist' 
			lock.release()
	except:
		pass
		

def domain(site,f):
	total_domain = Queue.Queue()
	for line in f.readlines():
		total_domain.put(line.strip() + '.' + site)
	return total_domain

def start(nThread,total_domain):
	threadlist = []
	while not total_domain.empty():
		for i in range(0,nThread):
			site = total_domain.get()
			if site:
				t = threading.Thread(target=conn_test,args=(site,))
				threadlist.append(t)
	for t in threadlist:
		t.start()
	for t in threadlist:
		t.join()

def usage():
	
	print u'''
		多线程二级域名爆破工具使用方法
		-u :指定域名如 baidu.com
		-n :指定线程数 默认为20
		--file：指定二级域名字典，默认为当前目录下的domain.txt
		-h :查看帮助
		生成的结果在当前目录下的result.txt文件中
	'''



if __name__ == '__main__':

	if len(sys.argv) < 2:
		usage()
		sys.exit()
	opts, args = getopt.getopt(sys.argv[1:], "hu:n:","file=")
	for op, value in opts:
		if op == '-u':
			site = value
		elif op == '-n':
			nThread = string.atoi(value)
		elif op == '--file=':
			fagv = value
		elif op == '-h':
			usage()
			sys.exit()
	try:
		f = open(fagv,'r')  #二级域名字典
	except:
		f = open('./domain.txt','r')
	domains = domain(site,f)
	start(nThread,domains)
	r.close()
	








