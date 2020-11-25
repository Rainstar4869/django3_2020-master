/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"auth": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([1,"vendor"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/babel-loader/lib/index.js?!./node_modules/vue-loader/lib/index.js?!./src/App.vue?vue&type=script&lang=js&":
/*!****************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib??ref--2!./node_modules/vue-loader/lib??vue-loader-options!./src/App.vue?vue&type=script&lang=js& ***!
  \****************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
//
//
//
//
//
//
//
// import Hello from "./components/Hello.vue"
/* harmony default export */ __webpack_exports__["default"] = ({
  name: 'App',
  components: {// Hello,
  },
  created: function created() {
    console.log("from APP");
  }
});

/***/ }),

/***/ "./node_modules/vue-loader/lib/loaders/templateLoader.js?!./node_modules/vue-loader/lib/index.js?!./src/App.vue?vue&type=template&id=7ba5bd90&":
/*!**********************************************************************************************************************************************************************************!*\
  !*** ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/App.vue?vue&type=template&id=7ba5bd90& ***!
  \**********************************************************************************************************************************************************************************/
/*! exports provided: render, staticRenderFns */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return staticRenderFns; });
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _vm._m(0)
}
var staticRenderFns = [
  function() {
    var _vm = this
    var _h = _vm.$createElement
    var _c = _vm._self._c || _h
    return _c("div", [_c("h1", [_vm._v("Hello VUE, finally see you")])])
  }
]
render._withStripped = true



/***/ }),

/***/ "./src/App.vue":
/*!*********************!*\
  !*** ./src/App.vue ***!
  \*********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _App_vue_vue_type_template_id_7ba5bd90___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./App.vue?vue&type=template&id=7ba5bd90& */ "./src/App.vue?vue&type=template&id=7ba5bd90&");
/* harmony import */ var _App_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./App.vue?vue&type=script&lang=js& */ "./src/App.vue?vue&type=script&lang=js&");
/* empty/unused harmony star reexport *//* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */

var component = Object(_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _App_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _App_vue_vue_type_template_id_7ba5bd90___WEBPACK_IMPORTED_MODULE_0__["render"],
  _App_vue_vue_type_template_id_7ba5bd90___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"],
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "src/App.vue"
/* harmony default export */ __webpack_exports__["default"] = (component.exports);

/***/ }),

/***/ "./src/App.vue?vue&type=script&lang=js&":
/*!**********************************************!*\
  !*** ./src/App.vue?vue&type=script&lang=js& ***!
  \**********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_babel_loader_lib_index_js_ref_2_node_modules_vue_loader_lib_index_js_vue_loader_options_App_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../node_modules/babel-loader/lib??ref--2!../node_modules/vue-loader/lib??vue-loader-options!./App.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js?!./node_modules/vue-loader/lib/index.js?!./src/App.vue?vue&type=script&lang=js&");
/* empty/unused harmony star reexport */ /* harmony default export */ __webpack_exports__["default"] = (_node_modules_babel_loader_lib_index_js_ref_2_node_modules_vue_loader_lib_index_js_vue_loader_options_App_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./src/App.vue?vue&type=template&id=7ba5bd90&":
/*!****************************************************!*\
  !*** ./src/App.vue?vue&type=template&id=7ba5bd90& ***!
  \****************************************************/
/*! exports provided: render, staticRenderFns */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_node_modules_vue_loader_lib_index_js_vue_loader_options_App_vue_vue_type_template_id_7ba5bd90___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!../node_modules/vue-loader/lib??vue-loader-options!./App.vue?vue&type=template&id=7ba5bd90& */ "./node_modules/vue-loader/lib/loaders/templateLoader.js?!./node_modules/vue-loader/lib/index.js?!./src/App.vue?vue&type=template&id=7ba5bd90&");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "render", function() { return _node_modules_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_node_modules_vue_loader_lib_index_js_vue_loader_options_App_vue_vue_type_template_id_7ba5bd90___WEBPACK_IMPORTED_MODULE_0__["render"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return _node_modules_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_node_modules_vue_loader_lib_index_js_vue_loader_options_App_vue_vue_type_template_id_7ba5bd90___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"]; });



/***/ }),

