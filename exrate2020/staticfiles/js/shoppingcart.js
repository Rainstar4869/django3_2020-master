import {getCookie,ToastMessage} from "./utils.js";

const TopCartNumber = document.querySelector(".top-cart-number");
const ProductModal = document.querySelector("#ProductModal");
const ProductName = document.querySelector("#product_name");
const ProductDiscountPrice = document.querySelector("#product_discountprice");
const ProductPrice = document.querySelector("#product_price");
const ProductImage = document.getElementById("product_image");
const ProductDescription = document.getElementById("product_description");
const ProductModal_minus = document.getElementById("ProductModal_minus");
const ProductModal_plus = document.getElementById("ProductModal_plus");
const ProductModal_quantity = document.getElementById("ProductModal_quantity");


var accessToken = getCookie("accessToken");
const baseUrl="/store/api/add-to-cart/";

function AddToCart(e) {
    var product_id = e.target.getAttribute("product_id");
    var url = baseUrl+product_id+"/";

    console.log(url);
    console.log(accessToken);

    if (accessToken !== undefined && accessToken !== null) {
        fetch(baseUrl, {
            body: JSON.stringify({product_id: product_id}),
            method: "POST",
            headers: {
                'Authorization': accessToken,
            }
        }).then((res) => res.json()).then((data) => {
            console.log(data);
            console.log(data.order_count);
            TopCartNumber.innerHTML = data["order_count"];

            ToastMessage("success","Add successfully!");
        });
    } else {
        window.location.href = "/webauth/login/";
    }

}

function ShowProduct(e){
    var product_id = e.target.getAttribute("product_id");
    var url = "/store/api/product/get/";

    console.log(url);
    console.log(accessToken);

    fetch(url, {
            body: JSON.stringify({product_id: product_id}),
            method: "POST",
            headers: {
                'Authorization': accessToken,
            }
        }).then((res) => res.json()).then((data) => {
            console.log(data);
            if (data.result ==="OK"){
                console.log(data.product.description);
                ProductName.innerHTML=data.product.item_name;
                ProductDiscountPrice.innerHTML="¥"+data.product.discount_price;
                ProductPrice.innerHTML="¥"+data.product.price;
                // document.getElementById("product_image").src = 'img/new-image.jpg';
                ProductImage.src=data.product.image;
                ProductDescription.innerHTML=data.product.description;

                ToastMessage("success","OK");
            }
            // console.log(data.order_count);
            // TopCartNumber.innerHTML = data["order_count"];
        });

    $('#ProductModal').modal('toggle');
}
document.querySelectorAll(".btnAddToCart").forEach(item => {
    item.addEventListener("click",AddToCart);
});


document.querySelectorAll(".btnShowProduct").forEach(item => {
    item.addEventListener("click",ShowProduct);
});
