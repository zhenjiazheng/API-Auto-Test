# -*- coding: utf-8 -*-
'''
Author: Zheng.zhenjia
'''
from Public.Common import dbOperation
from Public.Common import regCheck
from Public.Common import Json2Dict
from Public.Common import parseExcelData
from Public.Common import FilePath
from Public.postAndGet import post,get
import unittest,re
from PreCondition.preCondition import readyPrecondition
from PreCondition import cfgValue
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable


Ldict = {}
Ldict = cfgValue.testAccouts
print Ldict

caseFile = cfgValue.caseSheet
filename = FilePath(caseFile)
dbOperation().BackupDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
print '-'*80
print u'执行测试的用例文件:%s'%caseFile
print '-'*80
sheetname = cfgValue.PreConditionCase
print u' 初始化的用例表格:%s'%sheetname
print '-'*80
readyPrecondition(Ldict,filename, sheetname)

def unlockOpportunity(url,sessionId,mobile,pluginId):
    #print 'Unlock the opportunity from redis.'
    para = '{"jsonrpc":"2.0","method":"opportunity_unlock","params":{"sessionId":"%s","mobile":"%s","pluginId":"%s"}, "id": -2339}'%(sessionId,mobile,pluginId)
    rest = '/xw3/ClientService'
    unlock = post(url,rest,para)
    #print unlock

def expireAndDelRequirementId(url,sessionId, id):
    print 'take off the requirementId(remove from search engine.)'
    para = '{"jsonrpc":"2.0","method":"requirement_expire","params":{"sessionId":"%s","requirementId":%s}, "id": -2339}'%(sessionId, id)
    rest = '/xw3/MerchantService'
    expire = post(url, rest, para)
    dbOperation().execSqlCommand('DELETE from requirement WHERE id = %s'%id)
    print expire


