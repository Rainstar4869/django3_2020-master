<template>
    <div class="row ">
        <h2>Margin List</h2>

    </div><!-- #shop end -->


</template>

<script>
export default {
    name: 'marginlist',
    props:['marginlist'],
    data() {
        return {};
    },
    components: {
    },
    computed: {
    },
    mounted() {
        console.log(this.marginlist);
        // this.$store.dispatch('shoppingcart/load_category_products', 4);
    },
    methods: {
        shoppingcart_operation(actionType, product_id) {
            this.$store.dispatch('shoppingcart/update_shoppingcart', {actionType, product_id});
        },
        pingoitem_process(e) {
            console.log(e);

        }
    }
};
</script>

<style>

</style>
