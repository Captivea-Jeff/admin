# coding: utf-8

import re

from odoo import fields, models, _

class ProductTemplate(models.Model):
    _inherit='product.template'

    sales_pricelist = fields.Float(
        'Sales Pricelist', default=1.0,
        digits="Product Price", company_dependent=True,
        help="Base price to compute the customer price. Sometimes called the catalog price.")

    def write(self, vals):
        ppi = self.env['product.pricelist.item']
        pricelist_items = ppi.search([('product_tmpl_id','=',self.id)])

        sale_ok = vals.get('sale_ok')

        if sale_ok is None:
            sale_ok = self.sale_ok

        if pricelist_items is not None and sale_ok == True:

            for pricelist_item in pricelist_items:

                if type(pricelist_item) is not list:

                    if pricelist_item.min_quantity in [0, 1] and pricelist_item.date_start == False and pricelist_item.date_end == False:
                        fixed_price = pricelist_item.fixed_price
                        vals.update({'sales_pricelist': fixed_price})

                elif pricelist_item[2] is not False:

                    min_quantity = pricelist_item[2].get('min_quantity')
                    date_start = pricelist_item[2].get('date_start')
                    date_end = pricelist_item[2].get('date_end')
                    fixed_price = pricelist_item[2].get('fixed_price')

                    if re.search("virtual_",str(pricelist_item[1])):

                        if min_quantity in [0,1] and date_start == False and date_end == False:
                            vals.update({'sales_pricelist': fixed_price})
                    else:

                        if pricelist_item[2].get('fixed_price') or pricelist_item[2].get('min_quantity') in [0,1]:
                            ppi_item = ppi.browse(pricelist_item[1])
                            if date_start is None:
                                date_start = ppi_item.date_start
                            if date_end is None:
                                date_end = ppi_item.date_end
                            if min_quantity is None:
                                min_quantity = ppi_item.min_quantity
                            if min_quantity in [0,1] and date_start == False and date_end == False:
                                if fixed_price is None:
                                    fixed_price = ppi_item.fixed_price
                                vals.update({'sales_pricelist': fixed_price})
        else:
            vals.update({'sales_pricelist': 0})

        result = super(ProductTemplate, self).write(vals)

        return result
