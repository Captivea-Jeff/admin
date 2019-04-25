# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import UserError


class ReportPurchaseLabel(models.AbstractModel):
    _name = 'report.maqabim_purchase.report_polabel'

    @api.model
    def get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        order_ids = self.env.context.get('active_ids', [])
        orders = self.env['purchase.order'].browse(order_ids)
        report_format = data['form'].get('formats')
        return {
            'doc_ids': order_ids,
            'doc_model': 'purchase.order',
            'docs': orders,
            'data': data,
            'report_format': report_format
        }
