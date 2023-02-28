# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class LineasSolicitud(models.Model):
    _name = "lineas.solicitud"
    _description = "Líneas de solicitud"
    
    @api.onchange('producto')
    def _onchange_name(self):
        if self.producto:
            self.tax_id = self.producto.taxes_id
            self.unidad_medida = self.producto.uom_id
    
    @api.depends('precio_unitario')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.precio_unitario
            taxes = line.tax_id.compute_all(price)
            line.update({
                'total_impuesto': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'total_calculado': taxes['total_included'],
                'subtotal_calculado': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
                  
    producto = fields.Many2one(comodel_name="product.product", string="Producto")
    cantidad = fields.Float(string="Cantidad")
    unidad_medida = fields.Many2one(comodel_name="uom.uom", string="Unidad de medida") 
    impuesto = fields.Many2many(
        comodel_name="account.tax",
        relation="impuesto_lineasolicitud_account_fax",
        column1="impuesto_id",
        column2="account_fax_id",
        string="Impuesto",
        copy=False
    )
    precio_unitario = fields.Float(related="producto.list_price",string="Precio unitario")
    lineas_solicitud_id = fields.Many2one(
        comodel_name="exdoo.request",
        string="Exdoo Request",
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
    company_id = fields.Many2one(related='lineas_solicitud_id.compania', string='Company')

    