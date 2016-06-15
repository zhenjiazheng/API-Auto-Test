# -*- coding: utf-8 -*-
'''
Author: Zheng.zhenjia
'''

import os
from unittest import TestSuite
from Public.HTMLTestRunner import HTMLTestRunner as tr
from Public.testReport import TestReport
#from common.showTestReport import auto_show_test_report
from Public.Common import dbOperation
from Public.Common import send_the_Mail
from PreCondition import cfgValue


 

def get_tests_path():
    curr_path=os.path.dirname(os.path.abspath(__file__))
    curr_dir=os.path.dirname(curr_path)
    tests_path=os.path.realpath(os.path.join(curr_dir,cfgValue.ModuleFolder))#'MileStone4TestCase')) #,cfgValue.ModuleFolder))
    return tests_path
    
def get_modules():

    files=os.listdir(get_tests_path())
    #pdb.set_trace()
    modules=[]
    initFile='__init__.py'
    myself='testRunner.py'
    for eachFile in files:
        if eachFile.endswith(".py"):
        #if fnmatch.fnmatch(eachFile, '*.py'):
            modules.append(eachFile)
    if initFile and myself in modules:
        modules.remove(initFile)
        modules.remove(myself)
    return modules
    
def build_testsuite():
    modules=get_modules()
    rawTests=[]
    tests=[]
    #print os.curdir
    for eachModule in modules:
        rawTests.append(eachModule.split(".py"))
    #print rawTests
    #print rawTests[0][0]
    for i in range(len(rawTests)):
        tests.append('%s.%s' % (cfgValue.ModuleFolder, rawTests[i][0]))#cfgValue.ModuleFolder MileStone4TestCase
    return tests


DASH='__'

def testsuite():
    moduleNames=build_testsuite()
    testsuite=TestSuite()

    for module_name in moduleNames:
        print module_name
        import importlib
        m = importlib.import_module(module_name)
        #modules=map(__import__,moduleNames)
        testsuite.addTest(m.suite())
        #suite.addTest(element(module.suite()))
    return testsuite


def main():
    global report_file, runner, fp, Report_title
    tolist=cfgValue.mailToList
    #dbOperation().BackupDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
    reportTitle = cfgValue.M4Report
    report_file = TestReport.generate_report(reportTitle)
    #print 'report_file: ',report_file
    runner = tr()
    fp = file(report_file, 'wb')
    Report_title = reportTitle + DASH + testsuite.__name__
    runner = tr(stream=fp, title=Report_title, description=report_file)
    runner.run(testsuite())
    fp.close()
    dbOperation().RestoreDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
    #send_the_Mail(report_file, tolist)


if __name__ == '__main__':
    main()