/***/ "./src/auth.js":
/*!*********************!*\
  !*** ./src/auth.js ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var vue__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue */ "./node_modules/vue/dist/vue.esm.js");
/* harmony import */ var _App_vue__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./App.vue */ "./src/App.vue");
/* harmony import */ var _stores__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./stores */ "./src/stores.js");



vue__WEBPACK_IMPORTED_MODULE_0__["default"].config.productionTip = false;
new vue__WEBPACK_IMPORTED_MODULE_0__["default"]({
  render: function render(h) {
    return h(_App_vue__WEBPACK_IMPORTED_MODULE_1__["default"]);
  },
  store: _stores__WEBPACK_IMPORTED_MODULE_2__["default"]
}).$mount('#app');

/***/ }),

/***/ "./src/axios-api.js":
/*!**************************!*\
  !*** ./src/axios-api.js ***!
  \**************************/
/*! exports provided: getAPI, getAPI_tokenized */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getAPI", function() { return getAPI; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getAPI_tokenized", function() { return getAPI_tokenized; });
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axios */ "./node_modules/axios/index.js");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_common_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/common.js */ "./src/utils/common.js");


var jwt_token = Object(_utils_common_js__WEBPACK_IMPORTED_MODULE_1__["getCookie"])("accessToken");
var getAPI = axios__WEBPACK_IMPORTED_MODULE_0___default.a.create({
  baseURL: 'http://localhost',
  timeout: 1000
});
var getAPI_tokenized = axios__WEBPACK_IMPORTED_MODULE_0___default.a.create({
  baseURL: 'http://localhost',
  timeout: 1000,
  headers: {
    Authorization: jwt_token ? jwt_token : ""
  }
});


/***/ }),

/***/ "./src/stores.js":
/*!***********************!*\
  !*** ./src/stores.js ***!
  \***********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var vue__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue */ "./node_modules/vue/dist/vue.esm.js");
/* harmony import */ var vuex__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! vuex */ "./node_modules/vuex/dist/vuex.esm.js");
/* harmony import */ var vuex_persistedstate__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! vuex-persistedstate */ "./node_modules/vuex-persistedstate/dist/vuex-persistedstate.es.js");
/* harmony import */ var _stores_auth__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./stores/auth */ "./src/stores/auth.js");
/* harmony import */ var _stores_shoppingcart_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./stores/shoppingcart.js */ "./src/stores/shoppingcart.js");





vue__WEBPACK_IMPORTED_MODULE_0__["default"].use(vuex__WEBPACK_IMPORTED_MODULE_1__["default"]);
var debug = "development" !== 'production';
/* harmony default export */ __webpack_exports__["default"] = (new vuex__WEBPACK_IMPORTED_MODULE_1__["default"].Store({
  modules: {
    auth: _stores_auth__WEBPACK_IMPORTED_MODULE_3__["default"],
    shoppingcart: _stores_shoppingcart_js__WEBPACK_IMPORTED_MODULE_4__["default"]
  },
  // strict: true,
  plugins: [Object(vuex_persistedstate__WEBPACK_IMPORTED_MODULE_2__["default"])()],
  strict: debug
}));

/***/ }),

/***/ "./src/stores/auth.js":
/*!****************************!*\
  !*** ./src/stores/auth.js ***!
  \****************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var core_js_modules_es_object_to_string__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! core-js/modules/es.object.to-string */ "./node_modules/core-js/modules/es.object.to-string.js");
/* harmony import */ var core_js_modules_es_object_to_string__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_object_to_string__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _axios_api__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../axios-api */ "./src/axios-api.js");


