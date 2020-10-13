require('./bootstrap');
import Vue from 'vue';
import Hello from './components/Hello.vue';
import store from "./stores.js";

// const MainContent=new Vue({
//     el: '#app',
//     // store,
//     render: h => h(Hello)
// });

const mainContent = new Vue({
    el: '#app',
    store,
    components:{
        Hello
    }
})