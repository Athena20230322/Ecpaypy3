# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActUpdateShipInfo import actUpdateShipInfo
from ECpay.Verification.VerifyECpayAPI.VerifyUpdateShipInfo import verifyUpdateShipInfo


#(DO NO Edit) Static declare 

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str , default='', help='Specify the runtime guid for this run.')
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
ACT_API = actUpdateShipInfo()
VER_API = verifyUpdateShipInfo()

#Testing exec
#precondition: generate order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'AioCheckOut', 'AioCheckOut_RAT_0002', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createECpayOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9522-2222-2222', '22', '05', '222', '0900000000')

#otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')

#EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']

MERC_T_DT = order_info['MerchantTradeDate']
time.sleep(5)

DRIVER.delete_all_cookies()
DRIVER.quit()

#precondition: generate B2C order
B2C_ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_data', 'ECpayAPI', 'UpdateShipInfo', 'Initial_Data', 'Create.csv')

b2c_order_info = EXEC_ACT(ACT_API.genB2COrderRequestInfo, B2C_ORDER_INFO_CSV, MERC_TID, MERC_T_DT)

response_text = EXEC_ACT(ACT_API.createOrderByRequest, b2c_order_info)

LOGISTICS_ID = EXEC_ACT(ACT_API.getLogisticsID, response_text)

print(LOGISTICS_ID)
time.sleep(5)

#UpdateShipmentInfo api
UPDATE_SHIPMENT_INFO_CSV = os.path.join(ROOTDIR, 'Test_data', 'ECpayAPI', 'UpdateShipInfo', CASE_NAME, 'OrderInfo.csv')

update_shipment_info = EXEC_ACT(ACT_API.genUpdateShipInfo, UPDATE_SHIPMENT_INFO_CSV, 'sleep(__TIME__)#')

update_shipment_info['ShipmentDate'] = EXEC_ACT(ACT_API.updateShipmentDate, 3)

update_shipment_info = EXEC_ACT(ACT_API.genCheckMacValue, update_shipment_info)

result = EXEC_ACT(ACT_API.updateShipInfoByRequest, update_shipment_info)

#VERIFY
VERIFY(VER_API.verifyRATResult, result)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)