var state = {
  accessToken: null,
  refreshToken: null,
  APIData: [],
  membertreenodes: null
};
var mutations = {
  updateStorage: function updateStorage(state, _ref) {
    var access = _ref.access,
        refresh = _ref.refresh;
    state.accessToken = access;
    state.refreshToken = refresh;
  },
  updateAPIData: function updateAPIData(state, value) {
    state.APIData = value;
  },
  updateMemberTree: function updateMemberTree(state, profiles) {
    state.membertreenodes = profiles;
  }
};
var actions = {
  setAPIData: function setAPIData(_ref2, value) {
    var commit = _ref2.commit;
    commit("updateAPIData", value);
  },
  userLogin: function userLogin(_ref3, usercredentials) {
    var commit = _ref3.commit;
    return new Promise(function (resolve, reject) {
      _axios_api__WEBPACK_IMPORTED_MODULE_1__["getAPI"].post("/apiauth/login/", {
        email: usercredentials.username,
        password: usercredentials.password
      }).then(function (response) {
        if (response.status == 200) {
          console.log(response);
          commit("updateStorage", {
            access: response.data.tokens.access,
            refresh: response.data.tokens.refresh
          });
          localStorage.setItem("accessToken", "Bearer " + response.data.tokens.access);
          resolve();
        } else {
          reject();
        }
      });
    });
  },
  get_membertree_node: function get_membertree_node(_ref4) {
    var commit = _ref4.commit;
    var get_membertree_url = "/apiauth/api/profiles/";
    axios.post(get_membertree_url).then(function (res) {
      if (res.data.result == "OK") {
        commit("updateMemberTree", res.data.profiles);
      }
    }).catch(function (error) {
      console.log(error);
    });
  }
};
var getters = {
  loggedIn: function loggedIn(state) {
    return state.accessToken != null;
  }
};
/* harmony default export */ __webpack_exports__["default"] = ({
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
});

/***/ }),

/***/ "./src/stores/shoppingcart.js":
/*!************************************!*\
  !*** ./src/stores/shoppingcart.js ***!
  \************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _utils_common_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/common.js */ "./src/utils/common.js");


var state = {
  accessToken: null,
  cart: null,
  products: [],
  categories: [],
  margins: [],
  category_products: [],
  shippingaddress: [],
  shoppingcart_url: "/store/api/shoppingcart/",
  product_url: "/store/api/product/get/",
  categories_url: "/store/api/categories/"
};
var mutations = {
  update_cart: function update_cart(state, cart) {
    state.cart = cart;
  },
  update_products: function update_products(state, products) {
    state.products = products;
  },
  update_categories: function update_categories(state, categories) {
    state.categories = categories;
  },
  update_margins: function update_margins(state, margins) {
    state.margins = margins;
  },
  update_shippingaddress: function update_shippingaddress(state, shippingaddress) {
    state.shippingaddress = shippingaddress;
  },
  update_accessToken: function update_accessToken(state) {
    state.accessToken = Object(_utils_common_js__WEBPACK_IMPORTED_MODULE_0__["getCookie"])("accessToken");
  }
};
var actions = {
  get_shoppingcart: function get_shoppingcart(_ref) {
    var commit = _ref.commit,
        state = _ref.state;
    axios.get(state.shoppingcart_url).then(function (res) {
      if (res.data.result == "OK") {
        commit("update_cart", res.data.cart);
      }
    }).catch(function (error) {
      console.log(error);
    });
    commit("update_accessToken");
  },
  update_shoppingcart: function update_shoppingcart(_ref2, _ref3) {
    var commit = _ref2.commit,
        state = _ref2.state;
    var actionType = _ref3.actionType,
        product_id = _ref3.product_id;
    axios.post(state.shoppingcart_url, JSON.stringify({
      product_id: product_id,
      action: actionType
    })).then(function (res) {
      console.log(res.data);

      if (res.data.result == "OK") {
        commit("update_cart", res.data.cart);
        Object(_utils_common_js__WEBPACK_IMPORTED_MODULE_0__["sweetalert_toast"])("success", "top-end", "successfully updated!");
      }
    }).catch(function (error) {
      Object(_utils_common_js__WEBPACK_IMPORTED_MODULE_0__["sweetalert_toast"])("error", "top-end", "Something Wrong!");
      console.log(error);
    });
  },
  get_store_active_products: function get_store_active_products(_ref4) {
    var commit = _ref4.commit,
        state = _ref4.state;
    axios.post(state.product_url).then(function (res) {
      if (res.data.result == "OK") {
        commit("update_products", res.data.products);
      }
    }).catch(function (error) {
      console.log(error);
    });
  },
  get_categories: function get_categories(_ref5) {
    var commit = _ref5.commit;
    axios.post(state.categories_url).then(function (res) {
      if (res.data.result == "OK") {
        commit("update_categories", res.data.categories);
      }
    }).catch(function (error) {
      console.log(error);
    });
  },
  load_category_products: function load_category_products(_ref6, category_id) {
    var commit = _ref6.commit;
    // const url = "/store/api/category/products/";
    var url = "/store/api/products/list_by_category/";
    axios.post(url, {
      category_id: category_id
    }).then(function (res) {
      if (res.data.result == "OK") {
        commit("update_products", res.data.products);
      }
    }).catch(function (error) {
      console.log(error);
    });
  },
  load_shippingaddress: function load_shippingaddress(_ref7) {
    var commit = _ref7.commit;
    var baseUrl = "/store/account/shippingaddress/";
    axios.get(baseUrl).then(function (res) {
      if (res.data.result == "OK") {
        commit("update_shippingaddress", res.data.shippingaddress);
      }
    }).catch(function (error) {
      console.log(error);
    });
  },
  load_margins: function load_margins(_ref8) {
    var commit = _ref8.commit;
    var baseUrl = "/store/api/margins/";
    axios.get(baseUrl).then(function (res) {
      console.log(res.data);

      if (res.data.result == "OK") {
        commit("update_margins", res.data.margins);
      }
    }).catch(function (error) {
      console.log(error);
    });
  }
};
var getters = {
  loggedIn: function loggedIn(state) {
    return state.accessToken != null;
  }
};
/* harmony default export */ __webpack_exports__["default"] = ({
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
});

