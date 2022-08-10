# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    m_created_by = fields.Char(string="Created By")
    product_product_ids = fields.Many2many("product.product", compute="_get_products_of_vendor")

    @api.depends('partner_id', 'company_id')
    def _get_products_of_vendor(self):
        if self.partner_id:
            product_supplier_ids = self.env['product.supplierinfo'].search([('name', '=', self.partner_id.id)])
            self.product_product_ids = self.env['product.product'].search([
                ('product_tmpl_id', 'in', product_supplier_ids.product_tmpl_id.ids), ('purchase_ok', '=', True)])
        else:
            self.product_product_ids = self.env['product.product'].search([('purchase_ok', '=', True)])

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        if self.partner_id:
            if self.order_line:
                warning_mess = {
                    'title': _('Vendor Change!'),
                    'message': 'You changed the vendor but product lines are still there.'
                }
                res.update({'warning': warning_mess})
        return res
