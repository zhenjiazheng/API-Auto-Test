#coding=UTF-8
'''
Author: Zheng.zhenjia
'''

from Public.Common import parseExcelData,dbOperation,regCheck,Json2Dict
from Public.postAndGet import post
import re
import cfgValue



def getArgsList(filename,sheetname):
    '''
    :param1 filename: for file which will be opened.
    :param2 sheetname: for loading the test data from sheetname
    :return: caselist and casenamelist
    '''

    CaseList = []
    arglist = []
    pe = parseExcelData(filename,sheetname)
    sheetdata = pe.getCases()
    #print sheetdata
    for i in xrange(len(sheetdata)):
        param = sheetdata[i][3:7]
        arglist.append(param)
        caseName = str(sheetdata[i][0])+sheetdata[i][2]
        CaseList.append(caseName)
    return arglist,CaseList




def readyPrecondition(Ldict,filename,sheetname):#u'precondition'):
    '''
    Load the data from sheet precondition.
    Execute the test with the data loaded.
    Return the data get the wanted parameter store to Ldict.
    Arguement:
    1. Ldict : Global dictionary for storing the key and value.
    2. sheetname : the excel spreadsheet data for testing.
    '''
    print "Here is the precondition for all the test case testing:  \n"
    arglist=getArgsList(filename,sheetname)[0]
    caseName = getArgsList(filename,sheetname)[1]
    for i in xrange(len(arglist)):
        url = cfgValue.url
        rest = arglist[i][1]
        paramlist = arglist[i][2]
        expectlist = arglist[i][3]
        print caseName[i]
        for j in xrange(len(paramlist.split("\n"))):
            print "\n"
            print u"执行步骤%d. "%(j+1)
            if len(rest.split("\n")) > 1:
                rest = rest.split("\n")[j]
                print rest
            param = str(paramlist.split("\n")[j])
            param = insteadString(Ldict,param)

            #print param
            if len(expectlist.split("\n")) > 1:
                expect = expectlist.split("\n")[j]
            if "SQL:" in param:
                Command = param.split(":")[1]
                db = dbOperation()
                data = str(db.execSqlCommand(Command)[0][0])
                print data
                print "\n"
                if 'P<' in expect:
                    pattern = expect
                    #print pattern
                    rec= regCheck(pattern, data)
                    value = rec.getDict()
                    #print value
                    #value = re.findall(pattern, data)
                    Ldict.update(value)
            else:
                print url ,rest ,param
                data = post(url, rest, param)
                #sleep(1)
                print data
                print "\n"
                if Json2Dict(data).has_key("result"):
                    if "||" in expect:
                        reStr = expect.split("||")[0]
                        keyStr = expect.split("||")[1]
                        if 'P<' in reStr:
                            pattern = reStr
                            value = regCheck(pattern, data).getDict()
                            print u"匹配到第一部分期望值。"
                            Ldict.update(value)
                        elif regCheck(reStr,data).reString():
                            print u"匹配到第一部分期望值。"
                        for key in keyStr.split(","):
                            if not regCheck(key,data).reString():
                                print u"找不到该期望返回Key：" + key
                    else:
                        if 'P<' in expect:
                            pattern = expect
                            value = regCheck(pattern, data).getDict()
                            Ldict.update(value)
                            print u"匹配到期望值。"
                        elif regCheck(expect,data).reString():
                            print u"匹配到期望值。"
                      
                        





def insteadString(Ldict,params):
    '''
    function for instead the value of key in dictionary for params string where found the string startwith # character and suitable for mixed with number and A-Za-z characters.
    '''
    pats = '#[a-zA-Z0-9]+'
    listI = re.findall(pats, params)
    if listI == []:
        pass
    else:
        for item in listI:
            key = item.split("#")[1]
            params = re.sub(item,Ldict[key],params) 
    return params
            
            
            
# if __name__=='__main__':
#     #print getArgsList('TestCase.xlsx',"MileStone4")
#      
#     Ldict = {}
#     #path = cfgfile_path('TestData','phoneData.txt')
#     #print path
#     #cfg = getTestConfig(path)
#     user = cfgValue.testAccouts#['testAccounts']['Accounts']
#     Ldict = eval(user)
#     #print Ldict
#     sheetname = u'precondition'
#     from readConfig import findfileRealPath
#     
#     filename = findfileRealPath('TestCase.xlsx')
#     #BackupDB("%s/backup.sql"%os.getcwd())
#     readyPrecondition(Ldict, filename,sheetname)
#     #RestoreDB("%s/backup.sql"%os.getcwd())
