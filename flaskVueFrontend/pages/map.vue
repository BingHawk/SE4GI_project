<template>
  <div class="row">
    <div class="col-md-12">
      <div
        class="btn-group btn-group-toggle "
             :class="false ? 'float-left' : 'float-right'"
        data-toggle="buttons"
        style="zindex-dropdown:100"
      >
        <select
          class="custom-select m-1  text-white w-100"
          name="Cities"
          id="idCitiesDDL"
          data-toggle="tooltip"
          title="Your destination city"
          style="
                background-image: linear-gradient(
                    45deg,
                    transparent 50%,
                    white 50%
                  ),
                  linear-gradient(135deg, white 50%, transparent 50%),
                  linear-gradient(to right, #242424, #242424);
                background-position: calc(100% - 20px) calc(1em + 2px),
                  calc(100% - 15px) calc(1em + 2px), 100% 0;
                background-size: 5px 5px, 5px 5px, 2.5em 2.5em;
                background-repeat: no-repeat;
                background-color: #41B883;
              "
        >
          <option
            v-for="selectValue in selectValues"
            :value="selectValue"
            v-bind:key="option"
            >{{ selectValue }}</option
          >
        </select>
      </div>
      <card type="plain">
        <h4 slot="header" class="card-title">MapBox Map</h4>

        <div id="regularMap" class="map">
          <map-component
            :latest="latest"
          ></map-component>
        </div>
      </card>
    </div>
  </div>
</template>

<script>
import MapComponent from "../components/mapComponent.vue";
export default {
  name: "MapPage",
  components: {
    MapComponent,
  },
  async asyncData({ $axios }) {
    console.log("asyncData running");
    try {
      const [latest, cities] = await Promise.all([
        $axios.get("/api/latest",{responseType: "json"}),
        $axios.get("/api/cities",{responseType: "json"})
      ]);
      
      console.log(latest.data);
      console.log(cities.data);

      return {
        latest: latest.data.locations,
        city: cities.data,
        selectValues: cities.data.cities,
      };
    } catch (e) {
      console.log(e);
    }
  },
};
</script>

<!-- <template>
<div class="row">
    <div class="col-md-12">
      <card type="plain">
        <h4 slot="header" class="card-title">Leaflet Map</h4>
        <div id="regularMap" class="map">
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
      </card>
    </div>
  </div> -->
<!-- <div id="map-wrap" style="height: 100vh">
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
  </div> -->
<!-- </template>

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
<style lang="scss">
.card-map {
  min-height: 350px;
  .map {
    height: 300px;
    width: 100%;
  }
}
</style> -->

<!-- <style scoped>
.map {
  height: 100%;
  width: 100%;
  background-color: red;
}
</style> -->

<!-- <template>
  <div class="row">
    <div class="col-md-12">
      <card type="plain">
        <h4 slot="header" class="card-title">Leaflet Map</h4>
        <div id="regularMap" class="map"></div>
      </card>
    </div>
  </div>
</template>
<script>
import config from '@/config';

export default {
  name: 'google',
  methods: {
    initRegularMap() {
      // Regular Map
      const myLatlng = new window.google.maps.LatLng(40.748817, -73.985428);
      const mapOptions = {
        zoom: 8,
        center: myLatlng,
        scrollwheel: false,
        styles: [
          {
            elementType: 'geometry',
            stylers: [
              {
                color: '#1d2c4d'
              }
            ]
          },
          {
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#8ec3b9'
              }
            ]
          },
          {
            elementType: 'labels.text.stroke',
            stylers: [
              {
                color: '#1a3646'
              }
            ]
          },
          {
            featureType: 'administrative.country',
            elementType: 'geometry.stroke',
            stylers: [
              {
                color: '#4b6878'
              }
            ]
          },
          {
            featureType: 'administrative.land_parcel',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#64779e'
              }
            ]
          },
          {
            featureType: 'administrative.province',
            elementType: 'geometry.stroke',
            stylers: [
              {
                color: '#4b6878'
              }
            ]
          },
          {
            featureType: 'landscape.man_made',
            elementType: 'geometry.stroke',
            stylers: [
              {
                color: '#334e87'
              }
            ]
          },
          {
            featureType: 'landscape.natural',
            elementType: 'geometry',
            stylers: [
              {
                color: '#023e58'
              }
            ]
          },
          {
            featureType: 'poi',
            elementType: 'geometry',
            stylers: [
              {
                color: '#283d6a'
              }
            ]
          },
          {
            featureType: 'poi',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#6f9ba5'
              }
            ]
          },
          {
            featureType: 'poi',
            elementType: 'labels.text.stroke',
            stylers: [
              {
                color: '#1d2c4d'
              }
            ]
          },
          {
            featureType: 'poi.park',
            elementType: 'geometry.fill',
            stylers: [
              {
                color: '#023e58'
              }
            ]
          },
          {
            featureType: 'poi.park',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#3C7680'
              }
            ]
          },
          {
            featureType: 'road',
            elementType: 'geometry',
            stylers: [
              {
                color: '#304a7d'
              }
            ]
          },
          {
            featureType: 'road',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#98a5be'
              }
            ]
          },
          {
            featureType: 'road',
            elementType: 'labels.text.stroke',
            stylers: [
              {
                color: '#1d2c4d'
              }
            ]
          },
          {
            featureType: 'road.highway',
            elementType: 'geometry',
            stylers: [
              {
                color: '#2c6675'
              }
            ]
          },
          {
            featureType: 'road.highway',
            elementType: 'geometry.fill',
            stylers: [
              {
                color: '#9d2a80'
              }
            ]
          },
          {
            featureType: 'road.highway',
            elementType: 'geometry.stroke',
            stylers: [
              {
                color: '#9d2a80'
              }
            ]
          },
          {
            featureType: 'road.highway',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#b0d5ce'
              }
            ]
          },
          {
            featureType: 'road.highway',
            elementType: 'labels.text.stroke',
            stylers: [
              {
                color: '#023e58'
              }
            ]
          },
          {
            featureType: 'transit',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#98a5be'
              }
            ]
          },
          {
            featureType: 'transit',
            elementType: 'labels.text.stroke',
            stylers: [
              {
                color: '#1d2c4d'
              }
            ]
          },
          {
            featureType: 'transit.line',
            elementType: 'geometry.fill',
            stylers: [
              {
                color: '#283d6a'
              }
            ]
          },
          {
            featureType: 'transit.station',
            elementType: 'geometry',
            stylers: [
              {
                color: '#3a4762'
              }
            ]
          },
          {
            featureType: 'water',
            elementType: 'geometry',
            stylers: [
              {
                color: '#0e1626'
              }
            ]
          },
          {
            featureType: 'water',
            elementType: 'labels.text.fill',
            stylers: [
              {
                color: '#4e6d70'
              }
            ]
          }
        ]
      };

      const map = new window.google.maps.Map(
        document.getElementById('regularMap'),
        mapOptions
      );

      const marker = new window.google.maps.Marker({
        position: myLatlng,
        title: 'Regular Map!'
      });

      marker.setMap(map);
    }
  },
  async mounted() {
    let GoogleMapsLoader = await import('google-maps')
    GoogleMapsLoader = GoogleMapsLoader.default
    GoogleMapsLoader.KEY = config.MAPS_API_KEY;
    GoogleMapsLoader.load(google => {
      this.initRegularMap(google);
    });
  }
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
</style> -->
