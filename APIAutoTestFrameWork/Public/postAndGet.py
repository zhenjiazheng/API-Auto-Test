# coding=UTF-8
__author__ = 'zhengandy'

import requests
import time
import threading
from multiprocessing import Process


    
def post(url,rest,param):
    urlall="http://"+url+rest
    print '*'*90
    print u"发送服务: " + urlall
    print u"发送参数:" + param
    time_before = time.time()
    try:
        response = requests.post(urlall, data=str(param))
    except requests.RequestException, e:
        return e
    time_after = time.time()
    data = response.text
    trp = time_after - time_before
    print u"请求相应时间：" + str(trp)
    return data
        
def get(url,rest,param):
    urlall="http://"+url+rest
    param = str(param)
    time_before = time.time()

    try:
        response = requests.get(urlall,param)
    except  requests.RequestException, e:
        return e
    time_after = time.time()
    data = response.text
    trp = time_after - time_before
    print u"请求相应时间：" + str(trp)
    return data

def processRun(func, arg, num):
    '''
    此函数用于同多进程执行同一个目标，非并发执行
    func：被执行目标
    args：被执行目标的参数
    num：目标执行进程数
    '''
    proc_record = []
    for i in xrange(num):
        p = Process(target = func, args = (arg,))
        p.start()
        proc_record.append(p)
    for p in proc_record:
        p.join() 

     
def threadRun(num,test_func):
    '''
    此函数用于出发并行线程的测试，并发执行
    num: 代表运行多少个线程
    test_func：代表被运行的对象
    '''
    global total, mutex     #定义全局变量
    total = 0
    mutex = threading.Lock() # 创建线程锁
    threads = []  #定义线程池
    
    for x in xrange(0, num):
        threads.append(threading.Thread(target=test_func))  # 先创建线程执行对象
    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()       
    
# if __name__ == '__main__':    
#     pe = common.parseExcelData()
#     list1 = pe.getCases(u'Sheet1')
#     #print list1[0]
#     #print type(list1[0][5])
#     parms = list1[0][5]
#     #print parms.split('\n')[6]
#     pa = parms.split('\n')[0]
#     r = postAndGet('192.168.1.188:8080','/xw3/MerchantService',pa)
#     data = r.post()
#     print data