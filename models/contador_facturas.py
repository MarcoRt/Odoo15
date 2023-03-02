# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ClientePagos(models.Model):
    _inherit = "account.move"
    
    contador_facturas = fields.Many2one(required=True, comodel_name="exdoo.request",string="Contador de facturas")