# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ExdooRequest(models.Model):
    _name = "exdoo.request"

    _description = "Exdoo Request"

    name = fields.Char(string='Nombre')
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
    def aprobar_presupuesto(self):
        logger.info("Se cambió el state a aprobado")
        self.state = "aprobado"
        self.fecha_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.info("Se cambió el state a cancelado")
        self.state = "cancelado"
