<template>

		<div class="row ">

            <div class=" col-lg-4 col-sm-12"
                 v-for="product in products">
                <div class="grid-inner">
                    <div class="product-image">
                        <a href="#"><img :src="product.thumbimage"
                                         alt="Checked Short Dress"></a>

                        <div class="sale-flash badge badge-secondary p-2" v-if="product.inventory==0">Out of Stock</div>

<!--                        <div class="bg-overlay">-->
<!--                            <div class="bg-overlay-content align-items-end justify-content-between"-->
<!--                                 data-hover-animate="fadeIn" data-hover-speed="400">-->
<!--                                <a href="javascript:void(0);" class="btn btn-dark mr-2 "-->
<!--                                   @click="shoppingcart_operation('add_cartitem',product.id)">-->
<!--                                    <i class="icon-shopping-cart "></i>-->
<!--                                </a>-->
<!--                            </div>-->
<!--                            <div class="bg-overlay-bg bg-transparent"></div>-->
<!--                        </div>-->
                    </div>
                    <div class="product-desc">
                        <div class="product-rating text-right mb-3" style="margin-top: -50px;">
                            <a href="javascript:void(0);" class="btn btn-success mr-2 "
                               @click="shoppingcart_operation('add_cartitem',product.id)">
                                <i class="icon-shopping-cart "></i>
                            </a>
                        </div>
                        <div class="product-title">
                            <h3><a href="#">{{ product.item_name }}</a></h3>
                        </div>
                        <div class="product-price">
                            <del>¥{{ product.price| currency_jpy}}</del>
                            <ins>¥{{ product.discount_price | currency_jpy }}</ins>
                        </div>
                        <div class="product-rating">
                            <el-rate
                                    v-model="product.rate"
                                    disabled
                                    show-score
                                    text-color="#ff9900"
                                    score-template="{value}">
                            </el-rate>
                        </div>
                    </div>
                </div>
            </div>

		</div><!-- #shop end -->




</template>

<script>

    import {Rate} from "element-ui"

    export default {
        name: 'product',
        data() {
            return {
            }
        },
        components:{
          "el-rate":Rate
        },
        computed: {
            products() {
                return this.$store.state.shoppingcart.products
            }
        },
        mounted() {
            this.$store.dispatch("shoppingcart/load_category_products",4);
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
