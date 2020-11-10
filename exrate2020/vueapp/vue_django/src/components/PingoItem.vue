<template>

		<div class=" text-danger">
            <p v-for="item in pingoitems" class="text-center font-primary">
                <vac :time="countdown_deadline" v-if="countdown_deadline">
                    <template slot-scope="props" class="lionhu">
                        <i class="icon el-icon-timer"></i> {{ props.days }} 日 {{ props.hours }} 時 {{
                        props.minutes }} 分 {{
                        props.seconds }} 秒
                    </template>
                </vac>
            </p>
		</div>
</template>

<script>
    import FlipCountdown from 'vue2-flip-countdown'
    import Countdown from 'vuejs-countdown'
    import VueCountdown from '@chenfengyuan/vue-countdown'

    export default {
        name: 'pingoitems',
        props:["pingoitems"],
        data() {
            return {
            }
        },
        components:{
            FlipCountdown,
            'countdown' : Countdown,
            'vac' : VueCountdown
        },
        computed: {
            countdown_deadline() {
                var deadlinestr=this.pingoitems[0].until_at.replace('T',' ');
                var deadline=new Date(deadlinestr);
                var now = new Date();
                if (deadline-now>=0){
                    return deadline-now
                }else{
                    return 0
                }
            }
        },
        mounted() {
        },
        methods:{
            // shoppingcart_operation(actionType, product_id) {
            //     this.$store.dispatch("shoppingcart/update_shoppingcart",{actionType,product_id});
            // }
        }
    }
</script>

<style>
.vuejs-countdown .digit{
    font-size: 12px!important;
}

</style>
