<template>
    <div  class="shop row grid-container gutter-20" data-layout="fitRows">
        <div class="product col-md-4 col-sm-6" :class="product.category" v-for="product in products">
            <div class="grid-inner">
                <div class="product-image">
                    <a href="#"><img :src="product.thumbimage"
                                     alt="Checked Short Dress"></a>

                    <div class="sale-flash badge badge-secondary p-2" v-if="product.inventory==0">Out of Stock</div>

                    <div class="bg-overlay">
                        <div class="bg-overlay-content align-items-end justify-content-between"
                             data-hover-animate="fadeIn" data-hover-speed="400">
                            <a href="javascript:void(0);" class="btn btn-dark mr-2 "
                               @click="shoppingcart_operation('add_cartitem',product.id)">
                                <i class="icon-shopping-cart "></i>
                            </a>
                            <!--                        <a href="javascript:void(0);"-->
                            <!--                           class="btn btn-dark btnShowProduct"><i-->
                            <!--                                class="icon-line-expand"-->
                            <!--                                product_id="{{ product.id }}"></i></a>-->
                        </div>
                        <div class="bg-overlay-bg bg-transparent"></div>
                    </div>
                </div>
                <div class="product-desc">
                    <div class="product-title"><h3><a
                            href="#">{{ product.item_name }} {{ product.is_valid }}</a></h3>
                    </div>
                    <div class="product-price">
                        <del>¥{{ product.price| currency_jpy}}</del>
                        <ins>¥{{ product.discount_price | currency_jpy }}</ins>
                    </div>
                    <div class="product-rating">
                        <i class="icon-star3"></i>
                        <i class="icon-star3"></i>
                        <i class="icon-star3"></i>
                        <i class="icon-star3"></i>
                        <i class="icon-star-half-full"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        name: 'product',
        data() {
            return {
                // cart: {},
            }
        },
        computed: {
            products() {
                return this.$store.state.shoppingcart.products
            }
        },
        mounted() {
            this.$store.dispatch("shoppingcart/get_store_active_products");
        },
        methods:{
            shoppingcart_operation(actionType, product_id) {
                console.log("shoppingcart_operation: "+actionType);
                this.$store.dispatch("shoppingcart/update_shoppingcart",{actionType,product_id});
            }
        }
    }
</script>

<style>

</style>
