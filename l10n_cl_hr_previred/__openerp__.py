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


{
        "name" : "Previred",
        "version" : "3",
        "author" : "Pedro Arroyo M ; MallConnection",
        "website" : "www.mallconnection.cl",
        "category" : "payroll",
        "description": """  """,
        "depends" : ['base','hr','account'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : [
                        'xml/hr_payslip_run_view.xml',
                        'xml/hr_payslip_view.xml',
                        'xml/hr_previred_config_view.xml',
                        'xml/hr_previred_export_view.xml',
                        'xml/hr_previred_line_view.xml',
                        #'hr_previred_view.xml',
                        
                        ],# 'security/ir.model.access.csv'],
        "installable": True
}
