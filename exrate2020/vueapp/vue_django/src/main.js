require('./bootstrap');


import './styles/style.css';
import Vue from 'vue';
import store from "./stores";
import Hello from './components/Hello.vue';
import Searchexpenses from './components/SearchExpenses.vue';


new Vue({
  el: '#app',
  store,
  components:{
    Hello,
    Searchexpenses,
  }
})
// const routes = [
//   { component: ArticleList, path: '/article/', },
//   { component: AuthorList,  path: '/author/',  },
//   { component: ArticleItem, path: '/article/:slug/', },
//   { component: AuthorItem,  path: '/author/:slug/',  },
// ]
//
// const router = new VueRouter({
//   mode: 'history',
//   routes: routes,
// })