/***/ }),

/***/ "./src/utils/common.js":
/*!*****************************!*\
  !*** ./src/utils/common.js ***!
  \*****************************/
/*! exports provided: getCookie, sweetalert_toast */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getCookie", function() { return getCookie; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sweetalert_toast", function() { return sweetalert_toast; });
/* harmony import */ var core_js_modules_es_array_find_index__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! core-js/modules/es.array.find-index */ "./node_modules/core-js/modules/es.array.find-index.js");
/* harmony import */ var core_js_modules_es_array_find_index__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_array_find_index__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var core_js_modules_es_regexp_exec__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! core-js/modules/es.regexp.exec */ "./node_modules/core-js/modules/es.regexp.exec.js");
/* harmony import */ var core_js_modules_es_regexp_exec__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_regexp_exec__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var core_js_modules_es_string_split__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! core-js/modules/es.string.split */ "./node_modules/core-js/modules/es.string.split.js");
/* harmony import */ var core_js_modules_es_string_split__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_string_split__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var core_js_modules_es_string_starts_with__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! core-js/modules/es.string.starts-with */ "./node_modules/core-js/modules/es.string.starts-with.js");
/* harmony import */ var core_js_modules_es_string_starts_with__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_string_starts_with__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var core_js_modules_es_string_trim__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! core-js/modules/es.string.trim */ "./node_modules/core-js/modules/es.string.trim.js");
/* harmony import */ var core_js_modules_es_string_trim__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_string_trim__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var sweetalert2__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! sweetalert2 */ "./node_modules/sweetalert2/dist/sweetalert2.all.js");
/* harmony import */ var sweetalert2__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(sweetalert2__WEBPACK_IMPORTED_MODULE_5__);






function getCookie(cookie_name) {
  var cookies = document.cookie.split(";");
  var index = cookies.findIndex(function (item) {
    return item.trim().startsWith(cookie_name);
  });

  if (index > -1) {
    return cookies[index].split("=")[1];
  }

  return null;
}
function sweetalert_toast(msgType, position, message) {
  var Toast = sweetalert2__WEBPACK_IMPORTED_MODULE_5___default.a.mixin({
    toast: true,
    position: position,
    showConfirmButton: false,
    timer: 3000
  });
  Toast.fire({
    icon: msgType,
    title: message
  });
}

/***/ }),

/***/ 1:
/*!******************************************!*\
  !*** multi babel-polyfill ./src/auth.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! babel-polyfill */"./node_modules/babel-polyfill/lib/index.js");
module.exports = __webpack_require__(/*! ./src/auth.js */"./src/auth.js");


/***/ })

/******/ });
//# sourceMappingURL=auth.js.map