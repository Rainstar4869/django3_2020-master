
import {getCookie, ToastMessage} from "./utils.js";

const TopCartNumbers = document.querySelectorAll(".top-cart-number");
const CartTotal = document.querySelectorAll(".order_total");
const ProductModal = document.querySelector("#ProductModal");
const ProductName = document.querySelector("#product_name");
const ProductDiscountPrice = document.querySelector("#product_discountprice");
const ProductPrice = document.querySelector("#product_price");
const ProductImage = document.getElementById("product_image");
const ProductDescription = document.getElementById("product_description");
const ProductModal_minus = document.getElementById("ProductModal_minus");
const ProductModal_plus = document.getElementById("ProductModal_plus");
const ProductModal_quantity = document.getElementById("ProductModal_quantity");
const RemoveItemBtns = document.querySelectorAll(".btnRemoveItem");

var accessToken = getCookie("accessToken");
const baseUrl = "/store/api/shoppingcart/";

function removeItemRow(product_id) {
    document.querySelectorAll(".cartitem_row_" + product_id).forEach(item => {
        item.classList.add("d-none");
    });
}

function updateOrderItemInfo(product_id, quantity, subtotal, order_count, order_total) {
    var orderitem_id = ".orderitem_quantity_" + product_id;
    var orderitem_els = document.querySelectorAll(orderitem_id);
    var subtotal_id = ".order_item_" + product_id + "_subtotal"
    var ordersubtotal_els = document.querySelectorAll(subtotal_id);

    orderitem_els.forEach(item => {
        item.innerHTML = quantity;
    });
    ordersubtotal_els.forEach(item => {
        item.innerHTML = subtotal;
    });

    TopCartNumbers.forEach(item => {
        item.innerHTML = order_count;
    });
    CartTotal.forEach(item => {
        item.innerHTML = order_total;
    });


}

function AddToCart(e) {
    var product_id = e.target.getAttribute("product_id");
    // var url = "/store/api/shoppingcart/";

    // if (accessToken !== undefined && accessToken !== null) {
    fetch(baseUrl, {
        body: JSON.stringify({product_id: product_id,action:"add_cartitem"}),
        method: "POST",
        // headers: {
        //     'Authorization': accessToken,
        // }
    }).then((res) => res.json()).then((data) => {

        if (data.result == "OK" && data.action=="add_cartitem") {
            updateOrderItemInfo(product_id, data.product_count, data.product_subtotal, data.order_count, data.order_total)
            ToastMessage("success", "Add successfully!");
        }
    });
}

function DecreaseToCart(e) {
    var product_id = e.target.getAttribute("product_id");
    // var url = "/store/api/decrease-to-cart/";
    fetch(baseUrl, {
        body: JSON.stringify({product_id: product_id,action:"decrease_cartitem"}),
        method: "POST",
    }).then((res) => res.json()).then((data) => {
        console.log(data)
        if (data.result == "OK" && data.action == "decrease_cartitem") {

            updateOrderItemInfo(product_id, data.product_count, data.product_subtotal, data.order_count, data.order_total)
            if (data.product_count < 1) {
                removeItemRow(product_id);
            }
            if (data.order_count < 1) {
                document.querySelectorAll(".cartcontent").forEach(item => {
                    item.classList.add("d-none");
                });
            }

            ToastMessage("success", "Decrease successfully!");
        }

    });
}

function RemoveCartItem(e) {
    var product_id = e.target.getAttribute("product_id");
    // var url = "/store/api/removeitem-from-cart/";

    fetch(baseUrl, {
        body: JSON.stringify({product_id: product_id,action:"remove_cartitem"}),
        method: "POST",
    }).then((res) => res.json()).then((data) => {
        console.log(data)
        if (data.result == "OK" && data.action=="remove_cartitem") {

            updateOrderItemInfo(product_id, 0, 0, data.order_count, data.order_total)

            removeItemRow(product_id)

            if (data.order_count < 1) {
                document.querySelectorAll(".cartcontent").forEach(item => {
                    item.classList.add("d-none");
                });
            }

            ToastMessage("success", "Remove from cart successfully!");
        }

    });
}

function ShowProduct(e) {
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
        if (data.result === "OK") {
            console.log(data.product.description);
            ProductName.innerHTML = data.product.item_name;
            ProductDiscountPrice.innerHTML = "¥" + data.product.discount_price;
            ProductPrice.innerHTML = "¥" + data.product.price;
            // document.getElementById("product_image").src = 'img/new-image.jpg';
            ProductImage.src = data.product.image;
            ProductDescription.innerHTML = data.product.description;

            ToastMessage("success", "OK");
        }
        // console.log(data.order_count);
        // TopCartNumber.innerHTML = data["order_count"];
    });

    $('#ProductModal').modal('toggle');
}

document.querySelectorAll(".btnAddToCart").forEach(item => {
    item.addEventListener("click", AddToCart);
});
document.querySelectorAll(".btnDecreaseToCart").forEach(item => {
    item.addEventListener("click", DecreaseToCart);
});

document.querySelectorAll(".btnShowProduct").forEach(item => {
    item.addEventListener("click", ShowProduct);
});

RemoveItemBtns.forEach(item => {
    item.addEventListener("click", RemoveCartItem);
})