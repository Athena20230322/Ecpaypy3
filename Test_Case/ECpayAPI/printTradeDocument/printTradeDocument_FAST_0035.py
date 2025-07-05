# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import os

# Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCreateHiLifeTestData import actCreateHiLifeTestData
from ECpay.Verification.VerifyECpayAPI.VerifyCreateHiLifeTestData import verifyCreateHiLifeTestData
from ECpay.ProdActions.ActECpayAPI.ActprintTradeDocument import actprintTradeDocument
from ECpay.Verification.VerifyECpayAPI.VerifyprintTradeDocument import verifyprintTradeDocument

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
DRIVER = clsWebDriverHelper().initWebDriverHilife(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
CRTT_API = actCreateHiLifeTestData()
PTD_APT = actprintTradeDocument()
VER_API = verifyprintTradeDocument()

# Testing exec

# Precondition create new HiLifeTestData

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateTestData', 'CreateTestData_RAT_0001',
                              'OrderInfo.csv')

EXEC_ACT(PTD_APT.enableWebOperate, DRIVER)

order_info = EXEC_ACT(CRTT_API.genOrderRequestInfo, ORDER_INFO_CSV)

# order_info_crt_res = EXEC_ACT(PTD_APT.genpostRequestToAPI, order_info,
#                               'https://logistics-stage.ecpay.com.tw/Express/CreateHiLifeTestData')

order_info_chktd_res = EXEC_ACT(PTD_APT.genPostRequestToAPI, order_info, 'CreateTestData_API')

EXEC_ACT(VER_API.enableWebOperate, DRIVER)

# Do printTradeDocument_API test

ORDER_INFO_CVS_PTD = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'printTradeDocument', CASE_NAME, 'OrderInfo.csv')

modify_str = EXEC_ACT(PTD_APT.modifyAllpaylogisticsSplit, order_info_chktd_res)

order_info_ptd = EXEC_ACT(PTD_APT.genOrderRequestInfo, ORDER_INFO_CVS_PTD, modify_str)

EXEC_ACT(PTD_APT.createOrderByBrowser, DRIVER, order_info_ptd, 'printTradeDoc_API')

VERIFY(VER_API.verifyRtnChekHiLifeimg)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)