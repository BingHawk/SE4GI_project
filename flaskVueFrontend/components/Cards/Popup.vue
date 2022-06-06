<template>
  <div style="text-align: center;" id="home">
    <!-- Rendering data to DOM -->
    
    <h2 class="text-muted">{{ message }}</h2> 
    <p class="text-muted">{{"Here are the most recent measurements for"}}</p>   
    <p class="text-muted" v-for="particle in particles" :key="particle.parameter">{{ particle.parameter }} {{ particle.value.toFixed(2) }} {{particle.unit}}</p>
    <p class="text-muted">{{ particles[0].lastUpdated.substring(0, 10)}}</p>
  </div>
</template>

<script>
export default {
  name: "Popup",
  props: { message: {}, particles: {} },
};

</script>
