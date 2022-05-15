<template>
  <div id="mapContainer" class="basemap"></div>
</template>

<script>
import mapboxgl from "mapbox-gl";

export default {
  name: "BaseMap",
  data() {
    return {
      accessToken: "pk.eyJ1IjoiYmluZ2hhd2siLCJhIjoiY2wzMzB5OHd1MDNnYjNmcXNzZDNtbDhlMCJ9.3tvN62AljWjE75-vCY3qOQ",
      map: {}
    };
  },
  mounted() {
    this.createMap()
  },
  methods: {
    createMap(){
      mapboxgl.accessToken = this.accessToken;

      this.map =  new mapboxgl.Map({
        container: "mapContainer",
        style: "mapbox://styles/mapbox/streets-v11",
        center: [9.18,45.4],
        zoom: 8,
      })
  }
  }
};
</script>
<style scoped>
#map{
   width:100%;
   height:100%;
}
.basemap {
  height: 100vh;
  width: 100%;
  background-color: red;
}
</style>
<!-- <template>
  <div id="map-wrap" style="height: 100vh">
    <no-ssr>
      <l-map :zoom="8" :center="[45.4, 9.18]" :attribution="attribution">
        <L-marker
          v-for="location in locations"
          :key="location.id"
          :lat-lng="location.coordinates"
        >
        </L-marker>
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        ></l-tile-layer>
      </l-map>
    </no-ssr>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
import { Icon } from 'leaflet'

delete Icon.Default.prototype._getIconUrl

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
})

export default {
  name: 'MapComponent',
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  props: {
    locations: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }
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
</style> -->
