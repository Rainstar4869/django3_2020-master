<template>
    <div>

        <table class="table table-striped" v-if="user_addressbook.length">
            <thead>
            <tr>
                <th>NAME</th>
                <th>EMAIL</th>
                <th>PHONE</th>
                <th>ADDRESS</th>
                <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="address in user_addressbook">
                <td>{{ address.name }}</td>
                <td>{{ address.email }}</td>
                <td>{{ address.phone }}</td>
                <td>
                    {{ address.postcode }} <br>
                    {{ address.state }} {{ address.town }} {{ address.street }} <br>
                    {{ address.address_1 }} <br>
                    {{ address.address_2 }} <br>
                </td>
                <td>
                    <button class="btn btn-primary" data-toggle="modal" @click="select_address(address.id)"
                            data-target="#AddressBookModal">
                        <i class="icon-address-card"></i> Edit
                    </button>
                    <button class="btn btn-danger" @click="delete_address(address.id)">
                        <i class="icon-trash"></i> Delete
                    </button>
                </td>
            </tr>
            </tbody>
        </table>

        <div class="alert alert-warning" v-else>
            <i class="icon-warning-sign"></i><strong>Warning!</strong> You have no Shipping
            Address!
        </div>

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
                            <form id="shipping-form" name="shipping-form" class="row mb-0"
                                  action="/store/checkout/" method="post">

                                <div class="col-md-6 form-group">
                                    <label for="id_name">Name:</label>
                                    <input type="text" name="name" class="sm-form-control"
                                           v-model="shippingaddress.name"
                                           placeholder="1234 Main St" required="true" id="id_name">
                                </div>

                                <div class="w-100"></div>

                                <div class="col-md-6 form-group">
                                    <label for="id_phone">Phone:</label>
                                    <input type="text" name="phone" class="sm-form-control"
                                           v-model="shippingaddress.phone"
                                           placeholder="phone" required="true" id="id_phone">
                                </div>

                                <div class="w-100"></div>

                                <div class="col-md-6 form-group">
                                    <label for="id_email">Email:</label>
                                    <input type="text" name="email" class="sm-form-control"
                                           v-model="shippingaddress.email"
                                           placeholder="email" required="true" id="id_email">
                                </div>

                                <div class="w-100"></div>

                                <div class="col-6 form-group">
                                    <label for="postcode">Postcode:</label>
                                    <input type="text" name="postcode" class="sm-form-control"
                                           v-model="shippingaddress.postcode"
                                           placeholder="postcode" id="postcode" required="true"
                                           @blur="autocomplete_postcode">
                                </div>


                                <div class="col-6 form-group">
                                    <label for="state">State:</label>
                                    <input type="text" name="state" class="sm-form-control"
                                           v-model="shippingaddress.state"
                                           placeholder="state" id="state" required="true">
                                </div>

                                <div class="w-100"></div>

                                <div class="col-6 form-group">
                                    <label for="town">Town:</label>
                                    <input type="text" name="town" class="sm-form-control"
                                           v-model="shippingaddress.town" placeholder="town"
                                           id="town" required="true">
                                </div>


                                <div class="col-6 form-group">
                                    <label for="street">Street:</label>
                                    <input type="text" name="street" class="sm-form-control"
                                           v-model="shippingaddress.street"
                                           placeholder="street" id="street" required="true">
                                </div>

                                <div class="w-100"></div>
                                <div class="col-12 form-group">
                                    <label for="id_address_1">Address Details:</label>
                                    <input type="text" name="address_1" class="sm-form-control"
                                           v-model="shippingaddress.address_1"
                                           placeholder="address_1" value="address_1" required="true"
                                           id="id_address_1">
                                </div>
                                <div class="col-12 form-group">
                                    <input type="text" name="address_2" class="sm-form-control"
                                           v-model="shippingaddress.address_2"
                                           placeholder="address_2" value="address_2" id="id_address_2" required="true">
                                </div>
                            </form>


                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-dismiss="modal" @click="update_address">
                                Save
                            </button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    import Swal from "sweetalert2";

    export default {
        name: 'shippingaddressedit',
        data() {
            return {
                shippingaddress: {
                    id: 0,
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
                user_addressbook:[]
            }
        },
        computed: {},
        mounted() {
            this.load_shippingaddress();
        },
        methods: {
            load_shippingaddress() {
                var baseUrl = "/store/api/shippingadress/";
                axios.get(baseUrl).then((res) => {
                    this.shippingaddress={};
                    if (res.data.result == "OK") {
                        this.user_addressbook = res.data.addressbook
                    }

                }).catch(function (error) {
                    console.log(error)
                });
            },
            select_address(id) {
                var itemIndex = this.user_addressbook.findIndex(address => address.id == id)

                if (itemIndex > -1) {
                    this.shippingaddress = this.user_addressbook[itemIndex]
                }
            },
            delete_address(id) {
                Swal.fire({
                    title: 'Do you really want delete this address?',
                    showCancelButton: true,
                    confirmButtonText: `Delete`,
                }).then((result) => {
                    if (result) {
                        var baseUrl = "/store/api/shippingadress/" + id + "/";
                        axios.delete(baseUrl).then((res) => {
                            if (res.data.result == "OK") {
                                var itemIndex = this.user_addressbook.findIndex(item => item.id == res.data.id)
                                if (itemIndex > -1) {
                                    this.user_addressbook.splice(itemIndex, 1)
                                    Swal.fire('Deleted!', '', 'success')
                                }
                            }
                        }).catch((error) => {
                            console.log(error);
                        })
                    }
                })
            },
            update_address() {
                console.log("update_address");
                var vm=this;

                var baseUrl = "/store/api/shippingadress/"+vm.id+"/";
                axios.put(baseUrl,this.shippingaddress).then((res) => {
                    if (res.data.result == "OK") {
                        var itemIndex = this.user_addressbook.findIndex(address=>address.id==vm.id)

                        if(itemIndex>-1){
                            this.user_addressbook.splice(itemIndex,1,res.data.address)
                            Swal.fire('Updated!', '', 'success')
                        }
                    }

                }).catch(function (error) {
                    console.log(error)
                });
            },
            autocomplete_postcode() {
                var url = "https://api.anko.education/zipcode?zipcode=" + this.shippingaddress.postcode;

                if (this.shippingaddress.postcode.length > 6) {
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
