# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ClientePagos(models.Model):
    _inherit = "res.partner"
    
    terminos_pagos = fields.Many2many('account.payment.term', string='Taxes')