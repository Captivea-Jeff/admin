# coding: utf-8

import logging

from odoo import api, fields, models, tools, _
from odoo.tools import pycompat
from odoo.tools import float_compare
# from odoo.addons import decimal_precision as dp
# from odoo.exceptions import UserError, ValidationError
# from datetime import datetime

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _get_combination_info_variant(self, add_qty=1, pricelist=False, parent_combination=False):
        """Return the variant info based on its combination.
        See `_get_combination_info` for more information.
        """
        self.ensure_one()
        return self.product_tmpl_id._get_combination_info(self.product_template_attribute_value_ids, self.id, add_qty,
                                                          pricelist, parent_combination)


