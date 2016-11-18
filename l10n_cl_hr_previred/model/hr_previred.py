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



from osv import osv
from osv import fields

class hr_previred(osv.osv):
    '''
    Open ERP Model
    '''
    _name = 'hr.previred'
    _description = 'hr.previred'
 
    _columns = {
            'name':fields.char('data', size=64, required=False, readonly=False),
            'hr_payslip_id':fields.many2one('hr.payslip.run', 'Payslip runned', required=False), 
            'state':fields.selection([
                ('draft','Draft'),
                ('done','Done'),
                 ],    'State', select=True, readonly=True),
            'previred_line_ids':fields.one2many('hr.previred.line', 'previred_id', 'Line', required=False),
            
        }
    
    def generate_report(self, cr, uid, ids,payslip_group, context=None):
        
        
        return
    
    
hr_previred()