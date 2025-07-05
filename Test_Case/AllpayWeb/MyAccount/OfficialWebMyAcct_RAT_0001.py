# -*- coding: utf-8 -*-

import Allpay.ProdActions.ActAllpayWeb.LoginPage as LOGIN
import Allpay.ProdActions.ActAllpayWeb.MyAccount as MYACCT
import Allpay.Verification.Verify_Web.VerifyLoginPage as VERIFY
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#(DO NO Edit) Static declare 

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir' , type = str, help = 'Specify the log dir')
ARGP.add_argument('--package' , type = str, help = 'Specify the package name')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
DRIVER = clsWebDriverHelper().initWebDriver(PKG)

# Declare feature testing instances

ACT_LOGIN = LOGIN.actLoginPage(DRIVER, DETAIL_LOG)
ACT_MYACCT = MYACCT.myAccountPage(DRIVER, DETAIL_LOG)
VERIFY_LOGIN = VERIFY.loginVerify(DRIVER, DETAIL_LOG)

# Test execution area

HELPER.execTestAction(ACT_LOGIN.generalLogin, 'b88612029', 'E4vytiax5298')

time.sleep(1)

HELPER.execTestAction(ACT_MYACCT.gotoAcctDetail)

HELPER.execTestAction(ACT_MYACCT.selectTransCategory, '交易')

HELPER.execTestAction(ACT_MYACCT.specifyStartDate, '2016', '2', '17')

HELPER.execTestAction(ACT_MYACCT.specifyEndDate, '2016', '4', '21')

HELPER.execTestAction(ACT_MYACCT.submitQuery)


time.sleep(2)
DRIVER.delete_all_cookies()
DRIVER.quit()

HELPER.processResult()
