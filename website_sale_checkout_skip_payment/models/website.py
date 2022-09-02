
from odoo import fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"


    checkout_skip_payment = fields.Boolean(compute="_compute_checkout_skip_payment")

    def _compute_checkout_skip_payment(self):
        for rec in self:
            rec.checkout_skip_payment = (
                request.env.user.partner_id.skip_website_checkout_payment
            )
