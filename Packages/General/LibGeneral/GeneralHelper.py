import os
import sys
import time
import subprocess
from colorama import init as colorinit
from LibGeneral.AddLog import customLog

PJOIN = os.path.join

class typeHelper():
    
    def __init__(self):
        pass
    
    def toInt(self, obj):
        if isinstance(obj, int) is False:
            try:
                ret = int(obj)
            except:
                raise ValueError("Fail to convert object to integer, object value: %s" % (obj))
            else:
                return ret
        else:
            return obj


class configHelper():
    
    def __init__(self):
        pass
    
    def commaStringToList(self, data):
        if isinstance(data, str):
            if data.startswith(' '):
                data = data.strip(' ')
            if data.startswith('('):
                data = data.lstrip('(').rstrip(')')
            
            rtn_list = [x.strip(' ') for x in data.split(',')]
            return rtn_list
        else:
            raise TypeError("Provided argument is not string")


class messageProcessor():
    
    def __init__(self):
        self.color_dict = {
                    'red': '\033[1;31m',
                    'green': '\033[1;32m',
                    'orange': '',
                    'yellow': '',
                    'white': '\033[0;39m'
                    }

        self.osh = osHelper()
        self.curr_platform = self.osh.getOSPlatform()
        if self.curr_platform == 'windows':
            colorinit()
            
        
    def genHighlightDispDict(self, dictobj, name, value, color):
        if isinstance(dictobj, dict):
            try:
                color_code = self.color_dict[color]
            except KeyError:
                raise ValueError("Provided color name is not in color dictionary.")
            else:
                dictobj[name] = ''.join([color_code, value, self.color_dict['white']])
                return dictobj
        else:
            raise TypeError("First provided argument is not an dictionary.")
        
    def outAlignDictStr(self, dictobj):
        if isinstance(dictobj, dict):
            keys = list(dictobj.keys())
            lens = [len(x) for x in keys]
            max_len = max(lens)
            ret_string = ''
            i = 0
            for k in keys:
                space_mid = ' ' * (max_len - lens[i]) + (' ' * 4)
                indent = (' ' * 4)
                line = ''.join([indent, k, space_mid, str(dictobj[k]), '\n'])
                ret_string = ret_string + line
                i+=1
            print(ret_string)
            
        else:
            raise TypeError("printAlignDict: Recieved object is not an dictionary.")
    
    
