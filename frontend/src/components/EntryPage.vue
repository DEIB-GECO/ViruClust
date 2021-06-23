<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
    <v-row justify="center" align="center">
      <v-card width="600px" style="margin-top:50px; padding: 50px" color="#F0E68C">
         <v-card-text>
           <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
              <v-btn @click="changePageLoad()"
                     x-large
                     class="white--text"
                     color="rgb(122, 139, 157)">
                UPLOAD
              </v-btn>
            </v-flex>
            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
              <v-btn @click="changePageAnalyze()"
                     x-large
                     class="white--text"
                     color="rgb(122, 139, 157)">
                ANALYZE
              </v-btn>
            </v-flex>
           </v-layout>
         </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>

import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "EntryPage",
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAnalyzePage', 'setLoadPage']),
    ...mapActions([]),
    changePageLoad(){
      this.setLoadPage();
    },
    changePageAnalyze(){
      this.setAnalyzePage();
    },
  },
}
</script>

<style scoped>

</style>