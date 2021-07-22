odoo.define('bista_website_sale_options.website_sale_options', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');
    var weContext = require('web_editor.context');
    var core = require('web.core');
    var _t = core._t;
    var OptionalProductsModal = require('sale.OptionalProductsModal');
    OptionalProductsModal.include({
        /**
         * @override
         */
        /**
         * @override
         */
        willStart: function () {
            var self = this;

            var uri = this._getUri("/product_configurator/show_optional_products");
            var getModalContent = ajax.jsonRpc(uri, 'call', {
                product_id: self.rootProduct.product_id,
                variant_values: self.rootProduct.variant_values,
                pricelist_id: self.pricelistId || false,
                add_qty: self.rootProduct.quantity,
                kwargs: {
                    context: _.extend({
                        'quantity': self.rootProduct.quantity
                    }, weContext.get()),
                }
            })
            .then(function (modalContent) {
                if (modalContent) {
                    var $modalContent = $(modalContent);
                    $modalContent = self._postProcessContent($modalContent);
                    self.$content = $modalContent;
                    self._trigger(self);
                } else {
                    self.trigger('options_empty');
                    self.preventOpening = true;
                }
            });

            var parentInit = self._super.apply(self, arguments);
            return $.when(getModalContent, parentInit);
        },
        _trigger: function(action){
            var header = action.$modal[0];
            var title = $(header).find(".modal-title")[0];
            title.innerText = "Product successfully added to your shopping cart";
            var close_button = $(header).find("button.close");
            close_button.hide();
            var footer = action.$footer[0];
            $(footer).hide();
            var btn = footer.firstChild;
            setTimeout(function () {
                $(btn).trigger('click');
            }, 3000);
        }
    });
});
