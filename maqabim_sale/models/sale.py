# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.tools import float_is_zero


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False):
        """
        Add undelivered so lines in invoice lines 
        """
        zero_qty_lines = []
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for order in self:
            for line in order.order_line.sorted(key=lambda l: l.qty_to_invoice < 0):
                if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    vals = line._prepare_invoice_line(quantity=0)
                    vals.update({'sale_line_ids': [(6, 0, [line.id])]})
                    zero_qty_lines += [vals]
        move = super(SaleOrder, self)._create_invoices(grouped, final)
        if move:
            for vals in zero_qty_lines:
                vals.update({'move_id': move.id,
                             'account_id': move.journal_id.default_account_id.id})
                self.env['account.move.line'].create(vals)
        return move
