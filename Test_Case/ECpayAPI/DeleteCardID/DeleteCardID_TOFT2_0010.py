# -*- coding: utf-8 -*-

#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActBindingCardID import actBindingCardID
from ECpay.ProdActions.ActECpayAPI.ActDeleteCardID import actDeleteCardID
from ECpay.Verification.VerifyECpayAPI.VerifyDeleteCardID import verifyDeleteCardID


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
BINDING_CARD = actBindingCardID()
ACT_API = actDeleteCardID()
VER_API = verifyDeleteCardID()


#Pre-condition: BindingCardID

BINDING_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'DeleteCardID', 'Initial_Data', 'BindingInfo_MMID_P.csv')

EXEC_ACT(BINDING_CARD.enableWebOperate, DRIVER)

binding_info = EXEC_ACT(BINDING_CARD.genBindingRequestInfo, BINDING_INFO_CSV)

binding_response = EXEC_ACT(BINDING_CARD.createOrderByBrowser, DRIVER, binding_info)

EXEC_ACT(BINDING_CARD.inputCreditCardInfo, '4311-9522-2222-2222', '2020', '12', '222')

res_CliReUrl = EXEC_ACT(BINDING_CARD.GetInfoFromClientRedirectUrl)

res_CliReUrl_dict = EXEC_ACT(BINDING_CARD.redirectStrToDict, res_CliReUrl)

merchant_mem_id = res_CliReUrl_dict['MerchantMemberID']
card_id = res_CliReUrl_dict['CardID']

#Testing exec

DELETE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'DeleteCardID', CASE_NAME, 'DeleteInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

delete_info = EXEC_ACT(ACT_API.genOrderRequestInfo, DELETE_INFO_CSV, merchant_mem_id, card_id)

delete_res = EXEC_ACT(ACT_API.genPostRequestToAPI, delete_info)

delete_res_dict = EXEC_ACT(ACT_API.strToDict, delete_res)

#VERIFY

VERIFY(VER_API.verifyResponseValues, delete_res_dict, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)