import axios from 'axios';

const localAccessToken =localStorage.getItem("accessToken");
console.log(localAccessToken);
const getAPI = axios.create({
    baseURL: 'http://localhost',
    timeout: 1000,
});

const getAPI_tokenized = axios.create({
    baseURL: 'http://localhost',
    timeout: 1000,
    headers:{Authorization: localAccessToken?"Bearer "+localAccessToken:""}
});

export { getAPI,getAPI_tokenized };