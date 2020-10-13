import {getAPI} from "../axios-api";

const state = {
    accessToken: null,
    cart:null,
    products:null,
    categories:[],
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
            console.log(res.data);
            if(res.data.result=="OK"){
                commit("update_cart",res.data.cart)
            }
        }).catch(function (error) {
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
        console.log("get_categories");
        axios.post(state.categories_url).then((res) => {
            if(res.data.result=="OK"){
                commit("update_categories",res.data.categories)
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