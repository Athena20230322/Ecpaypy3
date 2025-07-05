
# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from  ECpay.ProdActions.ActECpayAPI.ActAioCheckOut import actAioCheckOut
from ECpay.Verification.VerifyECpayAPI.VerifyAioCheckOut import verifyAioCheckOut

#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir' , type=str, help = 'Specify the log dir')
ARGP.add_argument('--package' , type=str, help = 'Specify the package name')
ARGP.add_argument('--runid' , type=str , default='', help = 'Specify the runtime guid for this run.')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
RUN_UID = ARGS.runid
CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actAioCheckOut()
VER_API = verifyAioCheckOut()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'AioCheckOut', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

EXEC_ACT(ACT_API.createECPAYByBrowser)

EXEC_ACT(ACT_API.Login,'xgxg006','Aa123456','7371')

timestamp = int(time.time())
storename = 'test' + str(timestamp)

EXEC_ACT(ACT_API.ChangeStoreName, storename)

time.sleep(10)

EXEC_ACT(ACT_API.clsinputECPaymentPageCreditInfo, '4311-9522-2222-2222', '23', '05', '222', '0900000000', 'divide','test')

EXEC_ACT(ACT_API.CheckStoreName, storename)




DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)