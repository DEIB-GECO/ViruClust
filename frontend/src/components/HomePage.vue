<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
    <v-row justify="center" align="center">
      <v-card width="80%" style="margin-top:50px; padding: 10px" color="#E2C178">
         <v-card-text>
           <v-layout row wrap justify-center>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               <div style="border: grey solid 3px; border-radius: 50%; height: 300px; width: 70%;
               background-color: #C42F3E; text-align: center; padding-top: 130px">
                  <span style="color: white; font-size: 10vw;">
                      <span class="font-weight-bold">Viru</span>
                      <span class="font-weight-light">Clust</span>
                  </span>
               </div>
            </v-flex>
           </v-layout>
         </v-card-text>
      </v-card>

      <v-card width="80%" style="margin-top:50px; padding: 10px;" color="#E2C178">
        <v-card-title class="justify-center" style="background-color: #C42F3E; color: white; margin: 1% 20% 3%;">
          <span style="font-size: 2vw;">HOW TO USE VIRUCLUST</span>
        </v-card-title>
         <v-card-text>
           <v-layout row wrap justify-center style="margin-right: 10%; margin-left: 10%; margin-top: 1%">
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">

                <v-expansion-panels
                v-model="expansionPanels"
                dark
                multiple>
                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #C42F3E;">
                        <span style="width: 80%; color: white;">ANALYZE DISTRIBUTION LINEAGE IN GEO</span>
                        <div>
                          <v-btn @click="goToRelatedPart(1)" small class="white--text" color="#323F8B">
                            START THIS ANALYSIS
                          </v-btn>
                        </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #C42F3E;">
                      <span style="width: 80%; color: white;">TEMPORAL ANALYSIS</span>
                      <div>
                        <v-btn @click="goToRelatedPart(2)" small class="white--text" color="#323F8B">
                          START THIS ANALYSIS
                        </v-btn>
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #C42F3E;">
                      <span style="width: 80%; color: white;">SPATIAL ANALYSIS</span>
                      <div>
                        <v-btn @click="goToRelatedPart(3)" small class="white--text" color="#323F8B">
                          START THIS ANALYSIS
                        </v-btn>
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #C42F3E;">
                      <span style="width: 80%; color: white;">FREE TARGET VS BACKGROUND</span>
                      <div>
                        <v-btn @click="goToRelatedPart(4)" small class="white--text" color="#323F8B">
                          START THIS ANALYSIS
                        </v-btn>
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                </v-expansion-panels>

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
  name: "HomePage",
  data(){
    return {
      expansionPanels: [],
    }
  },
  computed: {
    ...mapState(['queryGeo', 'queryTime', 'queryFreeTarget', 'queryFreeBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAnalyzePage', 'setLoadPage', 'setSelectedTabAnalyzeFromHome']),
    ...mapActions(['setQueryGeo', 'setQueryTime', 'setQueryFreeTarget', 'setQueryFreeBackground']),
    changePageLoad(){
      this.setLoadPage();
    },
    changePageAnalyze(){
      this.setSelectedTabAnalyzeFromHome(1);
      this.setAnalyzePage();
    },
    goToRelatedPart(num_part){
      this.setSelectedTabAnalyzeFromHome(num_part);
      this.setAnalyzePage();
    }
  },
  mounted() {
    Object.keys(this.queryTime).forEach(elem => {
      this.setQueryTime({field: elem, list: []})
    })

    Object.keys(this.queryGeo).forEach(elem => {
      this.setQueryGeo({field: elem, list: []})
    })

    Object.keys(this.queryFreeTarget).forEach(elem => {
      this.setQueryFreeTarget({field: elem, list: []})
    })

    Object.keys(this.queryFreeBackground).forEach(elem => {
      this.setQueryFreeBackground({field: elem, list: []})
    })
  }
}
</script>

<style scoped>

</style>