class osHelper():
    
    def __init__(self):
        self.proc = subprocess
        self.chkout= self.proc.check_output
        self.osplat = self.getOSPlatform()
        self.type_helper = typeHelper()
        self.log = None
        if self.osplat == 'windows':
            self.path_delimeter = '\\'
        else:
            self.path_delimeter = '/'
        
    def enableLogging(self, logobj):
        self.log = logobj
        
    def getOSPlatform(self):
        os_type = sys.platform
        if os_type == 'win32':
            plat = 'windows'
        elif os_type == 'linux2':
            plat = 'linux'
        else:
            plat = 'unknown'
        return plat
        
    def startProc(self, path, duplicate=True, *args):

        print(path)
        cmd_list = []
        if isinstance(path, str):
            cmd_list.append(path)
        elif isinstance(path, list):
            cmd_list.extend(path)
            
        if duplicate is False:
            if isinstance(path, list):
                pids = self.getProcPIDbyPartCmd(path[1])
            else:
                pids = self.getProcPIDbyPartCmd(path)
            if pids is not False:
                print("Process Found, skip initialization")
                return False  
            
        cmd_list.extend(args)
        print("Start Proc", cmd_list)
        #self.log.INFO("Start process by running [%s] with argument %s" % (path, args))
        if self.osplat == 'windows':
            self.proc.Popen(cmd_list, shell=False)
        return True
    
    def runCommand(self, cmd_list):
        try:
            output = self.chkout(cmd_list, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            self.log.WARN(err.output)
        else:
            pass
        #finally:
            #print output
    
    def getProcPIDbyBinPath(self, path):
        if self.osplat == 'windows':
            pscmd = "(get-process | where {$_.path -eq '%s'}).id" % (path)
            pid = self.chkout(['powershell', pscmd]).split('\r\n')
            pid.remove('')
        if pid == []:
            return False
        else:
            return pid
    
    def getProcPIDbyName(self, procname):
        if self.osplat == 'windows':
            pscmd = "(get-process | where {$_.ProcessName -eq '%s'}).id" % (procname)
            pid = self.chkout(['powershell', pscmd]).split('\r\n')
            pid.remove('')
        if pid == []:
            return False
        else:
            return pid
        
    def getProcPIDbyPartCmd(self, cmdstr):
        if self.osplat == 'windows':
            pscmd = "(Get-WmiObject Win32_Process | select Commandline, Handle | where {($_.commandline -match %s) -and !($_.commandline -match 'WmiObject')}).Handle" % (repr(cmdstr))
            pscmd2 = "(Get-WmiObject Win32_Process | select Commandline, Handle | where {($_.commandline -match %s) -and !($_.commandline -match 'WmiObject')}).Commandline" % (repr(cmdstr))
            pid = self.chkout(['powershell', pscmd]).split('\r\n')
            cmd = self.chkout(['powershell', pscmd2]).split('\r\n')
            pid.remove('')
        if pid == []:
            return False
        else:
            return pid
        
    def stopProcByPID(self, pid, force=False):
        pid = self.type_helper.toInt(pid)
        print(pid)
        if self.osplat == 'windows':
            pscmd = "stop-process -id %i" % (pid)
            if force is True:
                pscmd = pscmd.replace('stop-process', 'stop-process -force')
            print(pscmd)
            perf = self.runCommand(['powershell', pscmd])
            #perf = self.chkout(['powershell', pscmd])
    
    def stopProcByName(self, procname, force=False):
        if self.osplat == 'windows':
            pscmd = "(get-process | where {$_.ProcessName -eq '%s'}).id | %%{stop-process -id $_ 2> $NULL}" % (procname)
            if force is True:
                pscmd = pscmd.replace('stop-process', 'stop-process -force')
            print(pscmd)
            perf = self.chkout(['powershell', pscmd])
            

    
class ServiceHelper():
    
    def __init__(self):
        self.osh = osHelper()
        self.conf_helper = configHelper()
        self.msgh = messageProcessor()
        
    def startServices(self, confobj, rootdir=None):
        to_list = self.conf_helper.commaStringToList
        if rootdir is None:
            root_opt = ['GeneralSettings', 'RootDir']
            if confobj.has_option(*root_opt):
                rootdir = confobj.get(*root_opt)
            else:
                raise ValueError("[%s] option not found in section [%s], please add this setting or provide rootdir in keyword argument." % (root_opt[1], root_opt[0]))
                
        start_seq = to_list(confobj.get('StartSequence', 'Seq'))
        
        result_dict = {}
        for svc in start_seq:
            cmdlist = []
            exe = confobj.get(svc, 'Executive')
            path_elem = to_list(confobj.get(svc, 'Folder'))
            path_elem.append(exe)
            path = PJOIN(rootdir, *path_elem)
            print(repr(path))
            executor = [svc, 'Script_executor']
            if confobj.has_option(*executor):
                cmdlist.append(confobj.get(*executor))

            cmdlist.append(path)
            
            args_opt = [svc, 'Args']
            arg = []
            if confobj.has_option(*args_opt):
                arg = to_list(confobj.get(*args_opt))
            print(cmdlist)
            self.osh.startProc(cmdlist, duplicate=False, *arg)
            time.sleep(30)
            pid = self.osh.getProcPIDbyPartCmd(exe)
            print(pid)
            
            if pid is not False:
                self.msgh.genHighlightDispDict(result_dict, svc, 'Success', 'green')
            else:
                self.msgh.genHighlightDispDict(result_dict, svc, 'Fail', 'red')
            
        print(self.msgh.outAlignDictStr(result_dict))

            
        
