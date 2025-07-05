# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActEmbeddedCreatePaymentWeb import actEmbeddedcreatepaymentweb
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedCreatePaymentWeb import verifyEmbeddedcreatepaymentweb

from ECpay.ProdActions.ActECpayAPI.ActShopifyN import actShopifyN
from ECpay.Verification.VerifyECpayAPI.VerifyShopifyN import verifyShopifyN


from ECpay.ProdActions.ActECpayAPI.ActEmbedded import actEmbedded
from ECpay.Verification.VerifyECpayAPI.VerifyEmbedded import verifyEmbedded

from ECpay.ProdActions.ActECpayAPI.ActEmbeddedPayToken import actEmbeddedpaytoken
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedPayToken import verifyEmbeddedpaytoken


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
ACT_API = actEmbeddedcreatepaymentweb()
VER_API = verifyEmbeddedcreatepaymentweb()

ACT_API1 = actShopifyN()
VER_API1 = verifyShopifyN()
ACT_API2 = actEmbedded()
VER_API2 = verifyEmbedded()
ACT_API3 = actEmbeddedpaytoken()
VER_API3 = verifyEmbeddedpaytoken()
ACT_API5 = actEmbeddedpaytoken()
VER_API5 = verifyEmbeddedpaytoken()

#Testing exec


INV_INFO_CSV2 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ShopifyN', CASE_NAME, 'Tokenget.csv')

print('6563535')
inv_info = EXEC_ACT(ACT_API1.genOrderRequestInfoThreeD2, INV_INFO_CSV2)



api_response = EXEC_ACT(ACT_API1.genPostRequestToAPINoheaderinstallment, inv_info)


res_dict = EXEC_ACT(ACT_API1.strToDict, api_response)

EXEC_ACT(ACT_API1.enableWebOperate, DRIVER)

EXEC_ACT(ACT_API1.createShopifyByBrowser,res_dict)

time.sleep(5)

merchantNumber=EXEC_ACT(ACT_API1.CheckOrderNum,res_dict)

#EXEC_ACT(ACT_API1.inputPaymentPageCreditInfoBindbydivisionE, '4311-9522-2222-2222', '22', '05', '222', '0900000000', 'divide','test',' autotest123@gmail.com')

EXEC_ACT(ACT_API1.inputPaymentPageCreditInfo, '4311-9522-2222-2222', '23', '05', '222', '0900000000', 'divide','test')

EXEC_ACT(ACT_API1.inputOTPCredit, '1234')
time.sleep(3)


ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ShopifyN', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API1.genOrderRequestInfo, ORDER_INFO_CSV,merchantNumber)

#res = EXEC_ACT(ACT_API.createOrderByRequestThreeD, order_info)

order_info_res = EXEC_ACT(ACT_API1.genPostRequestToAPIShopifyQuery, order_info)

res_dict = EXEC_ACT(ACT_API1.strToDictShopifyQuery, order_info_res)

data = EXEC_ACT(ACT_API1.decryptData, res_dict['Data'])
print(data)
#MERC_UID = order_info['MerchantID']
time.sleep(5)
#VERIFY(VER_API.verifyPaymentReturn, MERC_TID, {'PayAmt':'100'})

#VERIFY(VER_API.verifyPaymentReturn, MERC_TID, CASE_NAME)

VERIFY(VER_API1.verifyPaymentReturn, data, CASE_NAME)

#EXEC_ACT(ACT_API1.QueryOrderNum)

#MERC_TID = res_dict
#VERIFY(VER_API1.verifyOrderByQuery, res_dict, merc_tid,CASE_NAME,data)






#VERIFY(VER_API.verifyResponseValuesforcreatepayment,CASE_NAME)
#time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
