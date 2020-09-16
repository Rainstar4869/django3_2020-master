import Vue from 'vue'
import App from './App.vue'
import router from "./routes";
import store from "./stores"
import "bootstrap/dist/css/bootstrap.min.css";

Vue.config.productionTip = false

router.beforeEach((to,from,next)=>{
  if(to.matched.some(record => record.meta.requiresLogin)){
        console.log("auth/loggedIn");
    if(!store.getters["auth/loggedIn"]){
      next({name:"login"});
    }else{
      next();
    }
  }else{
    next();
  }
});

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
