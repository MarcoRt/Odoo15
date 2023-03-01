# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ContadorCompras(models.Model):
    
    _inherit = "purchase.order"
    
    contador_compras = fields.Many2one(required=True, comodel_name="exdoo.request",string="Contador de compras")