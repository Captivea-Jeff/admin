odoo.define('maq_point_of_sale.CustomerVarify', function(require) {
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
            if (config === true) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Verification'),
                    body: this.env._t('Has this customers ID been verified?'),
                    confirmText: this.env._t('Yes'),
                    cancelText: this.env._t('No')
                });
                if (confirmed) {
                    order.customer_verified = true;
                    super._onClickPay(...arguments)
                }
            }else {
                super._onClickPay(...arguments)
            }
        }
    }
    Registries.Component.extend(ProductScreen, CustomerVarify);
    return ProductScreen;

});
