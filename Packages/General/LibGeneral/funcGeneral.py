import time
import datetime
import logging
import uuid
import os
import shutil



def chkTupleElem(obj, value):
    
    if type(obj) is tuple:
        
        if value in obj:
            return True
        else:
            msg = "chkTupleElem : input value %s not found in specified tuple %s ." % (value, obj)
            logging.warning(msg)
            return False
        
    else:
        msg = "chkTupleElem : The given object %s is not a tuple" % (obj)
        raise TypeError(msg)
        
            
        
def genRandomUuid(with_dash = True):
    
    if with_dash:
        uid = uuid.uuid4()
        return uid
    elif with_dash == False:
        uid = str(uuid.uuid4()).replace('-', '')
        return uid

def getCurrentDatetimeStamp(mode = 'local'):
    dt = datetime.datetime
    if mode == 'local':
        now = dt.now()
    elif mode == 'utc':
        now = dt.utcnow()
    unix = int(time.mktime(now.timetuple()))
    res = (str(now), unix)
    return res
    

def fncopyfile(src, dst):
    if os.path.exists(dst) is False:
        with open(src, mode='r') as src_file:
            with open(dst, mode='w') as out_file:
                for li in src_file:
                    out_file.write(li) 
    else:
        print(("Destination file already exists, skip. [%s]" % (dst)))

def copyFolder(src, dst):
    if os.path.exists(src):
        try:
            shutil.copytree(src, dst)
        except IOError as ioerr:
            msg = ioerr.message
            print (msg)
        except WindowsError as winerr:
            msg = winerr.strerror
            win_err_no = winerr.winerror
            if win_err_no == 183:
                print(("Destination folder exists, skip. [%s] " % (dst)))
            else:
                print(("Unexpected windows error occurs , msg : %s" % (msg)))
        except Exception as e:
            print(("Unexpected exception occurred, error msg: %s" % (e.message)))
        else:
            print(("Copy folder complete.\n Source : %s\n Destination : %s" % (src, dst)))
        finally:
            pass
    else:
        raise IOError("copyFolder: Source folder not exists. [%s]") % (src)

def testFolderPath(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    else:
        print(("Folder exists, skip. [%s]" % (dirpath)))
        
    
def testFilePath(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    open(filepath, 'a').close()
    
    
def chkCmdInject(*args):
    injectors = [';', '|', '$', '`']
    found = 0
    for arg in args:
        for inj in injectors:
            if str(arg).__contains__(inj):
                found += 1
                return True
    if found == 0:
        return False
            
def resolveElemStyle(sty_str):
    style_list = str(sty_str).split(';')
    style_setting = {x.replace(' ', '').split(':')[0] : x.replace(' ', '').split(':')[1] for x in style_list if x != ''} 
    return style_setting

def genJSONString(jformat, values):
    pass
    
def mergeDict(src, append):
    if type(src) is dict and type(append) is dict:
        res = src.copy()
        res.update(append)
        return res
    else:
        raise TypeError("mergeDict: Specified argument is not an dictionary.")
    
def uniqMergeList(*mul_lists):
    container = []
    for l in mul_lists:
        if type(l) is list:
            container.extend(l)
        else:
            raise TypeError("uniqMergeList: Specified argument is not a list.")
    res =list(set(container))
    res.sort()
    return res


def listToModuloStr(list_tuple):
    modlist = []
    for i in list_tuple:
        typ = type(i)
        if typ == str:
            sym = '%s'
        elif typ == int:
            sym = '%d'
        elif typ == float:
            sym = '%f'
        elif typ == str:
            sym = '%s'
        elif i is None:
            sym = '%s'
        else:
            raise TypeError("listToModuloStr: Unexpected type of '%s'" % (typ))
        modlist.append(sym)
    modtup = tuple(modlist)
    modstr = modtup.__str__().replace("'", "")
        
    return modstr
            
    