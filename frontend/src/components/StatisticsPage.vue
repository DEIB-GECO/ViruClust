<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
      <v-card width="95%" style="margin-top:50px; padding: 50px" color="#F0E68C">
        <v-btn color="red" class="white--text" @click="setMetadataPage()">
          <v-icon style="margin-right: 5px">mdi-arrow-left-bold-outline</v-icon>CHANGE POPULATION / CHANGE METADATA
        </v-btn>
        <v-card-title class="justify-center"><h1>STATISTICS</h1></v-card-title>
        <v-card-text>
          <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 20px">
              <v-btn small color="blue" class="white--text" @click="inputStatsDialog = true">
                INPUT STATISTICS
              </v-btn>
            </v-flex>
            <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
              <v-card width="500px" color="#DAA520">
                <v-card-title>
                  <h5>Cluster counter (num of seq.):  (greater than)</h5>
                </v-card-title>
                <v-card-text style="margin-top: 30px">
                  <v-slider
                    v-model="sliderClusterCount"
                    always-dirty
                    persistent-hint
                    thumb-label="always"
                    min = "0"
                    max = "100"
                    color="#191970"
                    track-color="#191970"
                    thumb-color="#191970"
                  ></v-slider>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
              <v-card width="500px" color="#DAA520">
                <v-card-title>
                  <h5>Select Protein:</h5>
                </v-card-title>
                <v-card-text style="margin-top: 30px">
                  <v-select
                    v-model="selectedProtein"
                    :items="possibleProtein"
                    label="Protein"
                    solo
                    hide-details
                  ></v-select>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
              <v-card width="500px" color="#DAA520">
                <v-card-title>
                  <h5>Lineage frequency: (less than)</h5>
                </v-card-title>
                <v-card-text style="margin-top: 30px">
                  <v-slider
                    v-model="sliderLineageFrequency"
                    always-dirty
                    persistent-hint
                    thumb-label="always"
                    :step="1"
                    min = "0"
                    max = "100"
                    color="#191970"
                    track-color="#191970"
                    thumb-color="#191970"
                  ></v-slider>
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
          <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <v-btn
                     @click="apply()"
                     color="red"
                     class="white--text"
              >
                  APPLY
              </v-btn>
            </v-flex>
          </v-layout>

          <div v-if = "applied">
            <v-layout row wrap justify-center style="padding: 30px; margin-bottom: 50px">
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                <div style="width:80%; background-color: white">
                  <BarSeqChart></BarSeqChart>
                </div>
              </v-flex>
            </v-layout>

            <v-card color="#DAA520">
            <v-layout wrap align-center justify-center style="margin-bottom: 50px">
              <v-data-table
                      :headers="allResultTableHeaders"
                      :items="results"
                      class="data-table"
                      style="width: 90%; margin-top: 50px; margin-bottom: 50px"
                      multi-sort
              >
                <!--height="650"
                      fixed-header-->
                  <template v-slot:item ="{ item }">
                    <tr>
                      <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in allResultTableHeaders"
                          :key="header.value" v-show="header.show" :title=header.text>

                        <span v-if="header.value === 'pubs linear' || header.value === 'pubs non-linear' || header.value === 'sequences_count'">
                            <v-dialog width="500" scrollable>
                              <template v-slot:activator="{ on }">
                              <v-btn
                                    v-on="on"
                                    slot="activator"
                                    color="rgb(122, 139, 157)"
                                    small
                                    class="white--text">
                                <span v-if="header.value !== 'sequences_count'">
                                  {{header.value}}
                                </span>
                                <span v-else>
                                  sequences  ({{item[header.value]}})
                                </span>
                               </v-btn>
                              </template>
                              <v-card>
                                  <v-card-title
                                          style="background-color: #DAA520 ; color: white;"
                                          class="justify-center"
                                  >
                                    <span v-if="header.value === 'pubs linear'">
                                      Publications linear epitopes
                                    </span>
                                    <span v-else-if="header.value === 'pubs non-linear'">
                                      Publications non-linear epitopes
                                    </span>
                                    <span v-else-if="header.value === 'sequences_count'">
                                      Sequences
                                    </span>
                                  </v-card-title>
                                  <v-card-text style="margin-top: 20px; text-align: center">
                                    <span v-if="header.value !== 'sequences_count'">
                                      <span v-for="link in item[header.value]" v-bind:key="link">
                                        <a :href="link" target="_blank">- {{link}}</a>
                                        <br><br>
                                      </span>
                                    </span>
                                    <span v-else>
                                      <span v-for="seq in item['sequences']" v-bind:key="seq">
                                        <span>- {{seq}}</span>
                                        <br><br>
                                      </span>
                                    </span>
                                  </v-card-text>
                              </v-card>
                          </v-dialog>
                        </span>

                        <span v-else-if="Array.isArray(item[header.value])">
                          <span v-if="item[header.value].length > 0">
                            <span v-if="header.value === 'mutation'">
                              <span v-for="(item3, index) in item[header.value]" v-bind:key="item3">
                                <span v-if="index !== 0">, </span>
                                <span>{{item3}}</span>
                              </span>
                            </span>

                            <span v-else-if="header.value === 'pubs linear' || header.value === 'pubs non-linear'">
                              <br>
                              <span v-for="item2 in item[header.value]" v-bind:key="item2">
                                <a :href="item2" target="_blank">{{item2}}</a><br><br>
                              </span>
                            </span>

                            <span v-else>
                              <br>
                              <span v-for="item2 in item[header.value]" v-bind:key="item2">
                                <span style="white-space:nowrap;">{{item2}}</span><br><br>
                              </span>
                            </span>
                          </span>
                          <span v-else>
                            <span>N/D</span>
                          </span>
                        </span>

                        <span v-else>
                          <span v-if="item[header.value] !== '' && item[header.value] !== null && item[header.value] !== undefined">
                            <span v-if="header.value === '% lineage' || header.value === '% cluster'">{{(item[header.value]*100).toFixed(3)}}</span>
                            <span v-else-if="header.value === 'FC'">{{(item[header.value]).toFixed(3)}}</span>
                            <span v-else>{{item[header.value]}}</span>
                          </span>
                          <span v-else>
                            <span>N/D</span>
                          </span>
                        </span>
                      </td>
                    </tr>
                  </template>

              </v-data-table>
            </v-layout>
            </v-card>
          </div>

        </v-card-text>
      </v-card>
    </v-row>

    <div v-if = "applied">
      <ListResults></ListResults>
    </div>

    </v-container>

    <v-dialog
      persistent
    v-model="inputStatsDialog"
    width="1500"
  >
    <v-card>
      <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
        Input Statistics
        <v-spacer></v-spacer>
        <v-btn
            style="background-color: rgb(122, 139, 157)"
            slot="activator"
            icon
            small
          color="white"
          @click="inputStatsDialog = !inputStatsDialog"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="text-xs-center">
        <InputStats></InputStats>
      </v-card-text>

    </v-card>
  </v-dialog>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import BarSeqChart from "./BarSeqChart";
