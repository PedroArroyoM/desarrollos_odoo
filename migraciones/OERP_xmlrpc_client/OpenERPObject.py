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

class OpenERPObject(object):
    __client = object
    
    def __init__(self, openerpclient):
        self.__client = openerpclient
        self.__client.setDomain("object")
        
    def search(self,model, args):    
        return self.__client.execute(model, 'search', args)
    
    def read(self, model, ids, fields):
        return self.__client.execute(model, 'read', ids, fields)

    def searchread(self, model, where, fields):
        res = self.search(model, where)
        if res==None or len(res)==0:
            return None
        return self.read(model, res, fields)
        
    def create(self, model, data):
        return self.__client.execute(model, 'create', data )
        
    def update(self, ids, model, data):
        return self.__client.execute(model, 'write', ids, data)
    
    def delete(self, model, ids):
        return self.__client.execute( model, 'unlink', ids)
    
    def workflow(self, model, action, ids):
        return self.__client.exec_workflow( model, action, ids)