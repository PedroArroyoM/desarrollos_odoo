#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#
#   Pedro Arroyo M <parroyo@mallconnection.com>
#   Copyright (C) 2015 Mall Connection(<http://www.mallconnection.org>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################## 
import xmlrpclib

class OpenERPClient(object):
    
    __server = ""
    __dbname = ""
    __user = ""
    __pwd = ""
    __uid = 0
    sock = object

    def get_server(self):
        return self.__server


    def get_dbname(self):
        return self.__dbname


    def get_user(self):
        return self.__user


    def get_pwd(self):
        return self.__pwd


    def get_uid(self):
        return self.__uid


    def set_server(self, value):
        self.__server = value


    def set_dbname(self, value):
        self.__dbname = value


    def set_user(self, value):
        self.__user = value


    def set_pwd(self, value):
        self.__pwd = value


    def set_uid(self, value):
        self.__uid = value


    def __init__(self, server, dbname,user,pwd):
        self.__server = server
        self.__dbname = dbname
        self.__user = user
        self.__pwd = pwd
        
        self.sock = xmlrpclib.ServerProxy(server + 'common')
        self.__uid = self.sock.login(dbname ,user ,pwd)
    
    def execute(self,*params):
        return self.sock.execute(self.__dbname, self.__uid, self.__pwd, *params)
    
    def execute_kw(self, *params):
        return self.sock.execute_kw(self.__dbname, self.__uid, self.__pwd, *params)
    
    def exec_workflow(self, *params):
        return self.sock.exec_workflow(self.__dbname, self.__uid, self.__pwd, *params)
    
    def login(self, *params):
        return self.sock.login(self.__dbname, self.__uid, self.__pwd, *params)
    
    def report(self, *params):
        return self.sock.report(self.__dbname, self.__uid, self.__pwd, *params)
     
    def report_get(self, *params):
        return self.sock.report_get(self.__dbname, self.__uid, self.__pwd, *params)
    
    def setDomain(self,domain):
        self.sock = xmlrpclib.ServerProxy(self.__server + domain)  