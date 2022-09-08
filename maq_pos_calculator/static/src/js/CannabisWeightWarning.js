odoo.define('maq_point_of_sale.CannabisWeightWarning', function(require) {
'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');

    const CustomerVarify = ProductScreen => class extends ProductScreen {
        async _onClickPay() {
            var order = this.env.pos.get_order();
            var config = this.env.pos.config.payment_confirmation_box;
            if (order.ordered_cannabis > this.env.pos.config.cannabis_purchase_limit) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t("CANNABIS WEIGHT CHECK WARNING"),
                    body: this.env._t('The equivalency of the contents of Cannabis Products in your cart exceeds the customer\'s Public Possession Limit.'),
                    msg: this.env._t('Please adjust the order accordingly in order to process payment.'),
                });
                return false;
            }
            super._onClickPay(...arguments)
        }
    }

    Registries.Component.extend(ProductScreen, CustomerVarify);
    return ProductScreen;

});
