<template>
    <div>
        <button class="btn btn-primary" data-toggle="modal" v-if="addressbook.length" data-target="#AddressBookModal">
            <i class="icon-address-book"></i> Address Book
        </button>
        <button class="btn btn-warning" @click="input_new_address"  v-if="addressbook.length" >
            <i class="icon-address-card"></i> New Address
        </button>
        <form id="shipping-form" name="shipping-form" class="row mb-0"
              action="/store/checkout/" method="post">
            <input type="text" name="csrfmiddlewaretoken" class="sm-form-control" v-model="csrf_token" hidden>
            <input type="text" name="existed_address_id" class="sm-form-control" v-model="existed_address_id" hidden>
            <div class="w-100"></div>

            <div class="col-md-6 form-group">
                <label for="id_name">Name:</label>
                <input type="text" name="name" class="sm-form-control" v-model="shippingaddress.name"
                       placeholder="1234 Main St" required="true" :readonly="existed" id="id_name">
            </div>

            <div class="w-100"></div>

            <div class="col-md-6 form-group">
                <label for="id_phone">Phone:</label>
                <input type="text" name="phone" class="sm-form-control" v-model="shippingaddress.phone"
                       placeholder="phone" required="true" :readonly="existed" id="id_phone">
            </div>

            <div class="w-100"></div>

            <div class="col-md-6 form-group">
                <label for="id_email">Email:</label>
                <input type="text" name="email" class="sm-form-control" v-model="shippingaddress.email"
                       placeholder="email"  required="true" :readonly="existed" id="id_email">
            </div>

            <div class="w-100"></div>

            <div class="col-6 form-group">
                <label for="postcode">Postcode:</label>
                <input type="text" name="postcode" class="sm-form-control" v-model="shippingaddress.postcode"
                       placeholder="postcode" id="postcode"  required="true" @blur="autocomplete_postcode" :readonly="existed">
            </div>


            <div class="col-6 form-group">
                <label for="state">State:</label>
                <input type="text" name="state" class="sm-form-control" v-model="shippingaddress.state"
                       placeholder="state" id="state" required="true" :readonly="existed">
            </div>

            <div class="w-100"></div>

            <div class="col-6 form-group">
                <label for="town">Town:</label>
                <input type="text" name="town" class="sm-form-control" v-model="shippingaddress.town" placeholder="town"
                       id="town" required="true" :readonly="existed">
            </div>


            <div class="col-6 form-group">
                <label for="street">Street:</label>
                <input type="text" name="street" class="sm-form-control" v-model="shippingaddress.street"
                       placeholder="street" id="street" required="true" :readonly="existed">
            </div>

            <div class="w-100"></div>
            <div class="col-12 form-group">
                <label for="id_address_1">Address Details:</label>
                <input type="text" name="address_1" class="sm-form-control" v-model="shippingaddress.address_1"
                       placeholder="address_1" value="address_1" required="true" :readonly="existed" id="id_address_1">
            </div>
            <div class="col-12 form-group">
                <input type="text" name="address_2" class="sm-form-control" v-model="shippingaddress.address_2"
                       placeholder="address_2" value="address_2" id="id_address_2" required="true" :readonly="existed">
            </div>

            <div class="col-12 form-group">
                <label for="shipping-form-message">Notes <small>*</small></label>
                <textarea class="sm-form-control" id="shipping-form-message"
                          name="shipping-form-message" rows="6" cols="30"></textarea>
            </div>

            <div class="col-12 form-group">

                <button class="button button-3d float-right" type="submit">Place Order</button>
            </div>

        </form>


        <div class="modal fade" id="AddressBookModal" tabindex="-1" role="dialog" aria-labelledby="AddressBookModal"
             aria-hidden="true">

            <div class="modal-dialog">
                <div class="modal-body">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title" id="myModalLabel">My Address Book</h4>
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        </div>
                        <div class="modal-body" id="shippingaddressbook">
                            <div class="table-responsive mb-5 cartcontent">
                                <table class="table cart">
                                    <thead>
                                    <tr>
                                        <th class="cart-product-name">name</th>
                                        <th class="cart-product-price">Info</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr v-for=" address in addressbook">

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
                                            <button class="btn btn-primary" @click="select_address(address.id)">Select
                                            </button>
                                            <button class="btn btn-danger" @click="delete_address(address.id)">Delete
                                            </button>

                                        </td>
                                    </tr>
                                    </tbody>

                                </table>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    export default {
        name: 'shippingaddform',
        props: ["csrf_token"],
        data() {
            return {
                shippingaddress: {
                    name: "",
                    email: "",
                    phone: "",
                    postcode: "",
                    state: "",
                    town: "",
                    street: "",
                    address_1: "",
                    address_2: "",
                },
                addressbook:[],
                existed: false,
                existed_address_id:0
            }
        },
        computed: {
            cart() {
                return this.$store.state.shoppingcart.cart
            }
        },
        mounted() {
            this.load_shippingaddress();
        },
        methods: {
            shoppingcart_operation(actionType, product_id) {
                this.$store.dispatch("shoppingcart/update_shoppingcart", {actionType, product_id});
            },
            load_shippingaddress() {
                var baseUrl = "/store/api/shippingadress/";
                axios.get(baseUrl).then((res) => {
                    if (res.data.result == "OK") {
                        this.addressbook=res.data.addressbook
                        $("#AddressBookModal").modal('show');
                    }

                }).catch(function (error) {
                    console.log(error)
                });
            },
            select_address(id) {
                var index = this.addressbook.findIndex(item => item.id == id)
                if (index > -1) {
                    this.shippingaddress = this.addressbook[index];
                    console.log("existed: "+this.existed)
                    this.existed = true;
                    this.existed_address_id=id;
                    $("#AddressBookModal").modal('hide');
                }
            },
            delete_address(id) {
                Swal.fire({
                    title: 'Do you really want delete this address?',
                    showCancelButton: true,
                    confirmButtonText: `Delete`,
                }).then((result) => {
                    /* Read more about isConfirmed, isDenied below */
                    if (result.isConfirmed) {

                        // var baseUrl = "/store/account/shippingaddress/";
                        var baseUrl = "/store/api/shippingadress/"+id+"/";
                        axios.delete(baseUrl).then((res)=>{
                            if (res.data.result == "OK") {
                                var itemIndex = this.addressbook.findIndex(item => item.id == res.data.id)
                                if (itemIndex > -1) {
                                    this.addressbook.splice(itemIndex, 1)
                                    Swal.fire('Deleted!', '', 'success')

                                }
                            }
                        }).catch((error)=>{
                            console.log(error);
                        })



                        // axios.post(baseUrl,{id:id}).then((res) => {
                        //     console.log(res)
                        //     if (res.data.result == "OK") {
                        //         var itemIndex = this.addressbook.findIndex(item=>item.id == res.data.id)
                        //         if(itemIndex>-1){
                        //             this.addressbook.splice(itemIndex,1)
                        //             Swal.fire('Deleted!', '', 'success')
                        //
                        //         }
                        //     }
                        // }).catch(function (error) {
                        //     console.log(error)
                        // });
                    } else if (result.isDenied) {
                        Swal.fire('Illegal operation', '', 'info')
                    }
                })
            },
            input_new_address(){
                    this.shippingaddress = {};
                    this.existed_address_id=0;
                    this.existed = false;
            },
            autocomplete_postcode(){
                var url = "https://api.anko.education/zipcode?zipcode=" + this.shippingaddress.postcode;

                if(this.shippingaddress.postcode.length>6){
                    var vm = this;
                    fetch(url)
                        .then(function (response) {
                            return response.json();
                        })
                        .then(function (address) {
                            console.log(address);
                            vm.shippingaddress.state = address.pref;
                            vm.shippingaddress.town = address.city;
                            vm.shippingaddress.street = address.area;
                        });
                }
            }
        }
    }
</script>

<style>

</style>
