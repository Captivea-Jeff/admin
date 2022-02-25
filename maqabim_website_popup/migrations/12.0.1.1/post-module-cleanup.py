# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# from odoo.addons.base.maintenance.migrations import util


def migrate(cr, version):
    print("Enabling multi-website...")
    # cr.execute("insert into res_groups_users_rel (uid, gid) values (2, (select id from res_groups where name = 'Multi-website'));")
    cr.execute("update ir_module_module set state = 'uninstalled' where name = 'website_multi';")
    cr.execute("update ir_ui_view set active = 'f' where id in (select res_id from ir_model_data where module = 'website_multi');")

    print("Moving registered_on_website_id to website_id on the res.partner...")
    cr.execute("UPDATE res_partner SET website_id = res_users.registered_on_website_id FROM res_users WHERE res_partner.user_id = res_users.id;")
    cr.execute("UPDATE res_users SET website_id = registered_on_website_id;")
    # util.remove_module(cr, "website_multi")
