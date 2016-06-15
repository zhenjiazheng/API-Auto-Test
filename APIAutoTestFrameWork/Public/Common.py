# coding=UTF-8
__author__ = 'zhengandy'

# import MySQLdb
import os
import xlrd
import sys
import re
import hashlib
import simplejson
import time
from PreCondition import cfgValue
import pymysql

reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable



def get_md5_value(src): 
    '''
    It will used for getting MD5 value for string.
    Almost it will used for login.
    '''
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def Json2Dict(json):
    '''
    This function is for the define for Json format transfer to Dictionary format.
    It will using for the GetInfo result transfer almost.
    '''
    dictinfo = simplejson.loads(json)
    return dictinfo

class dbOperation:
    def __init__(self):
        self.host = cfgValue.dbHOST
        self.user = cfgValue.dbUSER
        self.psw = cfgValue.dbPASSWD
        self.dbname = cfgValue.dbName
        self.port = cfgValue.dbPORT
        self.btool = cfgValue.btool
        self.rtool = cfgValue.rtool

    def BackupDB(self,target):
        print 'Start to backup'
        command = '%s -h%s -u%s -p%s %s > %s' % (self.btool, self.host, self.user, self.psw, self.dbname, target)
        #print command
        try:
            os.system(command)
            #print 'Success'
        except Exception , e :
            #print 'Fail'
            print e

    def RestoreDB(self,source):
        print 'Start to restore sql'
        command = '%s -h%s -u%s -p%s -P3306 %s < %s' % (self.rtool, self.host, self.user, self.psw, self.dbname, source)
        #print command
        try:
            os.system(command)
            #print 'Success'
        except Exception , e :
            #print 'Fail'
            print e
    def execSqlCommand(self,sql):
        try:
            conn = pymysql.connect(host=self.host,user=self.user,passwd=self.psw,db=self.dbname)#host='127.0.0.1', user='root', passwd="123456", db='xw')
            # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd=None, db='mysql')
            cur = conn.cursor()
            cur.execute(sql)
            r = cur.fetchall()
            cur.close()
            conn.close()
            return r
        except Exception,e:
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    #
    # def execSqlCommand(self,sql):
    #     try:
    #         conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.psw,port=int(self.port),db=self.dbname)
    #         cur=conn.cursor()
    #         cur.execute(sql)
    #         result=cur.fetchall()
    #         conn.commit()
    #         cur.close()
    #         conn.close()
    #         return result
    #     except MySQLdb.Error,e:
    #         print 'Mysql Error %d: %s' % (e.args[0], e.args[1])


class parseExcelData:

    def __init__(self,casefile,sheetName):
        self.excelFile = casefile
        print self.excelFile
        self.sheetName = sheetName

    def getCases(self):
        '''
        Get the test data from execl sheet which named TestCase.
        And the folder is named common.
        Excel file name is TestCase.xlsx.
        '''
        try:
            data=xlrd.open_workbook(self.excelFile)
        except Exception,e:
            print e
        table = data.sheet_by_name(self.sheetName)
        rows = table.nrows
        #print rows
        List=[]
        for i in xrange(1,rows):
            colName =  table.row_values(i)
            List.append(colName)
        return List

    

class regCheck:
    def __init__(self,patt,data):
        self.patt = patt
        self.data = data
    def getDict(self):
        try:
            reg2 = re.compile(self.patt)
            reg2Match = reg2.match(self.data)
            ldict = reg2Match.groupdict()
            #print ldict
            return ldict
        except Exception, e:
            print e

    def reString(self):
        try:
            val = re.findall(self.patt,self.data)
            #print val
            return val
        except:
            return False
    


def send_the_Mail(fileTosend, mailto):
    """
    This function takes in recipient and will send the email to that email address with an attachment.
    :param recipient: the email of the person to get the text file attachment
    """

    # Import the needed email libraries
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from smtplib import SMTP
    time_strf = time.strftime("%Y-%m-%d %X", time.localtime())
    # Set the server and the message details
    send_from = 'ceshi@echiele.com'
    subject = "TestReport For XW API %s." % time_strf
    # Create the multipart
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ",".join(mailto)  # recipient

    # msg preable for those that do not have a email reader
    msg.preamble = 'Multipart message.\n'

    # Text part of the message
    part = MIMEText("Dear Receiver,\n\nThis is the latest XW API test report,and it is an automated sent email. \nNo need to reply... it won't be answered anyway.\nAny issue please contact with the sender, \n\nThanks!")
    msg.attach(part)

    # The attachment part of the message
    fp = open("%s" % fileTosend, "rb")
    part = MIMEApplication(fp.read())
    fp.close()
    part.add_header('Content-Disposition', 'attachment', filename="%s" % fileTosend)
    msg.attach(part)

    # Create an instance of a SMTP server
    sp = SMTP()
    sp.connect('smtp.exmail.qq.com')
    # Start the server
    sp.set_debuglevel(1)
    # sp.ehlo()
    sp.starttls()
    sp.login('ceshi@echiele.com', 'cs123456')

    # Send the email
    sp.sendmail(msg['From'], mailto, msg.as_string())
    sp.quit()

def FilePath(filename):                                       # 指明被遍历的文件夹
    cudir = os.path.dirname(os.path.abspath(__file__))
    rootdir=os.path.dirname(cudir)
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
#         for dirname in  dirnames:                       #输出文件夹信息
#             print "parent is: " + parent
#             print  "dirname is " + dirname
        for each in filenames:     
            if filename == each:                   #输出文件信息
#                 print "parent is: " + parent
#                 print "filename is: " + filename
                print "the full name of the file is: " + os.path.join(parent,filename) #输出文件路径信息       
                return os.path.join(parent,filename)
# if __name__ == '__main__':
#
#     # conn = pymysql.connect(host='127.0.0.1', user='root', passwd="123456", db='xw')
#     # # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd=None, db='mysql')
#     # cur = conn.cursor()
#     # cur.execute("SELECT price FROM price where id = 1")
#     # # print cur.description
#     # r = cur.fetchall()
#     # # print r
#     # # ...or...
#     # #for r in cur:
#     # print r
#     #
#     # cur.close()
#     # conn.close()