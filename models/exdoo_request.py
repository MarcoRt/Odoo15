# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)


class ExdooRequest(models.Model):
    _name = "exdoo.request"

    _description = "Exdoo Request"

    @api.onchange("cliente")
    def _onchange_name(self):
        if self.cliente:
            if len(self.cliente.terminos_pagos) > 0:
                self.termino_pago = self.cliente.terminos_pagos[0]
                self.terminos_pagos = self.cliente.terminos_pagos

    @api.depends("lineas_solicitud_ids.total_calculado")
    def _compute_amount(self):
        total_impuesto_sum = (
            total_calculado_sum
        ) = subtotal_calculado_sum = descuento_sum = 0
        for i in self:
            for line in i.lineas_solicitud_ids:
                total_impuesto_sum += line.total_impuesto
                total_calculado_sum += line.total_calculado
                subtotal_calculado_sum += line.subtotal_calculado
                descuento_sum += line.descuento
            i.descuento = descuento_sum
            i.total_impuesto = total_impuesto_sum
            i.total_calculado = total_calculado_sum
            i.subtotal_calculado = subtotal_calculado_sum

    name = fields.Char(string="Nombre")
    fecha_creacion = fields.Datetime(
        string="Fecha de creación",
        copy=False,
        default=lambda self: fields.Datetime.now(),
    )
    contador_ventas = fields.One2many(comodel_name="sale.order",
        inverse_name="contador_ventas",
        string="Contador de ventas",)
    contador_compras = fields.One2many(comodel_name="purchase.order",
        inverse_name="contador_compras",
        string="Contador de compras")
    cantidad_ventas = fields.Integer(string="Cantidad de ventas")
    cantidad_compras = fields.Integer(string="Cantidad de compras")
    fecha_confirmacion = fields.Datetime(string="Fecha aprobado", copy=False)
    cliente = fields.Many2one(comodel_name="res.partner", string="Cliente")
    termino_pago = fields.Many2one(
        comodel_name="account.payment.term", string="Termino de pago"
    )
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
        comodel_name="res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id.id,
    )
    tax_id = fields.Many2many("account.tax", string="Taxes")
    almacen = fields.Many2one("stock.warehouse", required=True, string="Almacén")
    descuento = fields.Float(string="Descuento")
    terminos_pagos = fields.Many2many(
        comodel_name="account.payment.term", string="Terminos de pagos"
    )
    subtotal_calculado = fields.Monetary(
        string="Subtotal", store=False, compute="_compute_amount"
    )
    total_calculado = fields.Monetary(
        string="Total", store=False, compute="_compute_amount"
    )
    total_impuesto = fields.Monetary(
        string="Total impuesto", store=False, compute="_compute_amount"
    )

    def BuyItems(self, id_producto: int, cantidad: int):
        purchase_id = None
        line_id = None
        for line in self.lineas_solicitud_ids:
            if line.producto.id == id_producto:
                sellers = line.producto.seller_ids
                if len(sellers) > 0:
                    dict_purchase = {"contador_compras": self.id,
                                     "name": "Compra ejemplo "+ str(self.id), "partner_id": sellers[0].name.id}
                    purchase_id = self.env["purchase.order"].create(dict_purchase)
                    producto_dict = {
                        "order_id": purchase_id.id,
                        "name": "["
                        + line.producto.default_code
                        + "] "
                        + line.producto.name,
                        "product_id": line.producto.id,
                        "product_qty": cantidad,
                        "price_unit": line.precio_unitario
                        - (line.precio_unitario * 0.25),
                    }
                    line_id = self.env["purchase.order.line"].create(producto_dict)

    def IsEnoughInStock(self):
        products_dict = {}
        quantity_dict = {}
        for order in self:
            producto = order.lineas_solicitud_ids.mapped("producto")
            for p in producto:
                if p.detailed_type == "product":
                    stock = p.with_context(location=self.almacen.id).qty_available
                    products_dict[p.id] = stock

        for line in self.lineas_solicitud_ids:
            quantity_dict[line.producto.id] = line.cantidad

        for i in products_dict:
            cantidad = quantity_dict.get(i)
            if cantidad:
                if cantidad > products_dict.get(i):
                    self.BuyItems(i, cantidad - products_dict.get(i))

    def aprobar_presupuesto(self):
        logger.info("Se cambió el state a aprobado")
        # Cosas que necesito para crear una venta
        # Almacén
        # Cliente
        # Vendedor
        self.IsEnoughInStock()
        orden = {}
        dict_sale = {}
        if self.cliente.id is not False:
            if self.almacen.id is not False:
                if self.termino_pago.id is not False:
                    dict_sale = {
                        "contador_ventas": self.id,
                        "name": "Venta de prueba " + str(self.id),
                        "partner_id": self.cliente.id,
                        "warehouse_id": self.almacen.id,
                        "payment_term_id": self.termino_pago.id
                    }
                    order_id = self.env['sale.order'].create(dict_sale)
        #sales.order.line
        #order_id
        for line in self.lineas_solicitud_ids:
            line_dict = {
                'order_id': order_id.id,
                'product_id': line.producto.id,
                'name': line.producto.name,
                'product_uom_qty': line.cantidad,
                'product_uom': line.unidad_medida.id,
                'price_unit': line.precio_unitario,
                'tax_id': [line.tax_id.id],
                'discount': line.descuento,
                'price_subtotal': line.subtotal_calculado
            }
            if False in line_dict.get("tax_id"):
                line_dict.pop("tax_id")
            orden = self.env['sale.order.line'].create(line_dict)
        # self.state = "aprobado"
        self.cantidad_ventas = len(self.contador_ventas)
        self.cantidad_compras = len(self.contador_compras)
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