class ExecuteTest(unittest.TestCase):

    def setUp(self):
        #dbOperation().BackupDB("%s/backup.sql"%os.path.dirname(os.path.abspath(__file__)))
        pass


    def TestCase(self, method, rest, params, expected):
        expected = str(expected)
        # print type(expected)
        #print "\nThe length of expected: %d\n" % len(expected.split(";"))

        if len(expected.split(";")) > 1:
            errorcode = expected.split(";")[0]
            errorMsg = expected.split(";")[1]
            print "errorcode: " + errorcode
            print "errorMsg: " + errorMsg
        if "SQL:" in params:
            if "SELECT" in params:
                print params
                print str(dbOperation().execSqlCommand(params.split(":")[1])[0])
                data = str(dbOperation().execSqlCommand(params.split(":")[1])[0][0])
            elif "DELETE" or "update" in params:
                data = str(dbOperation().execSqlCommand(params.split(":")[1]))
        else:
            url = cfgValue.url
            if method == "POST":
                data = post(url, rest, params)
            elif method == "GET":
                data = get(url, rest, params)
        '''打印接口返回值
        '''
        print '\n'
        print data
        if data == '':
            print "Fail to get data"
            self.assertTrue(0, "Fail to get data, please check the post value and url.")
        elif "SQL:" in params:
            if 'P<' in expected:
                pattern = expected
                value = regCheck(pattern, data).getDict()
                global Ldict
                Ldict.update(value)
                self.assertIsNotNone(value, 'Cannot find the expected string in response data.')
            if regCheck(expected,str(data)).reString():
                self.assertTrue('1=2',"The expected String cannot be found in response data.")
            else:
                self.assertIn(expected, data,'Cannot find the expected string in response data.')
        elif Json2Dict(data).has_key("error"):
            if len(expected.split(";")) > 1:
                # print type(Json2Dict(data)['error']['code'])
                self.assertIn(errorcode, str(Json2Dict(data)['error']['code']), "The return error code is incorrect.")
                self.assertIn(errorMsg, Json2Dict(data)['error']['message'], "The return error message is incorrect.")

            elif len(expected.split(";")) == 1:
                patt = expected
                val = regCheck(patt, data).reString()
                #for item in val:
                    #print item.decode("unicode_escape")
                self.assertTrue(val, "The excepted message is not in return message.")

            elif len(expected.split(";")) == 0:
                self.assertTrue(1 == 2, "Please input the correct expected data.")

        elif Json2Dict(data).has_key("result"):
            if "||" in expected:
                reStr = expected.split("||")[0]
                keyStr = expected.split("||")[1]
                if 'P<' in reStr:
                    pattern = reStr
                    value = regCheck(pattern, data).getDict()
                    self.assertIsNotNone(value, 'Cannot find the expected string in response data.')
                    print u"匹配到第一部分期望值。"
                    Ldict.update(value)
                elif regCheck(reStr,data).reString():
                    self.assertTrue(regCheck(reStr,data).reString(),u"返回值与第一部分期望值不匹配")
                for key in keyStr.split(","):
                    self.assertIn(key, data,u'找不到该期望返回Key：%s'%key)
                    print u"找到期望返回字段：%s"%key
            else:
                if 'P<' in expected:
                    pattern = expected
                    value = regCheck(pattern, data).getDict()
                    self.assertIsNotNone(value, 'Cannot find the expected string in response data.')
                    print u"匹配到期望值。"
                    Ldict.update(value)
                elif regCheck(expected,data).reString():
                    self.assertTrue(regCheck(expected,data).reString(),u"返回值与第一部分期望值不匹配")

                else:
                    self.assertIn(expected, data,'Cannot find the expected string in response data.')

    def exe(self, method, rests, params, expecteds):
        restall = rests.split("\n")
        paramlist = params.split("\n")
        expectedlist = expecteds.split("\n")
        global Ldict

        for j in xrange(len(paramlist)):
            if len(restall) == 1:
                rest = restall[0]
            elif len(restall) > 1 :
                rest = restall[j]
            else:
                print 'Please fill in the rest to perform the test.\n'

            params = paramlist[j]
            expected = expectedlist[j]
            print u"开始执行测试：步骤 %d \n" % (j + 1)
            print u"期望字符串：" + expected
            pats = '#[a-zA-Z0-9]+'
            #params = ast.literal_eval(params)
            listI = re.findall(pats, params)
            if listI == []:
                pass
            else:
                for item in listI:
                    key = item.split("#")[1]
                    params = re.sub(item,Ldict[key],params)
            params = str(params)
            # print params
            expected = expectedlist[j]
            # print expected
            # print expected
            self.TestCase(method, rest, params, expected)

    def tearDown(self):
        print "\nBelow is the tearDown data output.\n"
        dbOperation().execSqlCommand("DELETE FROM service where id = %s"%Ldict['shopId1'])
        dbOperation().execSqlCommand("DELETE FROM service where id = %s"%Ldict['shopId2'])
        sid = Ldict['UsessionId']
        url = cfgValue.url
        mobile1 = Ldict['ResourceMobile1']
        mobile2 = Ldict['ResourceMobile2']
        unlockOpportunity(url, sid, mobile1, "xw:recruitment")
        unlockOpportunity(url, sid, mobile1, "xw:transfer")
        unlockOpportunity(url, sid, mobile1, "xw:siting")
        unlockOpportunity(url, sid, mobile2, "xw:recruitment")
        unlockOpportunity(url, sid, mobile2, "xw:transfer")
        unlockOpportunity(url, sid, mobile2, "xw:siting")
        try:
            #print Ldict
            if Ldict.has_key('requirementId'):
                #print Ldict['sessionId']
                url = cfgValue.url
                if Ldict.has_key('MsessionId'):
                    sid =Ldict['MsessionId']
                    expireAndDelRequirementId(url,sid,Ldict['requirementId'])
                    del(Ldict['requirementId'])
        except:
            pass
        try:
            dal = dbOperation().execSqlCommand('SELECT id FROM requirement WHERE title = \"RequirementTitle\"')
            if dal:
                for i in len(dal):
                    id = dal[i][0]
                    url = cfgValue.url
                    if Ldict.has_key('MsessionId'):
                        sid = Ldict['MsessionId']
                        expireAndDelRequirementId(url,sid,id)
                        del(Ldict['requirementId'])
        except:
            pass


        try:
            #print Ldict
            if Ldict.has_key('requirementId2'):
                #print Ldict['sessionId']
                    url = cfgValue.url
                    if Ldict.has_key('MsessionId'):
                        sid = Ldict['MsessionId']
                        expireAndDelRequirementId(url,sid,Ldict['requirementId2'])
                        del(Ldict['requirementId2'])
        except:
            pass
        try:
            if Ldict.has_key('opportunityId'):
                dbOperation().execSqlCommand("DELETE FROM opportunity WHERE id = %s"%Ldict['opportunityId'])
                del(Ldict['opportunityId'])
            if dbOperation().execSqlCommand("SELECT id FROM opportunity where mobile = %s"%Ldict['MUser1']):
                dbOperation().execSqlCommand("DELETE FROM opportunity where mobile = %s"%Ldict['MUser1'])
            if dbOperation().execSqlCommand("SELECT id FROM opportunity where mobile = %s"%Ldict['MUser2']):
                dbOperation().execSqlCommand("DELETE FROM opportunity where mobile = %s"%Ldict['MUser2'])
        except:
            pass
        try:
            if Ldict.has_key('resourceId'):
                dbOperation().execSqlCommand("DELETE FROM resource WHERE id = %s"%Ldict['resourceId'])
                del(Ldict['resourceId'])
        except:
            pass

        try:
            if Ldict.has_key('resourceId2'):
                dbOperation().execSqlCommand("DELETE FROM resource WHERE id = %s"%Ldict['resourceId2'])
                del(Ldict['resourceId2'])
        except:
            pass

        try:
            if Ldict.has_key('preferenceId'):
                dbOperation().execSqlCommand("DELETE FROM preference WHERE id = %s"%Ldict['preferenceId'])
                del(Ldict['preferenceId'])
        except:
            pass

        try:
            if Ldict.has_key('recommendationId'):
                dbOperation().execSqlCommand("DELETE FROM recommendation WHERE id = %s"%Ldict['recommendationId'])
                print "del the recommendation from database."
                del(Ldict['resourceId'])
        except:
            pass
        #
        # try:
        #     if Ldict.has_key('serviceId'):
        #         #print Ldict['serviceId']
        #         dbOperation().execSqlCommand("DELETE FROM service WHERE id = %s"%Ldict['serviceId'])
        #         print "del the serviceId %s from database."%Ldict['serviceId']
        #         del(Ldict['serviceId'])
        # except:
        #     pass
        try:
            if Ldict.has_key('contractId'):
                dbOperation().execSqlCommand("DELETE FROM contract WHERE id = %s"%Ldict['contractId'])
                del(Ldict['contractId'])
        except:
            pass
        try:
            if Ldict.has_key('businessId'):
                dbOperation().execSqlCommand("DELETE FROM business WHERE id = %s"%Ldict['businessId'])
                del(Ldict['businessId'])
        except:
            pass

        try:
            if Ldict.has_key('opportunityId0'):
                print u"多余一个以上的商机在数据库中存在。"
                for x in xrange(0,21):
                    command = 'DELETE FROM opportunity WHERE id = %s'%Ldict['opportunityId%d'%x]
                    del(Ldict['opportunityId%d'%x])
                    try:
                        dbOperation().execSqlCommand(command)
                    except:
                        pass
        except:
            pass
        try:
            if Ldict.has_key('businessId0'):
                print u"多余一个以上的业务ID在数据库中存在。"
                for i in xrange(0,20):
                    dbOperation().execSqlCommand("DELETE FROM business WHERE id = %s"%Ldict['businessId%d']%i)
                    del(Ldict['businessId%d'%i])
        except:
            pass

        try:
            if Ldict.has_key('tradeNo'):
                dbOperation().execSqlCommand('DELETE FROM trade WHERE tradeno = \'%s\''%Ldict['tradeNo'])
                del(Ldict['tradeNo'])
        except:
            pass

        try:
            if Ldict.has_key('exampleId'):
                dbOperation().execSqlCommand("DELETE FROM example WHERE id = %s"%Ldict['exampleId'])
                print u"删除案例。"
                del(Ldict['exampleId'])
        except:
            pass


    @staticmethod
    def getTestFunc(method,rests, params, expecteds):
        def func(self):
            self.exe(method, rests, params, expecteds)
        return func

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
        caseName = sheetdata[i][2] #str(sheetdata[i][0])+
        CaseList.append(caseName)
    return arglist,CaseList


