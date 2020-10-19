import {sweetalert_toast} from "../utils/common.js";

const state = {
    accessToken: null,
    cart:null,
    products:[],
    categories:[],
    category_products:[],
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
    update_category_products(state,products){
        state.category_products=products;
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
    },
    update_shoppingcart({commit, state}, {actionType, product_id}) {
        axios.post(state.shoppingcart_url, JSON.stringify({
            product_id: product_id,
            action: actionType
        })).then((res) => {
            // console.log(res.data);
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
        const url = "/store/api/category/products/";
        axios.post(url,JSON.stringify({category_id:category_id})).then((res) => {
            if(res.data.result=="OK"){
                commit("update_products",res.data.category_products);
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