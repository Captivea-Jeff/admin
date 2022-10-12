# -*- coding: utf-8 -*-
# Part of Bistasolutions. See LICENSE file for full copyright and licensing details.
# 10-22-22  Jeff Mueller, Added product_format_uom, was defined in Studio, incorporated into module.
import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_format_uom = fields.Selection([
        ('g','g'),
        ('ml','ml'),
        ('Seed(s)','Seed(s)')],
        string='Product Format UoM')
    product_format = fields.Float(string="Product Format", digits='Weight Precision Three')
    reporting_weight = fields.Float(string="Reporting Weight", digits='Weight Precision Three')
    equivalent_weight = fields.Float(string="Cannabis Equivalent Weight", digits='Weight Precision Three')
