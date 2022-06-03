<template>
  <MglMap
    :accessToken="accessToken"
    :mapStyle="mapStyle"
    :center="center"
    :zoom="zoom"
  >
  <!-- <MglGeocoderControl
      :accessToken="accessToken"
      :input.sync="defaultInput"
      @results="handleSearch"    
    /> -->
    <MglMarker 
      v-for = "location in locations"
      :key = "location.id"
      :coordinates="location.coordinates">
    </MglMarker>
  </MglMap>
</template>

<script>
import Mapbox from "mapbox-gl";
import { MglMap, MglMarker } from "vue-mapbox";
//import MglGeocoderControl from 'vue-mapbox-geocoder'


export default {
  name: "BaseMap",
  components: {
    MglMap,
    MglMarker,
    //MglGeocoderControl,
  },
  props: {
    locations: {
      type: Array,
      required: true,
    },
    cities:{
    }
  },
  head: {
    link: [
      {
        rel: "stylesheet",
        href: "https://api.tiles.mapbox.com/mapbox-gl-js/v0.53.0/mapbox-gl.css",
      },
    ],
  },
  data() {
    return {
      accessToken:
        "pk.eyJ1IjoiYmluZ2hhd2siLCJhIjoiY2wzMzB5OHd1MDNnYjNmcXNzZDNtbDhlMCJ9.3tvN62AljWjE75-vCY3qOQ",
      mapStyle: "mapbox://styles/mapbox/streets-v11",
      center: [9.5, 44],
      zoom: 4,
    };
  },
  methods: {
    handleSearch(event) {
      console.log(event)
    }
  },
  created() {
    this.mapbox = Mapbox;
  },
};
</script>
<style lang="scss">
.card-map {
  min-height: 350px;
  .map {
    height: 300px;
    width: 100%;
  }
}
</style>

