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


from osv import fields,osv
import time



class hr_previred_config(osv.osv):
    '''
    
    
    '''
    _name = 'hr.previred.config' 
    
    _columns = {
                'name':fields.char('Description', size=64, required=False, readonly=False),
                'state':fields.selection([
                    ('active','Active'),
                    ('inactive','Inactive'),
                     ],    'State', select=True, readonly=False),
                'positions': fields.text('Type and positions'), 
                'worked_days_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_worked_days_rules_rel', 'previred_conf_id', 'workday_rule_id', 'Taxable rules'),
                'taxable_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_taxable_rules_rel', 'previred_conf_id', 'taxable_rule_id', 'Taxable rules'),
                'afp_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_afp_rules_rel', 'previred_conf_id', 'afp_rule_id', 'AFP rules'), 
                'sis_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_sis_rules_rel', 'previred_conf_id', 'sis_rule_id', 'SIS rules'), 
                'count_2_rule_ids':fields.many2many('hr.salary.rule', 'hr_previredcount_2_rules_rel', 'previred_conf_id', 'cuenta_2_rule_id', 'Count 2 rules'), 
                'family_assigment_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_family_assigment_rules_rel', 'previred_conf_id', 'family_assigment_rule_id', 'Family assigment rules'), 
                'family_assigment_retro_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_family_assigment_retro_rules_rel', 'previred_conf_id', 'family_assigment_retro_rule_id', 'Family assigment retro rules'), 
                'family_reassigment_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_family_reassigment_rules_rel', 'previred_conf_id', 'family_reassigment_rule_id', 'Family reassigment rules'), 
                'young_worker_app_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_young_worker_app_rules_rel', 'previred_conf_id', 'young_worker_app_rule_id', 'Young worker application rules'),
                'taxable_income_repl_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_taxable_income_repl_rules_rel', 'previred_conf_id', 'taxable_income_repl_rule_id', 'Taxable income repl rules'),
                'contribution_repl_indemty_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_contribution_repl_indemty_rules_rel', 'previred_conf_id', 'contribution_repl_indemty_rule_id', 'Contribution repl indemty rules'),
                'drudgery_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_drudgery_rules_rel', 'previred_conf_id', 'drudgery_rule_id', 'Drudgery rules'),
                'apvi_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_apvi_rules_rel', 'previred_conf_id', 'apvi_rule_id', 'APV indivitual rules'),
                'agreed_deposits_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_agreed_deposits_rules_rel', 'previred_conf_id', 'agreed_deposit_rule_id', 'Agreed deposit rules'),
                'apvc_employer_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_apvc_employer_rules_rel', 'previred_conf_id', 'apvc_employer_rule_id', 'previred apvc employer rules'),
                'apvc_employee_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_apvc_employee_rules_rel', 'previred_conf_id', 'apvc_employee_rule_id', 'previred apvc employee rules'),
                'afp_voluntary_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_afp_voluntary_rules_rel', 'previred_conf_id', 'afp_voluntary_rule_id', 'AFP voluntary rules'),
                'count_2_voluntary_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_count_2_voluntary_rules_rel', 'previred_conf_id', 'count_2_voluntary_rule_id', 'Count 2 voluntary rules'),
                'ips_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ips_rules_rel', 'previred_conf_id', 'ips_rule_id', 'IPS rules'),
                'eviction_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_eviction_rules_rel', 'previred_conf_id', 'eviction_rule_id', 'Eviction rules'),
                'fonasa_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_fonasa_rules_rel', 'previred_conf_id', 'fonasa_rule_id', 'FONASA rules'),
                'isl_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_isl_rules_rel', 'previred_conf_id', 'isl_rule_id', 'ISL rules'),
                #'15386_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_15386_rules_rel', 'previred_conf_id', '15386_rule_id', 'Law 15.386 bonus rules'),
                'isl_family_assigment_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_isl_family_assigment_rules_rel', 'previred_conf_id', 'isl_family_assigment_rule_id', 'ISL family assigment rules'), 
                'compulsory_isapre_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_compulsory_isapre_rules_rel', 'previred_conf_id', 'compulsory_isapre_rule_id', 'Compulsory isapre rules'), 
                'voluntary_isapre_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_voluntary_isapre_rules_rel', 'previred_conf_id', 'voluntary_isapre_rule_id', 'Voluntary isapre rules'), 
                'ges_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ges_rules_rel', 'previred_conf_id', 'ges_rule_id', 'GES rules'), 
                'ccaf_personal_credit_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_personal_credit_rules_rel', 'previred_conf_id', 'ccaf_personal_credit_rule_id', 'CCAF personal credit rules'), 
                'ccaf_dental_disc_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_dental_disc_rules_rel', 'previred_conf_id', 'ccaf_dental_disc_rule_id', 'CCAF dental discount rules'), 
                'ccaf_leasing_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_leasing_rules_rel', 'previred_conf_id', 'ccaf_leasing_rule_id', 'CCAF leasing rules'), 
                'ccaf_life_insurance_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_life_insurance_rules_rel', 'previred_conf_id', 'ccaf_life_insurance_rule_id', 'CCAF life insurance rules'), 
                'ccaf_not_affiliated_quote_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_not_affiliated_quote_rules_rel', 'previred_conf_id', 'ccaf_not_affiliated_quote_rule_id', 'CCAF life insurance rules'), 
                'ccaf_others_disc1_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_others_disc1_rules_rel', 'previred_conf_id', 'others_disc1_rule_id', 'Others discunts 1 rules'), 
                'ccaf_others_disc2_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_ccaf_others_disc2_rules_rel', 'previred_conf_id', 'others_disc2_rule_id', 'Others discunts 2 rules'), 
                'mutual_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_mutual_rules_rel', 'previred_conf_id', 'mutual_rule_id', 'Mutual rules'), 
                'afc_employer_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_afc_employer_rules_rel', 'previred_conf_id', 'afc_employer_rule_id', 'AFC employer rules'), 
                'afc_employee_rule_ids':fields.many2many('hr.salary.rule', 'hr_previred_afc_employee_rules_rel', 'previred_conf_id', 'afc_employee_rule_id', 'AFC employee rules'), 
                
                    } 
    
    _defaults = {  
        'state': 'active',  
        }
hr_previred_config()