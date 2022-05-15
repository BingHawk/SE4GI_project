<template>
  <div class="window">
    <map-component :locations="data.locations"></map-component>
    <div class="map"></div>
  </div>
</template>

<script>
import MapComponent from '../components/mapComponent.vue'
export default {
  name: 'MapPage',
  components: {
    MapComponent,
  },
  async asyncData({ $axios }) {
    console.log("asyncData running")
    const { data } = await $axios.get('api/locations')
    console.log(data)
    return { data }
  },
}
</script>
