<template>
    <div id="_menunavi">
        <h1>Categories</h1>
        <el-tree :data="tree" :props="defaultProps"
                 highlight-current
                 accordion
                 @node-click="handleNodeClick" >
        </el-tree>

    </div>
</template>

<script>
    import { Tree } from 'element-ui';

    export default {
        name: 'menunavi',
        components:{
            "el-tree":Tree,
        },
        data() {
            return {
                defaultProps: {
                    children: 'children',
                    label: 'label'
                }
            }
        },
        computed: {
            tree() {
                return this.$store.state.shoppingcart.categories
            }
        },
        mounted() {
            // this.$store.dispatch("shoppingcart/get_shoppingcart");
        },
        methods: {
            handleNodeClick(data,node,object) {
                // if(node.isLeaf){
                    this.$store.dispatch("shoppingcart/load_category_products",data.id);
                // }
                // console.log(data.id);
                // console.log(node.isLeaf);
                // console.log(this.$store.state.shoppingcart.products);
            }
        }
    }
</script>

<style>
.el-tree-node__label{
    color: red!important;
}
</style>
