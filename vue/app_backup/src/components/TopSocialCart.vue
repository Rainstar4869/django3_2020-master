<template>
    <li class="d-block d-sm-none"><a href="/store/order-summary/" class="si-dribbble"><span class="ts-icon"><i
            class="icon-shopping-cart"></i></span>
        <span class="top-cart-number" style="top: 13px!important;">{{ cart.Qty }}</span>
    </a></li>
</template>

<script>
    export default {
        name: 'topsocialcart',
        computed: {
            cart() {
                return this.$store.state.shoppingcart.cart
            }
        }
    }
</script>

<style>

</style>
