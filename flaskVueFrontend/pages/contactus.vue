<template>
  <card>
    <!-- :person="particles -->
  </card>
</template>

<script>
import Card from '../components/Cards/Card.vue';
import CardInfo from "../components/Cards/Cardinfo.vue";
export default {
  name: "ContactUs",
  components: {
    CardInfo,
    Card,
  },
  async asyncData({ $axios }) {
    console.log("asyncData running");
    const { data } = await $axios.get("/api/contactus");
    console.log(data);
    console.log(data.contactus);
    return {
      persons: data.contactus,
    };
  },
};
</script>