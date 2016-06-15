
#!/usr/bin/env python
#  coding=utf-8"""

from locust import HttpLocust, TaskSet, task

"""
    Locust test
"""
class UserBehavior(TaskSet):


    def on_start(self):
        """ called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        self.client.post({"jsonrpc":"2.0","method":"user_login","params":{"account":"13662207483","password":"123456"}, "id": 100})

    @task(2)
    def price_get(self):
        "http://automationtesting.sinaapp.com/"
        self.client.get({"jsonrpc":"2.0", "method":"price_get","params":{"sessionId":"testnologin","pluginId":"xw:recruitment","param":{"cycle":90,"positionNumber":10}},"id": -2339})

    @task(1)
    def business_getList(self):
        "http://automationtesting.sinaapp.com/about"
        self.client.get({
        "jsonrpc":"2.0",
        "method": "business_getList",
        "params": {
            "sessionId": "%s"%self.login()['sessionId'],
            "status" :  0,
            "orderType" : 0,
            "pageNo":  0,
            "pageSize":  10,
            "pluginId": "all:all"
        }
    })

class WebsiteUser(HttpLocust):

    """
    The HttpLocust class inherits from the Locust class, and it adds
    a client attribute which is an instance of HttpSession,
    that can be used to make HTTP requests.
    """
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000