<template>
    <div class="root">
        <div v-for="item in pingoitems" class="bg-light border-top border-danger text-center mt-3">
            <h3>PinGo!</h3>
            <div class="text-right">
                <vac :time="countdown_deadline" v-if="countdown_deadline" class=" text-danger">
                    <template slot-scope="props" class="lionhu">
                        <i class="icon el-icon-timer"></i> {{ props.days }} 日 {{ props.hours }} 時 {{
                        props.minutes }} 分 {{
                        props.seconds }} 秒
                    </template>
                </vac>

            </div>
            <div class="row ">
                <div class="clearfix"></div>
                <div class="col-6">{{item.price | currency_jpy}}</div>
                <div class="col-6 text-right">{{item.currentNum | currency}}/{{item.targetNum| currency}}</div>
                <div class="clearfix"></div>
                <div class="col-12 my-3">
                    <a :href="'/store/pingo_checkout/'+item.id+'/'">Join!</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import FlipCountdown from 'vue2-flip-countdown'
    import Countdown from 'vuejs-countdown'
    import VueCountdown from '@chenfengyuan/vue-countdown'
    import Swal from "sweetalert2";

    export default {
        name: 'pingoitems',
        props: ["param_pingoitems"],
        data() {
            return {
                pingoitems:[]
            }
        },
        components: {
            FlipCountdown,
            'countdown': Countdown,
            'vac': VueCountdown
        },
        computed: {
            countdown_deadline() {
                var deadlinestr = this.pingoitems[0].until_at.replace('T', ' ');
                var deadline = new Date(deadlinestr);
                var now = new Date();
                if (deadline - now >= 0) {
                    return deadline - now
                } else {
                    return 0
                }
            }
        },
        mounted() {
            this.pingoitems=this.param_pingoitems;
        },
        methods: {
            pingoitem_qty(opt) {
                if (opt == "plus") {
                    this.pingoitem.qty += 1;
                } else if (this.pingoitem.qty > 1) {
                    this.pingoitem.qty -= 1;
                }
            },
            async place_pingoitem_order(id) {
                var vm=this;
                const {value: qty} = await Swal.fire({
                    title: 'Select qty',
                    input: 'select',
                    inputOptions: {
                        1: '1',
                        2: '2',
                        3: '3',
                        4: '4',
                        5: '5',
                    },
                    inputPlaceholder: 'Select qty',
                    showCancelButton: true,
                });
                if (qty) {
                    var params = {
                        id: id,
                        qty: qty
                    };
                    Swal.fire({
                        title: 'Are you sure?',
                        showCancelButton: true,
                        confirmButtonText: `OK`,
                    }).then((result) => {
                        if (result.value) {
                            var baseUrl = "/store/api/pingo_orders/";
                            axios.post(baseUrl, params).then((res) => {
                                if (res.data.result == "OK") {
                                    Swal.fire('Success!', '', 'success');
                                    vm.$emit("pingoitem_operate","hello");
                                    vm.pingoitems[0].currentNum=res.data.currentNum;
                                }
                            }).catch((error) => {
                                console.log(error);
                            })
                        }
                    })
                }


            }
        }
    }
</script>

<style>
    .vuejs-countdown .digit {
        font-size: 12px !important;
    }

</style>
