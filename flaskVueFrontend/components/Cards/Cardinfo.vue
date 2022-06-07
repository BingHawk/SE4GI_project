<template>
  <div>
    <card v-for="person in persons" :key="person.last_name">
      <div slot="header">
        {{ person.first_name }} {{ person.last_name }}
        <p class="text-muted">Nationality: {{ person.nationality }}</p>
        <div style="border-bottom: 1px solid #2b3553"></div>
      </div>
      <div>
        <p class="text">{{ person.description }}</p>
      </div>
      <div slot="footer">
        <a class="tim-icons icon-email-85" :href="'mailto:' + person.email"></a>
        <a :href="'mailto:' + person.email">: {{
          person.email
        }}</a>
      </div>
    </card>
  </div>
</template>

<script>
import Card from "./Card.vue";
export default {
  components: { Card },
  name: "CardInfo",
  props: { persons: {} },
};
</script>
