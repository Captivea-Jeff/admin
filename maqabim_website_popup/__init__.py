# -*- coding: utf-8 -*-

from . import models

from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


def _update_website_menus(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    res = env['ir.module.module'].search_read([('name', '=', 'maqabim_website_sale')], ['latest_version'], limit=1)
    if res and res[0]['latest_version'] and res[0]['latest_version'].startswith('11.0'):
        # execute only for the database in v12.0
        # TODO: still require control to execute it one time only
        def get_menu_for_website(website):
            return env["website.menu"].search(
                [
                    ("parent_id", "=", False),
                    "|",
                    ("website_id", "=", website.id),
                    ("website_id", "=", False),
                ],
                order="id",
                limit=1,
            )

        def _compute_most_specific_child_ids(menu, current_website_id):
            if not current_website_id:
                return menu.child_id
            else:
                res = env["website.menu"]
                for child_menu in menu.child_id:
                    if (
                        child_menu.website_id and child_menu.website_id.id == current_website_id
                    ) or (
                        not child_menu.website_id
                        and not any(
                            menu.url == child_menu.url
                            and menu.website_id.id == current_website_id
                            for menu in menu.child_id
                        )
                    ):
                        res |= child_menu
                return res

        def max_depth(menu):
            if not menu or not menu.child_id:
                return []

            return max([[menu] + max_depth(child) for child in menu.child_id], key=len)
        
        _logger.info("Restoring website_menu website_ids...")
        env.cr.execute("update website_menu set website_id = 1 where id in (2,22,344,345,346,347,348,349,350,351,352,326,327,176,177,178,179,180,184,185,186,203,204,205,206,207,208,209,210,211,212,213,214,215,216,218,221,222,353,333,331,6,324,5);")
        
        _logger.info("Creating v12 menu items...")
        old = env["website.menu"].search([])
        for website in env["website"].search([]):
            _logger.info("doing {}".format(website.name))
            website_specific_root = env["website.menu"].create(
                {
                    "name": "top menu for {} (ID: {})".format(website.name, website.id),
                    "website_id": website.id,
                }
            )
            root_menu = get_menu_for_website(website)
            v11_children = _compute_most_specific_child_ids(root_menu, website.id)
            # no need to do it recursively as they haven't nested menuitems deeper
            for child in v11_children:
                child.copy({"website_id": website.id, "parent_id": website_specific_root.id})

            _logger.info("v11 children: {}".format(v11_children.mapped("url")))
            _logger.info("v12 children: {}".format(website_specific_root.child_id.mapped("url")))

        new = env["website.menu"].search([]) - old
        _logger.info("newly created: {}".format(new.mapped("id")))
        env["website.menu"].search([("id", "not in", new.mapped("id"))]).unlink()
