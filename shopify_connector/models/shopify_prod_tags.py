# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ShopifyProdTags(models.Model):
    _name = 'shopify.prod.tags'
    _description = 'Shopify Product Tags'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Name', help='Enter Name',
                       tracking=True, required=True)
    shopify_config_ids = fields.Many2many('shopify.config', string='Shopify Configurations',
                                          help='Enter Shopify Configurations', tracking=True, required=True)
    color = fields.Integer('Color', help='Enter the Color',
                           tracking=True)
    is_province = fields.Boolean(
        'Province', help='Province Yes/No', tracking=True)
    active = fields.Boolean('Active', help='Active Yes/No',
                            tracking=True, default=True)
