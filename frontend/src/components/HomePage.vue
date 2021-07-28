<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
    <v-row justify="center" align="center">
      <v-card width="80%" style="margin-top:50px" color="#A8DADC">
         <v-card-text>
                  <h2 style=" text-align: center">
                     <b>Viru</b>Clust is a web application developed at Politecnico di Milano by the group of Prof. Stefano Ceri.
                     <br>
                      Users can freely select GISAID-provided metadata (lineages, locations, collection dates) to drive their analyses on SARS-CoV-2
                      <br>
                      We support four modes: (1) Lineage analysis; (2) Temporal analysis; (3) Spatial analysis; (4) Open analysis.
                      Modes (2), (3) and (4) allow to compare two different sub-populations, respectively referenced as target and background.
                  </h2>
         </v-card-text>
      </v-card>

      <v-card width="80%" style="margin-top:50px; padding: 10px;" color="#A8DADC">
        <v-card-title class="justify-center" style=" margin: 1% 20% 3%;">
          <span style="font-size: 1.2vw;">HOW TO USE <b>VIRU</b>CLUST</span>
        </v-card-title>
         <v-card-text>
           <v-layout row wrap justify-center style="margin-right: 10%; margin-left: 10%; margin-top: 1%">
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">

                <v-expansion-panels
                v-model="expansionPanels"
                dark
                multiple>
                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #457B9D;">
                        <span style="width: 80%; color: white;">LINEAGE ANALYSIS</span>
                        <div>
                          <v-btn @click="goToRelatedPart(1)" small class="white--text" color="#1D3557">
                            START THIS ANALYSIS
                          </v-btn>
                        </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #457B9D;">
                      <span style="width: 80%; color: white;">TEMPORAL ANALYSIS</span>
                      <div>
                        <v-btn @click="goToRelatedPart(2)" small class="white--text" color="#1D3557">
                          START THIS ANALYSIS
                        </v-btn>
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #457B9D;">
                      <span style="width: 80%; color: white;">SPATIAL ANALYSIS</span>
                      <div>
                        <v-btn @click="goToRelatedPart(3)" small class="white--text" color="#1D3557">
                          START THIS ANALYSIS
                        </v-btn>
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="background-color: white; color: black">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                  <v-expansion-panel style="margin-bottom: 10px">
                    <v-expansion-panel-header style="background-color: #457B9D;">
                      <span style="width: 80%; color: white;">OPEN ANALYSIS</span>
                      <div>
                        <v-btn @click="goToRelatedPart(4)" small class="white--text" color="#1D3557">
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
    },
    goToRelatedPart(num_part){
      this.setSelectedTabAnalyzeFromHome(num_part);
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