# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "res.users"

    warehouse_ids = fields.Char('warehouse')

    
