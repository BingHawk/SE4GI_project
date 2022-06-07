<template>
    <div>
        <card :title="city" style="margin: 0px;">
            <v-container class="my-5">
                    <v-layout row wrap>
                        <v-flex sm2 md3 lg5 v-for="person in persons" :key="person.name">
                            <v-card flat class="text-xs-center ma-3">
                                <v-responsive class="pt-4"> 
                                    <v-avatar size="100" class="grey lighten-2">
                                        <img :src="person.avatar">
                                    </v-avatar>
                                </v-responsive>
                                <v-card-text> 
                                    <div class="subheading">{{ person.first_name }}</div>
                                    <div class="grey--text">{{ person.last_name }}</div>
                                    <div class="grey--text">{{ person.nationality }}</div>
                                    <div class="grey--text">{{ person.description }}</div>
                                    <v-icon aria-label="My Account" role="img" aria-hidden="false" > {{ person.email }}  </v-icon>
                                </v-card-text>
                            </v-card>
                        </v-flex>
                    </v-layout>
            </v-container>
        </card>

    </div>
    
</template>

<script>
import Card from "./Card.vue";
import Icon from "./Icon.vue"
export default {
  components: { Card, Icon },
  name: "CardInfo",
  props: { persons: {} },
};
</script>