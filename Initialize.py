# Clean all dataset db file
# Stop all running test
        #update all running task to terminated
# Check test result DB connection


import os
import re
import sys
import subprocess

PJOIN = os.path.join
RM = os.remove
CLOSE_FILE = os.close
RENAME = os.rename
PROC = subprocess.Popen

def genEnvVariableStr(var_name, var_data, os_type='win', filter_str=[]):
    ##Determine system platform
    if os_type == 'win':
        separator = ';'
    elif os_type == 'unix':
        separator = ':'
    curr_data = os.environ.get(var_name)
    if curr_data is not None:
        if curr_data != '':
            var_elems = curr_data.split(separator)
            if filter_str:
                for s in filter_str:
                    var_elems = [x for x in var_elems if not x.__contains__(s)]
            else:
                pass
            raw_elems = var_elems + var_data
            new_elems = []
            [new_elems.append(x) for x in raw_elems if not new_elems.count(x)]
            str_path_var = '{}'.format(separator.join(new_elems))
        else:
            str_path_var = '{}'.format(separator.join(var_data))
    else:
        str_path_var = '{}'.format(separator.join(var_data))

    return str_path_var

ROOTDIR = os.path.dirname(os.path.realpath(__file__))
print(ROOTDIR)


###Define folders in pypath
PKG_FOLDER = PJOIN(ROOTDIR, 'Packages')
GEN_FOLDER = PJOIN(ROOTDIR, 'Packages', 'General')
TDS_FOLDER = PJOIN(ROOTDIR, 'Lib', 'FreeTDS')
OPSSL_FOLDER = PJOIN(ROOTDIR, 'Lib', 'OpenSSL')


PYPATH = [PKG_FOLDER, GEN_FOLDER, TDS_FOLDER, OPSSL_FOLDER]


###Verify OS platform
OS_TYPE = sys.platform
if OS_TYPE == 'win32':
    WIN_STR_PYPATH = ['%PYTHONPATH%']
    PYPATH_FILTER = ['AutoTest']
    PYPATH_STRING = genEnvVariableStr('PYTHONPATH' ,PYPATH, os_type='win', filter_str=PYPATH_FILTER)
    print(PYPATH_STRING)
    PROC(['setx', '/M', 'PYTHONPATH', PYPATH_STRING])
    PATH_STR = genEnvVariableStr('PATH', WIN_STR_PYPATH, os_type='win')
    print(PATH_STR)
    PROC(['setx', '/M', 'PATH', PATH_STR])
elif OS_TYPE == 'linux':
    WIN_STR_PYPATH = '%PYTHONPATH%'
    SEPARATOR = ':'
    STR_PYPATH = SEPARATOR.join(PYPATH)
    print(STR_PYPATH)

##Upgrade pip

PROC(['python', '-m', 'pip', 'install', '--upgrade', 'pip']).wait()


##install pip packages
PIP_PKG_LIST = PJOIN(ROOTDIR, 'Utility', 'Requirement', 'Dependency_pkg.txt')
with open(PIP_PKG_LIST, mode='r') as reqlist:
    for pkg in reqlist:
        print(pkg)
        proc = PROC(['pip', 'install', pkg])
        output, errors = proc.communicate()
        print(('after:', pkg))

##modify root folder settings in config file
CONFIG_FILE = PJOIN(ROOTDIR, 'Conf', 'Settings.ini')
CONF_TMP = PJOIN(ROOTDIR, 'Conf', 'Settings.tmp')
ROOTDIR_CONF = 'root_dir = %s' % (ROOTDIR)
with open(CONFIG_FILE, mode='r') as src_file:
    with open(CONF_TMP, mode='w') as out_file:
        for li in src_file:
            out_file.write(re.sub("root_dir = .*", ROOTDIR_CONF, li))
BACKUP = CONFIG_FILE.replace('.ini', '.bak')
RM(BACKUP)
RENAME(CONFIG_FILE, BACKUP)
RENAME(CONF_TMP, CONFIG_FILE)

