<template>
    <div id="_menunavi">
        <el-tree :data="tree" :props="defaultProps"
                 node-key="user_id"
                 @node-drag-start="handleDragStart"
                 @node-drag-enter="handleDragEnter"
                 @node-drag-leave="handleDragLeave"
                 @node-drag-over="handleDragOver"
                 @node-drag-end="handleDragEnd"
                 @node-drop="handleDrop"
                 draggable
                 :allow-drop="allowDrop"
                 :allow-drag="allowDrag">
        </el-tree>

    </div>
</template>

<script>
    import {Tree,Button} from 'element-ui';

    export default {
        name: 'membertree',
        components: {
            "el-tree": Tree,
            "el-button":Button
        },
        data() {
            return {
                defaultProps: {
                    children: 'children',
                    label: 'username'
                }
            }
        },
        computed: {
            tree() {
                return this.$store.state.auth.membertreenodes
            }
        },
        mounted() {
            // this.$store.dispatch("shoppingcart/get_shoppingcart");
        },
        methods: {
            handleDragStart(node, ev) {
                // console.log('drag start', node);
            },
            handleDragEnter(draggingNode, dropNode, ev) {
                // console.log('tree drag enter: ', dropNode.label);
            },
            handleDragLeave(draggingNode, dropNode, ev) {
                // console.log('tree drag leave: ', dropNode.label);
            },
            handleDragOver(draggingNode, dropNode, ev) {
                // console.log('tree drag over: ', dropNode.label);
            },
            handleDragEnd(draggingNode, dropNode, dropType, ev) {
                // console.log('tree drag end: ', dropNode && dropNode.label, dropType);
            },
            handleDrop(draggingNode, dropNode, dropType, ev) {
            },
            allowDrop(draggingNode, dropNode, type) {
                // var isAllowed = type !== 'prev' && type !== "next"
                // console.log("allowdrop type !== 'prev' && type !=='next': " + isAllowed);
                // if (dropNode.data.label === 'admin') {
                //     return false;
                // }
                return true;

            },

            allowDrag(draggingNode) {
                var isallow= draggingNode.data.username=="admin"?false:true;
                return isallow;
            },
        }
    }
</script>

<style>
.el-tree-node__label{
    color: red!important;
}
</style>
