<template>
    <div id="_menunavi">
        <h1>Categories</h1>
        <el-tree :data="tree" :props="defaultProps" accordion @node-click="handleNodeClick" ></el-tree>

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
                    label: 'name'
                }
            }
        },
        computed: {
            tree() {
                return this.$store.state.shoppingcart.categories
            }
        },
        mounted() {
            console.log("top menunavi");
            console.log(this.tree);
            // this.$store.dispatch("shoppingcart/get_shoppingcart");
        },
        methods: {
            handleNodeClick(data,node) {
                console.log(data);
                console.log(node.isLeaf);
            }
        }
    }
</script>

<style>
.el-tree-node__label{
    color: red!important;
}
</style>
