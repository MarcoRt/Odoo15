# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ContadorVentas(models.Model):
    
    _inherit = "sale.order"
    
    contador_ventas = fields.Many2one(required=True, comodel_name="exdoo.request",string="Contador de ventas")
    
    def _prepare_invoice(self):   
        invoice_vals = super(ContadorVentas,self)._prepare_invoice()
        invoice_vals["contador_facturas"] = self.contador_ventas.id
        return invoice_vals
        
    
