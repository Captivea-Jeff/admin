# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ShopifyImages(models.Model):
    _name = 'shopify.images'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Shopify Images'

    type = fields.Selection([('url', 'URL'), ('binary', 'Binary')], string="type",
                            help="Enter Type of Image", default="binary", tracking=True)
    binary = fields.Binary("Binary Image", help="Enter Binary Image",
                           attachment=True, tracking=True)
    src = fields.Char("Source Image", help="Enter Source Image",
                      tracking=True)
    filename = fields.Char(
        "File Name", help="Enter File Name", tracking=True)
    shopify_image_id = fields.Char(
        "Shopify Image", help="Enter Shopify Image", tracking=True, readonly=True)
    shopify_config_id = fields.Many2one(
        "shopify.config", help="Enter Shopify Configuration", tracking=True, readonly=True)
