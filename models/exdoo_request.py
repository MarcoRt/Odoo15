# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class ExdooRequest(models.Model):
    _name = "exdoo.request"

    _description = "Exdoo Request"
    
    @api.onchange('cliente')
    def _onchange_name(self):
        if self.cliente:
            if len(self.cliente.terminos_pagos) > 0:
                self.termino_pago = self.cliente.terminos_pagos[0]
    
    @api.depends('lineas_solicitud_ids')
    def _compute_amount(self):
        total_impuesto_sum = total_calculado_sum = subtotal_calculado_sum = 0
        for i in self:
            for line in i.lineas_solicitud_ids:
                price = line.precio_unitario
                taxes = line.tax_id.compute_all(price)
                total_impuesto_sum += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                total_calculado_sum += taxes['total_included']
                subtotal_calculado_sum +=  taxes['total_excluded']
            i.total_impuesto = total_impuesto_sum
            i.total_calculado = total_calculado_sum
            i.subtotal_calculado = subtotal_calculado_sum
        
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
    lineas_solicitud_ids = fields.One2many(
        comodel_name="lineas.solicitud",
        inverse_name="lineas_solicitud_id",
        string="Lineas de solicitud",
    )
    num_presupuesto = fields.Char(string="Número presupuesto", copy=False)
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
    currency_id = fields.Many2one(
        comodel_name = 'res.currency',
        string = 'Moneda',
        default=lambda self: self.env.company.currency_id.id 
    )
    tax_id = fields.Many2many('account.tax', string='Taxes')
    subtotal_calculado = fields.Monetary(string="Subtotal",store=False, compute="_compute_amount")
    total_calculado = fields.Monetary(string="Total",store=False, compute="_compute_amount")
    total_impuesto = fields.Monetary(string="Total impuesto",store=False, compute="_compute_amount")
    def aprobar_presupuesto(self):
        logger.info("Se cambió el state a aprobado")
        self.state = "aprobado"
        self.fecha_confirmacion = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.info("Se cambió el state a cancelado")
        self.state = "cancelado"
    
    @api.model
    def create(self, variables):
        logger.info("Variables: {0}".format(variables))
        sequence_obj = self.env["ir.sequence"]
        correlativo = sequence_obj.next_by_code("secuencia.solicitud")
        variables["num_presupuesto"] = correlativo
        return super(ExdooRequest, self).create(variables)
    
    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = self.name + " (Copia)"
        return super(ExdooRequest, self).copy(default)

