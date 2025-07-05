# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActEmbeddedtoken import actEmbeddedtoken
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedtoken import verifyEmbeddedtoken
from ECpay.ProdActions.ActECpayAPI.ActEmbeddedtokenuser import actEmbeddedtokenuser
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedtokenuser import verifyEmbeddedtokeuser


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
ACT_API = actEmbeddedtoken()
VER_API = verifyEmbeddedtoken()
ACT_API2 = actEmbeddedtokenuser()
VER_API2 = verifyEmbeddedtokeuser()

#Testing exec

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedTokenbyUser', CASE_NAME, 'Inv1.csv')

inv_info = EXEC_ACT(ACT_API.genOrderRequestInfoThreeD2RemoveRevision, INV_INFO_CSV)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

data = EXEC_ACT(ACT_API.decryptDatab2b2, res_dict['Data'])

print(data)


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

#VERIFY(VER_API.verifyResponseValuesforApp, CASE_NAME, data)
#time.sleep(3)




INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedTokenbyUser', CASE_NAME, 'Inv.csv')

inv_info = EXEC_ACT(ACT_API2.genOrderRequestInfoNoThreeD2, INV_INFO_CSV)

api_response = EXEC_ACT(ACT_API2.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_API2.strToDict, api_response)

data2 = EXEC_ACT(ACT_API2.decryptDatab2b2, res_dict['Data'])

print(data2)


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API2.verifyResponseValuesforApp, CASE_NAME, data2)
time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
