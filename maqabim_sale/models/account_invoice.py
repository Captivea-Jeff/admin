# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    ordered_qty = fields.Float(string="Ordered Qty", compute="_compute_ordered_qty", digits='Product Unit of Measure')
    back_order_qty = fields.Float(string="Backorder Qty", compute="_compute_backorder_qty",
                                digits='Product Unit of Measure')


    @api.depends('sale_line_ids')
    def _compute_ordered_qty(self):
        self.ordered_qty = 0
        for invoice_line in self.filtered(lambda l: l.sale_line_ids):
            invoice_line.ordered_qty = sum([l.product_uom_qty for l in invoice_line.sale_line_ids])


    @api.depends('ordered_qty','quantity')
    def _compute_backorder_qty(self):
        """
        Back order Quantity = Order Quantity - Invoice Quantity
        """
        self.back_order_qty = 0
        for invoice_line in self.filtered(lambda l: l.sale_line_ids):
            if invoice_line.quantity:
                invoice_line.back_order_qty = invoice_line.ordered_qty - invoice_line.quantity
            else:
                invoice_line.back_order_qty = invoice_line.ordered_qty

