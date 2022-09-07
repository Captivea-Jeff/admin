# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ShopifyOrderErrorLog(models.Model):
    _name = 'shopify.order.error.log'
    _description = 'Shopify Order Error Log'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = "create_date desc"

    shopify_so_id = fields.Char(
        "Shopify SO ID", help="Enter Shopify SO ID", tracking=True)
    odoo_so_id = fields.Many2one("sale.order", "Odoo Sale Order ID",
                                 help="Enter Sale Order ID", tracking=True)
    error = fields.Text("Error", help="Error Message",
                        tracking=True)
    company_id = fields.Many2one(
        "res.company", "Company", help="Company", tracking=True)
    date = fields.Date("Date", help="Company", tracking=True)
    shopify_config_id = fields.Many2one(
        "shopify.config", "Shopify Config.", help="Shopify Config.", tracking=True)
