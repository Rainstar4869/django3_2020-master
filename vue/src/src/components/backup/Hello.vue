<template>
<div>
    <h1>Hello</h1>
    <p>{{product.item_name}}</p>
</div>
</template>

<script>
    export default {
        name: 'Hello',
        data() {
            return {
                product: {},
            }
        },
        mounted() {
            var url = "/store/api/product/get/";
            axios.post(url, {product_id: 1}).then((res) => {
                console.log(res)
                this.product=res.data.product;
            }).catch(function (error) {
                console.log(error)
            });
            this.$store.dispatch("auth/userLogin",{
                username:"huhaiguang@me.com",
                password:"lionhu"
            });
            // this.$store.auth.
        }

    }
</script>

<style>

</style>
