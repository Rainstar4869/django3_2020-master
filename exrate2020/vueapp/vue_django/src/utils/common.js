export function getCookie  (cookie_name) {
        var result = null;
    var cookieName = name + '=';
    var allcookies = document.cookie;
    var position = allcookies.indexOf( cookie_name );
    if( position !== -1 ) {
      var startIndex = position + cookieName.length;
      var endIndex = allcookies.indexOf( ';', startIndex );
      if( endIndex === -1 ) {
        endIndex = allcookies.length;
      }
      result = decodeURIComponent(allcookies.substring( startIndex, endIndex ));
    }
    return result;

  // var cookies=document.cookie.split(";");
  //
  // var index=cookies.findIndex(item => item.trim().startsWith(cookie_name));
  //
  // if(index>0){
  //   return cookies[index].split("=")[1]
  // }
  // return null;
}