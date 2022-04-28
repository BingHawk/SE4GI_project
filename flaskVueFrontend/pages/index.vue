<template>
  <div class="window">
    <h1>This is the map:</h1>
    <map-component/>
    <div class="map"></div>
  </div>
</template>

<script>
import MapComponent from '../components/mapComponent.vue';
export default {
  name: 'MapPage',
  components: {
    MapComponent
  },
}
</script>
