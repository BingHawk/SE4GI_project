<template>
  <div class="window">
    <h1>Welcome!</h1>
    <button v-on:click="goToMap">Go to Map</button>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    goToMap() {
      this.$router.push('/mapPage')
    },
  },
}
</script>
