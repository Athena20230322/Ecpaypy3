import argparse
import os
import re
import sys
import subprocess
import configparser
import LibGeneral.funcGeneral as funcGen
import LibGeneral.GetConfigValue as getConf

def configToDic(configobj):
    all_sections = configobj._sections
    for sec in all_sections:
        all_sections[sec].__delitem__('__name__')
    return all_sections

def processCustomPath(path_dic, aliasdic):
    result_dic = {}
    for k in list(path_dic.keys()):
        print('Path Element :', path_dic[k])
        elems = list(x.strip(' ') for x in path_dic[k].lstrip('(').rstrip(')').split(','))
        p = os.path.join(*elems)
        for alias_key in list(aliasdic.keys()):
            p = p.replace(alias_key, aliasdic[alias_key])
        new_key = '%' + k
        aliasdic[new_key] = p
        print('Processed alias dic:', aliasdic)
        result_dic[new_key] = p
    return result_dic

def replaceContentByConf(conf):
    print("Replacing with conf : %s " % (conf))
    conf_list = [x.strip(' ').lstrip('(').rstrip(')') for x in conf.split(';')]
    print('CONF_LIST:', conf_list)
    src_partial = [x.strip(' ') for x in conf_list[0].split(',')]
    src = PJOIN(ROOTDIR , PJOIN(*src_partial))
    tmp = src + '.tmp'
    sub_list = [x.strip(' ').replace("'", "") for x in conf_list[1].split(':')]
    print(sub_list)
    pattern = sub_list[0]
    val = sub_list[1]
    print("PATTERN:", pattern)
    print("VALUE:", val)
    with open(src, mode='r') as src_file:
        with open(tmp, mode='w') as out_file:
            for li in src_file:
                out_file.write(re.sub(pattern, val, li))
    print("Removing file %s..." % (src))    
    RM(src)
    RENAME(tmp, src)
     


def addCustomPathFromConf(configobj):
    pass


ARGP = argparse.ArgumentParser(description='Script for creating new product module related objects in Testing Framework.')
ARGP.add_argument('--product' , type=str, help = '')
ARGP.add_argument('--module' , type=str, help = '')
ARGP.add_argument('--caselist' , type=str , default='', help = '')
#ARGP.add_argument('--list-product' , type=str , default='', help = '')

## Turn argument into variable

ARGS = ARGP.parse_args()
PRODUCT = ARGS.product
MODULE = ARGS.module
CASE_LIST = ARGS.caselist
ALIAS_DICT = {}
ALIAS_DICT['%PRODUCTNAME'] = PRODUCT
ALIAS_DICT['%MODNAME'] = MODULE


##General instance define
PJOIN = os.path.join
RM = os.remove
RENAME = os.rename
CLOSE_FILE = os.close
PROC = subprocess.Popen

## Import framework config 
CONF = getConf.getConfig()

## Import product specific config 
PRODCONF = configparser.ConfigParser()
PRODCONF.optionxform = str

ROOTDIR = CONF.getRootDir()
CASE_FOLDER = PJOIN(ROOTDIR, 'Test_Case')
AVALIABLE_PROD_DIR = PJOIN(ROOTDIR, 'Tmp', 'TestModule_Template')

CURR_PRODUCT = next(os.walk(AVALIABLE_PROD_DIR))[1]

if CURR_PRODUCT.__contains__(PRODUCT):
    PRODUCT_CONFIG_PATH = PJOIN(AVALIABLE_PROD_DIR, PRODUCT, 'config.ini')
    PRODCONF.read(PRODUCT_CONFIG_PATH)
    if MODULE is not None and MODULE != '':
        
        ## Process Path alias
        DIC_CONFIG = configToDic(PRODCONF)
        print('Config DIC: ', DIC_CONFIG)
        print('Alias Config:', DIC_CONFIG['PathAlias'])
        C_PATHS = processCustomPath(DIC_CONFIG['PathAlias'], ALIAS_DICT)
        print(C_PATHS)
        ALIAS_DICT = funcGen.mergeDict(ALIAS_DICT, C_PATHS)
        AVAL_ALIAS = list(ALIAS_DICT.keys())
        print('Merged ALIAS:', ALIAS_DICT)
        
        ## Process folder creation
        CREATE_CONF = DIC_CONFIG['CreateFolder']
        CREATE_FOLDERS = [ALIAS_DICT[x.strip(' ')] for x in CREATE_CONF['Create'].split(',')]
        print(CREATE_FOLDERS)
        for folder in CREATE_FOLDERS:
            fullpath = PJOIN(ROOTDIR, folder)
            print(fullpath)
            funcGen.testFolderPath(fullpath)
        
        ## Process file copy
        COPY_CONF = DIC_CONFIG['CopyFile']
        
        for key in list(COPY_CONF.keys()):
            PATH_STR = COPY_CONF[key]
            for aname in AVAL_ALIAS:
                PATH_STR = PATH_STR.replace(aname, ALIAS_DICT[aname])
            if PATH_STR.__contains__('%') is False:
                F_LIST = [x.replace('(', '').replace(')', '').strip(' ') for x in PATH_STR.split(';')]
                if len(F_LIST) == 2:
                    print(F_LIST)
                    SRC_FILE = PJOIN(ROOTDIR, *[x.strip(' ') for x in F_LIST[0].split(',')])
                    print(SRC_FILE)
                    DEST_FILE = PJOIN(ROOTDIR, *[x.strip(' ') for x in F_LIST[1].split(',')])
                    print(DEST_FILE)
                    funcGen.fncopyfile(SRC_FILE, DEST_FILE)
                else:
                    raise ValueError('''Process file copy fail, cannot split source & dest file path from data
                    in config key : %s, please make sure the data is devided by ";".''' % (key) )
            else:
                raise ValueError('''Processed file path contains unknown alias name, config string : %s ";".''' % (PATH_STR) )                
                
        
        
        ## Process file content substitute      
        REPLACE_CONF = DIC_CONFIG['Substitute']
        for key in list(REPLACE_CONF.keys()):
            CONF_STR = REPLACE_CONF[key]
            for aname in AVAL_ALIAS:
                CONF_STR = CONF_STR.replace(aname, ALIAS_DICT[aname]) 
            print(CONF_STR)
            replaceContentByConf(CONF_STR)
        
    else:
        print("Module name cannot be empty.")
else:
    print("Product name not found in %s" % (CASE_FOLDER))




    

