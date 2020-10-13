export function getCookie  (cookie_name) {
  var cookies=document.cookie.split(";");
  var index=cookies.findIndex(item => item.trim().startsWith(cookie_name));

  if(index>0){
    return cookies[index].split("=")[1]
  }
  return null;
}