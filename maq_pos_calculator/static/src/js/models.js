odoo.define('maq_pos_calculator.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('pos.order', ['ordered_cannabis']);
    models.load_fields('pos.config', ['cannabis_purchase_limit']);
    models.load_fields('product.product', ['product_format', 'reporting_weight', 'equivalent_weight']);

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({

        save_to_db: function(){
            var OrderLines = this.get_orderlines();
            this.ordered_cannabis = 0.0;
            for (var i = 0, len = OrderLines.length; i < len; i++) {
                this.ordered_cannabis += OrderLines[i].quantity * OrderLines[i].product.equivalent_weight;
            }

            this.ordered_cannabis = this.ordered_cannabis;
            if (!this.temporary && !this.locked) {
                this.pos.db.save_unpaid_order(this);
            }
            $('.product_weight').text(this.ordered_cannabis);
            if (this.ordered_cannabis > this.pos.config.cannabis_purchase_limit){
                $('.product_weight').removeClass("text-green");
                $('.product_weight').addClass("text-red");
            } else{
                $('.product_weight').removeClass("text-red");
                $('.product_weight').addClass("text-green");
            }
        },

        initialize: function (session, attributes) {
            _super_order.initialize.apply(this,arguments);
            this.ordered_cannabis = this.ordered_cannabis || 0.0;
            this.save_to_db();
        },

        init_from_JSON: function(json){
            _super_order.init_from_JSON.apply(this,arguments);
            this.ordered_cannabis = json.ordered_cannabis || 0.0;
        },

        export_as_JSON: function(){
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.ordered_cannabis = this.get_ordered_cannabis();
            return json;
        },

        get_ordered_cannabis() {
            return this.ordered_cannabis;
        },

    });

});
