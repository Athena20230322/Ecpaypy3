# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from  Allpay.ProdActions.ActAllpayAPI.ActInvQueryChkMobBarCode import actInvQueryChkMobBarCode
from Allpay.Verification.VerifyAllpayAPI.VerifyInvQueryChkMobBarCode import verifyInvQueryChkMobBarCode


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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actInvQueryChkMobBarCode()
VER_API = verifyInvQueryChkMobBarCode()

# Testing exec

QUERY_MOBARCODE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryChkMobBarCode', CASE_NAME, 'OrderInfo.csv')

query_mobarcode_info = EXEC_ACT(ACT_API.genOrderRequestInfo, QUERY_MOBARCODE_INFO_CSV)

query_mobarcode_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, query_mobarcode_info)

query_mobarcode_res_dict = EXEC_ACT(ACT_API.strToDict, query_mobarcode_info_res)

# Verify

VERIFY(VER_API.verifyInvQueryChkMobBarCodeRequestInfo, query_mobarcode_res_dict, CASE_NAME)

# DRIVER.delete_all_cookies()
# DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)