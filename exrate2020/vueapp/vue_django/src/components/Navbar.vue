<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">Navbar</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item ">
        <router-link class="nav-link" :to="{name:'posts'}" exact>Posts</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{name:'login'}" exact>Login</router-link>
      </li>
    </ul>
  </div>
</nav>

</template>

<script>

export default {
  name: 'Posts',

}
</script>

<style>

</style>
