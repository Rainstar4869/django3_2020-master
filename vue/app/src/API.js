// let objCSRF=document.querySelector('meta[name="csrf_token"]');
// // let objJWTTOKEN =document.querySelector('meta[name="access_token"]');
// //
// // const axiosBase = require('axios');
// // window.axios = axiosBase.create({
// //   baseURL: 'http://localhost', // バックエンドB のURL:port を指定する
// //   headers: {
// //     'Content-Type': 'application/json',
// //     'X-Requested-With': 'XMLHttpRequest',
// //     'X-CSRFTOKEN': objCSRF?objCSRF.content:'',
// //     'Authorization': objJWTTOKEN?objJWTTOKEN.content:''
// //   },
// //   responseType: 'json'
// // });
// //
// // window.lionhu='Hu';

import axios from 'axios';
const accessToken=sessionStorage.getItem('accessToken');
axios.defaults.baseURL = process.env.VUE_APP_ROOT_API;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common.Authorization = accessToken;

export function fileUpload(repository, params) {
  return new Promise(resolve => {
    const payload = axios
      .post(`${repository}`, params, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      })
      .then(response => {
        return { payload: response };
      })
      .catch(error => {
        return { error };
      });
    console.log(payload);
    resolve(payload);
  });
}


export function get(repository, params) {
  return new Promise(resolve => {
    const payload = axios
      .get(`${repository}`, params, {
        headers: {
          'content-type': 'application/json',
          'Authorization': accessToken?accessToken:''
        },
      })
      .then(response => {
        return { payload: response };
      })
      .catch(error => {
        return { error };
      });
    resolve(payload);
  });
}

export function post(repository, params) {
  return new Promise(resolve => {
    const payload = axios
      .post(`${repository}`, params, {
        headers: {
          'content-type': 'application/json',
          'Authorization': accessToken?accessToken:''
        },
      })
      .then(response => {
        return { payload: response };
      })
      .catch(error => {
        return { error };
      });
    resolve(payload);
  });
}
