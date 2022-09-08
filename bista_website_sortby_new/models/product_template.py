# coding: utf-8

from odoo import fields, models
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit='product.template'

    publish_date = fields.Datetime('Publish Date', company_dependent=True)

    def write(self, vals):
        for rec in self:
            if vals.get('website_published') == True and vals.get('sale_ok') == True:
                if vals.get('publish_date'):
                    vals['publish_date'] = vals.get('publish_date')
                else:
                    vals['publish_date'] = datetime.now()
            elif vals.get('website_published') == True and rec.sale_ok == True:
                if vals.get('publish_date'):
                    vals['publish_date'] = vals.get('publish_date')
                else:
                    vals['publish_date'] = datetime.now()
            elif vals.get('website_published') == False and vals.get('sale_ok') == True:
                vals['publish_date'] = rec.create_date
            elif rec.website_published == False and vals.get('sale_ok') == True:
                vals['publish_date'] = rec.create_date
            elif vals.get('website_published') == False and rec.sale_ok == True:
                vals['publish_date'] = rec.create_date
            elif vals.get('website_published') == False and vals.get('sale_ok') == False:
                vals['publish_date'] = None
            elif rec.website_published == False and vals.get('sale_ok') == False:
                vals['publish_date'] = None
            elif vals.get('website_published') == False and rec.sale_ok == False:
                vals['publish_date'] = None

        return super(ProductTemplate, self).write(vals)