<template >
  <!-- <div >
        <card style="margin: 5px;">
            <div >
                <v-col cols="5">
                    <v-container class="my-5" >
                        <v-layout row wrap>
                            <v-flex sm2 md3 lg5 >
                                <v-card flat class="text-xs-center ma-3">
                                    <v-responsive class="pt-4"  v-for="person in persons" :key="person['last_name']"> 
                                        <v-card-text > 
                                        <div class="subheading">{{ person.first_name }}</div>
                                        <div class="grey--text">{{ person['last_name'] }}</div>
                                        <div class="grey--text">{{ person.nationality }}</div>
                                        <div class="grey--text">{{ person.description }}</div>
                                        <div  > <a class="tim-icons icon-email-85"  :href="'mailto:'+ person.email"></a> </div>
                                    </v-card-text> -->
  <!-- <v-avatar size="100" class="grey lighten-2">  
                                            <img :src="person.avatar">
                                        </v-avatar> -->
  <!-- </v-responsive>
                                </v-card>
                            </v-flex>
                        </v-layout>
                </v-container>
                </v-col>
            </div>
        </card>
    </div>
     -->

  <div>
    <v-card
      class="mx-auto"
      max-width="400"
      v-for="person in persons"
      :key="person['last_name']"
    >
      <v-img
        class="white--text align-end"
        height="200px"
        src="https://media.istockphoto.com/photos/akihabara-tokyo-picture-id484915982?k=20&m=484915982&s=612x612&w=0&h=jeEPg-Xt5Uv-vUoeTVpaW0ilaGJ1LuazPU-7dUBnhUs="
      >
        <v-card-title>{{ person.first_name }}</v-card-title>
      </v-img>

      <v-card-subtitle class="pb-0">
        {{ person["last_name"] }}
      </v-card-subtitle>

      <v-card-text class="text--primary">
        <div>{{ person.nationality }}</div>

        <div>{{ person.description }}</div>
      </v-card-text>

      <v-card-actions>
        <div>
          <a
            class="tim-icons icon-email-85"
            :href="'mailto:' + person.email"
          ></a>
        </div>
        
        <!-- <v-btn
         color="orange"
         text
       >
         Share
       </v-btn>

       <v-btn
         color="orange"
         text
       >
         Explore
       </v-btn> -->
        
      </v-card-actions>
      
    </v-card>
    
  </div>
</template>

<script>
import Card from "./Card.vue";
export default {
//   components: { Card },
  name: "CardInfo",
  props: { persons: {} },
};
</script>