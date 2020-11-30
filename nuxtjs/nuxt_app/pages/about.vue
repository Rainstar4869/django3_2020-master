<template>
  <section class="container">
    <div>
      <h1 class="title">
        {{$store.state.users.ME.accessToken}}
      </h1>
<!--          <ul>-->
<!--      <li v-for="mountain of mountainlist" v-bind:key="mountain.slug">{{ mountain.title }}</li>-->
<!--    </ul>-->
    </div>
  </section>
</template>

<script>

export default {
  computed: {
    accessToken () {
      return this.$store.state.users.ME.accessToken
    }
  },
  components: {
  },
  async asyncData({ app }) {
    var mountains=[];
    var localAPI=app.$api();
    console.log(localAPI);

    var localAPI_api_accesstoken=app.$api_accesstoken();
    console.log(localAPI_api_accesstoken);

    return { mountains }
  }

}
</script>

<style>
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>

