import {getCookie} from "./utils/common.js";

window.axios = require('axios');

window.axios.defaults.headers.common = {
	'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
};

let jwt_token =getCookie("accessToken");

if(jwt_token !==""){
	window.axios.defaults.headers = {
		'X-CSRFToken': getCookie("csrftoken"),
	    'accept': 'application/json',
	    'Authorization': jwt_token
	};
}else{
	window.axios.defaults.headers.Accept='application/json';
}
