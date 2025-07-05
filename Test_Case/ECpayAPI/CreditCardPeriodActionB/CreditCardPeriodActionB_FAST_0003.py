# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCreditCardPeriodActionB import actCreditCardPeriodActionB
from ECpay.Verification.VerifyECpayAPI.VerifyCreditCardPeriodActionB import verifyCreditCardPeriodActionB



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
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actCreditCardPeriodActionB()
VER_API = verifyCreditCardPeriodActionB()

#Testing exec


ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreditCardPeriodActionB', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo1, ORDER_INFO_CSV)

#res = EXEC_ACT(ACT_API.createOrderByRequestThreeD, order_info)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

res_dict = EXEC_ACT(ACT_API.strToDict3D, order_info_res)

data = EXEC_ACT(ACT_API.decryptData3D, res_dict['Data'])
print(data)

VERIFY(VER_API.verifyResponseValuesThreeD, CASE_NAME, res_dict, data)


# ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreditCardPeriodActionB', CASE_NAME, 'OrderInfo.csv')
#
# order_info = EXEC_ACT(ACT_API.genOrderRequestInfoThreeD2, ORDER_INFO_CSV)
#
# res = EXEC_ACT(ACT_API.createOrderByRequestThreeD, order_info)
#
# res_dict = EXEC_ACT(ACT_API.strToDict3D, res)
#
# data = EXEC_ACT(ACT_API.decryptData3D, res_dict['Data'])
#
# VERIFY(VER_API.verifyResponseValuesThreeD, CASE_NAME, client_dict, data2)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)