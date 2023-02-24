# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ExdooRequest(models.Model):
    _name = "exdoo.request"

    _description = "Exdoo Request"

    nombre = fields.Char(String='Nombre')
    fecha_creacion = fields.Datetime(
        string="Fecha de creación",
        copy=False,
        default=lambda self: fields.Datetime.now())

    fecha_confirmacion = fields.Datetime(string="Fecha aprobado", copy=False)
    cliente = fields.Many2one(comodel_name="res.partner", string="Cliente")
    termino_pago = fields.Many2one(comodel_name="account.payment.term", string="Termino de pago")
    usuario = fields.Many2one(comodel_name="res.users", string="Usuario")
    compania = fields.Many2one(comodel_name="res.company", string="Compañía")
    moneda = fields.Many2one(comodel_name="res.currency", string="Moneda")
    state = fields.Selection(
        selection=[
            ("borrador", "Borrador"),
            ("aprobado", "Aprobado"),
            ("cancelado", "Cancelado"),
        ],
        default="borrador",
        string="Estados",
        copy=False,
    )
