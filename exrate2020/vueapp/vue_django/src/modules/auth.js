import {getAPI} from "../axios-api";

const state = {
    accessToken: null,
    refreshToken: null,
    APIData: []
};

const mutations = {
    updateStorage(state, {access, refresh}) {
        state.accessToken = access;
        state.refreshToken = refresh;
    },
    updateAPIData(state, value) {
        state.APIData = value;
    }
};

const actions = {
    setAPIData(context, value) {
        context.commit("updateAPIData", value);
    },
    userLogin(context, usercredentials) {
        return new Promise(((resolve, reject) => {
            getAPI.post("/apiauth/login/", {
                email: usercredentials.username,
                password: usercredentials.password
            }).then(response => {
                if (response.status == 200) {
                    console.log(response);
                    context.commit("updateStorage", {
                        access: response.data.tokens.access,
                        refresh: response.data.tokens.refresh
                    });
                    localStorage.setItem("accessToken", "Bearer " + response.data.tokens.access)
                    resolve();
                } else {

                    reject();
                }
            });
        }));
    }

};

const getters = {
    loggedIn(state) {
        return state.accessToken != null;
    }
}
export default {
    namespaced: true,
    state,
    mutations,
    getters,
    actions
};