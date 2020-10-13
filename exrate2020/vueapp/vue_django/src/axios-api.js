import axios from 'axios';
import {getCookie} from "./utils/common.js";

let jwt_token =getCookie("accessToken");
const getAPI = axios.create({
    baseURL: 'http://localhost',
    timeout: 1000,
});

const getAPI_tokenized = axios.create({
    baseURL: 'http://localhost',
    timeout: 1000,
    headers:{Authorization: jwt_token?jwt_token:""}
});

export { getAPI,getAPI_tokenized };