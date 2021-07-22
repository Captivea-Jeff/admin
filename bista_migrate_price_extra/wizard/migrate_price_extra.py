# -*- coding: utf-8 -*-

import logging

from odoo import api, models, fields, tools, _
from odoo.exceptions import UserError, Warning
import base64
import xlrd

_logger = logging.getLogger(__name__)


class MigratePriceExtra(models.TransientModel):
    _name = "migrate.price.extra"
    _description = "Migrate Price Extra"

    company_id = fields.Many2one('res.company', 'Company')
    file = fields.Binary('File')
    filename = fields.Char()

    def migrate_price_extra(self):
        # Company: Cannabis Point of sale. Company_id = 4
        if not self.company_id:
            raise Warning(_("Please select Company"))
        if not self.file:
            raise Warning(_("Please upload a file"))
        try:
            file_path = '/tmp/price_extra_%s' % (self.company_id.name)
            fp = open(file_path, 'wb')
            fp.write(base64.decodestring(self.file))
            fp.close()
            xl_workbook = xlrd.open_workbook(file_path)
        except Exception:
            raise Warning(_("Bad file format."))
        # cannabis_pos_data = [[52491,'Dried Cannabis - SK - Aurora Banana Split Flower - Format:',164,10,'1.0g',10.6], [52491,'Dried Cannabis - SK - Aurora Banana Split Flower - Format:',166,10,'3.5g',33.3]]
        worksheet = xl_workbook.sheet_by_index(0)
        product_template_obj = self.env['product.template']
        product_attr_obj = self.env['product.attribute.value']
        product_attribute_value_obj = self.env['product.template.attribute.value']
        for row_index in range(1, worksheet.nrows):
            price_extra = worksheet.cell_value(row_index, 6)
            if price_extra != 0:
                product_tmpl_id = product_template_obj.search([('name', '=', str(worksheet.cell_value(row_index, 2)))], limit=1)
                if product_tmpl_id:
                    product_attr_value_id = product_attr_obj.search([('attribute_id', '=', int(worksheet.cell_value(row_index, 4))), ('name', '=', str(worksheet.cell_value(row_index, 5)).strip())], limit=1)
                    if product_attr_value_id:
                        tmpl_extra_price = product_attribute_value_obj.search([('product_tmpl_id', '=', product_tmpl_id.id), ('product_attribute_value_id', '=', product_attr_value_id.id)], limit=1)
                        tmpl_extra_price.sudo().with_context(company_id=self.company_id.id).write({'price_extra': price_extra})
