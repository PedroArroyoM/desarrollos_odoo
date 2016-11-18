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
import xmlrpclib
import pwd
from OERP_xmlrpc_client.OpenERPClient import OpenERPClient
from OERP_xmlrpc_client.OpenERPObject import OpenERPObject


class migrate_params(osv.osv):
    '''
    Open ERP Model
    '''
    _name = 'migrate.params'
    _description = 'migrate.params'
 
    _columns = {
            'name':fields.char('url Servidor openerp', size=64, required=False, readonly=False),
            'bbdd':fields.char('Base de datos', size=64, required=False, readonly=False),
            'user':fields.char('Usuario', size=64, required=False, readonly=False),
            'pwd':fields.char('pass', size=64, required=False, readonly=False),
            'parity_ids':fields.one2many("migrate.parity","migrate_params_id","Parity Objects"),
        }
    def act_initial_configuration(self, cr, uid, ids, context):
        migrate = self.pool.get('migrate.migrate')
        params_obj = self.browse(cr,uid,ids,context)[0]
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name 
        #migrate.testcrud(cr, uid, ids,params_obj, context)
        #migrate.migradocumentos(cr, uid, ids,params_obj, context)
        migrate.migrate_initial_config(cr, uid, ids,params_obj, context)
        
    def act_pos_movement(self, cr, uid, ids, context):
        migrate = self.pool.get('migrate.migrate')
        params_obj = self.browse(cr,uid,ids,context)[0]
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name 
        #migrate.testcrud(cr, uid, ids,params_obj, context)
        #migrate.migradocumentos(cr, uid, ids,params_obj, context)
        migrate.migrate_pos_movement(cr, uid, ids,params_obj, context)
migrate_params()

class migrate_parity(osv.osv):
    
    _name = "migrate.parity"
    _columns={
            'name':fields.char('name'),
            'model':fields.char('model' ),
            'migrated_id':fields.integer('Migrated id'),
            'current_id':fields.integer('Current id'),
            'migrate_params_id':fields.many2one('migrate.params', 'Migrate params'),
             }
    
    def get_parity_id(self,cr,uid,migrated_id,object, context):
        
        id = self.search(cr, uid, [('migrated_id','=',migrated_id),('model','=',object)])
        id = self.read(cr, uid, id, ['current_id'])
        return id[0]['current_id'] if id  else None
    
migrate_parity()  
    
    

class migrate_migrate(osv.osv):
    
    _name = "migrate.migrate"
    _sock = object
    
    def testcrud(self, cr, uid, ids, params_obj, context=None):

        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name 
        
        model = 'res.partner'
        
        oerpcli = OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        #server = 'http://localhost:8069/'
         
        #sock = xmlrpclib.ServerProxy(server + '/xmlrpc/common')
        #uid = sock.login(dbname ,user ,pwd)
         
        #sock = xmlrpclib.ServerProxy(server + '/xmlrpc/object')
        
        # CREATE A PARTNER
        partner_data = {'name':'Tiny', 'active':True, 'vat':'CL154006214'}
        #partner_id = sock.execute(dbname, uid, pwd, model, 'create', partner_data)
        partner_id = oerpobj.create(model, partner_data) 
        # The relation between res.partner and res.partner.category is of type many2many
        # To add  categories to a partner use the following format:
        partner_data = {'name':'Provider2', 'category_id': [(6,0,[3, 2, 1])]}
        # Where [3, 2, 1] are id fields of lines in res.partner.category
         
        # SEARCH PARTNERS
        args = [('vat', '=', 'CL154006214'),]
        #ids = sock.execute(dbname, uid, pwd, model, 'search', args)
        ids =  oerpobj.search(model, args)
        # READ PARTNER DATA
        fields = ['name', 'active', 'vat', 'ref']
        #results = sock.execute(dbname, uid, pwd, model, 'read', ids, fields)
        results = oerpobj.read(model, ids, fields)
        print results
         
        # EDIT PARTNER DATA
        values = {'vat':'cl152000715'}
        #results = sock.execute(dbname, uid, pwd, model, 'write', ids, values)
        results = oerpobj.update(ids, model, values) 
        # DELETE PARTNER DATA
        #results = sock.execute(dbname, uid, pwd, model, 'unlink', ids)
        
    def migradocumentos(self, cr, uid, ids, params_obj, context=None):
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name 
        
