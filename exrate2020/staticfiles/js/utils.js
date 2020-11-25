export function getCookie  (cookie_name) {
  var cookies=document.cookie.split(";");
  var index=cookies.findIndex(item => item.trim().startsWith(cookie_name));

  if(index>0){
    return cookies[index].split("=")[1]
  }
  return null;
}

export function ToastMessage(m_type,m_message) {
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  Toast.fire({
    icon: m_type,
    title: m_message
  })
}