<template>
 <l-marker
   :key="marker.id"
   :lat-lng="marker.coordinates"
 >
   <l-icon ref="icon">
     <p>X</p>
   </l-icon>
 </l-marker>
</template>

<script>
import { LIcon, LMarker } from 'vue2-leaflet'
export default {
 components: { LIcon, LMarker },
 props: {
   marker: {
     type: Object,
     required: true
   }
 }
}
</script>

<style>
 .marker-icon {
   height: 24px;
   width: auto;
 }
</style>