#        sock = xmlrpclib.ServerProxy(server + 'common')
#        ruid = sock.login(dbname ,user ,pwd)
#        sock = xmlrpclib.ServerProxy(server + 'object')  
       
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        def consultaidpartner(rut):
            model = 'res.partner'
            args = [("vat","=", rut)]
            campos = ['id','name']
            rescall = oerpobj.searchread(args, model, campos)
            res = []
            for i in rescall:
                res += [i['id'], i['name']]
            return res
        
        def consultaidmoneda(cod_moneda):
            model = 'res.currency'
            args = [("name","=", cod_moneda)]
            return oerpobj.search(model, args)
        
        def buscarcuentapartner(partner_id, type_account):
            model = 'res.partner'
            args = [('id','=', partner_id)]
            return oerpobj.searchread(args, model, [type_account])
            
        def buscarcuenta(code, company_id):
            model = 'account.account'
            args = [("code","=", code),("company_id","=",company_id)]
            return oerpobj.search(model, args)
        
        def buscarjournal(code):
            model = 'account.journal'
            args = [("code","=", code)]
            return oerpobj.search(model, args)
        
        def buscarterminospago(name):
            model = 'account.payment.term'
            args = [("name","=", name)]
            return oerpobj.search(model, args)
        
        def buscarperiodocontable(code, company_id):
            #fechabusqueda = date[8:10] + "/" + date[0:4];
            model = 'account.period'
            args = [("code","=", code),('company_id','=',company_id)]
            return oerpobj.search(model, args)
        
        def buscarproducto(ref_interna):
            model = 'product.product'
            args = [("default_code","=", ref_interna)]
            return oerpobj.search(model, args)
        
        
        facturas_obj = self.pool.get('account.invoice')
        facturas = facturas_obj.search(cr, uid, [('state','!=','draft'),('type','=','out_invoice')])
        facturas = facturas_obj.browse(cr, uid, facturas)
        
        for factura in facturas:
            
            rut = factura.partner_id.vat or 'cl154006214'
            cod_moneda = factura.currency_id.name
            ncuotas = factura.payment_term.name
            origin = factura.origin
            name = factura.name
            arrlineas = []
            company_id = 1
            date_invoice = factura.date_invoice
            partner_id = consultaidpartner(rut)
            currency_id = consultaidmoneda(cod_moneda)
            tipodocumento = "FV"
            miestructuraparametros = {'comment':False}
            idjournal = buscarjournal(factura.journal_id.code);
            idpayterm = buscarterminospago(ncuotas)
            period_id = buscarperiodocontable(factura.period_id.code, factura.company_id.id)
            #buscar account id con cuenta de partner
            idcuenta = 0;
            idtax=0;
            
            if "FV" == tipodocumento:
                idcuenta = buscarcuentapartner(partner_id[0], "property_account_receivable")[0]
            elif "FC" == tipodocumento:
                idcuenta = buscarcuentapartner(partner_id[0], "property_account_payable")[0]
            elif "NC" == tipodocumento:
                idcuenta = buscarcuentapartner(partner_id[0], "property_account_payable")[0]
            
    
            
            miestructuraparametros.update({'currency_id':currency_id[0],
                                           'fiscal_position': False,
                                           'user_id': uid,
                                           'account_id':idcuenta['property_account_receivable'][0],
                                           'partner_bank_id': False, 
                                           'payment_term': idpayterm[0],
                                           'tax_line':False,
                                           'journal_id':idjournal[0],
                                           'company_id':company_id,
                                           'date_invoice': date_invoice,
                                           'origin':origin,
                                           'date_due':False,
                                           "period_id":period_id[0],
                                           "message_follower_ids":False,
                                           "partner_id":int(partner_id[0]),
                                           "message_ids":False,
                                           "tax_line":[],
                                           "name": name,
                                           
                                           })
            lineas = []
            for linea in factura.invoice_line:
                producto_id = buscarproducto(linea.product_id.default_code)
                account_id = 0
                account_id = buscarcuenta(linea.account_id.code,factura.company_id.id)
                miestructuralinea = {
                                     'uos_id':1,
                                     'product_id':producto_id[0],
                                     'invoice_id':0,
                                     'price_unit':linea.price_unit,
                                     'quantity': linea.quantity,
                                     'account_id': account_id,
                                     'name':linea.name,
                                     'discount': 0,
                                     'account_id': account_id[0]
                                     }
                
                lineas+=[0,False,miestructuralinea]
            arrlineas+=[lineas]
            miestructuraparametros.update({'invoice_line':arrlineas})
            
            #creo y valido la factura
            model = 'account.invoice'
            
            ids = oerpobj.create(model, miestructuraparametros)
        
            res = oerpobj.workflow(model, 'invoice_open', ids)
            
            #actualizo el numero de factura
            data={
                  'number':factura.number,
                  'invoice_number':factura.invoice_number
                  }
            
            res = oerpobj.update(ids, model, data)
            print res
	'''    
    def migracompania(self, cr, uid, ids, params_obj, context=None):
        
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        model = 'res.company'
        res_company = self.pool.get(model)
        args = [('id', '>=', '1')]
        campos = ['id','logo','name','parent_id','street','street2','city','state_id','zip','country_id','website',
                  'phone','fax','email']
        companys= oerpobj.searchread(model, args,campos)  
        curr_id_parent_id=[]
        for company in companys:
            remoteid = company['id']
            del company['id']
            parentremoteid = company['parent_id'] and company['parent_id'][0] or None 
            del company['parent_id']
            if company['country_id']:
                country = self.pool.get('res.country').search(cr, uid, [('name','=',company['country_id'][1])])
                company['country_id'] = country[0]
            
            if company['state_id']:
                state = self.pool.get('res.country.state').search(cr, uid, [('name','=',company['state_id'][1])])
                state = self.pool.get('res.country.state').create(cr, uid, {'name':company['state_id'][1],'code':'code', 'country_id': country[0]}) if len(state)==0 else None
                company['state_id'] = state[0] if isinstance(state, list) else state
            

            id = res_company.create(cr, uid, company)   
            curr_id_parent_id += [[id,remoteid,parentremoteid]]    
            #self.pool.get('migrate.params').write(cr, uid,params_obj.id, {'parity_ids':[(0,0,{'name':company['name'],
            params_obj.write( {'parity_ids':[(0,0,{'name':company['name'],
            'model':'res.company',
            'migrated_id':remoteid,
            'current_id':id,
            })]})
        parity_obj = self.pool.get('migrate.parity')
        for item in curr_id_parent_id:
            res_company_browse = res_company.browse(cr, uid, item[0])
            id = parity_obj.search(cr, uid, [('migrated_id','=',item[2]),('model','=','res.company')])
            id = parity_obj.read(cr, uid, id, ['current_id'])
            if len(id)>0:
                res_company_browse.write({'parent_id':id[0]['current_id'] if id[0]['current_id']  else None})
        
            

        return    
    
    def migradiarios(self, cr, uid, ids, params_obj, context=None):   
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        parity_obj = self.pool.get('migrate.parity')
        
        model = 'account.journal'
        model_obj = self.pool.get(model)
        args = [('id', '>=', '1')]
        campos = ['id','code','name','type','company_id','sentralisation','entry_posted','allow_date','group_invoice_lines','journal_user','amount_authorized_diff',
                  ]
        data = oerpobj.searchread(model, args,campos)  

        for item in data:
            remoteid = item['id']            
            if parity_obj.get_parity_id(cr, uid,remoteid, model, context): continue
            
            del item['id']
            if item['company_id']:
                item['company_id'] = parity_obj.get_parity_id(cr, uid,item['company_id'][0], model, context ) or 1

            id = model_obj.create(cr, uid, item)   
                
            #self.pool.get('migrate.params').write(cr, uid,params_obj.id, {'parity_ids':[(0,0,{'name':company['name'],
            params_obj.write( {'parity_ids':[(0,0,{'name':item['name'],
            'model':model,
            'migrated_id':remoteid,
            'current_id':id,
            })]})
            
    def get_stock_journal(self, cr, uid, ids, params_obj, context=None):   
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        parity_obj = self.pool.get('migrate.parity')
        
        model = 'stock.journal'
        model_obj = self.pool.get(model)
        args = [('id', '>=', '1')]
        campos = ['id','name']
        data= oerpobj.searchread(model, args,campos)  

        for item in data:
            remoteid = item['id']            
            
            if parity_obj.get_parity_id(cr, uid,remoteid, model, context): continue
            
            del item['id']
            if item['company_id']:
                item['company_id'] = parity_obj.get_parity_id(cr, uid,item['company_id'][0], model, context )

            id = model_obj.create(cr, uid, item)   
                
            #self.pool.get('migrate.params').write(cr, uid,params_obj.id, {'parity_ids':[(0,0,{'name':company['name'],
            params_obj.write( {'parity_ids':[(0,0,{'name':item['name'],
            'model':model,
            'migrated_id':remoteid,
            'current_id':id,
            })]})
            
    def get_stock_location(self, cr, uid, ids, params_obj, context=None):   
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        parity_obj = self.pool.get('migrate.parity')
        
        model = 'stock.location'
        model_obj = self.pool.get(model)
        args = [('id', '>=', '1')]
        campos = ['id','name','location_id','usage','company_id','icon','scrap_location','active','posx','posy','posz','chained_location_type',
                  'chained_auto_packing','chained_delay','chained_journal_id','chained_picking_type','chained_company_id']
        data= oerpobj.searchread(model, args,campos)  

        curr_id_parent_id=[]
        for item in data:
            remoteid = item['id']            
            
            if parity_obj.get_parity_id(cr, uid,remoteid, model, context): continue
            
            del item['id']
            parentremoteid = item['parent_id'] and item['parent_id'][0] or None 
            del item['parent_id']
            
            if item['company_id']:
                item['company_id'] = parity_obj.get_parity_id(cr, uid,item['company_id'][0], 'res.company', context )

            if item['chained_journal_id']:
                item['chained_journal_id'] = parity_obj.get_parity_id(cr, uid,item['chained_journal_id'][0], 'stock.journal', context )
            
            if item['chained_company_id']:
                item['chained_company_id'] = parity_obj.get_parity_id(cr, uid,item['chained_company_id'][0], 'res.company', context )


            id = model_obj.create(cr, uid, item)   
            curr_id_parent_id += [[id,remoteid,parentremoteid]]
            #self.pool.get('migrate.params').write(cr, uid,params_obj.id, {'parity_ids':[(0,0,{'name':company['name'],
            params_obj.write( {'parity_ids':[(0,0,{'name':item['name'],
            'model':model,
            'migrated_id':remoteid,
            'current_id':id,
            })]})
        
        for item in curr_id_parent_id:
            id = parity_obj.get_parity_id(cr, uid,item[2], model, context )
            if id:
                model_obj = model_obj.browse(cr, uid, item[0])
                model_obj.write({'parent_id':id})
    '''                    
    
    def get_data(self, cr, uid, ids, params_obj, model, fields, filter=[], context=None):   
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        

        args = [('id', '>=', '1')]
        if len(filter)>0:
            args += filter
            
        data= oerpobj.searchread(model, args,fields)  


        
        return data
    
    def write_data_config(self, cr, uid, ids, params_obj, data, model, context=None):
        parity_obj = self.pool.get('migrate.parity')
        
        model_obj = self.pool.get(model)
        curr_id_parent_id=[]
        for item in data:
            print item
            remoteid = item['id']            
            parentremoteid=None
            
            if parity_obj.get_parity_id(cr, uid,remoteid, model, context): continue
            
            del item['id']
            if 'parent_id' in item:
                parentremoteid = item['parent_id'] and item['parent_id'][0] or None 
                del item['parent_id']

            if 'location_id' in item:
                parentremoteid = item['location_id'] and item['location_id'][0] or None 
                del item['location_id']            

            if 'company_id' in item and item['company_id']:
                item['company_id'] = parity_obj.get_parity_id(cr, uid,item['company_id'][0], 'res.company', context)

            if model == 'stock.location': 
                if item['chained_journal_id']:
                    item['chained_journal_id'] = parity_obj.get_parity_id(cr, uid,item['chained_journal_id'][0], 'stock.journal', context )
                
                if item['chained_company_id']:
                    item['chained_company_id'] = parity_obj.get_parity_id(cr, uid,item['chained_company_id'][0], 'res.company', context )
                    
            elif model == 'res.company':
                if item['country_id']:
                    country = self.pool.get('res.country').search(cr, uid, [('name','=',item['country_id'][1])])
                    item['country_id'] = country[0]
                
                if item['state_id']:
                    state = self.pool.get('res.country.state').search(cr, uid, [('name','=',item['state_id'][1])])
                    state = self.pool.get('res.country.state').create(cr, uid, {'name':item['state_id'][1],'code':'code', 'country_id': country[0]}) if len(state)==0 else None
                    item['state_id'] = state[0] if isinstance(state, list) else state
            elif model == 'stock.warehouse':
                item['lot_input_id']= parity_obj.get_parity_id(cr, uid,item['lot_input_id'][0], 'stock.location', context ) 
                item['lot_output_id']= parity_obj.get_parity_id(cr, uid,item['lot_output_id'][0], 'stock.location', context )
                item['lot_stock_id']= parity_obj.get_parity_id(cr, uid,item['lot_stock_id'][0], 'stock.location', context )  
            
            elif model=='sale.shop':
                item['warehouse_id'] = parity_obj.get_parity_id(cr, uid,item['warehouse_id'][0], 'stock.warehouse', context )
                item['payment_default_id'] = self.pool.get('account.payment.term').search(cr, uid, [('name','=',item['payment_default_id'][1] or "")])[0] or 1
                #item['pricelist_id'] = self.pool.get('product.pricelist').search(cr, uid, [('name','=',item['pricelist_id'][1] or "")])[0] or 1
            elif model=='pos.config':
                item['shop_id'] =  parity_obj.get_parity_id(cr, uid,item['shop_id'][0], 'sale.shop', context )
                item['journal_ids'] = [(4, parity_obj.get_parity_id(cr, uid, journal_item, 'account.journal', context ) )  for journal_item in item['journal_ids'] ]   
            
            elif model=='product.product':
                item['categ_id'] = parity_obj.get_parity_id(cr, uid,item['categ_id'][0], 'product.category', context )
                item['pos_categ_id'] = parity_obj.get_parity_id(cr, uid,item['pos_categ_id'][0], 'pos.category', context )
                item['uom_id'] = self.pool.get('product.uom').search(cr, uid,[('name','=', item['uom_id'][1])])[0]
                item['uom_po_id'] = self.pool.get('product.uom').search(cr, uid,[('name','=', item['uom_po_id'][1])])[0]
                
            elif model=='res.users':
                item['company_ids'] = [(4, parity_obj.get_parity_id(cr, uid, company_item, 'res.company', context ) )  for company_item in item['company_ids'] ]
                item['pos_config'] = parity_obj.get_parity_id(cr, uid,item['pos_config'][0], 'pos.config', context ) if item['pos_config'] and len(item['pos_config'])>0 else None
                item['groups_id'] = [(4,group_id) for group_id in item['groups_id'] if self.pool.get('res.groups').search(cr, uid, [('id','=',group_id)])]
                item['lang'] = 'es_ES'
            
            elif model=='account.period':
                item['fiscalyear_id'] = parity_obj.get_parity_id(cr, uid,item['fiscalyear_id'][0], 'account.fiscalyear', context ) if item['fiscalyear_id'] and len(item['fiscalyear_id'])>0 else None
            
            id = model_obj.create(cr, uid, item)   
            if parentremoteid:
                curr_id_parent_id += [[id,remoteid,parentremoteid]]
            #self.pool.get('migrate.params').write(cr, uid,params_obj.id, {'parity_ids':[(0,0,{'name':company['name'],
            params_obj.write( {'parity_ids':[(0,0,{'name':item['name'],
            'model':model,
            'migrated_id':remoteid,
            'current_id':id,
            })]})
        
        for item in curr_id_parent_id:
            id = parity_obj.get_parity_id(cr, uid,item[2], model, context )
            if id:
                if model == 'stock.location':
                    self.pool.get(model).write(cr, uid, item[0],{'location_id':id})
                else:
                    self.pool.get(model).write(cr, uid, item[0],{'parent_id':id})
        
    def migrate_initial_config(self, cr, uid, ids, params_obj, context=None):
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)
        
        
        #self.migracompania(cr, uid, ids,params_obj, context)
        #migra compañias
        model = 'res.company'
        fields = ['id','logo','name','parent_id','street','street2','city','state_id','zip','country_id','website',
                  'phone','fax','email']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)        
        #print 'paso res.company'
        #migra periodos
        model = 'account.fiscalyear'
        fields = ['id','code','name','state','company_id','date_start','date_stop']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)  
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)          
        
        model = 'account.period'
        fields = ['id','code','name','state','company_id','date_start','date_stop','fiscalyear_id','special']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)  
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)   
        
        #migra cuentas de impuestos
        #model = 'account.tax.code'
        #fields = ['id','code','name','type','parent_id','company_id','notprintable','sign','sum_period','sum', 'info' ]
        #data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)  
        #self.write_data_config(cr, uid, ids, params_obj, data, model, context)        


        #migra cuentas
        #model = 'account.account'
        #fields = ['id','code','name','type','user_type','company_id','active','tax_ids','reconcile',
        #          'currency_mode','note', 'parent_id' ]
        #data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)  
        #self.write_data_config(cr, uid, ids, params_obj, data, model, context)

        #migra impuestos
        model = 'account.tax'
        fields = ['id','code','name','type','company_id','sentralisation','entry_posted','allow_date','group_invoice_lines','journal_user','amount_authorized_diff',
                  ]
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)  
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
                
        #migra diarios
        model = 'account.journal'
        fields = ['id','code','name','type','company_id','sentralisation','entry_posted','allow_date','group_invoice_lines','journal_user','amount_authorized_diff',
                  ]
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context)  
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)   
        
 
        
         
        #migra diarios de stock
        model = 'stock.journal'
        fields = ['id','name']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
               
        #migra ubicaciones de stock
        model = 'stock.location'
        fields = ['id','name','location_id','usage','company_id','icon','scrap_location','active','posx','posy','posz','chained_location_type',
                  'chained_auto_packing','chained_delay','chained_journal_id','chained_picking_type','chained_company_id']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
                
        #migra ubicaciones de stock
        model = 'stock.warehouse'
        fields = ['id','name','lot_input_id','lot_stock_id','lot_output_id','company_id']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        #migra tiendas
        model = 'sale.shop'
        fields = ['id','name', 'company_id', 'warehouse_id','payment_default_id']#,'pricelist_id']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        #migra configuracion de punto de venta
        model = 'pos.config'
        fields = ['id','name', 'company_id', 'shop_id','journal_ids']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        #migra categorias de producto
        model = 'product.category'
        fields = ['id','name', 'parent_id', 'type']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        #migra categorias de producto del punto de ventas
        model = 'pos.category'
        fields = ['id','name', 'parent_id', 'secuence']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        #migra unidades de medida de producto
        #model = 'product.uom'
        #fields = ['id','name', 'parent_id', 'secuence']
        #data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        #self.write_data_config(cr, uid, ids, params_obj, data, model, context)

        #migra productos
        model = 'product.product'
        fields = ['id','name', 'categ_id', 'type', 'uom_id','uom_po_id', 'default_code', 'ean13','list_price','procure_method','supply_method'
                  ,'cost_method','standard_price','cost_price_extra','active', 'qty_available', 'incoming_qty', 'outgoing_qty', 'virtual_available'
                  , 'company_id', 'available_in_pos','pos_categ_id','valuation']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        model = 'res.users'
        filter = [('login','!=', 'admin')]
        fields = ['id','name', 'login', 'company_id', 'active','lang', 'tz', 'email','signature','company_ids','pos_config'
                  ,'ean13']
        data = self.get_data(cr, uid, ids,params_obj, model, fields,filter=filter, context = context) 
        self.write_data_config(cr, uid, ids, params_obj, data, model, context)
        
        
        return True

    def migrate_pos_movement(self, cr, uid, ids, params_obj, context=None):
        user = params_obj.user
        pwd = params_obj.pwd
        dbname = params_obj.bbdd
        server = params_obj.name  
        
        oerpcli=  OpenERPClient(server, dbname,user,pwd)
        oerpobj = OpenERPObject(oerpcli)   
        
        
        model = 'res.company'
        fields = ['id','logo','name','parent_id','street','street2','city','state_id','zip','country_id','website',
                  'phone','fax','email']
        data = self.get_data(cr, uid, ids,params_obj, model, fields, context = context) 
        
        
        
        
        
        
        
        return True
             
migrate_migrate()
        