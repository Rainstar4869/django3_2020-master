<template>

    <div class="row ">

        <div class=" col-lg-4 col-sm-12"
             v-for="product in products">
            <div class="grid-inner">
                <div class="product-image">
                    <a :href="'/store/product/'+product.id+'/'"><img :src="product.thumbimage"></a>

                    <div class="bg-overlay-content align-items-end justify-content-between"
                         style="margin-top: -50px;position: relative!important;padding: 0;">
                        <a href="javascript:void(0);" class="btn btn-dark mr-2 "
                           @click="shoppingcart_operation('add_cartitem',product.id)">
                            <i class="icon-shopping-cart "></i>
                        </a>
                        <a href="javascript:void(0);" class="btn btn-dark mr-2 " data-toggle="modal"
                           :data-target="'#ProductModal'+product.id">
                            <i class="icon-line-expand"></i>
                        </a>
                    </div>
                    <div class="sale-flash badge badge-secondary p-2" v-if="product.inventory==0">Out of Stock</div>
                </div>
                <div class="product-desc">

                    <div class="product-title">
                        <h3><a href="javascript:void(0);" data-toggle="modal"
                               :data-target="'#ProductModal'+product.id">{{ product.item_name }}</a></h3>
                    </div>
                    <div class="product-price" v-if="product.discount_price">
                        <del>{{ product.price| currency_jpy}}</del>
                        <ins>{{ product.discount_price | currency_jpy }}</ins>
                    </div>
                    <div class="product-price" v-else>
                        <ins>{{ product.price | currency_jpy }}</ins>
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
                    <div v-if="product.pingo_items.length">
                        <pingoitem :param_pingoitems="product.pingo_items"  v-on:pingoitem_operate="pingoitem_process"></pingoitem>
                    </div>
                </div>
            </div>

            <!-- Modal -->
            <div class="modal fade" :id="'ProductModal'+product.id" tabindex="-1" role="dialog"
                 aria-labelledby="myModalLabel"
                 aria-hidden="true">
                <div class="single-product shop-quick-view-ajax mt-lg-6">

                    <div class="ajax-modal-title">
                        <h2 class="modal-title d-inline-block">{{ product.item_name }}</h2>
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                    </div>

                    <div class="product modal-padding">

                        <div class="row gutter-40 col-mb-50">
                            <div class="col-md-6">
                                <div class="product-image">
                                    <img :src="product.thumbimage">
                                    <div class="sale-flash badge badge-danger p-2">Sale!</div>
                                </div>
                            </div>
                            <div class="col-md-6 product-desc">
                                <div class="product-price" v-if="product.discount_price">
                                    <del>{{ product.price| currency_jpy}}</del>
                                    <ins>{{ product.discount_price | currency_jpy }}</ins>
                                </div>
                                <div class="product-price" v-else>
                                    <ins>{{ product.price | currency_jpy }}</ins>
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
                                <div class="clear"></div>
                                <div class="line"></div>

                                <a href="javascript:void(0);" class="add-to-cart button m-0"
                                   @click="shoppingcart_operation('add_cartitem',product.id)">
                                    <i class="icon-shopping-cart "></i>Add to cart
                                </a>
                                <div class="clear"></div>
                                <div class="line"></div>
                                <p id="product_description"></p>
                                <ul class="iconlist">
                                    <li><i class="icon-caret-right"></i> Lots of Size Options</li>
                                    <li><i class="icon-caret-right"></i> 30-Day Return Policy</li>
                                </ul>
                                <div class="card product-meta mb-0">
                                    <div class="card-body">
                                <span itemprop="productID" class="sku_wrapper">SKU: <span
                                        class="sku">8465415</span></span>
                                        <span class="posted_in">Category: <a href="#"
                                                                             rel="tag">Shoes</a>.</span>
                                        <span class="tagged_as">Tags: <a href="#" rel="tag">Barena</a>, <a
                                                href="#" rel="tag">Blazers</a>, <a href="#"
                                                                                   rel="tag">Tailoring</a>, <a
                                                href="#" rel="tag">Unconstructed</a>.</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                </div>
                <div class="modal-dialog"></div>
            </div>

        </div>


    </div><!-- #shop end -->


</template>

<script>

    import {Rate} from "element-ui"
    import PingoItem from "./PingoItem.vue"

    export default {
        name: 'product',
        data() {
            return {}
        },
        components: {
            "el-rate": Rate,
            "pingoitem": PingoItem
        },
        computed: {
            products() {
                return this.$store.state.shoppingcart.products
            }
        },
        mounted() {
            this.$store.dispatch("shoppingcart/load_category_products", 4);
            console.log(this.products)
        },
        methods: {
            shoppingcart_operation(actionType, product_id) {
                this.$store.dispatch("shoppingcart/update_shoppingcart", {actionType, product_id});
            },
            pingoitem_process(e){
                console.log(e);
            }
        }
    }
</script>

<style>

</style>
