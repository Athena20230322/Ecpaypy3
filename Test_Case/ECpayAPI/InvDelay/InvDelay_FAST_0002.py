# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvDelay import actInvDelay
from ECpay.Verification.VerifyECpayAPI.VerifyInvDelay import verifyInvDelay


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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actInvDelay()
VER_API = verifyInvDelay()

# Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvDelay', CASE_NAME, 'OrderInfo.csv')

exclusive_args = ['InvoiceRemark', 'ItemName', 'ItemWord']

revert_args = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord']

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV, revert_args, exclusive_args)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

VERIFY(VER_API.verifyInvDelayRequestInfo, order_info_res, CASE_NAME)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)