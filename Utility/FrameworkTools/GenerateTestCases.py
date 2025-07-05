import argparse
import os
import re
import sys
import shutil
import subprocess
import configparser
import LibGeneral.funcGeneral as funcGen
import LibGeneral.GetConfigValue as getConf


def createCaseStructure(casename):
    if casename is not None and casename != '':
        ## Create Case folder & Data folder
        script_name = casename + '.py'
        case_folder = CASE_ROOT
        data_folder = PJOIN(DATA_ROOT, casename)
        case_path = PJOIN(case_folder, script_name)
        funcGen.testFolderPath(case_folder)
        
        ## Copy test data
        #### Copy through shutil might with potential risk because not all metadata would be replicate on every OS
        data_template_dir = PJOIN(ROOTDIR, 'Tmp', 'TestModule_Template', PRODUCT, 'Data')
        funcGen.copyFolder(data_template_dir, data_folder)
        
        ## Copy case template
        temp_file = MODULE + '_Case_Template.py'
        case_temp = PJOIN(CASE_ROOT, 'BaseCase', temp_file)
        funcGen.fncopyfile(case_temp, case_path)
    else:
        print("Casename cannot be empty.")

PJOIN = os.path.join

ARGP = argparse.ArgumentParser(description='Script for creating new test case script file & related folder.')
ARGP.add_argument('--product' , type=str, help = '')
ARGP.add_argument('--module' , type=str, help = '')
ARGP.add_argument('--caselist' , type=str , help = '')
#ARGP.add_argument('--list-product' , type=str , default='', help = '')

## Turn argument into variable

ARGS = ARGP.parse_args()
PRODUCT = ARGS.product
MODULE = ARGS.module
CASE_LIST = ARGS.caselist

## Import framework config 
CONF = getConf.getConfig()
ROOTDIR = CONF.getRootDir()
AVALIABLE_PROD_DIR = PJOIN(ROOTDIR, 'Tmp', 'TestModule_Template')
CURR_PRODUCT = next(os.walk(AVALIABLE_PROD_DIR))[1]
CASE_ROOT = PJOIN(ROOTDIR, 'Test_Case', PRODUCT, MODULE)
DATA_ROOT = PJOIN(ROOTDIR, 'Test_Data', PRODUCT, MODULE)

if CURR_PRODUCT.__contains__(PRODUCT):
    if os.path.exists(CASE_ROOT):
        if os.path.exists(DATA_ROOT):
            if os.path.exists(CASE_LIST):
                with open(CASE_LIST, mode='r') as case_names:
                    for name in case_names:
                        name = name.rstrip('\n')
                        createCaseStructure(name)
            else:
                print("Case list file not found.")
        else:
                print("Test Data container of specified product module not found but case container exists, please check related folder name.\n Case Folder: %s\n Data Folder: %s\n" % (CASE_ROOT, DATA_ROOT))            
    else:
        print("Test Case container of specified product module not found. Please make sure the module name you provided is correct.")
else:
    print("Product name not found in %s" % (AVALIABLE_PROD_DIR))