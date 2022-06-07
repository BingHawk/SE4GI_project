<template >
  <CardInfo :persons="persons">
    
    <!-- :person="particles -->
  </CardInfo>
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
    const { data } = await $axios.get("/api/contact");
    console.log(data);
    console.log(data.contactus);
    console.log(data.contactus[0]['first_name'])
    console.log(data.contactus[0].first_name)
      console.log(data.contactus[0]['last_name'])
    console.log(data.contactus[0].last_name)
      console.log(data.contactus[0]['nationality'])
    console.log(data.contactus[0].nationality)
      console.log(data.contactus[0]['nationality'])
    console.log(data.contactus[0].nationality)
    console.log(data.contactus[0])
    console.log(data.contactus[0].first_name)
    
    return {
      persons: data.contactus,
    };
  },
};
</script>