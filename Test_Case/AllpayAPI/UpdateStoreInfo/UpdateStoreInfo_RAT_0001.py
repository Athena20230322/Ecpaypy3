# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActUpdateStoreInfo import actUpdateStoreInfo
from Allpay.Verification.VerifyAllpayAPI.VerifyUpdateStoreInfo import verifyUpdateStoreInfo


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
ACT_API = actUpdateStoreInfo()
VER_API = verifyUpdateStoreInfo()

#Testing exec
#precondition add new order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'UpdateStoreInfo', 'Initial_Data', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createAllpayOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9533-3333-3333', '22', '05', '222', '0911429215')

#otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0911429215')

#EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']

MERC_T_DT = order_info['MerchantTradeDate']
time.sleep(5)

DRIVER.delete_all_cookies()
DRIVER.quit()

#precondition: generate C2C order
C2C_ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_data', 'AllpayAPI', 'UpdateStoreInfo', 'Initial_Data', 'Create.csv')

c2c_order_info = EXEC_ACT(ACT_API.genC2COrderRequestInfo, C2C_ORDER_INFO_CSV, MERC_TID, MERC_T_DT)

response_text = EXEC_ACT(ACT_API.createOrderByRequest, c2c_order_info)

rtn_msg = EXEC_ACT(ACT_API.getRtnMsg, response_text)

#UpdateStoreInfo api
UPDATE_STORE_INFO_CSV = os.path.join(ROOTDIR, 'Test_data', 'AllpayAPI', 'UpdateStoreInfo', CASE_NAME, 'OrderInfo.csv')

update_store_info = EXEC_ACT(ACT_API.genUpdateStoreInfo, UPDATE_STORE_INFO_CSV)

update_store_info['StoreType'] = '01'
update_store_info['ReceiverStoreID'] = '870766'

update_store_info = EXEC_ACT(ACT_API.genCheckMacValue, update_store_info)

result = EXEC_ACT(ACT_API.updateStoreInfoByRequest, update_store_info)

#VERIFY
VERIFY(VER_API.verifyPrecondition, rtn_msg)

VERIFY(VER_API.verifyApiServing, result)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
