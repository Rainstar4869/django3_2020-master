<template>
    <div>
        <div class="table-responsive mb-5 cartcontent">
            <table class="table cart">
                <thead>
                <tr>
                    <th class="cart-product-name">name</th>
                    <th class="cart-product-price">Info</th>
                </tr>
                </thead>
                <tbody>
                <tr  v-for=" address in shippingaddress">

                    <td class="cart-product-name">
                        <p>{{ address.name }}</p>
                    </td>

                    <td class="cart-product-price">
                        <p class="text-left">
                            〒{{address.postcode}} {{address.state}} <br>
                            {{address.town}}{{address.street}} <br>
                            {{address.address_1}} <br>
                            {{address.address_2}} <br>
                            Email: {{address.email}} <br>
                            Phone: {{address.phone}}
                        </p>
                        <button class="btn btn-primary" @click="select_address(address.id)">Select</button>

                    </td>
                </tr>
                </tbody>

            </table>
        </div>
    </div>
</template>

<script>
    import {sweetalert_toast} from "../utils/common.js";
    export default {
        name: 'shippingaddress',
        data() {
            return {
                // cart: {},
            }
        },
        computed: {
            shippingaddress() {
                return this.$store.state.shoppingcart.shippingaddress
            }
        },
        mounted() {
            this.$store.dispatch("shoppingcart/load_shippingaddress");
        },
        methods:{
            select_address(id){
                var indexID=this.shippingaddress.findIndex(item=>item.id==id);
                var address = this.shippingaddress[indexID];
                document.getElementById("id_name").value=address.name;
                document.getElementById("id_phone").value=address.phone;
                document.getElementById("id_email").value=address.email;
                document.getElementById("postcode").value=address.postcode;
                document.getElementById("state").value=address.state;
                document.getElementById("town").value=address.town;
                document.getElementById("street").value=address.street;
                document.getElementById("id_address_1").value=address.address_1;
                document.getElementById("id_address_2").value=address.address_2;


                sweetalert_toast("success","top-end","successfully selected!");
            }
        }
    }
</script>

<style>

</style>
