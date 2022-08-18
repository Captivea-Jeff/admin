# -*- coding: utf-8 -*-
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute

_logger = logging.getLogger(__name__)

PPG = 28  # Products Per Page
PPR = 4   # Products Per Row

class WebsiteSale(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = 0
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = 0

        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        # Custom code Start
        current_website = request.env['website'].get_current_website()
        if current_website.website_shop_login and (
                request.env.user._is_public() or request.env.user.id == request.website.user_id.id):
            redirect_url = '/web/login?redirect=%s' % (request.httprequest.url)
            if current_website.website_shop_login_redirect:
                redirect_url = '%s?redirect=%s' % (current_website.website_shop_login_redirect, request.httprequest.url)
            else:
                # redirct user to /web/signup if b2c signup is enable
                if current_website.website_auth_signup_uninvited == 'b2c':
                    redirect_url = '/web/signup?redirect=%s' % (request.httprequest.url)
            return request.redirect(redirect_url)
        # Custom Code End

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, min_price=min_price, max_price=max_price, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id, request.website.company_id, fields.Date.today())
        else:
            conversion_rate = 1

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        options = self._get_search_options(
            category=category,
            attrib_values=attrib_values,
            pricelist=pricelist,
            min_price=min_price,
            max_price=max_price,
            conversion_rate=conversion_rate,
            **post
        )
        # No limit because attributes are obtained from complete product list
        product_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
            limit=None, order=self._get_search_order(post), options=options)
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            # TODO Find an alternative way to obtain the domain through the search metadata.
            Product = request.env['product.template'].with_context(bin_size=True)
            domain = self._get_search_domain(search, category, attrib_values)

            # This is ~4 times more efficient than a search for the cheapest and most expensive products
            from_clause, where_clause, where_params = Product._where_calc(domain).get_sql()
            query = f"""
                SELECT COALESCE(MIN(list_price), 0) * {conversion_rate}, COALESCE(MAX(list_price), 0) * {conversion_rate}
                  FROM {from_clause}
                 WHERE {where_clause}
            """
            request.env.cr.execute(query, where_params)
            available_min_price, available_max_price = request.env.cr.fetchone()

            if min_price or max_price:
                # The if/else condition in the min_price / max_price value assignment
                # tackles the case where we switch to a list of products with different
                # available min / max prices than the ones set in the previous page.
                # In order to have logical results and not yield empty product lists, the
                # price filter is set to their respective available prices when the specified
                # min exceeds the max, and / or the specified max is lower than the available min.
                if min_price:
                    min_price = min_price if min_price <= available_max_price else available_min_price
                    post['min_price'] = min_price
                if max_price:
                    max_price = max_price if max_price >= available_min_price else available_max_price
                    post['max_price'] = max_price

        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False), ('website_id', '=', request.context['website_id'])] + website_domain
        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        # Custom Code Start
        company_id = current_website.company_id.id
        node_field = False
        product_list = []
        Product = request.env['product.template'].with_context(bin_size=True)
        domain = self._get_search_domain(search, category, attrib_values)
        order = post.get('order')
        if order:
            node = order.split(" ")
            if node[0]:
                node_field = node[0]
        elif order == None:
            post['order'] = "publish_date desc"
            node_field = "publish_date"
        if node_field == 'sales_pricelist' or node_field == 'publish_date':
            product_list_values = self._company_dependent_order_by(company_id, Product, categs, domain, url, page, ppg,
                                                                   post)
            product_list = product_list_values.get('product_list')
            product_count = product_list_values.get('product_count')
            pager = product_list_values.get('pager')
        if len(product_list) > 0 and post.get('search') is None:
            products = Product.browse(product_list)
        else:
            product_count = Product.search_count(domain)
            pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
            products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
        # Custom Code End

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([
                ('product_tmpl_ids', 'in', selected_products.ids),
                ('visibility', '=', 'visible'),
            ])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': fuzzy_search_term or search,
            'original_search': fuzzy_search_term and search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
            'url':url,
        }
        if filter_by_price_enabled:
            values['min_price'] = min_price or available_min_price
            values['max_price'] = max_price or available_max_price
            values['available_min_price'] = tools.float_round(available_min_price, 2)
            values['available_max_price'] = tools.float_round(available_max_price, 2)
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    def _company_dependent_order_by(self, company_id, Product, categs, domain, url, page, ppg, post):

        ir_property = request.env['ir.property']
        ir_property_ids = False
        ir_domain = []
        product_ids = request.env['product.template']

        node = post.get('order').split(" ")
        node_field = node[0]
        node_order = node[1]

        if node_field and node_order:

            ir_domain += [('name', '=', node_field), ('company_id', '=', company_id)]

            if node_field == "publish_date":
                order = "value_datetime " + str(node_order)
            else:
                order = "value_float " + str(node_order)

            if categs:
                domain += [('public_categ_ids', 'child_of', [x.id for x in categs])]
                product_ids = Product.search(domain).ids

            res_ids = []
            for res_id in product_ids:
                res_ids.append('product.template,' + str(res_id))

            if len(res_ids) > 0:
                ir_domain += [('res_id', 'in', res_ids)]

            product_count = ir_property.search_count(ir_domain)
            pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
            ir_property_ids = ir_property.search(ir_domain, limit=ppg, offset=pager['offset'], order=order)

        product_list = []
        if ir_property_ids:
            for ir_property_id in ir_property_ids:
                res_id = ir_property_id.res_id
                res_val = res_id.split(',')
                product_id = int(res_val[1])
                product_list.append(product_id)

        return {"product_list": product_list, "product_count": product_count, "pager": pager}
