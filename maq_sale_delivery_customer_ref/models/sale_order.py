# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    m_customer_ref = fields.Char(string="External Reference", tracking=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    m_delivery_customer_ref = fields.Char(related='sale_id.client_order_ref', string="External PO Reference", tracking=True)
