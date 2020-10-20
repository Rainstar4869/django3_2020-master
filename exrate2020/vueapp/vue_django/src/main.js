require('./bootstrap');
import Vue from 'vue';
import Cart from './components/Cart.vue';
import Topmenucart from './components/TopMenuCart.vue';
import Products from './components/Product.vue';
import Menunavi from './components/MenuNavi.vue';
import Membertree from './components/MemberTree.vue';
import Topsocialcart from './components/TopSocialCart.vue';
import Shippingaddress from './components/ShippingAddress.vue';
import store from "./stores.js";
import msaFilters from './utils/filters.js';
Vue.filter('currency', msaFilters.currency);
Vue.filter('currency_jpy', msaFilters.currency_jpy);
Vue.filter('currency_rmb', msaFilters.currency_rmb);
Vue.filter('filterUsername', msaFilters.filterUsername);


const elCartComponent = document.getElementById("cart");
const elTopMenuCartComponent = document.getElementById("topmenucart");
const elProductsComponent = document.getElementById("products");
const elMenuNaviComponent = document.getElementById("menunavi");
const elMemberTreeComponent = document.getElementById("membertree");
const elTopSocialCartComponent = document.getElementById("topsocialcart");
const elShippingAddressComponent = document.getElementById("shippingaddressbook");


if (elTopSocialCartComponent) {
    const TopSocialCartComponent = new Vue({
        el: '#topsocialcart',
        store,
        components: {
            Topsocialcart
        }
    });
}


if (elShippingAddressComponent) {
    const ShippingAddressComponent = new Vue({
        el: '#shippingaddressbook',
        store,
        components: {
            Shippingaddress
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