# def __generateTestCases():
#     sheetname = cfgValue.TestCase
#     arglists = getArgsList(filename,sheetname)[0]
#     CaseNameLists = getArgsList(filename,sheetname)[1]
#     #item = GT().run()
#     item = int(os.environ.get('UT_ITEM', -1))
#     print '-' * 60
#     if item == -1:
#         print 'current test suite is ALL TESTS'
#     else:
#         print 'current test item is: %d' % item
#     print '-' * 60
#     if item == -1:
#         for i in xrange(len(arglists)):
#             test_func = "test_" + CaseNameLists[i]
#             setattr(ExecuteTest, test_func,
#                 ExecuteTest.getTestFunc(*arglists[i]))
#     else:
#         test_func = "test_" + CaseNameLists[item]
#         setattr(ExecuteTest, test_func,
#             ExecuteTest.getTestFunc(*arglists[item]))
# __generateTestCases()



def suite():
    sheetname = cfgValue.TestCase
    arglists = getArgsList(filename,sheetname)[0]
    CaseNameLists = getArgsList(filename,sheetname)[1]
    item = int(os.environ.get('UT_ITEM', -1))
    #item = GT().run()

    print '-' * 60
    if item == -1:
        print 'current test suite is ALL TESTS'
    else:
        print 'current test item is: %d' % item
    print '-' * 60

    if item == -1:
        for i in xrange(len(arglists)):
            test_func = "test_" + CaseNameLists[i]
            setattr(ExecuteTest, test_func,
                ExecuteTest.getTestFunc(*arglists[i]))
    else:
        test_func = "test_" + CaseNameLists[item]
        setattr(ExecuteTest, test_func,
            ExecuteTest.getTestFunc(*arglists[item]))
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ExecuteTest))
    return suite

if __name__ == '__main__':
    unittest.main()
