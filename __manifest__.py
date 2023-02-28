# -*- coding:utf-8 -*-

{
    'name': 'Modulo exdoo request',
    'version': '1.0',
    'category': 'exdoo_request',
    'depends': ['base','sale'],
    'author': 'Marco Rodriguez',
    'summary': 'Módulo para control de ventas, compras y movimientos.',
    'website': '',
    'description': """
Módulo para control de ventas, compras y movimientos.
======================================

    """,
    'data': ['security/security.xml',
            'security/ir.model.access.csv',
            'views/menu.xml',
            'views/exdoo_request_view.xml',
            'views/cliente_pagos.xml',
            'views/exdoo_request_admin_view.xml',
            'views/exdoo_request_ro_view.xml',
            'views/lineas_solicitud_view.xml',
            'data/secuencia.xml',],
}