const digitsRE = /(\d{3})(?=\d)/g;


export default {
  currency(value, currency, decimals) {
    value = parseFloat(value)
    if (!isFinite(value) || (!value && value !== 0)) return ''
    currency = currency != null ? currency : ''
    decimals = decimals != null ? decimals : 0
    var stringified = Math.abs(value).toFixed(decimals)
    var _int = decimals
      ? stringified.slice(0, -1 - decimals)
      : stringified
    var i = _int.length % 3
    var head = i > 0
      ? (_int.slice(0, i) + (_int.length > 3 ? ',' : ''))
      : ''
    var _float = decimals
      ? stringified.slice(-1 - decimals)
      : ''
    var sign = value < 0 ? '-' : ''
    return sign + currency + head +
      _int.slice(i).replace(digitsRE, '$1,') +
      _float
  },

  currency_jpy(value, currency, decimals){
    value = parseFloat(value)
    if (!isFinite(value) || (!value && value !== 0)) return ''
    currency = currency != null ? currency : '¥'
    decimals = decimals != null ? decimals : 0
    var stringified = Math.abs(value).toFixed(decimals)
    var _int = decimals
      ? stringified.slice(0, -1 - decimals)
      : stringified
    var i = _int.length % 3
    var head = i > 0
      ? (_int.slice(0, i) + (_int.length > 3 ? ',' : ''))
      : ''
    var _float = decimals
      ? stringified.slice(-1 - decimals)
      : ''
    var sign = value < 0 ? '-' : ''
    return sign + currency + head +
      _int.slice(i).replace(digitsRE, '$1,') +
      _float+"円"
  },
  currency_rmb(value, currency, decimals){
    value = parseFloat(value)
    if (!isFinite(value) || (!value && value !== 0)) return ''
    currency = currency != null ? currency : ''
    decimals = decimals != null ? decimals : 0
    var stringified = Math.abs(value).toFixed(decimals)
    var _int = decimals
      ? stringified.slice(0, -1 - decimals)
      : stringified
    var i = _int.length % 3
    var head = i > 0
      ? (_int.slice(0, i) + (_int.length > 3 ? ',' : ''))
      : ''
    var _float = decimals
      ? stringified.slice(-1 - decimals)
      : ''
    var sign = value < 0 ? '-' : ''
    return sign + currency + head +
      _int.slice(i).replace(digitsRE, '$1,') +
      _float+"元"
  },

  formateDate(value,formatstr){
    if(value =="" || value ==undefined ){
      return "";
    }
      Date.prototype.Format = function (fmt) { //author: meizz
          var o = {
              "M+": this.getMonth() + 1, //月份
              "d+": this.getDate(), //日
              "h+": this.getHours(), //小时
              "m+": this.getMinutes(), //分
              "s+": this.getSeconds(), //秒
              "q+": Math.floor((this.getMonth() + 3) / 3), //季度
              "S": this.getMilliseconds() //毫秒
          };
          if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
          for (var k in o)
              if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
          return fmt;
      }


      var time=new Date(value).Format(formatstr);
      return time;
  },


  StandardDate(value){
    if(value =="" || value ==undefined ){
      return "";
    }

    var time=value.split("T")[0];
    return time;
  },


  filterUsername(value){
    if(value !="" && value !=undefined){
      var str=value.substr(0,1)+"****"+value.substr(value.length-1,1)
      return str
    }

  }
}
