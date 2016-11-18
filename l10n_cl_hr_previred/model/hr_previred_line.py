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

class hr_previred_line(osv.osv):
    '''
    Open ERP Model
    '''
    _name = 'hr.previred.line'
    _description = 'hr.previred.line'
 
    _columns = {
            'name':fields.char('name', size=64, ),
            'previred_id':fields.many2one('hr.previred', 'Head'), 
            'rut':fields.integer('RUT'),
            'dv':fields.char('DV',size=1),
            'a_paterno':fields.char('Apellido Paterno',size=30),
            'a_materno':fields.char('Apellido Materno',size=30),
            'nombres':fields.char('Nombres',size=30),
            'sexo':fields.char('Sexo',size=1),
            'nacionalidad':fields.integer('Nacionalidad'),
            'tipo_pago':fields.integer('Tipo Pago'),
            'desde':fields.integer('Periodo Desde'),
            'hasta':fields.integer('Periodo Hasta'),
            'regimen':fields.char('Regimen Previsional',size=3),
            'tipo_trabajador':fields.integer('Tipo Trabajador'),
            'dias_trabajados':fields.integer('Dias Trabajados'),
            'tipo_linea':fields.char('Tipo de Linea',size=2),
            'cod_mov_personal':fields.integer('Codigo Movimiento de Personal'),
            'mov_desde':fields.char('Fecha Desde',size=10),
            'mov_hasta':fields.char('Fecha Hasta',size=10),
            'tramo_asign_fam':fields.char('Tramo Asignacion Familiar',size=1),
            'ncargas_simples':fields.integer('N° Cargas Simples'),
            'ncargas_maternales':fields.integer('N° Cargas Maternales'),
            'ncargas_invalidas':fields.integer('N° Cargas Invalidas'),
            'asign_fam':fields.integer('Asignacion Familiar'),
            'asign_fam_retro':fields.integer('Asignacion Familiar Retroactiva'),
            'reint_cargas_fam':fields.integer('Reintegro Cargas Familiares'),
            'sub_trab_joven':fields.char('Subsidio Trabajador Joven',size=1),
            'codigo_afp':fields.integer('Codigo de la AFP'),
            'imponible_afp':fields.integer('Renta Imponible AFP'),
            'cot_afp':fields.integer('Cotizacion Obligatoria AFP'),
            'cot_sis':fields.integer('Cotizacion Seguro de Invalidez y Sobrevivencia (SIS)'),
            'cuenta_2_afp':fields.integer('Cuenta de Ahorro Voluntario AFP'),
            'imponible_sustit_afp':fields.integer('Renta Imponible Sustitutiva AFP'),
            'tasa_pactada_sustit':fields.float('Tasa Pactada (Sustit.)', digits=(2,2)),
            'aporte_indemn_sustit':fields.integer('Aporte Indemnisatorio Sustit'),
            'n_periodos_sustit':fields.integer('N° Periodos (Sustit.)'),
            'desde_sustit':fields.char('Periodo Desde (Sustit.)',size=10),
            'hasta_sustit':fields.char('Periodo Hasta (Sustit.)',size=10),
            'puesto_trab_pesado':fields.char('Puesto de Trabajo Pesado',size=40),
            'porc_cot_trab_pesado':fields.float('% Cotizacion Trabajo Pesado', digits=(2,2)),
            'cot_trab_pesado':fields.integer('Cotizacion Trabajo Pesado'),
            'cod_inst_apvi':fields.integer('Codigo de la Institucion APVI'),
            'num_de_contrato_apvi':fields.char('Numero de Contrato APVI',size=20),
            'forma_de_pago_apvi':fields.integer('Forma de Pago APVI'),
            'cot_apvi':fields.integer('Cotizacion APVI'),
            'cot_depo_conv':fields.integer('Cotizacion Depositos Convencidos'),
            'cod_inst_apvc':fields.integer('Codigo Institucion Autorizada APVC'),
            'ncontrato_apvc':fields.char('Numero de Contrato APVC',size=20),
            'forma_pago_apvc':fields.integer('Forma de Pago APVC'),
            'cot_trab_apvc':fields.integer('Cotizacion Trabajador APVC'),
            'cot_empl_apvc':fields.integer('Cotizacion Empleador APVC'),
            'rut_af_voluntario':fields.integer('RUT Afiliado Voluntario'),
            'dv_af_voluntario':fields.char('DV Afiliado Voluntario',size=1),
            'vol_a_paterno':fields.char('Apellido Paterno',size=30),
            'vol_a_materno':fields.char('Apellido Materno',size=30),
            'vol_nombres':fields.char('Nombres',size=30),
            'cod_mov_personal':fields.integer('Codigo Movimiento de Personal'),
            'cod_mov_per_desde':fields.char('Fecha Desde',size=10),
            'cod_mov_per_hasta':fields.char('Fecha Hasta',size=10),
            'cod_afp':fields.integer('Codigo de la AFP'),
            'monto_cap_vol':fields.integer('Monto Capitalizacion Voluntaria'),
            'monto_ahorro_vol':fields.integer('Monto Ahorro Voluntario'),
            'nperiodos_de_cotizacion':fields.integer('Numero de periodos de cotizacion'),
            'cod_excaja_regimen':fields.integer('Codigo Ex-Caja Regimen'),
            'tasa_cot_excajas_prevision':fields.float('Tasa Cotizacion Ex-Cajas de Prevision', digits=(2,2)),
            'imponible_ips':fields.integer('Renta Imponible IPS'),
            'cot_obl_ips':fields.integer('Cotizacion Obligatoria IPS'),
            'imponible_desahucio':fields.integer('Renta Imponible Desahucio'),
            'cod_excaja_regimen_desahucio':fields.integer('Codigo Ex-Caja Regimen Desahucio'),
            'tasa_cot_desahucio_excajas_prevision':fields.float('Tasa Cotizacion Desahucio Ex-Cajas de Prevision', digits=(2,2)),
            'cot_desahucio':fields.integer('Cotizacion Desahucio'),
            'cot_fonasa':fields.integer('Cotizacion Fonasa'),
            'cot_acc_trab_isl':fields.integer('Cotizacion Acc. Trabajo (ISL)'),
            'bono_ley':fields.integer('Bonificacion Ley 15.386'),
            'desc_cargas_fam_isl':fields.integer('Descuento por cargas familiares (ISL)'),
            'bono_gobierno':fields.integer('Bonos de Gobierno'),
            'cod_inst_salud':fields.integer('Codigo Institucion de Salud'),
            'num_fun':fields.char('Numero de FUN',size=16),
            'imponible_isapre':fields.integer('Renta Imponible Isapre'),
            'moneda_plan_isapre':fields.integer('Moneda del plan pactado Isapre'),
            'cot_pactada':fields.integer('Cotizacion Pactada'),
            'cot_obligatoria_isapre':fields.integer('Cotizacion Obligatoria Isapre'),
            'cot_adicional_voluntaria':fields.integer('Cotizacion Adicional Voluntaria'),
            'ges':fields.integer('Monto GES (Futuro)'),
            'cod_ccaf':fields.integer('Codigo CCAF'),
            'imponible_ccaf':fields.integer('Renta Imponible CCAF'),
            'cred_pers_ccaf':fields.integer('Creditos Personales CCAF'),
            'desc_dental_ccaf':fields.integer('Descuento Dental CCAF'),
            'desc_leasing':fields.integer('Descuentos por Leasing (Programa de Ahorro)'),
            'desc_seg_vida_ccaf':fields.integer('Descuentos por seguro de vida CCAF'),
            'otros_desc_ccaf':fields.integer('Otros descuentos CCAF'),
            'ccaf_no_afil_isapres':fields.integer('Cotizacion a CCAF de no afiliados a Isapres'),
            'cargas_fam_ccaf':fields.integer('Descuento Cargas Familiares CCAF'),
            'otros_desc_ccaf_1':fields.integer('Otros descuentos CCAF 1 (Futuro)'),
            'otros_desc_ccaf_2':fields.integer('Otros descuentos CCAF 2 (Futuro)'),
            'bonos_gobierno':fields.integer('Bonos Gobierno (Futuro)'),
            'codigo_de_suc':fields.char('Codigo de Sucursal (Futuro)',size=20),
            'cod_mutual':fields.integer('Codigo Mutualidad'),
            'imponible_mutual':fields.integer('Renta Imponible Mutual'),
            'cot_mutual':fields.integer('Cotizacion Accidente del Trabajo (MUTUAL)'),
            'suc_pago_mutual':fields.integer('Sucursal para pago Mutual'),
            'imponible_seg_ces':fields.integer('Renta Imponible Seguro Cesantia (Informar Renta Total Imponible)'),
            'trab_seg_ces':fields.integer('Aporte Trabajador Seguro Cesantia'),
            'empl_seg_ces':fields.integer('Aporte Empleador Seguro Cesantia'),
            'rut_pagadora_subsidio':fields.integer('Rut Pagadora Subsidio'),
            'dv_pagadora_subsidio':fields.char('DV Pagadora Subsidio',size=1),
            'centro_de_costos':fields.char('Centro de Costos, Sucursal, Agencia, Obra, Region',size=20),
}

hr_previred_line()