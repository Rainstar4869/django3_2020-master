require('./bootstrap');
import Vue from 'vue';
import Cart from './components/Cart.vue';
import Topmenucart from './components/TopMenuCart.vue';
import Products from './components/Product.vue';
import store from "./stores.js";
import msaFilters from './utils/filters.js';
Vue.filter('currency', msaFilters.currency);
Vue.filter('currency_jpy', msaFilters.currency_jpy);
Vue.filter('currency_rmb', msaFilters.currency_rmb);
Vue.filter('filterUsername', msaFilters.filterUsername);


const elCartComponent = document.getElementById("cart");
const elTopMenuCartComponent = document.getElementById("topmenucart");
const elProductsComponent = document.getElementById("products");

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

