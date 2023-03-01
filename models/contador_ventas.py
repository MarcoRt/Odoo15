# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ContadorVentas(models.Model):
    
    _inherit = "sale.order"
    
    contador_ventas = fields.Many2one(required=True, comodel_name="exdoo.request",string="Contador de ventas")