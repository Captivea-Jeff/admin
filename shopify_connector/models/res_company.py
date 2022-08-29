# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    def _valid_field_parameter(self, field, name):
        # I can't even
        return name == 'tracking' or super()._valid_field_parameter(field, name)

    shopify_vendor_id = fields.Many2one(
        "res.partner", "Shopify Vendor", help="Shopify Vendor", tracking=True)
    shopify_customer_id = fields.Many2one(
        "res.partner", "Shopify Customer", help="Shopify Customer", tracking=True)
    shopify_warehouse_id = fields.Many2one(
        "stock.warehouse", "Shopify Warehouse",  help="Shopify Warehouse", tracking=True)
    shopify_province_ids = fields.Many2many("res.country.state", 'res_company_state_rel', 'res_company_id',
                                            'res_state_id', "Shopify Province",  help="Shopify Province",
                                            tracking=True)
    shopify_location_id = fields.Many2one("stock.location", "Shopify Stock Location",
                                          help="Here you can set default Shopify Stock Location", tracking=True)
    shopify_user_id = fields.Many2one("res.users", "Default User", tracking=True, required=True,
                                      help="Default user who'll create SO and PO for a company")
    shopify_intercompany_customer_id = fields.Many2one(
        "res.partner", "Shopify Intercompany Customer", help="Shopify Intercompany Customer", tracking=True)
