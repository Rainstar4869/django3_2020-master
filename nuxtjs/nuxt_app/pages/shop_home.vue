<template>
  <section class="container">
    <div>
      <h1 class="title">
        Shop
      </h1>
         <h1>Nuxt Mountains</h1>
    <ul>
      <li v-for="mountain of mountainlist" v-bind:key="mountain.slug">{{ mountain.title }}</li>
    </ul>
    <button @click="$fetch">Refresh</button>
    </div>
  </section>
</template>

<script>

export default {
  layout: 'shop_layout',
  components: {
  },
  computed: {
    mountainlist () {
      return this.$store.state.mountains.list
    }
  },
  data() {
      return {
        mountains: []
      }
    },
    async fetch() {
      this.mountains = await fetch(
        'https://api.nuxtjs.dev/mountains'
      ).then(res => res.json());
      this.$store.commit('mountains/addtolist', this.mountains);
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

