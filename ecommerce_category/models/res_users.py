# coding: utf-8

import logging
import pytz
from odoo import api, models, fields, _, SUPERUSER_ID
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    login_website_ids = fields.Many2many(comodel_name='website', relation='user_website_login_check',
                                            column1='user_id', column2='website_id', string='Website Allowed Login ',
                                            help='This field must be used for intenral users authetication only and should not be used for portal users.')
    @api.onchange('company_id', 'company_ids')
    def onchange_company(self):
        user_company_websites = self.env['website'].search([('company_id', 'in', self.company_ids.ids)])
        self.login_website_ids = user_company_websites + self.registered_on_website_id

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        if not password:
            raise AccessDenied()
        ip = request.httprequest.environ['REMOTE_ADDR'] if request else 'n/a'
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                with self._assert_can_auth():
                    user = self.search(self._get_login_domain(login), order=self._get_login_order(), limit=1)
                    if not user:
                        raise AccessDenied()
                    # custom code
                    current_website_id = self.env['website'].get_current_website()
                    if user.id not in (SUPERUSER_ID, 2):
                        # Interal user can auth from different website as some company may 
                        # not have website so auth trough website of other company or
                        # allowed login website.
                        # share user auth to their own own website only.
                        if not user.share:
                            user_company_websites = self.env['website'].search([('company_id', 'in', user.company_ids.ids)])
                            auth_allow_website = user.login_website_ids + user_company_websites
                            print (auth_allow_website)
                            if current_website_id not in user.login_website_ids:
                                _logger.info('Multi-website login failed for db:%s login:%s website_id:%s', db, login, current_website_id)
                                raise AccessDenied()
                        elif current_website_id.company_id.id not in user.company_ids.ids:
                            _logger.info('Multi-website company login failed for db:%s login:%s website_id:%s', db, login, current_website_id)
                            raise AccessDenied()
                    # End Custom Code
                    if user and current_website_id:
                        try:
                            user = user.with_user(user)
                            user._check_credentials(password, user_agent_env)
                            tz = request.httprequest.cookies.get('tz') if request else None
                            if tz in pytz.all_timezones and (not user.tz or not user.login_date):
                                # first login or missing tz -> set tz to browser tz
                                user.tz = tz
                            user._update_last_login()
                        except AccessDenied:
                            _logger.info('Multi-website login failed for db:%s login:%s website_id:%s', db, login, current_website_id)
                            raise AccessDenied()

                    else:
                        raise AccessDenied()

        except AccessDenied:
            _logger.info("Login failed for db:%s login:%s from %s", db, login, ip)
            raise AccessDenied()

        _logger.info("Login successful for db:%s login:%s from %s", db, login, ip)

        return user.id
