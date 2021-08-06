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
                      The Lineage Analysis provides a concise summary of the prevalence of SARS-CoV-2 Pango lineages in a specific (user-selected) place (continent/country/region) at a specific time interval.<br>
                      A histogram is used to show the number of genome sequences deposited in the GISAID database associated with the selected geographic location at different time points and ,<br>
                      A slider is used to visually select the time interval of choice on this histogram. <br>
                      Filters can be applied to select/represent only lineages above a user selected prevalence threshold.<br><br>

                      <p align="center">
                        <v-img
                            src="../images/mode1-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>

                      <br>
                      Results are provided in two forms:
                      <ul>
                      <li> a table with the prevalence of lineages by sub-locations </li>
                      <li> a heatmap visualization of the prevalence of different lineages (rows) at different sub-locations</li>
                      </ul>
                      <br>

                      <p align="center">
                          <v-img alt="center"
                              src="../images/mode1-2.png" width="700" style="border: grey solid 1px"
                          />
                      </p>
                      <br>
                      In the heatmap any arbitrary selection of columns can be aggregated and/or renamed by the user by using the MERGE tool<br><br>

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
                      The Temporal Analysis allows the study of the evolution of the genome of SARS-CoV-2 in time, at a specific place. Users can  optionally limit this analysis to a specific lineage of interest (all lineages are considered otherwise); the selection of a geographic location (continent/country/region/) is mandatory. <br>
                      Similar to the lineage analysis, the number of genomes deposited at different dates are displayed in the form of an histogram; users can restrict the comparison to a specific time-window: the start and end dates can be set by using the slider under the histogram.
                      <br><br>

                      <p align="center">
                        <v-img
                            src="../images/mode2-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Two main types of analyses are performed:
                      <ul>
                      <li>Compare two intervals (to compare 2 user selected intervals of time)</li>
                      <li>Time series (comparisons by weeks/months/user defined intervals)</li>
                      </ul>
                      <br>
                      <hr>
                      <br>
                      <h3> Compare two intervals </h3>
                      <br>
                      The prevalence of non synonymous amino acid substitutions is compared between two intervals of time, hereafter defined as the <i>target</i> and <i>background</i> interval.
                      Genomic sequences are assigned either to <i>target</i> or <i>background</i>, based on their collection date.
                      The final report provides a comparison of the prevalence of amino acid changes in the two intervals.
                      <br><br>

                      <p align="center">
                        <v-img
                            src="../images/mode2-2.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Filters can be applied to select patterns of interest: for example over/under representation in the target (statistical significance according to a chi-squared test),
                      and/or overall prevalence of the amino acid substitution. Users can also restrict the analysis to specific protein coding genes. <br>
                      Additional annotations can be used to highlight substitutions with a prevalence of 75% or more in a lineage (prevalent changes) or relevant changes in the spike glycoprotein,
                      associated with variants of concern according to the ECDC.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode2-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Results are displayed in the form of a table which provides p-values and odds ratios for the comparison and the prevalence in the target and in the background.
                      Columns can be reordered by the users and important/characteristic changes of the lineages can be highlighted.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode2-4.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Finally, to allow a rapid inspection of the possible functional implications and the association with protein domains and functional sites, amino acid changes which show a prevalence >= in the target, can be represented graphically, in the form of a bar-char, which reports absolute counts, p-values and odds ratios of each single substitution.
                      Annotations of functional sites and/or protein domains, according to XX can be selected and visualized as an additional layer of the plot.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode2-5.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      <hr>
                      <br>
                      <h3> Time series analysis </h3>
                      <br>
                      This type of analysis compares the prevalence of amino acid substitutions at different intervals of time.
                      The conceptual framework is the same as that applied by the <i>two interval</i> analysis, however in this case the time-window to be analysed is split into multiple (compared to 2) intervals.
                      Basically, this analysis is an extension of the two-intervals analysis, which allows the side by side comparison of multiple targets and backgrounds. <br>
                      The span of the time intervals, used to “segment” the initial time window can be set by the user by means of a dedicated drop-down menu.
                      Genome sequences are assigned to an interval based on their collection date.
                      <br><br>

                      <p align="center">
                        <v-img
                            src="../images/mode2-6.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Comparisons are performed pairwise, by considering consecutive intervals: for every pair the most recent interval is used as the target and the preceding interval is used as background. <br>
                      The final output provides a detailed report of the prevalence of amino-acid substitutions at different points in time.
                      An intuitive heatmap representation (intervals on the column, amino-acid changes on the rows) is used to display the prevalence of each substitution in time.
                      Comparisons of consecutive intervals can provide useful information on relative prevalence trends and/or patterns of fixation of specific amino acid changes.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode2-7.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Users can also apply all the advanced filters (protein/gene, prevalence, odds ratio, p-value, under/over representation) described in the previous section to limit the scope of the analysis.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode2-8.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Amino acid changes can also be visualized in the form of a bar-plot (again, see above), since this analysis defines multiple <i>target</i> intervals, multiple bar-plots will be produced (one for every target interval, i.e total number of intervals -1)
                      <br>
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
                      The Spatial Analysis compares the prevalence of amino-acid substitutions in the genome of SARS-CoV-2 between two distinct geographic locations. <br>
                      A specific lineage can be optionally selected by the user (otherwise , all lineages are included). Selection of a geographic location (continent/country/region/sub-region) is mandatory.
                      The place selected by the user is used as the <i>target</i>, whereas the geographic entity of higher level (i.e country for a region, continent for a country and so on) is used as the <i>background</i>.
                      The <i>exclude</i> menu can be used to include/exclude specific entities from the background (thus providing users with a flexible mechanism for excluding specific sub-locations). <br>
                      When multiple locations are selected (e.g., California, Nevada, Washinghton, and Utah), four different comparisons can be built (e.g., California vs USA, Nevada vs USA, Washinghton vs USA, and Utah vs USA).
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode3-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Similar to the lineage analysis, the number of genomes deposited at different dates are displayed in the form of an histogram;
                      users can restrict the comparison to a specific time-window: the start and end dates can be set by using the slider under the histogram.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode3-2.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      The final output consists of a table with a detailed comparison of the prevalence of amino-acid substitutions between the target and background. <br><br>
                      A heatmap representation (amino-acid substitutions on the rows, target locations on the columns) is also provided to offer a more compact overview of the prevalence of different mutations in different places.
                      However, the heatmap is plotted only when multiple target locations are specified. <br>
                      In the heatmap, color maps may represent alternatively:
                      <ul>
                      <li>the percentage of sequences in the target;</li>
                      <li>the difference between target and background percentages;</li>
                      <li>the odds ration.</li>
                      </ul>
                      <br><br>

                      <p align="center">
                        <v-img
                            src="../images/mode3-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      In the multi-tab tables, different tabs represent the various selected target/background comparisons (below we selected the one for Nevada vs USA).
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode3-4.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      The same advanced filters and the bar-chart graphical visualization described in the <i>compare two intervals</i> analysis are available to the user to restrict the breadth of the comparison and to obtain additional information/annotation.
                      <br>
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
                      The Open Analysis, is used to perform an unconstrained comparison of a user-defined target and background. In other words users are free to select any lineage, time interval and place for both the target and background populations. <br>
                      The first panel is used to define the target (here, e.g., Europe/Italy/Lombardy).
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode4-1.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      The second to define the background (here, e.g., Europe/Switzwerland/Ticino).
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode4-2.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      A third tab, called summary, provides a brief recap of the filters/selection performed by the user and reports the total number of genomes included in both groups.<br>
                      Additionally, by using the dropdown menu included in this tab, comparisons can be restricted to one or more proteins.
                      <br><br>
                      <p align="center">
                        <v-img
                            src="../images/mode4-3.png" width="700" style="border: grey solid 1px"
                        />
                      </p>
                      <br>
                      Results are presented in the same form and output types as available for the <i>Temporal</i> and <i>Spatial</i> analyses described above. <br>
                      Analogously, advanced filters can be applied, and an advanced bar-chart graphical representation with enhanced annotations can be obtained for any protein of choice.<br><br>
                      An example is reported below. In this case the advanced filters were used to select only amino-acid substitutions observed in at least 3% of the target population, and results were ordered by descending odds ratio.
                      <br><br>
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