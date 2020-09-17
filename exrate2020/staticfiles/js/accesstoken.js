console.log("get accesstoke");



const get_accesstoken=()=>{
    const meta_token = document.querySelector("meta['accessToken']").getAttribute('content');

console.log(meta_token);
};
document.onload=get_accesstoken();