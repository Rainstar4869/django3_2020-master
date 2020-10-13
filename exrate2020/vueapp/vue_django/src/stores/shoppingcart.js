import {getAPI} from "../axios-api";

const state = {
    accessToken: null,
    cart:null,
    products:null,
    shoppingcart_url: "/store/api/shoppingcart/",
    product_url:"/store/api/product/get/"
};

const mutations = {
    update_cart(state,cart){
        state.cart=cart;
    },
    update_products(state,products){
        state.products=products
        console.log("state.products mutations");
        console.log(state.products);
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
        console.log("update_shoppingcart product_id:"+product_id)
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
        console.log("get_store_active_products");
        axios.post(state.product_url).then((res) => {
            console.log(res.data);
            if(res.data.result=="OK"){
                commit("update_products",res.data.products)
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