import ListResults from "./ListResults";
import InputStats from "./InputStats";

export default {
  name: "StatisticsPage",
  components: {InputStats, ListResults, BarSeqChart},
  data(){
    return{
      results: [],
      toBarGraphY: [],
      sliderClusterCount: 2,
      sliderLineageFrequency: 1,
      applied: false,
      inputStatsDialog: false,
      possibleProtein: ['Spike (surface glycoprotein)'],
      selectedProtein: 'Spike (surface glycoprotein)',
      listProteinLength: {
        'Spike (surface glycoprotein)' : 1274,
      }
    }
  },
  computed: {
    ...mapState(['allResultTable', 'allResultTableHeaders', 'allResultTable', 'allResultTableFixed', 'listResFixed', 'listRes', 'proteinSelected']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations(['setLoadPage', 'setMetadataPage', 'setStatisticsPage', 'setAllResultTable', 'setYAxisBarSeqChart', 'setListRes',
      'setProteinSelected']),
    ...mapActions([]),
    apply(){

      this.setAllResultTable(this.allResultTableFixed);
      var that = this;
      this.setAllResultTable(this.allResultTable.filter(function (i){
          let freq = JSON.parse(JSON.stringify(i['% lineage']));
          if (freq === -1 || freq === null){
            i['% lineage'] = null;
            i['FC'] = null;
            freq = 100;
          }
          else{
            freq = freq * 100;
          }
          let num_clust = i['# cluster']
          return (freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
        })
      );

      this.setListRes(this.listResFixed);
      this.setListRes(this.listRes.filter(function (i){
          let freq = JSON.parse(JSON.stringify(i['perc_lineage']));
          if (freq === -1 || freq === null){
            i['% lineage'] = null;
            i['FC'] = null;
            freq = 100;
          }
          else{
            freq = freq * 100;
          }
          let num_clust = i['num_cluster']
          return (freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
        })
      );


      this.applied = true;
      this.toBarGraphY = [];

      let res_table = JSON.parse(JSON.stringify(this.allResultTable));
      let len = res_table.length;
      let i = 0;
      let proteinLength = this.listProteinLength[this.proteinSelected];
      let barGraphY = new Array(proteinLength).fill(0);

      while (i < len){
        res_table[i]['sequences_count'] = res_table[i]['sequences'].length;
        let single_res = res_table[i];
        let mut = single_res['mutation'];
        let pos = mut[0];
        let seq = single_res['sequences'];
        let num_seq = seq.length;
        barGraphY[pos] = barGraphY[pos] + num_seq;
        i = i + 1;
      }

      let len2 = barGraphY.length;
      let j = 0;
      while (j < len2) {
        let pos = [j, barGraphY[j]];
        this.toBarGraphY.push(pos);
        j = j + 1;
      }

      this.setYAxisBarSeqChart(this.toBarGraphY);

    }
  },
  watch: {
    allResultTable(){
      this.results = JSON.parse(JSON.stringify(this.allResultTable));
    },
    sliderLineageFrequency(){
      this.applied = false;
    },
    sliderClusterCount(){
      this.applied = false;
    },
    selectedProtein(){
      this.applied = false;
      this.setProteinSelected(this.selectedProtein);
    }
  }
}
</script>

<style scoped>

</style>