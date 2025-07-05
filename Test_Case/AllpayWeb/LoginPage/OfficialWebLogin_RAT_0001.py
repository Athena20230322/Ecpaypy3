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
DIVER = clsWebDriverHelper().initWebDriver(PKG)

# Declare feature testing instances
DETAIL_LOG = os.path.join(CASE_NAME, 'Detail.log')
ACT_LOGIN = LOGIN.actLoginPage(DIVER, DETAIL_LOG)
ACT_MYACCT = MYACCT.myAccountPage(DIVER, DETAIL_LOG)
VERIFY_LOGIN = VERIFY.loginVerify(DIVER, DETAIL_LOG)

# Test execution area

HELPER.execTestAction(ACT_LOGIN.generalLogin, 'b88612029', 'E4vytiax5298')

time.sleep(1)


HELPER.execTestVerify(VERIFY_LOGIN.verifyLoginResult)


time.sleep(2)
DIVER.delete_all_cookies()
DIVER.quit()

HELPER.processResult()
