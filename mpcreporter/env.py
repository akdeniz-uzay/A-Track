# -*- coding: utf-8 -*-

import os
import glob
import numpy as np
import getpass
import inspect
import platform
from datetime import datetime


class etc():

    def __init__(self, verb=True):
        self.verb = verb
        self.log_file = "%s/log.my" % (os.path.expanduser("~"))
        self.mini_log_file = "%s/mlog.my" % (os.path.expanduser("~"))

    def time_stamp(self):
        return str(datetime.utcnow().strftime("%Y-%m-%IT%H:%M:%S"))

    def user_name(self):
        return str(getpass.getuser())

    def system_info(self):
        si = platform.uname()
        return(("%s, %s, %s, %s" % (si[0],
                                    si[2],
                                    si[5],
                                    self.user_name())))

    def caller_function(self, pri=True):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe
        self.system_info()
        if pri:
            return "%s>%s>%s" % (caller[0][3], caller[1][3], caller[2][3])
        else:
            return caller

    def print_if(self, text):
        self.log_if(text)
        self.mini_log_if(text)
        if self.verb:
            print(("[%s|%s|%s]%s" % (self.time_stamp(), self.caller_function(),
                 self.system_info(), text)))

    def log_if(self, text):
        log_file = open(self.log_file, "a")
        log_file.write("Time: %s\n" % self.time_stamp())
        log_file.write("System Info: %s\n" % self.system_info())
        log_file.write("Log: %s\n" % text)
        log_file.write("Function: %s\n\n\n" % (self.caller_function(pri=False)))
        log_file.close()

    def mini_log_if(self, text):
        mini_log_file = open(self.mini_log_file, "a")
        mini_log_file.write("[%s|%s|%s]%s\n" % (
            self.time_stamp(), self.caller_function(),
            self.system_info(), text))
        mini_log_file.close()


class file_op():

    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = etc(verb=self.verb)

    def read_file_as_array(self, file_name):
        try:
            return(np.genfromtxt(file_name,
                                 comments='#',
                                 delimiter=' | ',
                                 dtype="U"))
        except Exception as e:
            self.eetc.print_if(e)
        
    def read_res(self, file_name):
        try:
            return(np.genfromtxt(file_name,
                                 comments='O',
                                 skip_header=1,
                                 invalid_raise=False,
                                 delimiter=None,
                                 usecols=(0, 1, 3, 4, 5)))
        except Exception as e:
            self.eetc.print_if(e)

    def get_file_list(self, dir_name):
        try:
            images = sorted(glob.glob(dir_name + '/*.fit*'))
            return(images)
        except Exception as e:
            self.eetc.print_if(e)

    def find_if_in_database_id(self, database, idd):
        ret = ""
        try:
            f = open(database, "r")
            for i in f:
                ln = i.replace("\n", "").split()
                try:
                    if "(%s)" % idd == ln[21]:
                        id_name = ln[0]
                        if len(id_name) > 5:
                            ret = "     " + id_name
                        else:
                            ret = id_name
                except:
                    continue
            f.close()
        except Exception as e:
            self.eetc.print_if(e)

        return(ret)

    def find_if_in_database_name(self, database, name):
        ret = ""
        try:
            f = open(database, "r")
            for i in f:
                ln = i.replace("\n", "").split()
                try:
                    if len(ln[23]) < 8:
                        combname = "{0} {1}".format(ln[22], ln[23])
                    else:
                        combname = ln[22]

                    if name == combname:
                        id_name = ln[0]
                        if len(id_name) > 5:
                            ret = "     " + id_name
                        else:
                            ret = id_name
                except:
                    continue
            f.close()
        except Exception as e:
            self.eetc.print_if(e)

        return(ret)
