import {sweetalert_toast} from '../utils/common.js'
import {getCookie} from '../utils/common'

const state = {
    accessToken: null,
    cart:null,
    products:[],
    categories:[],
    margins:[],
    category_products:[],
    shippingaddress:[],
    shoppingcart_url: "/store/api/shoppingcart/",
    product_url:"/store/api/product/get/",
    categories_url:"/store/api/categories/",
};

const mutations = {
    update_cart(state,cart){
        state.cart=cart;
    },
    update_products(state,products){
        state.products=products
    },
    update_categories(state,categories){
        state.categories=categories;
    },
    update_margins(state,margins){
        state.margins=margins;
    },
    update_shippingaddress(state,shippingaddress){
        state.shippingaddress=shippingaddress;
    },
    update_accessToken(state){
        state.accessToken=getCookie("accessToken");
    }
};

const actions = {
    get_shoppingcart({commit, state}) {
        axios.get(state.shoppingcart_url).then((res) => {
            if(res.data.result=="OK"){
                commit("update_cart",res.data.cart)
            }
        }).catch(function (error) {
            console.log(error)
        });
        commit("update_accessToken");

    },
    update_shoppingcart({commit, state}, {actionType, product_id}) {
        axios.post(state.shoppingcart_url, JSON.stringify({
            product_id: product_id,
            action: actionType
        })).then((res) => {
            console.log(res.data);
            if(res.data.result=="OK"){
                commit("update_cart",res.data.cart);
                sweetalert_toast("success","top-end","successfully updated!");
            }
        }).catch(function (error) {
            sweetalert_toast("error","top-end","Something Wrong!");
            console.log(error)
        });
    },
    get_store_active_products({commit, state}) {
        axios.post(state.product_url).then((res) => {
            if(res.data.result=="OK"){
                commit("update_products",res.data.products)
            }
        }).catch(function (error) {
            console.log(error)
        });
    },
    get_categories({commit}){
        axios.post(state.categories_url).then((res) => {
            if(res.data.result=="OK"){
                commit("update_categories",res.data.categories);
            }
        }).catch(function (error) {
            console.log(error)
        });
    },
    load_category_products({commit},category_id){
        // const url = "/store/api/category/products/";

        const url = "/store/api/products/list_by_category/";
        axios.post(url,{category_id:category_id}).then((res) => {
            if(res.data.result=="OK"){
                commit("update_products",res.data.products);
            }
        }).catch(function (error) {
            console.log(error)
        });
    },
    load_shippingaddress({commit}){
        var baseUrl = "/store/account/shippingaddress/";
        axios.get(baseUrl).then((res) => {
            if(res.data.result=="OK"){
                commit("update_shippingaddress",res.data.shippingaddress);
            }
        }).catch(function (error) {
            console.log(error)
        });
    },
    load_margins({commit}){
        var baseUrl = "/store/api/margins/";
        axios.get(baseUrl).then((res) => {
            console.log(res.data)
            if(res.data.result=="OK"){
                commit("update_margins",res.data.margins);
            }
        }).catch(function (error) {
            console.log(error)
        });
    }
};

const getters = {
    loggedIn(state) {
        return state.accessToken != null;
    }
};
export default {
    namespaced: true,
    state,
    mutations,
    getters,
    actions
};