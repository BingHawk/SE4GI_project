<template>
  <l-marker :key="location.id" :lat-lng="location.coordinates">
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
    location: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style scoped>
.marker-icon {
  height: 24px;
  width: auto;
}
</style>
