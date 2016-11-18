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


import base64
import cStringIO
import csv
from osv import osv
from osv import fields
from openerp.tools.misc import get_iso_codes
from datetime import datetime, timedelta
import re

class hr_previred_export(osv.osv):
    
    _col_def_file={
                1:{'campo':'rut','tipo':'9 (11)','largo':11,'inicio':1,'fin':11,'valor':0},    2:{'campo':'dv','tipo':'X (1)','largo':1,'inicio':12,'fin':12,'valor':0},    3:{'campo':'a_paterno','tipo':'X (30)','largo':30,'inicio':13,'fin':42,'valor':0},    4:{'campo':'a_materno','tipo':'X (30)','largo':30,'inicio':43,'fin':72,'valor':0},    5:{'campo':'nombres','tipo':'X (30)','largo':30,'inicio':73,'fin':102,'valor':0},    6:{'campo':'sexo','tipo':'X (1)','largo':1,'inicio':103,'fin':103,'valor':0},    7:{'campo':'nacionalidad','tipo':'9 (1)','largo':1,'inicio':104,'fin':104,'valor':0},    8:{'campo':'tipo_pago','tipo':'9 (2)','largo':2,'inicio':105,'fin':106,'valor':0},    9:{'campo':'desde','tipo':'9 (6)','largo':6,'inicio':107,'fin':112,'valor':0},    10:{'campo':'hasta','tipo':'9 (6)','largo':6,'inicio':113,'fin':118,'valor':0},                    
                11:{'campo':'regimen','tipo':'X (3)','largo':3,'inicio':119,'fin':121,'valor':0},    12:{'campo':'tipo_trabajador','tipo':'9 (1)','largo':1,'inicio':122,'fin':122,'valor':0},    13:{'campo':'dias_trabajados','tipo':'9 (2)','largo':2,'inicio':123,'fin':124,'valor':0},    14:{'campo':'tipo_linea','tipo':'X (2)','largo':2,'inicio':125,'fin':126,'valor':0},    15:{'campo':'cod_mov_personal','tipo':'9 (2)','largo':2,'inicio':127,'fin':128,'valor':0},    16:{'campo':'mov_desde','tipo':'X (10)','largo':10,'inicio':129,'fin':138,'valor':0},    17:{'campo':'mov_hasta','tipo':'X (10)','largo':10,'inicio':139,'fin':148,'valor':0},    18:{'campo':'tramo_asign_fam','tipo':'X (1)','largo':1,'inicio':149,'fin':149,'valor':0},    19:{'campo':'ncargas_simples','tipo':'9 (2)','largo':2,'inicio':150,'fin':151,'valor':0},    20:{'campo':'ncargas_maternales','tipo':'9 (1)','largo':1,'inicio':152,'fin':152,'valor':0},                    
                21:{'campo':'ncargas_invalidas','tipo':'9 (1)','largo':1,'inicio':153,'fin':153,'valor':0},    22:{'campo':'asign_fam','tipo':'9 (6)','largo':6,'inicio':154,'fin':159,'valor':0},    23:{'campo':'asign_fam_retro','tipo':'9 (6)','largo':6,'inicio':160,'fin':165,'valor':0},    24:{'campo':'reint_cargas_fam','tipo':'9 (6)','largo':6,'inicio':166,'fin':171,'valor':0},    25:{'campo':'sub_trab_joven','tipo':'X (1)','largo':1,'inicio':172,'fin':172,'valor':0},    26:{'campo':'codigo_afp','tipo':'9 (2)','largo':2,'inicio':173,'fin':174,'valor':0},    27:{'campo':'imponible_afp','tipo':'9 (8)','largo':8,'inicio':175,'fin':182,'valor':0},    28:{'campo':'cot_afp','tipo':'9 (8)','largo':8,'inicio':183,'fin':190,'valor':0},    29:{'campo':'cot_sis','tipo':'9 (8)','largo':8,'inicio':191,'fin':198,'valor':0},    30:{'campo':'cuenta_2_afp','tipo':'9 (8)','largo':8,'inicio':199,'fin':206,'valor':0},                    
                31:{'campo':'imponible_sustit_afp','tipo':'9 (8)','largo':8,'inicio':207,'fin':214,'valor':0},    32:{'campo':'tasa_pactada_sustit','tipo':'99,99 (5)','largo':5,'inicio':215,'fin':219,'valor':0},    33:{'campo':'aporte_indemn_sustit','tipo':'9 (9)','largo':9,'inicio':220,'fin':228,'valor':0},    34:{'campo':'n_periodos_sustit','tipo':'9 (2)','largo':2,'inicio':229,'fin':230,'valor':0},    35:{'campo':'desde_sustit','tipo':'X (10)','largo':10,'inicio':231,'fin':240,'valor':0},    36:{'campo':'hasta_sustit','tipo':'X (10)','largo':10,'inicio':241,'fin':250,'valor':0},    37:{'campo':'puesto_trab_pesado','tipo':'X (40)','largo':40,'inicio':251,'fin':290,'valor':0},    38:{'campo':'porc_cot_trab_pesado','tipo':'99,99 (5)','largo':5,'inicio':291,'fin':295,'valor':0},    39:{'campo':'cot_trab_pesado','tipo':'9 (6)','largo':6,'inicio':296,'fin':301,'valor':0},    40:{'campo':'cod_inst_apvi','tipo':'9 (3)','largo':3,'inicio':302,'fin':304,'valor':0},                    
                41:{'campo':'num_de_contrato_apvi','tipo':'X (20)','largo':20,'inicio':305,'fin':324,'valor':0},    42:{'campo':'forma_de_pago_apvi','tipo':'9 (1)','largo':1,'inicio':325,'fin':325,'valor':0},    43:{'campo':'cot_apvi','tipo':'9 (8)','largo':8,'inicio':326,'fin':333,'valor':0},    44:{'campo':'cot_depo_conv','tipo':'9 (8)','largo':8,'inicio':334,'fin':341,'valor':0},    45:{'campo':'cod_inst_apvc','tipo':'9 (3)','largo':3,'inicio':342,'fin':344,'valor':0},    46:{'campo':'ncontrato_apvc','tipo':'X (20)','largo':20,'inicio':345,'fin':364,'valor':0},    47:{'campo':'forma_pago_apvc','tipo':'9 (1)','largo':1,'inicio':365,'fin':365,'valor':0},    48:{'campo':'cot_trab_apvc','tipo':'9 (8)','largo':8,'inicio':366,'fin':373,'valor':0},    49:{'campo':'cot_empl_apvc','tipo':'9 (8)','largo':8,'inicio':374,'fin':381,'valor':0},    50:{'campo':'rut_af_voluntario','tipo':'9 (11)','largo':11,'inicio':382,'fin':392,'valor':0},                    
                51:{'campo':'dv_af_voluntario','tipo':'X (1)','largo':1,'inicio':393,'fin':393,'valor':0},    52:{'campo':'vol_a_paterno','tipo':'X (30)','largo':30,'inicio':394,'fin':423,'valor':0},    53:{'campo':'vol_a_materno','tipo':'X (30)','largo':30,'inicio':424,'fin':453,'valor':0},    54:{'campo':'vol_nombres','tipo':'X (30)','largo':30,'inicio':454,'fin':483,'valor':0},    55:{'campo':'cod_mov_personal','tipo':'9 (2)','largo':2,'inicio':484,'fin':485,'valor':0},    56:{'campo':'cod_mov_per_desde','tipo':'X (10)','largo':10,'inicio':486,'fin':495,'valor':0},    57:{'campo':'cod_mov_per_hasta','tipo':'X (10)','largo':10,'inicio':496,'fin':505,'valor':0},    58:{'campo':'cod_afp','tipo':'9 (2)','largo':2,'inicio':506,'fin':507,'valor':0},    59:{'campo':'monto_cap_vol','tipo':'9 (8)','largo':8,'inicio':508,'fin':515,'valor':0},    60:{'campo':'monto_ahorro_vol','tipo':'9 (8)','largo':8,'inicio':516,'fin':523,'valor':0},                    
                61:{'campo':'nperiodos_de_cotizacion','tipo':'9 (2)','largo':2,'inicio':524,'fin':525,'valor':0},    62:{'campo':'cod_excaja_regimen','tipo':'9 (4)','largo':4,'inicio':526,'fin':529,'valor':0},    63:{'campo':'tasa_cot_excajas_prevision','tipo':'99,99 (5)','largo':5,'inicio':530,'fin':534,'valor':0},    64:{'campo':'imponible_ips','tipo':'9 (8)','largo':8,'inicio':535,'fin':542,'valor':0},    65:{'campo':'cot_obl_ips','tipo':'9 (8)','largo':8,'inicio':543,'fin':550,'valor':0},    66:{'campo':'imponible_desahucio','tipo':'9 (8)','largo':8,'inicio':551,'fin':558,'valor':0},    67:{'campo':'cod_excaja_regimen_desahucio','tipo':'9 (4)','largo':4,'inicio':559,'fin':562,'valor':0},    68:{'campo':'tasa_cot_desahucio_excajas_prevision','tipo':'99,99 (5)','largo':5,'inicio':563,'fin':567,'valor':0},    69:{'campo':'cot_desahucio','tipo':'9 (8)','largo':8,'inicio':568,'fin':575,'valor':0},    70:{'campo':'cot_fonasa','tipo':'9 (8)','largo':8,'inicio':576,'fin':583,'valor':0},                    
                71:{'campo':'cot_acc_trab_isl','tipo':'9 (8)','largo':8,'inicio':584,'fin':591,'valor':0},    72:{'campo':'bono_ley','tipo':'9 (8)','largo':8,'inicio':592,'fin':599,'valor':0},    73:{'campo':'desc_cargas_fam_isl','tipo':'9 (8)','largo':8,'inicio':600,'fin':607,'valor':0},    74:{'campo':'bono_gobierno','tipo':'9 (8)','largo':8,'inicio':608,'fin':615,'valor':0},    75:{'campo':'cod_inst_salud','tipo':'9 (2)','largo':2,'inicio':616,'fin':617,'valor':0},    76:{'campo':'num_fun','tipo':'X (16)','largo':16,'inicio':618,'fin':633,'valor':0},    77:{'campo':'imponible_isapre','tipo':'9 (8)','largo':8,'inicio':634,'fin':641,'valor':0},    78:{'campo':'moneda_plan_isapre','tipo':'9 (1)','largo':1,'inicio':642,'fin':642,'valor':0},    79:{'campo':'cot_pactada','tipo':'9 (8)','largo':8,'inicio':643,'fin':650,'valor':0},    80:{'campo':'cot_obligatoria_isapre','tipo':'9 (8)','largo':8,'inicio':651,'fin':658,'valor':0},                    
                81:{'campo':'cot_adicional_voluntaria','tipo':'9 (8)','largo':8,'inicio':659,'fin':666,'valor':0},    82:{'campo':'ges','tipo':'9 (8)','largo':8,'inicio':667,'fin':674,'valor':0},    83:{'campo':'cod_ccaf','tipo':'9 (2)','largo':2,'inicio':675,'fin':676,'valor':0},    84:{'campo':'imponible_ccaf','tipo':'9 (8)','largo':8,'inicio':677,'fin':684,'valor':0},    85:{'campo':'cred_pers_ccaf','tipo':'9 (8)','largo':8,'inicio':685,'fin':692,'valor':0},    86:{'campo':'desc_dental_ccaf','tipo':'9 (8)','largo':8,'inicio':693,'fin':700,'valor':0},    87:{'campo':'desc_leasing','tipo':'9 (8)','largo':8,'inicio':701,'fin':708,'valor':0},    88:{'campo':'desc_seg_vida_ccaf','tipo':'9 (8)','largo':8,'inicio':709,'fin':716,'valor':0},    89:{'campo':'otros_desc_ccaf','tipo':'9 (8)','largo':8,'inicio':717,'fin':724,'valor':0},    90:{'campo':'ccaf_no_afil_isapres','tipo':'9 (8)','largo':8,'inicio':725,'fin':732,'valor':0},                    
                91:{'campo':'cargas_fam_ccaf','tipo':'9 (8)','largo':8,'inicio':733,'fin':740,'valor':0},    92:{'campo':'otros_desc_ccaf_1','tipo':'9 (8)','largo':8,'inicio':741,'fin':748,'valor':0},    93:{'campo':'otros_desc_ccaf_2','tipo':'9 (8)','largo':8,'inicio':749,'fin':756,'valor':0},    94:{'campo':'bonos_gobierno','tipo':'9 (8)','largo':8,'inicio':757,'fin':764,'valor':0},    95:{'campo':'codigo_de_suc','tipo':'X (20)','largo':20,'inicio':765,'fin':784,'valor':0},    96:{'campo':'cod_mutual','tipo':'9 (2)','largo':2,'inicio':785,'fin':786,'valor':0},    97:{'campo':'imponible_mutual','tipo':'9 (8)','largo':8,'inicio':787,'fin':794,'valor':0},    98:{'campo':'cot_mutual','tipo':'9 (8)','largo':8,'inicio':795,'fin':802,'valor':0},    99:{'campo':'suc_pago_mutual','tipo':'9 (3)','largo':3,'inicio':803,'fin':805,'valor':0},    100:{'campo':'imponible_seg_ces','tipo':'9 (8)','largo':8,'inicio':806,'fin':813,'valor':0},                    
                101:{'campo':'trab_seg_ces','tipo':'9 (8)','largo':8,'inicio':814,'fin':821,'valor':0},    102:{'campo':'empl_seg_ces','tipo':'9 (8)','largo':8,'inicio':822,'fin':829,'valor':0},    103:{'campo':'rut_pagadora_subsidio','tipo':'9 (11)','largo':11,'inicio':830,'fin':840,'valor':0},    104:{'campo':'dv_pagadora_subsidio','tipo':'X (1)','largo':1,'inicio':841,'fin':841,'valor':0},    105:{'campo':'centro_de_costos','tipo':'X (20)','largo':20,'inicio':842,'fin':861,'valor':0},                                        
              }
    
    
    
    
    
    '''
    Open ERP Model
    '''
    _name = 'hr.previred.export'
    _description = 'hr.previred.export'
 
    _columns = {
            'name':fields.char('filename', size=64, required=False, readonly=False),
            'format': fields.selection([
                                        ('csv','CSV File'),
                                        ], 'File Format', required=True),
            'data': fields.binary('File', readonly=True),
            'state': fields.selection([('choose', 'choose'),   # choose language
                                       ('get', 'get')]),        # get the file
            'when':fields.selection([
                ('group','Group of payslip'),
                ('alone','Only one payslip'),
                 ],    'State', select=True),
            'payslip_run_id':fields.many2one('hr.payslip.run', 'payslip run', required=False), 
            'payslip_id':fields.many2one('hr.payslip', 'payslip', required=False), 
        }
    
    _defaults = { 
        'state': 'choose',
        'name': 'previred',#poner fecha tambien
        'format': 'csv',
        }
    
    def act_getfile(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids)[0]
        #lang = this.lang if this.lang != NEW_LANG_KEY else False
        #mods = map(lambda m: m.name, this.modules) or ['all']
        #mods.sort()
        exp = self.browse(cr, uid, ids)[0]
        buf = cStringIO.StringIO()
        #tools.trans_export(lang, mods, buf, this.format, cr)
        self.generate_file_export(cr, uid, ids,buf,exp.payslip_id, context)
        filename = 'new'
        #if lang:
        #    filename = get_iso_codes(lang)
        #elif len(mods) == 1:
        #    filename = mods[0]
        this.name = "%s.%s" % (filename, this.format)
        out = base64.encodestring(buf.getvalue())
        buf.close()
        self.write(cr, uid, ids, {'state': 'get',
                                  'data': out,
                                  'name':this.name}, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.previred.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
        
    def generate_file_export(self, cr, uid, ids,buf,payslip_id, context=None):
 
        ltemp = {}#self._col_def_file

        prev_conf_obj = self.pool.get('hr.previred.config')
        prev_conf_act = prev_conf_obj.browse(cr,uid,prev_conf_obj.search(cr,uid,[('state','=','active')]))[0]
        contract_obj = payslip_id.contract_id
        company_obj = contract_obj.company_id
        employee_obj = contract_obj.employee_id
        partner_obj = employee_obj.address_home_id
        imponible = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.taxable_rule_ids)
        imponible = imponible[0].total if imponible else 0
        
        #descuentos voluntarios previsionales
        apvi = [item for item in employee_obj.pension_vol_disc_ids if item.type =="apvi"]
        apvc = [item for item in employee_obj.pension_vol_disc_ids if item.type =="apvc"]
        count_2 = [item for item in employee_obj.pension_vol_disc_ids if item.type =="count2"]
        agreed_deposit = [item for item in employee_obj.pension_vol_disc_ids if item.type =="agreed_deposit"]
        
        #rut
        #positions = map(lambda x: {x.split(' ')[0]:x.split(' ')[1]} ,prev_conf_act.positions.split(';'))
        rut=partner_obj.vat
        dv=""
        if rut:
            dv = rut[len(rut)-1:len(rut)]
            rut = rut[2:len(rut)-1]
        
        ltemp['rut'] = rut
        ltemp['dv'] = dv
        lnombre = self.split_name(cr,uid,employee_obj.name)
        
        ltemp['a_paterno']=lnombre['a_paterno']
        ltemp['a_materno']=lnombre['a_materno']
        ltemp['nombres']=lnombre['nombres']
    
        ltemp['sexo'] = str(employee_obj.gender).upper()[0] if employee_obj.gender else ' '
        ltemp['nacionalidad'] = 0 if employee_obj.country_id.code=="CL" and employee_obj.country_id else 1
        
        # FIXME: tipo de pago por defecto normal pero debe ser dinamizado para cumplir con el estandar previred
        ltemp['tipo_pago']="01"
        
        #periodo de remuneracion
        dfrom=datetime.strptime(payslip_id.date_from, "%Y-%m-%d")
        dto=datetime.strptime(payslip_id.date_to, "%Y-%m-%d")
        
        ltemp['desde']=datetime.strftime(dfrom, '%m%Y')
        ltemp['hasta']=datetime.strftime(dto, '%m%Y')
        
        #regimen previsional y tipo trabajador
        ltemp['regimen'] = employee_obj.pension_scheme
        ltemp['tipo_trabajador'] = employee_obj.type
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.worked_days_rule_ids)
        ltemp['dias_trabajados'] = val[0].total if val else 0
        #tipo de linea y mov de personal
        # FIXME: el tipo de linea queda como normal para efectos de prueba pero debe ser dinamico
        # FIXME: el tipo de movimiento tambien queda fijo para efectos de pruebas y las fechas tambien
        
        ltemp['tipo_linea']='00'
        ltemp['cod_mov_personal']=0
        ltemp['mov_desde']=datetime.strftime(dfrom, '%d-%m-%Y') #if mov_tipo>0 else '00-00-0000'
        ltemp['mov_hasta']=datetime.strftime(dto, '%d-%m-%Y') #if mov_tipo>0 else '00-00-0000'
        
        
        #Deberes familiares
        ltemp['tramo_asign_fam'] = employee_obj.stretch
        ltemp['ncargas_simples'] = sum([1 if carga.type=="simple" else 0 for carga in employee_obj.family_responsibilities_ids]) 
        ltemp['ncargas_maternales'] = sum([1 if carga.type=="maternal" else 0 for carga in employee_obj.family_responsibilities_ids]) 
        ltemp['ncargas_invalidas'] = sum([1 if carga.type=="invalid" else 0 for carga in employee_obj.family_responsibilities_ids])
        
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.family_assigment_rule_ids)
        ltemp['asign_fam'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.family_assigment_retro_rule_ids)
        ltemp['asign_fam_retro'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.family_reassigment_rule_ids)
        ltemp['reint_cargas_fam'] = val[0].total if val else 0
        ltemp['sub_trab_joven'] = 'S' if contract_obj.young_worker_grant else 'N'     
        
        #Datos AFP
        ltemp['codigo_afp'] = employee_obj.security_institutions_id.code 
        ltemp['imponible_afp'] = imponible
        
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.afp_rule_ids)
        ltemp['cot_afp'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.sis_rule_ids)
        ltemp['cot_sis'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.count_2_rule_ids)
        ltemp['cuenta_2_afp'] = val[0].total if val else 0
        
        #FIXME:Datos indemnizacion sustitutiva del aviso previo
        #informacion adicional en 
        # - http://www.safp.cl/compendio/m/586/w3-propertyvalue-3587.html
        # - http://www.leychile.cl/Navegar?idNorma=30378
        
        #FIXME: no se abordan en esta version por lo que se dejan en blanco
        ltemp['imponible_sustit_afp'] = 0
        ltemp['tasa_pactada_sustit'] = 0.0
        ltemp['aporte_indemn_sustit'] = 0
        ltemp['n_periodos_sustit'] = 0
        ltemp['desde_sustit'] = '00-00-0000'
        ltemp['hasta_sustit'] = '00-00-0000'
        
        
        #datos trabajo pesado.
        
        ltemp['puesto_trab_pesado']=contract_obj.job_id.name if contract_obj.job_id.heavy_duty else ""
        ltemp['porc_cot_trab_pesado'] = contract_obj.job_id.heavy_duty_quote if contract_obj.job_id.heavy_duty else 0.0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.drudgery_rule_ids)
        ltemp['cot_trab_pesado'] = val[0].total if val else 0
        
        
        # APVI ex APV
        
        if len(apvi)>0:
            ltemp['cod_inst_apvi'] = apvi[0].security_institution_id.code
            ltemp['num_de_contrato_apvi'] = apvi[0].contract_number or ""
            ltemp['forma_de_pago_apvi'] = apvi[0].type_payment
            val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.apvi_rule_ids)
            ltemp['cot_apvi'] = val[0].total if val else 0
        
        if len(agreed_deposit)>0:
            val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.agreed_deposits_rule_ids)
            ltemp['cot_depo_conv'] = val[0].total if val else 0
        if len(apvc)>0:
            ltemp['cod_inst_apvc'] = apvc[0].security_institution_id.code
            ltemp['ncontrato_apvc'] = apvc[0].contract_number
            ltemp['forma_pago_apvc'] = apvc[0].type_payment
            val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.apvc_employee_rule_ids)
            ltemp['cot_trab_apvc'] = val[0].total if val else 0
            val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.apvc_employer_rule_ids)
            ltemp['cot_empl_apvc'] = val[0].total if val else 0
  
        rut=employee_obj.affiliate_volunteer_id.vat
        dv=""
        if rut:
            dv = rut[len(rut)-1:len(rut)]
            rut = rut[2:len(rut)-1]
          
        ltemp['rut_af_voluntario'] = rut
        ltemp['dv_af_voluntario'] = dv
        
        lnombre = self.split_name(cr,uid,employee_obj.affiliate_volunteer_id.name)  
        
        ltemp['vol_a_paterno'] =lnombre['a_paterno']
        ltemp['vol_a_materno'] =lnombre['a_materno']
        ltemp['vol_nombres'] =lnombre['nombres']
        ltemp['cod_mov_personal'] = 0
        ltemp['cod_mov_per_desde'] = datetime.strftime(dfrom, '%d-%m-%Y') #if mov_tipo>0 else '00-00-0000'
        ltemp['cod_mov_per_hasta'] = datetime.strftime(dto  , '%d-%m-%Y')
        ltemp['cod_afp'] = employee_obj.security_institutions_id.code 
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.afp_voluntary_rule_ids)
        ltemp['monto_cap_vol'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.count_2_voluntary_rule_ids)
        ltemp['monto_ahorro_vol'] = val[0].total if val else 0
        ltemp['nperiodos_de_cotizacion'] = 0
        ltemp['cod_excaja_regimen'] = employee_obj.security_institutions_id.code if employee_obj.pension_scheme == "IPS" else 0
        ltemp['tasa_cot_excajas_prevision'] = employee_obj.ex_regime_rate if employee_obj.pension_scheme == "IPS" else 0.0
        ltemp['imponible_ips'] = imponible if employee_obj.pension_scheme == "IPS" else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.ips_rule_ids)
        ltemp['cot_obl_ips'] = val[0].total if val else 0
        
        
        ltemp['imponible_desahucio'] = imponible if employee_obj.pension_scheme == "IPS" and employee_obj.security_institutions_id.type == "empart" else 0
        
        ltemp['cod_excaja_regimen_desahucio'] = employee_obj.security_institutions_id.code if employee_obj.pension_scheme == "IPS" and employee_obj.security_institutions_id.type == "empart" else 0
        ltemp['tasa_cot_desahucio_excajas_prevision'] = employee_obj.security_institutions_id.eviction_rate if employee_obj.pension_scheme == "IPS" and employee_obj.security_institutions_id.type == "empart" else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.eviction_rule_ids)
        ltemp['cot_desahucio'] = val[0].total if employee_obj.pension_scheme == "IPS" and employee_obj.security_institutions_id.type == "empart" else 0
        
        #fonasa si 
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.fonasa_rule_ids)
        ltemp['cot_fonasa'] = val[0].total if val and int(employee_obj.health_institutions_ids.code) == 7 else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.isl_rule_ids)
        ltemp['cot_acc_trab_isl'] = val[0].total if val and not company_obj.mutual_id else 0
        
        #bono ley 15386 
        #http://www.chileatiende.cl/fichas/ver/5323
        #http://www.leychile.cl/Navegar?idNorma=28172
        ltemp['bono_ley'] = 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.isl_family_assigment_rule_ids)
        ltemp['desc_cargas_fam_isl'] =  val[0].total if val and not company_obj.ccaf_id else 0
        ltemp['bono_gobierno'] = 0
        
        #si cotiza en isapre
        ltemp['cod_inst_salud'] = employee_obj.health_institutions_ids.code
        ltemp['num_fun'] = employee_obj.FUN or ""
        ltemp['imponible_isapre'] = imponible
        
        val = 0
        if employee_obj.agreed_quote_currency.name == 'CLP':
            val=1
        elif employee_obj.agreed_quote_currency.name == 'UF':
            val=2
        ltemp['moneda_plan_isapre'] = val
        ltemp['cot_pactada'] = employee_obj.agreed_quote
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.compulsory_isapre_rule_ids)
        ltemp['cot_obligatoria_isapre'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.voluntary_isapre_rule_ids)
        ltemp['cot_adicional_voluntaria'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.ges_rule_ids)
        ltemp['ges'] = val[0].total if val else 0
        ltemp['cod_ccaf'] = company_obj.ccaf_id.code or 0
        ltemp['imponible_ccaf'] = imponible if company_obj.ccaf_id else 0
        ltemp['cred_pers_ccaf'] = 0
        ltemp['desc_dental_ccaf'] = 0
        ltemp['desc_leasing'] = 0
        ltemp['desc_seg_vida_ccaf'] = 0
        ltemp['otros_desc_ccaf'] =  0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.ccaf_not_affiliated_quote_rule_ids)
        ltemp['ccaf_no_afil_isapres'] = val[0].total if val else 0
        ltemp['cargas_fam_ccaf'] = ltemp['asign_fam']+ltemp['asign_fam_retro']-ltemp['reint_cargas_fam'] if company_obj.ccaf_id else 0
        ltemp['otros_desc_ccaf_1'] = 0
        ltemp['otros_desc_ccaf_2'] = 0
        ltemp['bonos_gobierno'] = 0
        ltemp['codigo_de_suc'] = 0
        ltemp['cod_mutual'] = company_obj.mutual_id.code
        ltemp['imponible_mutual'] = imponible
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.ccaf_not_affiliated_quote_rule_ids)
        ltemp['cot_mutual'] = val[0].total if val else 0
        ltemp['suc_pago_mutual'] = 0
        ltemp['imponible_seg_ces'] = imponible
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.afc_employee_rule_ids)
        ltemp['trab_seg_ces'] = val[0].total if val else 0
        val = self.get_payslip_line(cr, uid, ids,payslip_id,prev_conf_act.afc_employer_rule_ids)
        ltemp['empl_seg_ces'] = val[0].total if val else 0
        
        rut=employee_obj.health_institutions_ids.vat
        dv=""
        if rut:
            dv = rut[len(rut)-1:len(rut)]
            rut = rut[2:len(rut)-1]
        ltemp['rut_pagadora_subsidio'] = rut
        ltemp['dv_pagadora_subsidio'] = dv
        ltemp['centro_de_costos'] = 1

        ltemp['previred_id'] = ids[0]
        
        masterline = self._col_def_file
        
        for item in masterline.values():
            try:
                item['valor'] = ltemp[item['campo']] if item['campo'] in ltemp else 0
            except (RuntimeError, TypeError, NameError):
                break
        
        line = ""
        for i in range(105):
            i+=1
            print i
            tipo = masterline[i]['tipo'].split(' ')[0]
            line += self.parse_value(masterline[i]['valor'],masterline[i]['largo'],tipo)
        
        line +='\n'
        
        
        
        
        
        
        return 
    
    def parse_value(self,value,lenght,val_type):
        print value,lenght,val_type
        res = ""
        spam = [None,' ']
        if val_type=='9':
            value = int(float(value) if value not in spam else 0)
            res = str(value).rjust(lenght).replace(' ', '0')
        elif val_type=='X':
            value = str(value) if type(value) in [int,float] else value.decode('utf8') if value != None else ''
            if value=='0': value=''
            res = str(value).ljust(lenght)# if value != None else ''
        elif val_type=='99,99':
            res = "{:2.2f}".format(value).rjust(lenght).replace('.',',').replace(' ', '0')
        else:
            res = value.ljust(lenght)
        return res
        
    def get_payslip_line(self,cr,uid,ids,payslip, previred_rule):
        rule_ids = [rule.id for rule in previred_rule]
        
        payslip_lines=[line for line in payslip.line_ids if line.salary_rule_id.id in rule_ids]     
        
        return payslip_lines if len(payslip_lines)>0 else False
        
    def split_name(self, cr, uid, name):
        def replace_chars(match):
            char = match.group(0)
            return chars[char]
        
        lres = {'a_paterno':'','a_materno':'','nombres':''}

        if name == None: return lres
        
        chars = {
                '\xc3\x81' : 'A','\xc3\x89' : 'E','\xc3\x8d' : 'I','\xc3\x93' : 'O','\xc3\x9a' : 'U',
                '\xc3\xa1' : 'a','\xc3\xa9' : 'e','\xc3\xad' : 'i','\xc3\xb3' : 'o','\xc3\xba' : 'u',
        }
        name = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, name.encode('utf-8'))
        lnombre= name.split(' ') 
        
        if len(lnombre)==4:
            lres['a_paterno']=lnombre[2].upper()
            lres['a_materno']=lnombre[3].upper()
            lres['nombres']=(lnombre[0]+' '+lnombre[1]).upper()
        elif len(lnombre)==3:
            lres['a_paterno']=lnombre[1].upper()
            lres['a_materno']=lnombre[2].upper()
            lres['nombres']=lnombre[0].upper()
        elif len(lnombre)==2:
            lres['a_paterno']=lnombre[1].upper()
            lres['nombres']=lnombre[0].upper()
        elif len(lnombre)==1:
            lres['nombres']=lnombre[0].upper()
        return lres
    
hr_previred_export()