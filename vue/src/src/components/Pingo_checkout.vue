<template>
    <div class="row col-mb-50 gutter-50">
        <div class="col-lg-6">
            <div class="product-image center">
                <img :src="pingoitem.thumbimage" style="max-width: 320px;margin: auto;">
                <div class="sale-flash badge badge-danger p-2">Pingo Sale!</div>
            </div>
            <p>{{pingoitem.description}}</p>
            <div class="pricing-box pricing-simple p-5 bg-light border-top border-danger text-center">
                <div class="pricing-title">

                    <div class="d-flex align-items-center justify-content-between">
                        <div class="product-rating">
                            <span>Pingo Price:</span>
                        </div>
                        <div class="product-price">
                            <ins>{{pingoitem.price|currency}}</ins>
                        </div>
                    </div>
                    <div class="d-flex align-items-center justify-content-between">
                        <div class="product-rating">
                            <span>Current Num:</span>
                        </div>
                        <div class="product-price">
                            <ins>{{pingoitem.currentNum|currency}}</ins>
                        </div>
                    </div>
                    <div class="d-flex align-items-center justify-content-between">
                        <div class="product-rating">
                            <span>Target Num:</span>
                        </div>
                        <div class="product-price">
                            <ins>{{pingoitem.targetNum|currency}}</ins>
                        </div>
                    </div>
                </div>
                <div class="pricing-price">
                    {{pingoitem.price * qty | currency}}
                </div>
                <div style="font-size: 1.5rem;">
                    <a href="javascript:void(0);" @click="adjust_qty(-1)">
                        <i class="icon-minus-sign mx-2"></i>
                    </a>
                    <span>{{ qty }}</span>

                    <a href="javascript:void(0);" @click="adjust_qty(1)">
                        <i class="icon-plus-sign mx-2"></i>
                    </a>
                </div>
                <!--								<div class="pricing-action">-->
                <!--									<a href="#" class="btn btn-danger btn-lg" @click="place_order">Place Order</a>-->
                <!--								</div>-->
            </div>

        </div>
        <div class="col-lg-6"  v-if="qty">
            <h3>Shipping Address</h3>
            <div class="d-flex align-items-center justify-content-between">
                <button class="btn btn-primary" data-toggle="modal" v-if="addressbook.length"
                        data-target="#AddressBookModal">
                    <i class="icon-address-book"></i> Address Book
                </button>
                <button class="btn btn-warning" @click="input_new_address" v-if="addressbook.length">
                    <i class="icon-address-card"></i> New Address
                </button>
            </div>
                <el-form :model="shippingaddress" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm mt-3" >
                    <el-form-item label="Name" prop="name" class="col-12 form-group">
                        <el-input v-model="shippingaddress.name" :readonly="existed"></el-input>
                    </el-form-item>
                    <el-form-item label="Phone" prop="phone" class="col-12 form-group">
                        <el-input v-model="shippingaddress.phone" :readonly="existed"></el-input>
                    </el-form-item>
                    <el-form-item label="Email" prop="email" class="col-12 form-group">
                        <el-input v-model="shippingaddress.email" :readonly="existed"></el-input>
                    </el-form-item>

                    <div class="w-100"></div>
                    <div class="row">
                        <el-form-item label="Postcode" prop="postcode" class="col-6 form-group">
                            <el-input v-model="shippingaddress.postcode" :readonly="existed"></el-input>
                        </el-form-item>
                        <el-form-item label="State" prop="state" class="col-6 form-group">
                            <el-input v-model="shippingaddress.state" :readonly="existed"></el-input>
                        </el-form-item>
                    </div>
                        <el-form-item label="Town" prop="town" class="col-12 form-group">
                            <el-input v-model="shippingaddress.town" :readonly="existed"></el-input>
                        </el-form-item>
                        <el-form-item label="Street" prop="street" class="col-12 form-group">
                            <el-input v-model="shippingaddress.street" :readonly="existed"></el-input>
                        </el-form-item>
                    <el-form-item label="Address" prop="address_1" class="col-12 form-group">
                        <el-input v-model="shippingaddress.address_1" :readonly="existed"></el-input>
                    </el-form-item>
                    <el-form-item label="" prop="address_2" class="col-12 form-group">
                        <el-input v-model="shippingaddress.address_2" :readonly="existed"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="success" @click="submitForm('ruleForm')" class="button button-3d float-right">立即创建</el-button>
                    </el-form-item>
                </el-form><!---->
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
                                            <div class="d-flex align-items-center justify-content-between">
                                                <button class="btn btn-primary" @click="select_address(address.id)">
                                                    Select
                                                </button>
                                                <button class="btn btn-danger" @click="delete_address(address.id)">
                                                    Delete
                                                </button>

                                            </div>

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

    import {Form, FormItem, Input,Button} from "element-ui"

    export default {
        name: 'pingoitemcheckout',
        props: ["csrf_token", "pingoitem_id"],
        components: {
            "el-form": Form,
            "el-form-item": FormItem,
            "el-input": Input,
            "el-button":Button
        },
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
                rules: {
                    name: [
                        {required: true, message: '请输入收件人姓名', trigger: 'blur'},
                        {min: 3, max: 10, message: '长度在 3 到 5 个字符', trigger: 'blur'}
                    ],
                    email: [
                        {required: true, message: '请输入邮箱', trigger: 'blur'}
                    ],
                    phone: [
                        {required: true, message: '请输入联系电话', trigger: 'blur'}
                    ],
                    postcode: [
                        {required: true, message: '请输入邮编', trigger: 'blur'}
                    ],
                    state: [
                        {required: true, message: '请输入省（县）', trigger: 'blur'}
                    ],
                    town: [
                        {required: true, message: '请输入市名称', trigger: 'blur'}
                    ],
                    street: [
                        {required: true, message: '请输入区名称', trigger: 'blur'}
                    ],
                    address_1: [
                        {required: true, message: '请输入地址 1', trigger: 'blur'}
                    ],
                    address_2: [
                        {required: true, message: '请输入地址 2', trigger: 'blur'}
                    ]
                },
                addressbook: [],
                existed: false,
                existed_address_id: 0,
                pingoitem: {},
                qty: 0
            }
        },
        computed: {
            cart() {
                return this.$store.state.shoppingcart.cart
            }
        },
        mounted() {
            this.load_shippingaddress();
            this.load_pingoitem();
        },
        methods: {
            submitForm(formName) {
                if(this.qty){
                    this.$refs[formName].validate((valid) => {
                        if (valid) {
                            alert('submit!');
                        } else {
                            console.log('error submit!!');
                            return false;
                        }
                    });
                }

            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            place_order() {
                console.log(this.qty)
            },
            adjust_qty(val) {
                this.qty += val;
                if (this.qty <= 0) {
                    this.qty = 0;
                }
            },
            shoppingcart_operation(actionType, product_id) {
                this.$store.dispatch("shoppingcart/update_shoppingcart", {actionType, product_id});
            },
            load_pingoitem() {
                var vm = this;
                var baseUrl = "/store/api/pingo_items/" + this.pingoitem_id + "/";
                axios.get(baseUrl).then((res) => {
                    console.log(res.data)
                    if (res.data.result == "OK") {
                        vm.pingoitem = res.data.pingoitem
                    }

                }).catch(function (error) {
                    console.log(error)
                });
            },
            load_shippingaddress() {
                var baseUrl = "/store/api/shippingadress/";
                axios.get(baseUrl).then((res) => {
                    if (res.data.result == "OK") {
                        this.addressbook = res.data.addressbook
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
                    console.log("existed: " + this.existed)
                    this.existed = true;
                    this.existed_address_id = id;
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
                        var baseUrl = "/store/api/shippingadress/" + id + "/";
                        axios.delete(baseUrl).then((res) => {
                            if (res.data.result == "OK") {
                                var itemIndex = this.addressbook.findIndex(item => item.id == res.data.id)
                                if (itemIndex > -1) {
                                    this.addressbook.splice(itemIndex, 1)
                                    Swal.fire('Deleted!', '', 'success')

                                }
                            }
                        }).catch((error) => {
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
            input_new_address() {
                this.shippingaddress = {};
                this.existed_address_id = 0;
                this.existed = false;
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
