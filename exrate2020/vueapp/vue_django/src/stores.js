import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";
import auth from "./modules/auth";
import shoppingcart from "./stores/shoppingcart.js";

Vue.use(Vuex);
const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
    modules: {
        auth,
        shoppingcart
    },
    // strict: true,
    plugins: [createPersistedState()],
    strict: debug
});