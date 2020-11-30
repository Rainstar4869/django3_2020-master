export default function ({$axios, $store}, inject) {
  // Create a custom axios instance

  const funAPI_token = async function (accessToken) {
    const api = $axios.create({
      headers: {
        common: {
          'Accept': 'application/json',
        },
        'Content-Type': 'application/json',
        'Authorization': accessToken
      },
    });
    return api;
  };

  const funAPI = async function () {
    const api = $axios.create({
      headers: {
        common: {
          'Accept': 'application/json',
        },
        'Content-Type': 'application/json',
      },
    });
    console.log("from api axios");
    return api;
  };


  // Inject to context as $api
  inject('api_accesstoken', funAPI_token);
  inject('api', funAPI);
}
