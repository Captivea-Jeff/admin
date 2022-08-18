# coding: utf-8

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit='product.template'

    bck_stock_date = fields.Datetime('Back In Stock Date', company_dependent=True)
