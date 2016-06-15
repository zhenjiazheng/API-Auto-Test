#-*- coding: utf-8 -*-


import time
from Common.Pubilc_Function import PostAndGet, get_md5_value,threadRun
import unittest
import threading



class viewAdTest(unittest.TestCase):
    def setUp(self):
        pass
        
        
    def viewAd(self):
#         secret=""  # Need to fill in the value.
#         time_stamp=time.time() 
#         device="HUAWEI GRA-UL00"
#         sign_value=get_md5_value(device+str(int(time_stamp))+secret) # according to the generate value. the sign value should be change as this one.
        rest="/scmsface/view/ads"
        #headers = {"Content-type":"application/json","Accept":"version:1.0","Accept-Encoding":" gzip, deflate","Accept-Language": "en-US"}
#         time_stamp=time.time() 
#         url = "https://ssl-api.putao.cn/scmsface/view/ads"
        params={"sys_version":"5.0","channel_no":"huawei_life","app_version":"2.3.0","device":"HUAWEI GRA-UL00","device_no":"866696022436818","location":"30.2784662,120.1194347","city": u"深圳","scene":"0","data_version":"220042","timestamp":"1436286885578","sign":"2ebc2e599db3e5180bd3c33487af4664","local_sign":""}
        data=PostAndGet("GET", rest, params)
        print "\n"
        print data[1]
        print "\n"
        
    def test_threadViewAdTest(self):
        proc=100
        threadRun(proc,self.viewAd)
        
    def tearDown(self):
        pass
        
def suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(viewAdTest,'test'))
    return suite
            
if __name__ == '__main__':  
    unittest.main()
