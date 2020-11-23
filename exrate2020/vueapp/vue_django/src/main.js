require('./bootstrap');
import Vue from 'vue';
import moment from 'moment'

import Cart from './components/Cart.vue';
import Topmenucart from './components/TopMenuCart.vue';
import Products from './components/Product.vue';
import Menunavi from './components/MenuNavi.vue';
import Membertree from './components/MemberTree.vue';
import Topsocialcart from './components/TopSocialCart.vue';
import Shippingaddressedit from './components/ShippingAddressEdit.vue';
import Shippingaddressform from './components/ShippingAddressForm.vue';
import Pingocheckout from './components/Pingo_checkout.vue';
import store from "./stores.js";
import msaFilters from './utils/filters.js';
Vue.filter('currency', msaFilters.currency);
Vue.filter('currency_jpy', msaFilters.currency_jpy);
Vue.filter('currency_rmb', msaFilters.currency_rmb);
Vue.filter('filterUsername', msaFilters.filterUsername);

Vue.prototype.$moment = moment;
moment.locale('zh-cn');

const elCartComponent = document.getElementById("cart");
const elTopMenuCartComponent = document.getElementById("topmenucart");
const elProductsComponent = document.getElementById("products");
const elMenuNaviComponent = document.getElementById("menunavi");
const elMemberTreeComponent = document.getElementById("membertree");
const elTopSocialCartComponent = document.getElementById("topsocialcart");
const elShippingAddressEditComponent = document.getElementById("shippingaddress_edit");
const elShippingAddressFormComponent = document.getElementById("shippingaddressform");
const elPingoCheckout = document.getElementById("pingocheckout");


if (elPingoCheckout) {
    const _PingoCheckout = new Vue({
        el: '#pingocheckout',
        store,
        components: {
            Pingocheckout
        }
    });
}

if (elShippingAddressFormComponent) {
    const ShippingaddressForm = new Vue({
        el: '#shippingaddressform',
        store,
        components: {
            Shippingaddressform
        }
    });
}

if (elTopSocialCartComponent) {
    const TopSocialCartComponent = new Vue({
        el: '#topsocialcart',
        store,
        components: {
            Topsocialcart
        }
    });
}

if (elShippingAddressEditComponent) {
    const ShippingAddressEditComponent = new Vue({
        el: '#shippingaddress_edit',
        store,
        components: {
            Shippingaddressedit
        }
    });
}


if (elMemberTreeComponent) {
    const MemberTreeComponent = new Vue({
        el: '#membertree',
        store,
        components: {
            Membertree
        }
    });
}

if (elMenuNaviComponent) {
    const MenuNaviComponent = new Vue({
        el: '#menunavi',
        store,
        components: {
            Menunavi
        }
    });
}


if (elCartComponent) {
    const CartComponent = new Vue({
        el: '#cart',
        store,
        components: {
            Cart
        }
    });
}

if (elProductsComponent) {
    const ProductsComponent = new Vue({
        el: '#products',
        store,
        components: {
            Products
        }
    });
}
if (elTopMenuCartComponent) {
    const TopMenuCartComponent = new Vue({
        el: '#topmenucart',
        store,
        components: {
            Topmenucart
        }
    });
}

