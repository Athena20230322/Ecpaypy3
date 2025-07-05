# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2b import actInvIssueb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueb2b import verifyInvIssueb2b


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
ACT_API = actInvIssueb2b()
VER_API = verifyInvIssueb2b()

#Testing exec

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvIssueb2b', CASE_NAME, 'Inv.csv')


inv_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2B, INV_INFO_CSV)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

data = EXEC_ACT(ACT_API.decryptDatab2b, res_dict['Data'])
print(data)

# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API.verifyResponseValuesb2b, CASE_NAME, data)
time.sleep(3)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
