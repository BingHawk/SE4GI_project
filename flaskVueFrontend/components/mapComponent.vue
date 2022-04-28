<template>
  <div id="map-wrap" style="height: 100vh">
    <no-ssr>
      <l-map :zoom="8" :center="[45.4, 9.18]" :attribution="attribution">
        <marker-icon
          v-for="location in locations"
          :key="location.id"
          :location="location"
        ></marker-icon>
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        ></l-tile-layer>
      </l-map>
    </no-ssr>
  </div>
</template>

<script>
//  import L from 'leaflet';
import { LMap, LTileLayer } from 'vue2-leaflet'
import MarkerIcon from './MarkerIcon.vue'

export default {
  name: 'MapComponent',
  components: {
    LMap,
    LTileLayer,
    MarkerIcon,
  },
  data() {
    return {
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }
  },
  props: {
    locations: {
      type: Array,
      required: true,
    },
  },

  head() {
    return {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css',
        },
      ],
    }
  },
}
</script>

<style scoped>
.map {
  height: 100%;
  width: 100%;
  background-color: red;
}
</style>
