odoo.define('bista_website_sale_options.custom_website_sale_options', function(require) {
"use strict";

var ajax = require('web.ajax');
var wSaleUtils = require('website_sale.utils');

$(document).on('click', '#quick_add_from_shop', function(){
     var arg1 = parseInt(event.target.children.product_id.value);
     var qty = parseInt(event.target.children.add_qty.value);
        ajax.jsonRpc("/shop/cart/update_json", 'call', {'product_id':arg1,'set_qty':qty}).then(function (data) {
            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showWarning(data.warning);
        });
 });
});