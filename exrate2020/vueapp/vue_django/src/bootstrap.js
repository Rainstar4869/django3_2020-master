import {getCookie} from "./utils/common.js";

window.axios = require('axios');

window.axios.defaults.headers.common = {
	'X-Requested-With': 'XMLHttpRequest',
	'X-CSRFTOKEN': document.querySelector('meta[name="csrf_token"]').content,
	'Content-Type': 'application/json'
};
window.axios.defaults.headers.Accept='application/json';

let jwt_token =document.querySelector('meta[name="access_token"]').content;

if(jwt_token !==""){
	window.axios.defaults.headers.Authorization=jwt_token;
}
console.log(axios.defaults.headers.Authorization);