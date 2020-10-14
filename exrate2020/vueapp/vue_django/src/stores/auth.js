import {getAPI} from "../axios-api";

const state = {
    accessToken: null,
    refreshToken: null,
    APIData: [],
    membertreenodes:null
};

const mutations = {
    updateStorage(state, {access, refresh}) {
        state.accessToken = access;
        state.refreshToken = refresh;
    },
    updateAPIData(state, value) {
        state.APIData = value;
    },
    updateMemberTree(state,profiles){
        state.membertreenodes=profiles
    }
};

const actions = {
    setAPIData({commit}, value) {
        commit("updateAPIData", value);
    },
    userLogin({commit}, usercredentials) {
        return new Promise(((resolve, reject) => {
            getAPI.post("/apiauth/login/", {
                email: usercredentials.username,
                password: usercredentials.password
            }).then(response => {
                if (response.status == 200) {
                    console.log(response);
                    commit("updateStorage", {
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
    },
    get_membertree_node({commit}){
        const get_membertree_url="/apiauth/api/profiles/";
        axios.post(get_membertree_url).then((res) => {
            if(res.data.result=="OK"){
                commit("updateMemberTree",res.data.profiles);
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
}
export default {
    namespaced: true,
    state,
    mutations,
    getters,
    actions
};