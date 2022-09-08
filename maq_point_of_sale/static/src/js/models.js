odoo.define('maq_point_of_sale.models', function (require) {
    "use strict";

    var rpc = require("web.rpc");
    var models = require('point_of_sale.models');
    var exports = {};

    models.load_fields("pos.order", ['customer_verified']);

//    models.load_models([
//        {
//            model:  'product.product',
//            label: 'load_products',
//            condition: function (self) { return !self.config.limited_products_loading; },
//            fields: ['display_name', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id',
//                     'barcode', 'default_code', 'to_weight', 'uom_id', 'description_sale', 'description',
//                     'product_tmpl_id','tracking', 'write_date', 'available_in_pos', 'attribute_line_ids', 'active'],
//            order:  _.map(['sequence','default_code','name'], function (name) { return {name: name}; }),
//            domain: function(self){
//                var domain = ['&', '&', ['sale_ok','=',true],['available_in_pos','=',true],'|',['company_id','=',self.config.company_id[0]],['company_id','=',false]];
//                if (self.config.limit_categories &&  self.config.iface_available_categ_ids.length) {
//                    domain.unshift('&');
//                    domain.push(['pos_categ_id', 'not in', self.config.iface_available_categ_ids]);
//                }
//                if (self.config.iface_tipproduct){
//                  domain.unshift(['id', '=', self.config.tip_product_id[0]]);
//                  domain.unshift('|');
//                }
//
//                return domain;
//            },
//            context: function(self){ return { display_default_code: false }; },
//            loaded: function(self, products){
//                var using_company_currency = self.config.currency_id[0] === self.company.currency_id[0];
//                var conversion_rate = self.currency.rate / self.company_currency.rate;
//                self.db.add_products(_.map(products, function (product) {
//                    if (!using_company_currency) {
//                        product.lst_price = round_pr(product.lst_price * conversion_rate, self.currency.rounding);
//                    }
//                    product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
//                    product.pos = self;
//                    return new models.Product({}, product);
//                }));
//            },
//        },
//    ])
//
//    models.load_models([
//        {
//            model:  'pos.category',
//            fields: ['id', 'name', 'parent_id', 'child_id', 'write_date'],
//            domain: function(self) {
//                return self.config.limit_categories && self.config.iface_available_categ_ids.length ? [['id', 'not in', self.config.iface_available_categ_ids]] : [];
//            },
//            loaded: function(self, categories){
//                console.log("console.log()====----------------------------=>", categories)
//                self.db.add_categories(categories);
//                console.log("self.db======>", self.db)
//            },
//        }
//    ])

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (session, attributes) {
            _super_order.initialize.apply(this, arguments);
            this.customer_verified = this.customer_verified || false;
        },
        init_from_JSON: function (json) {
            _super_order.init_from_JSON.apply(this, arguments);
            this.customer_verified = json.customer_verified || false;
        },
        export_as_JSON: function () {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            json.customer_verified = this.get_customer_verified();
            return json;
        },
        apply_ms_data: function (data) {
            if (_super_order.apply_ms_data) {
                _super_order.apply_ms_data.apply(this, arguments);
            }
            this.customer_verified = data.customer_verified || false;
        },
        get_customer_verified() {
            return this.customer_verified;
        },
        set_customer_verified(customer_verified) {
            this.customer_verified = customer_verified;
        },
    });
});
