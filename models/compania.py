# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)


class Compania(models.Model):
    _inherit = "res.company"
    
    realizar_compra = fields.Boolean(string="Realizar compra de productos faltantes", default=False)
    