# coding: utf-8

import logging
# import the additional module
import re

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare
# from odoo.exceptions import UserError, ValidationError
# from datetime import datetime

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit='product.template'

    sales_pricelist = fields.Float(
        'Sales Pricelist', default=1.0,
        digits=dp.get_precision('Product Price'), company_dependent=True,
        help="Base price to compute the customer price. Sometimes called the catalog price.")

    @api.multi
    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        """Override for website, where we want to:
            - take the website pricelist if no pricelist is set
            - apply the b2b/b2c setting to the result

        This will work when adding website_id to the context, which is done
        automatically when called from routes with website=True.
        """
        self.ensure_one()

        current_website = False

        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()

        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if self.env.context.get('website_id'):
            partner = self.env.user.partner_id
            company_id = current_website.company_id
            product = self.env['product.product'].browse(combination_info['product_id']) or self

            tax_display = self.env.user.has_group(
                'account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'
            taxes = partner.property_account_position_id.map_tax(
                product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id), product, partner)

            # The list_price is always the price of one.
            quantity_1 = 1
            price = taxes.compute_all(combination_info['price'], pricelist.currency_id, quantity_1, product, partner)[
                tax_display]
            if pricelist.discount_policy == 'without_discount':
                ppis = product.item_ids
                sales_pricelist = False
                for ppi in ppis:
                    if ppi.min_quantity in [0,
                                            1] and ppi.date_start == False and ppi.date_end == False and ppi.pricelist_id.id == pricelist.id:
                        sales_pricelist = ppi.fixed_price

                if sales_pricelist:
                    price_without_pricelist = sales_pricelist
                else:
                    price_without_pricelist = product.list_price
                if company_id.currency_id != pricelist.currency_id:
                    price_without_pricelist = company_id.currency_id.compute(price_without_pricelist,
                                                                             pricelist.currency_id)
                price_without_pricelist = taxes.compute_all(price_without_pricelist, pricelist.currency_id)[tax_display]
                if sales_pricelist:
                    list_price = \
                    taxes.compute_all(price_without_pricelist, pricelist.currency_id, quantity_1, product,
                                      partner)[tax_display]
                else:
                    list_price = \
                        taxes.compute_all(combination_info['list_price'], pricelist.currency_id, quantity_1, product,
                                      partner)[tax_display]
            else:
                list_price = price
            has_discounted_price = pricelist.currency_id.compare_amounts(list_price, price) == 1

            combination_info.update(
                price=price,
                list_price=list_price,
                has_discounted_price=has_discounted_price,
            )

        return combination_info

    @api.multi
    def write(self, vals):
        ppi = self.env['product.pricelist.item']
        pricelist_items = vals.get('item_ids')

        sale_ok = vals.get('sale_ok')

        if sale_ok == True:
            if pricelist_items == None:
                pricelist_items = self.item_ids
        if sale_ok is None:
            sale_ok = self.sale_ok
        if pricelist_items == None:

            pricelist_items = self.item_ids
        # define search string

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

    # @api.multi
    # def _compute_sales_pricelist(self):
    #     ppis = self.item_ids
    #     sales_pricelist = False
    #     for ppi in ppis:
    #         if ppi.min_quantity == 0 and ppi.date_start == False and ppi.date_end == False:
    #             if self.sales_pricelist == ppi.fixed_price:
    #                 continue
    #             else:
    #                 sales_pricelist = ppi.fixed_price
    #
    #     if sales_pricelist:
    #         self.write({"sales_pricelist": sales_pricelist})
