# -*- coding: utf-8 -*-
import os
import sys
import time
from UIOperate.MobileOperate import ClassMobileOperate as mobileop


mop = mobileop('RQ3000GT7X', 'Android', 'com.sonyericsson.conversations', '.ui.ConversationListActivity')
interval = 2

i = 0
while i == 0:
    print("Loop reset")
    runtime = 0
    while runtime < 7200:
        #mop.handleOTPSMS('D:\QA\AutoTest\Utility\OTPCollector\smsconf.xml')
        try:
            mop.handleOTPSMS('D:\ecpay\ECpayAutoFramework\\Utility\OTPCollector\smsconf.xml')
        except Exception as err:
            print("Error occurs")
            print(err.message)
            mop.driverReset()
        time.sleep(interval)
        runtime += interval
        ##print runtime
    mop.driverReset()
    print("Loop end")

