# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class LineasSolicitud(models.Model):
    _name = "lineas.solicitud"

    _description = "Líneas de solicitud"

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
    precio_unitario = fields.Float(string="Precio unitario")