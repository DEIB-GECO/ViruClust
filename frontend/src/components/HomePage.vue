<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
    <v-row justify="center" align="center">
<!--      <v-card width="80%" style="margin-top:50px" color="#A8DADC">-->
<!--         <v-card-text>-->
<!--                  <h2 style=" text-align: center">-->
<!--                     <b>Viru</b>Clust is a web application developed at Politecnico di Milano by the group of Prof. Stefano Ceri.-->
<!--                     <br>-->
<!--                      Users can freely select GISAID-provided metadata (lineages, locations, collection dates) to drive their analyses on SARS-CoV-2-->
<!--                      <br>-->
<!--                      We support four modes: (1) Lineage analysis; (2) Temporal analysis; (3) Spatial analysis; (4) Open analysis.-->
<!--                      Modes (2), (3) and (4) allow to compare two different sub-populations, respectively referenced as target and background.-->
<!--                  </h2>-->
<!--         </v-card-text>-->
<!--      </v-card>-->

      <v-card width="80%" style="margin-top:50px; padding: 10px;" color="#A8DADC">
        <v-card-title class="justify-center" style=" margin: 1% 20% 3%;">
          <span style="font-size: 1.2vw;">HOW TO USE <b>VIRU</b>CLUST</span>
        </v-card-title>
         <v-card-text>
           <v-layout row wrap justify-center style="margin-right: 10%; margin-left: 10%; margin-top: 1%">
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">

                <v-expansion-panels
                v-model="expansionPanels"
                :value="expansionPanels"
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
                    <v-expansion-panel-content style="background-color: white; color: black;">
                      <br>
                      The Lineage Analysis allows to select a specific location (among continent/country/region levels).
                      The time distribution of counts of collected sequences in the location is represented as a histogram, and a time interval can be graphically selected.
                      Lineages to be shown can be filtered on the basis of their minimum percentage in the selected population.

                      <p align="center">
                        <v-img
                            src="../images/mode1-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Results are provided in two forms:
                      <ul>
                      <li> a table with the distribution of lineages by sub-locations </li>
                      <li> a heatmap where rows are lineages, columns are sub-locations, color-scale represents how many sequences (absolute and in percentage) are assigned to the row lineage in the column sub-location.</li>
                      </ul>

                      <p align="center">
                          <v-img alt="center"
                              src="../images/mode1-2.png" width="700" style="border: grey solid 1px"
                          />
                      </p>

                      Columns scan be aggregated and/or renamed in the visual representation, using the MERGE function, merging together arbitrary columns, renamed by the user.

                      <p align="center">
                        <v-img
                            src="../images/mode1-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
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
                      <br>
                      The Temporal Analysis allows to optionally choose a specific lineage (else, all lineages are included); a location of interest must be selected using the continent/country/region/sub-region levels.

                      <p align="center">
                        <v-img
                            src="../images/mode2-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Two working modes are available:
                      <ul>
                      <li>Two-period comparison (two arbitrary periods, i.e., target and background)</li>
                      <li>N-period alaysis (weekly/monthly periods within a given time interval)</li>
                      </ul>


                      <hr>


                      <h3> Two-period comparison </h3>

                      We count sequences by collection date over time, selecting two arbitrary periods, respectively referenced as <i>target</i> and <i>background</i>.
                      The analysis produces a protein-specific target/background comparison of the prevalence of amino acid changes.

                      <p align="center">
                        <v-img
                            src="../images/mode2-2.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Considered amino-acid changes can be filtered according to percent in the background and target, and according to p-values and odd ratios.
                      Users can choose which proteins to see in the results and which particular changes to be highlighted (e.g., from ECDC annotations or prevalent changes that are present in >75% of the lineage sequences).

                      <p align="center">
                        <v-img
                            src="../images/mode2-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>


                      Filtered amino acids changes are then presented within a table, which provides, for each amino acid change, comparative analysis of target vs background, with p-values, odd ratios prevalence in the target and in the background. Columns can be reordered and important/characteristic changes of the lineages can be highlighted.

                      <p align="center">
                        <v-img
                            src="../images/mode2-4.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Amino acid changes of each target period can be then visually and comparatively inspected as bar charts on given proteins, where absolute counts are shown, and p-values and odds ratios can be inspected; several protein domains can also be visualized.

                      <p align="center">
                        <v-img
                            src="../images/mode2-5.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      <hr>


                      <h3> N-period analysis </h3>

                      We count sequences by collection date over time, selecting weekly/monthly periods within a given time interval.
                      The analysis produces a protein-specific target/background comparison of the prevalence of amino acid changes.

                      <p align="center">
                        <v-img
                            src="../images/mode2-6.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      When several period (weeks or months) are compared, each period is considered as a target with the precedent period as a background, so as to show trends in relative prevalence.

                      <p align="center">
                        <v-img
                            src="../images/mode2-7.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Considered amino-acid changes can be filtered according to percent in the background and target, and according to p-values and odd ratios. Filtered amino-acids are then presented within tables (similar to the previous mode) associated to each target/background pair and as a single heat map (shown below) comparing all target/background pairs

                      <p align="center">
                        <v-img
                            src="../images/mode2-8.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Amino acid changes of each target period can be then visually and comparatively inspected as bar-charts on given proteins as in the previous mode.

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
                      <br>
                      The Spatial Analysis allows to optionally choose a specific lineage (else, all lineages are included); a location of interest must be selected using the continent/country/region/sub-region levels.
                      This is defined as the <i>target</i>, whereas the <i>background</i> is the enclosing, typically larger region (providing users with a flexible mechanism for excluding specific sub-locations).
                      When multiple locations are selected (e.g., California, Nevada, Washinghton, and Utah), four different comparisons are built (e.g., California vs USA,  Nevada vs USA, Washinghton vs USA, and Utah vs USA).

                      <p align="center">
                        <v-img
                            src="../images/mode3-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>


                      The analysis can be restricted to a given time period and produces initially a visualization of collected sequences in the target and background, which are shown in absolute and counts and percentages; a dropdown allows to select the different selected targets one by one.

                      <p align="center">
                        <v-img
                            src="../images/mode3-2.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      Amino acid changes can be filtered and comparatively analyzed in:
                      <ul>
                      <li>a heatmap</li>
                      <li>a table</li>
                      </ul>

                      In the heatmap, all selected targets appear as columns and color maps may represent alternatively:
                      <ul>
                      <li>the percentage of sequences in the target;</li>
                      <li>the difference between target and background percentages;</li>
                      <li>the odds ration.</li>
                      </ul>

                      <p align="center">
                        <v-img
                            src="../images/mode3-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      In the multi-tab tables, different tabs represent the various selected target/background comparisons (below we selected the one for Nevada vs USA).

                      <p align="center">
                        <v-img
                            src="../images/mode3-4.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      As in the Temporal analysis mode, results can also be visually inspected as a bar-chart on a given protein.
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
                      <br>
                      In the Open Analysis, the user is free of selecting lineage, time period and location both for the target and background populations.
                      In the first panel, users define their target (here, e.g., Europe/Italy/Lombardy).

                      <p align="center">
                        <v-img
                            src="../images/mode4-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      In the second one, they define their background (here, e.g., Europe/Switzwerland/Ticino).

                      <p align="center">
                        <v-img
                            src="../images/mode4-2.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      The Summary tab can be opened to verify the previous choices (possibly partially overlapping---sequences that are present in both target and background are automatically removed). Proteins to be analyzed are selected here.

                      <p align="center">
                        <v-img
                            src="../images/mode4-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>


                      Results are presented as tables and bar-charts as in the Temporal and Spatial analyses described above. Below we show an example of comparison table where only changes that appear in >3% of the target population are included. We ordered by descending odds ratio.

                      <p align="center">
                        <v-img
                            src="../images/mode4-4.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
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
      let delayInMilliseconds = 10;
      let that = this;
      setTimeout(function() {
        that.expansionPanels = [];
      }, delayInMilliseconds);
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