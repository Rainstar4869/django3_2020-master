<template>
  <div >
    <h1>Hello VUE, finally see you</h1>
    <Hello username="lionhu"></Hello>
  </div>
</template>

<script>

  import Hello from "./components/Hello.vue"

export default {
  name: 'App',
  components:{
    Hello,
  },
  created() {
    console.log("from APP")
  }
}
</script>

<style>

</style>
