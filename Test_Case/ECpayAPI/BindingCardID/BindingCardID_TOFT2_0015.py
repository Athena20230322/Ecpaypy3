# -*- coding: utf-8 -*-

#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActBindingCardID import actBindingCardID
from ECpay.Verification.VerifyECpayAPI.VerifyBindingCardID import verifyBindingCardID


#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str, default='', help='Specify the runtime guid for this run.')
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
ACT_API = actBindingCardID()
VER_API = verifyBindingCardID()

#Testing exec

BINDING_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'BindingCardID', CASE_NAME, 'BindingInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

binding_info = EXEC_ACT(ACT_API.genBindingRequestInfo, BINDING_INFO_CSV)

binding_response = EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, binding_info)

EXEC_ACT(ACT_API.inputCreditCardInfo, '4311-9522-2222-2222', '2020', '12', '222')

res_in_CliReUrl = EXEC_ACT(ACT_API.GetInfoFromClientRedirectUrl)

res_in_CliReUrl_dict = EXEC_ACT(ACT_API.redirectStrToDict, res_in_CliReUrl)

#VERIFY

VERIFY(VER_API.verifyClientRedirectColumnsCheck, res_in_CliReUrl_dict, CASE_NAME)


DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)