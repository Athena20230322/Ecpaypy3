# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueb2c import verifyInvIssueb2c
# from ECpay.ProdActions.ActECpayAPI.ActInvIssueInvalid import actInvIssueInvalid
# from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueInvalid import verifyInvIssueInvalid
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceb2c import actInvAllowanceb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceb2c import verifyInvAllowanceb2c
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceInvalidb2c import actInvAllowanceInvalidb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceInvalidb2c import verifyInvAllowanceInvalidb2c
from ECpay.ProdActions.ActECpayAPI.ActInvNotifyb2c import actInvNotifyb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvNotifyb2c import verifyInvNotifyb2c


# (DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str, default='', help = 'Specify the runtime guid for this run.')
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

ACT_ISS_API = actInvIssueb2c()
VER_ISS_API = verifyInvIssueb2c()
# ACT_ISSIV_API = actInvIssueInvalid()
# VER_ISSIV_API = verifyInvIssueInvalid()
ACT_ALL_API = actInvAllowanceb2c()
VER_ALL_API = verifyInvAllowanceb2c()
ACT_ALLIV_API = actInvAllowanceInvalidb2c()
VER_ALLIV_API = verifyInvAllowanceInvalidb2c()
ACT_API = actInvNotifyb2c()
VER_API = verifyInvNotifyb2c()

# Testing exec

# precondition-Issue

ISS_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', 'Initial_Data', 'InvIssue.csv')


iss_info = EXEC_ACT(ACT_ISS_API.genOrderRequestInfoB2c, ISS_INFO_CSV)

iss_info_res = EXEC_ACT(ACT_ISS_API.genPostRequestToAPI, iss_info)

res_dict = EXEC_ACT(ACT_ISS_API.strToDict, iss_info_res)

data = EXEC_ACT(ACT_ISS_API.decryptDatab2c, res_dict['Data'])
print(data)

# precondition-Issue Verify

VERIFY(VER_ISS_API.verifyColumn, 'InvIssueb2c_RAT_0001',data)



# precondition-Allowance

ALL_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', 'Initial_Data', 'InvAllowance.csv')



all_info = EXEC_ACT(ACT_ALL_API.genOrderRequestInfoB2c, ALL_INFO_CSV, data)

all_info_res = EXEC_ACT(ACT_ALL_API.genPostRequestToAPIb2c, all_info)

all_res_dict = EXEC_ACT(ACT_ALL_API.strToDict, all_info_res)

data1 = EXEC_ACT(ACT_ALL_API.decryptDatab2c,  all_res_dict['Data'])
print(data1)

# precondition-Allowance Verify

VERIFY(VER_ALL_API.verifyColumn, 'InvAllowanceb2c_RAT_0001',data1)

# precondition-AllowanceInvalid

ALLIV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', 'Initial_Data', 'InvAllowanceInvalid.csv')

exclusive_list = ['Reason']

revert_list = ['Reason']

alliv_info = EXEC_ACT(ACT_ALLIV_API.genOrderRequestInfoB2c, ALLIV_INFO_CSV, data1)

alliv_info_res = EXEC_ACT(ACT_ALLIV_API.genPostRequestToAPI, alliv_info)

alliv_res_dict = EXEC_ACT(ACT_ALL_API.strToDict, alliv_info_res)

data2 = EXEC_ACT(ACT_ALL_API.decryptDatab2c,  alliv_res_dict['Data'])
print(data2)

# precondition-AllowanceInvalid Verify

VERIFY(VER_ALLIV_API.verifyColumn, 'InvAllowanceInvalidb2c_RAT_0001',data2)

# InvNotify

NOTIFY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', CASE_NAME, 'OrderInfo.csv')

revert_args = ['NotifyMail']

notify_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c3, NOTIFY_INFO_CSV, data1,"' or 1=1--")

notify_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, notify_info)

# InvNotify Verify
VERIFY(VER_API.verifyStatusResult, notify_info_res,'')
#VERIFY(VER_API.verifyInvNotifyRequestInfob2c, notify_info_res, 'MerchantID Parameters Error')

#VERIFY(VER_API.verifyInvNotifyRequestInfob2c, CASE_NAME,data)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
