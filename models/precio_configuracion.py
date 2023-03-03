# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class PrecioConfiguracion(models.TransientModel):
    _inherit = "res.config.settings"
    
    realizar_compra = fields.Boolean(related='company_id.realizar_compra', readonly=False)