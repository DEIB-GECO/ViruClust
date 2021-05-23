<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center;">

      <v-row justify="center" align="center">
      <v-card width="95%" style="margin-top:50px" color="#F0E68C">
        <v-card-title class="justify-center"><h1>STATISTICS</h1></v-card-title>
        <v-card-text>
          <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
              <v-card width="500px" color="#DAA520">
                <v-card-title>
                  <h5>Cluster counter: </h5>
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
            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
              <v-card width="500px" color="#DAA520">
                <v-card-title>
                  <h5>Lineage frequency: </h5>
                </v-card-title>
                <v-card-text style="margin-top: 30px">
                  <v-slider
                    v-model="sliderLineageFrequency"
                    always-dirty
                    persistent-hint
                    thumb-label="always"
                    :step="0.01"
                    min = "0"
                    max = "1"
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
                            <span>{{item[header.value]}}</span>
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
      <div id="new" style="margin-top: 50px"></div>
    </v-container>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import BarSeqChart from "./BarSeqChart";

export default {
  name: "StatisticsPage",
  components: {BarSeqChart},
  data(){
    return{
      results: [],
      toBarGraphY: [],
      sliderClusterCount: 0,
      sliderLineageFrequency: 1,
      applied: false,
    }
  },
  computed: {
    ...mapState(['allResultTable', 'allResultTableHeaders', 'htmlAttached', 'allResultTable', 'allResultTableFixed']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations(['setLoadPage', 'setMetadataPage', 'setStatisticsPage', 'setAllResultTable', 'setYAxisBarSeqChart']),
    ...mapActions([]),
    apply(){

      this.setAllResultTable(this.allResultTableFixed);
      var that = this;
      this.setAllResultTable(this.allResultTable.filter(function (i){
          let freq = i['% lineage'];
          let num_clust = i['# cluster']
          return (freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
        })
      );


      this.applied = true;
      this.toBarGraphY = [];

      let res_table = JSON.parse(JSON.stringify(this.allResultTable));
      let len = res_table.length;
      let i = 0;
      let barGraphY = new Array(1274).fill(0);

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
    htmlAttached(){
      let element = document.getElementById("new");
      element.insertAdjacentHTML('afterend', this.htmlAttached);
    },
    sliderLineageFrequency(){
      this.applied = false;
    },
    sliderClusterCount(){
      this.applied = false;
    }
  }
}
</script>

<style scoped>

</style>