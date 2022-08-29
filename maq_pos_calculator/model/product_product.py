# -*- coding: utf-8 -*-
# Part of Bistasolutions. See LICENSE file for full copyright and licensing details.
import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_format = fields.Float(string="Product Format", digits='Weight Precision Three')
    reporting_weight = fields.Float(string="Reporting Weight", digits='Weight Precision Three')
    equivalent_weight = fields.Float(string="Cannabis Equivalent Weight", digits='Weight Precision Three')
