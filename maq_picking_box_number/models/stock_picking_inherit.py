# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.tools.float_utils import float_is_zero

class StockMove(models.Model):
    _inherit = 'stock.move'

    '''Added Box number field in stock.move model'''

    m_box_number = fields.Char(string="Box Number")

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super(StockMoveLine, self)._get_aggregated_product_quantities(**kwargs)

        def get_aggregated_properties(move_line=False, move=False):
            move = move or move_line.move_id
            uom = move.product_uom or move_line.product_uom_id
            name = move.product_id.display_name
            description = move.description_picking
            if description == name or description == move.product_id.name:
                description = False
            product = move.product_id
            line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}'
            return (line_key, name, description, uom)

        for move_line in self:
            line_key, name, description, uom = get_aggregated_properties(move_line=move_line)
            aggregated_move_lines[line_key].update({'m_box_number': move_line.move_id.m_box_number})
        return aggregated_move_lines
