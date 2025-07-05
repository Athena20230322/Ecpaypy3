# -*- coding: utf-8 -*-


#Static Import Area
import urllib.request, urllib.parse, urllib.error


import requests
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActEmbeddedUI import actEmbeddedUI
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedUI import verifyEmbeddedUI


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
ACT_API = actEmbeddedUI()
VER_API = verifyEmbeddedUI()

#Testing exec



ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedUI', CASE_NAME, 'OrderInfo.csv')



EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

# order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cLog, ORDER_INFO_CSV)
# html_path = os.path.join(ROOTDIR, 'Tmp')
# order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI1, order_info,html_path)
EXEC_ACT(ACT_API.createOrderByBrowser)
time.sleep(5)
#response = EXEC_ACT(ACT_API.submitEmbeddedUI)

#EXEC_ACT(ACT_API.inputOTPCredit, '1234')


res_in_CliReUrl = EXEC_ACT(ACT_API.GetInfoFromClientRedirectUrl)

res_in_CliReUrl_dict = EXEC_ACT(ACT_API.strToDict1, res_in_CliReUrl)

#VERIFY

#VERIFY(VER_API.verifyResponseValuesb2cx, res_in_CliReUrl_dict, CASE_NAME)



#order_info_res_dict1 = EXEC_ACT(ACT_API.strToDict, response)



#data1 = EXEC_ACT(ACT_API.decryptDatab2c, response['Data'])

# VERIFY
#VERIFY(VER_API.verifyResponseValuesb2c, res_in_CliReUrl_dict, CASE_NAME, 'success')
#VERIFY(VER_API.verifyResponseValuesEmbeddedUI,res_in_CliReUrl_dict,'success')

time.sleep(4)

#EXEC_ACT(ACT_API.inputOTPCredit, '1234')

#print order_info_res
#print urllib.urlencode(order_info_res)

#order_info_res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)

#data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
#print data

#EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ACT_API.inputPaymentPageCreditInfobydivisionE, '4311-9522-2222-2222', '22', '05', '222', '0900000000',' autotest123@gmail.com','test', 'divide')
#EXEC_ACT(ACT_API.inputOTPCredit, '1234')
# EXEC_ACT(ACT_API.inputOTP)

# otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')
#
# EXEC_ACT(ACT_API.inputOTP, otp_info)

#MERC_TID = order_info['MerchantTradeNo']
#MERC_UID = order_info['MerchantID']

#VERIFY(VER_API.verifyPaymentReturn, MERC_TID, {'PayAmt':'100'})


#VERIFY(VER_API.verifyPaymentReturn, MERC_TID, CASE_NAME)

#VERIFY(VER_API.verifyOrderByQuery3D, MERC_TID, MERC_UID, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)