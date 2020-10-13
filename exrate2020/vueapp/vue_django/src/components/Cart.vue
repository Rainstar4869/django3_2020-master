<template>
    <div>

        <div class="table-responsive mb-5 cartcontent">
            <table class="table cart">
                <thead>
                <tr>
                    <th class="cart-product-remove">&nbsp;</th>
                    <th class="cart-product-thumbnail">&nbsp;</th>
                    <th class="cart-product-name">Product</th>
                    <th class="cart-product-price">Unit Price</th>
                    <th class="cart-product-quantity">Quantity</th>
                    <th class="cart-product-subtotal">Total</th>
                </tr>
                </thead>
                <tbody>
                <tr  v-for=" orderitem in cart.orderitems">
                    <td class="cart-product-remove">
                        <a href="javascript:void(0);" class="remove"  @click="shoppingcart_operation('remove_cartitem',orderitem.product.id)"><i class="icon-trash2"></i></a>
                    </td>

                    <td class="cart-product-thumbnail">
                        <a href="#"><img width="64" height="64" :src="orderitem.product.thumbimage"></a>
                    </td>

                    <td class="cart-product-name">
                        <a href="#">{{ orderitem.product.name }}</a>
                    </td>

                    <td class="cart-product-price" v-if="orderitem.product.discount_price">
                        <del>¥{{ orderitem.product.price | currency}}</del>
                        <span class="amount">¥{{ orderitem.product.discount_price| currency}}</span>
                    </td>
                    <td class="cart-product-price" v-else>
                        <span class="amount">{{ orderitem.product.price | currency}}</span>
                    </td>

                    <td class="cart-product-quantity">
                        <div class="quantity">
                            <a href="javascript:void(0);" @click="shoppingcart_operation('decrease_cartitem',orderitem.product.id)">
                                <i class="icon-minus-sign mx-2"></i>
                            </a>
                            <span>{{ orderitem.quantity }}</span>

                            <a href="javascript:void(0);" @click="shoppingcart_operation('add_cartitem',orderitem.product.id)">
                                <i class="icon-plus-sign mx-2"></i>
                            </a>
                        </div>
                    </td>

                    <td class="cart-product-subtotal">
                        <span  v-if="orderitem.product.discount_price">¥{{ orderitem.quantity* orderitem.product.discount_price | currency}}</span>
                        <span  v-else>¥{{ orderitem.quantity* orderitem.product.price | currency}}</span>
                    </td>
                </tr>
<!--                {% empty %}-->
<!--                <tr v-if="cart.Qty <1">-->
<!--                    <td colspan="6">Your Cart Empity</td>-->
<!--                </tr>-->

<!--                <tr>-->
<!--                    <td colspan="6">-->
<!--                        <a href="{% url 'store:home' %}" class="btn btn-primary float-right">Continue Shopping</a>-->
<!--                    </td>-->
<!--                </tr>-->
                </tbody>

            </table>
        </div>
        <div class="row col-mb-30 cartcontent">
            <div class="col-lg-6">
                <h4>Cart Totals</h4>
                <div class="table-responsive">
                    <table class="table cart">
                        <tbody>
                        <tr class="cart_item">
                            <td class="cart-product-name">
                                <strong>Total</strong>
                            </td>

                            <td class="cart-product-name">
                                <span class="amount color lead"><strong class="order_total">¥{{ cart.Total | currency_jpy}}</strong></span>
                            </td>
                        </tr>
                        </tbody>

                    </table>
                </div>
            </div>
            <div class="col-lg-6">
                <a href="{% url 'store:checkout' %}"
                   class="button button-3d mt-0 float-right">Proceed to
                    Checkout</a>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex"
    import shoppingcart from "../stores/shoppingcart";

    export default {
        name: 'cart',
        data() {
            return {
                // cart: {},
            }
        },
        computed: {
            cart() {
                return this.$store.state.shoppingcart.cart
            }
        },
        mounted() {
            // this.$store.dispatch("shoppingcart/get_shoppingcart");
        },
        methods:{
            shoppingcart_operation(actionType, product_id) {
                this.$store.dispatch("shoppingcart/update_shoppingcart",{actionType,product_id});
            }
        }
    }
</script>

<style>

</style>
