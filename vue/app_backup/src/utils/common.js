
import Swal from 'sweetalert2';

export function getCookie  (cookie_name) {
  var cookies=document.cookie.split(";");
  var index=cookies.findIndex(item => item.trim().startsWith(cookie_name));

  if(index>-1){
    return cookies[index].split("=")[1]
  }
  return null;
}

export function sweetalert_toast(msgType,position,message) {
  const Toast = Swal.mixin({
    toast: true,
    position: position,
    showConfirmButton: false,
    timer: 3000,
  });

  Toast.fire({
    icon:msgType,
    title: message
  });
}