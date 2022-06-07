<template>
  <MglMap
    :accessToken="accessToken"
    :mapStyle="mapStyle"
    :center="center"
    :zoom="zoom"
  >
    <MglMarker
      v-for="location in latest"
      :key="location.cityName"
      :coordinates="location.coordinates"
      style="padding:0pt"
    >
      <MglPopup style="background:#27293d !important">
        <Popup :city="location.cityName" :particles="location.particles">
        </Popup>
      </MglPopup>
    </MglMarker>
  </MglMap>
</template>

<script>
import Mapbox from "mapbox-gl";
import { MglMap, MglPopup, MglMarker } from "vue-mapbox";
import Popup from "../components/Cards/Popup.vue";

export default {
  name: "BaseMap",
  components: {
    MglMap,
    MglMarker,
    MglPopup,
    Popup,
  },
  props: {
    locations: {
      type: Array,
    },
    latest: {
      type: Array,
    },
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
      center: [10, 43],
      zoom: 4,
    };
  },

  created() {
    this.mapbox = Mapbox;
  },

  mounted() {
    console.log("Latest:" + this.latest[0].coordinates);

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
.mapboxgl-popup-content {
  padding: 0px;
}
.mapboxgl-popup-close-button{
  color: white;
}
.mapboxgl-popup-tip{
  border-bottom-color:#27293d !important;
  border-top-color:#27293d !important;
}

</style>

