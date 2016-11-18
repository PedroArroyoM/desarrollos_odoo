# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, api, fields
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools.safe_eval import safe_eval as eval


class FunctionCalc(models.Model):
    _name = "function.calc"
    name = fields.Char("Name")
    python_expression = fields.Text("Python expression")
    variable_ids = fields.One2many(
        'function.calc.var',
        'function_id',
        string='Function Calc')
    
    
    def compute_pricelist(self, cr, uid, ids, localdict, context):
        current = self.browse(cr, uid, ids)
        try:
            eval(current.python_expression, localdict, mode='exec', nocopy=True)
            return 'result' in localdict and float(localdict['result']) or 1.0
        except:
            raise except_orm('Error!', 'Wrong python code defined for qty calc %s (%s).'% (current.name, current.python_expression))


class FunctionCalcVar(models.Model):
    _name = "function.calc.var"
    name = fields.Char("Name")
    value = fields.Float("Value")
    function_id = fields.Many2one('function.calc','Variables function',)
    

class FunctionCalcWizard(models.Model):
    _name = 'funcion.calc.wizard'
    name = fields.Char("Name")
    function_id = fields.Many2one('function.calc','Variables function',)
    
    def action_calcquantity(self, cr, uid, ids, context=None):
        localdict = {}
        inv_line_obj = self.pool.get('sale.order.line')
        current_wiz = self.browse(cr, uid, ids)
        calc_selected = current_wiz.function_id
        curr_inv_line = inv_line_obj.browse(cr, uid, [context['default_order_line_id']])
        inv_line_qty = curr_inv_line.product_uom_qty
        
        localdict['qty'] = curr_inv_line.product_uom_qty
        localdict['width'] = curr_inv_line.width
        localdict['height'] = curr_inv_line.height
        localdict['cuantify'] = curr_inv_line.cuantify
        localdict['result'] = None
        product_uom_qty = calc_selected.compute_pricelist(dict(localdict))
        
        inv_line_obj.write(cr, uid, context['default_order_line_id'], {'product_uom_qty':product_uom_qty})
        
        return 
        


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    width = fields.Float('Width')
    height = fields.Float('Height')
    cuantify = fields.Float('Cuantify')
    
    calc_function_id = fields.Many2one('function.calc','Variables function',)
    
    #<button string="Add Entry" icon="STOCK_ADD" name="action_add_entry" type="object"/>
    def action_add_entry(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an meeting request
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
    
        ir_model_data = self.pool.get('ir.model.data')
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'funcion.calc.wizard', 'function_calc_wizard_form_view')[1]
        except ValueError:
            compose_form_id = False 
        ctx = dict(context)
        ctx.update({
            'default_model': 'sale.order.line',
            'default_order_line_id': ids[0],
        })
        return {
            'type': 'ir.actions.act_window',
            'name':'Create Complaint',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funcion.calc.wizard',
            'views': [(compose_form_id, 'form')],
            'view_id': False,
            'target': 'new',
            'flags': {'form': {'action_buttons': False}},
            'context': ctx,
            'nodestroy': True
        }
    
    
    