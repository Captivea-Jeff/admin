odoo.define('maq_pos_calculator.OrderWeightWidget', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class OrderWeightWidget extends PosComponent {
        get purchase_weight_limit() {
            const cannabis_purchase_limit = this.env.pos.config.cannabis_purchase_limit;
            return cannabis_purchase_limit;
        }
        get ordered_cannabis() {
            var order = this.env.pos.get_order();
            const ordered_cannabis = order.get_ordered_cannabis();
            return ordered_cannabis;
        }
    }
    OrderWeightWidget.template = 'OrderWeightWidget';

    Registries.Component.add(OrderWeightWidget);

    return OrderWeightWidget;
});
