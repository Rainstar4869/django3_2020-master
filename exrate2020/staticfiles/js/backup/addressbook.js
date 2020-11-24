const btnAddressBook=document.getElementById("btnAddressBook");

btnAddressBook.addEventListener("click",function (e) {
    var baseUrl = "/store/account/shippingaddress/";
    fetch(baseUrl, {
        method: "GET",
    }).then((res) => res.json()).then((data) => {
        console.log(data)
        console.log(data.shippingaddress);
        if (data.result == "OK") {
            $("#addressbook_area").empty();
            var shippingaddressbook = data.shippingaddress;
            shippingaddressbook.forEach(function (elem, index) {
                $("#addressbook_area").append('<div class="toggle">\n' +
                    '<div class="toggle-header">\n' +
                    '<div class="toggle-icon">\n' +
                    '<i class="toggle-closed icon-line-plus"></i>\n' +
                    '<i class="toggle-open icon-line-minus"></i>\n' +
                    '</div>\n' +
                    '<div class="toggle-title">\n' + elem.name + '</div>\n' +
                    '</div>\n' +
                    '<div class="toggle-content">Lorem ipsum dolor sit amet, consectetur adipisicing elit.\n' +
                    '</div>\n' +
                    '</div>');
            })

            $("#AddressBookModal").modal('show');
        }
    });



});


