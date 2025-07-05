# -*- coding: utf-8 -*-

from  Allpay.ProdActions.ActAllpayProdSemiAuto.ActConsoleLogin import actConsoleLogin
from  Allpay.Verification.VerifyAllpayVendorConsole.VerifyConsoleLogin import verifyConsoleLogin
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#(DO NO Edit) Static declare 

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir' , type=str, help = 'Specify the log dir')
ARGP.add_argument('--package' , type=str, help = 'Specify the package name')
ARGP.add_argument('--runid' , type=str , default='', help = 'Specify the runtime guid for this run.')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
RUN_UID = ARGS.runid

LOG_DIR = ''
PKG = 'Chrome'

CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify
INF = HELPER.getCustomUserInfo()
# Declare feature testing instances
DETAIL_LOG = os.path.join(CASE_NAME, 'Detail.log')
ACT_LOGIN = actConsoleLogin(DRIVER, DETAIL_LOG)
VERIFY_LOGIN = verifyConsoleLogin(DRIVER, DETAIL_LOG)

# Test execution area

EXEC_ACT(ACT_LOGIN.generalLogin, INF['USRN'], INF['PW'])

time.sleep(1)

EXEC_ACT(ACT_LOGIN.goToCreditDetail)

ABANDON = EXEC_ACT(ACT_LOGIN.abandCreditPayToday)
#ABANDON = ACT_LOGIN.abandCreditPayToday()
print(ABANDON)

TRADE_DETAIL = EXEC_ACT(ACT_LOGIN.retrieveTradeStat, ABANDON)

VERIFY(VERIFY_LOGIN.verifyTradeDetail, ABANDON, TRADE_DETAIL, CASE_NAME)


#VERIFY(VERIFY_LOGIN.verifyLoginResult)


time.sleep(2)
DRIVER.delete_all_cookies()
DRIVER.quit()

HELPER.processResult()
