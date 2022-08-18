# coding: utf-8

import logging

from odoo import api, fields, models, tools, _
from datetime import datetime

_logger = logging.getLogger(__name__)

class Product(models.Model):
    _inherit='product.product'

    def write(self, vals):
        for rec in self:
            sale_ok = vals.get('sale_ok')
            if sale_ok == True:
                vals['is_website_publish'] = False
            elif sale_ok is None:
                sale_ok = rec.product_tmpl_id.sale_ok

            if vals.get("is_website_publish") == True and sale_ok == True:
                rec.product_tmpl_id.update({"bck_stock_date": None})
            elif vals.get("is_website_publish") == False and sale_ok == True:
                rec.product_tmpl_id.update({"bck_stock_date": datetime.now()})
            else:
                rec.product_tmpl_id.update({"bck_stock_date": rec.bck_stock_date})

        return super(Product, self).write(vals)
