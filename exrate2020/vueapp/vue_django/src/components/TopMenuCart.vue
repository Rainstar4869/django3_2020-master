<template>
    <!-- Top Cart
    ============================================= -->
    <div id="top-cart" class="header-misc-icon d-none d-sm-block">
        <a href="#" id="top-cart-trigger"><i class="icon-line-bag"></i><span class="top-cart-number">{{cart.Qty}}</span></a>
        <div class="top-cart-content">
            <div class="top-cart-title">
                <h4>Shopping Cart</h4>
            </div>
            <div class="top-cart-items">
                <div class="top-cart-item" v-for="orderitem in cart.orderitems">
                    <div class="top-cart-item-image">
                        <a href="#"><img :src="orderitem.product.thumbimage"/></a>
                    </div>
                    <div class="top-cart-item-desc">
                        <div class="top-cart-item-desc-title">
                            <a href="#">{{ orderitem.product.name }}</a>
                            <span class="top-cart-item-price d-block" v-if="orderitem.product.discount_price">{{ orderitem.product.discount_price | currency_jpy}}</span>
                            <span class="top-cart-item-price d-block" v-else>{{ orderitem.product.price |currency_jpy}}</span>
                        </div>
                        <div class="top-cart-item-quantity">x {{ orderitem.quantity }}</div>
                    </div>
                </div>
            </div>
            <div class="top-cart-action">
                <span class="top-checkout-price">{{ cart.Total |currency_jpy }}</span>
                <a href="/store/order-summary/" class="button button-3d button-small m-0">View Cart</a>
            </div>
        </div>
    </div><!-- #top-cart end -->
</template>

<script>
    export default {
        name: 'topmenucart',
        data() {
            return {
            }
        },
        computed: {
            cart() {
                return this.$store.state.shoppingcart.cart
            }
        },
        mounted() {

            this.$store.dispatch("shoppingcart/get_categories");
            this.$store.dispatch("shoppingcart/get_shoppingcart");
        },
        methods:{
        }
    }
</script>

<style>

</style>
