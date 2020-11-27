// import {getCookie} from './utils/common.js';

window.axios = require('axios');

let objCSRF=document.querySelector('meta[name="csrf_token"]');
let objJWTTOKEN =document.querySelector('meta[name="access_token"]');

window.axios.defaults.headers.common = {
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFTOKEN': objCSRF?objCSRF.content:'',
    'Content-Type': 'application/json',
    'Authorization': objJWTTOKEN?objJWTTOKEN.content:''
};
// window.axios.defaults.headers.Accept='application/json';
//
//
// if(jwt_token !==""){
// 	window.axios.defaults.headers.Authorization=jwt_token;
// }