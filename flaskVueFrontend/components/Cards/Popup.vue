<template>
  <div style="text-align: center;" id="home">
    <!-- Rendering data to DOM -->
    <card :title="city" style="margin: 0px;">
      <div>
        <ul style="padding-left:8px; text-align:left;">
          <li
            class="text"
            v-for="particle in particles"
            :key="particle.parameter"
          >
            {{ particle.parameter }}: {{ particle.value.toFixed(2) }}
            {{ particle.unit }}
          </li>
        </ul>
      </div>
      <div slot="footer">
        <span class="text-muted">Last updated: {{particles[0].lastUpdated.substring(0, 10)}}</span>
      </div>
    </card>
  </div>
</template>

<script>
import Card from "./Card.vue";
export default {
  components: { Card },
  name: "Popup",
  props: { city: {}, particles: {} },
};
</script>
