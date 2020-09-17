<template>
  <div id="app">
    <h1>Hello VUE, finally see you</h1>
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',
  created() {
    console.log("from APP")
  }
}
</script>

<style>

</style>
