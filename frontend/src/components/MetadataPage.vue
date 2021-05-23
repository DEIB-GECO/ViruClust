<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
      <v-card width="1800px" style="margin-top:50px" color="#F0E68C">
        <v-card-title class="justify-center"><h1>METADATA</h1></v-card-title>
        <v-card-text>
          <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <v-btn
                     @click="apply()"
                     class="white--text"
                     color="red"
              >
                  APPLY
              </v-btn>
            </v-flex>
          </v-layout>

          <v-container fluid grid-list-xl>
            <v-layout wrap align-center justify-center>
                <v-flex class="no-horizontal-padding xs12 d-flex"
              v-for="(v1, v2) in allMetadata" v-bind:key="v2">
                <v-card color="#DAA520" style="margin: 20px; padding: 20px">
                  <v-container fluid grid-list-xl style="justify-content: center;">
                  <v-row justify="center" align="center">
                   <h2>{{v2.toUpperCase()}}</h2>
                  </v-row>
                </v-container>
                  <v-layout wrap align-center justify-center v-if="v2 === 'date'">
                    <v-container fluid grid-list-xl style="justify-content: center; margin-top: 50px">
                      <v-row justify="center" align="center">
                       <h5>Select Date Filter:</h5>
                      </v-row>
                    </v-container>
                    <v-container fluid grid-list-xl style="justify-content: center; width: 200px">
                      <v-row justify="center" align="center">
                        <v-select
                          v-model="selectedDateFilter"
                          :items="possibleDateFilter"
                          label="Date filter"
                          solo
                        ></v-select>
                      </v-row>
                    </v-container>
                    <v-row justify="center" align="center">
                      <v-flex class="no-horizontal-padding xs6 d-flex">
                        <MetadataPieChart
                            :nameMetadata="v2"
                            :metadataContent="v1"
                            :filterDate = "selectedDateFilter">
                        </MetadataPieChart>
                      </v-flex>
                      <v-flex class="no-horizontal-padding xs6 d-flex">
                        <MetadataBarChart
                            :nameMetadata="v2+v2"
                            :metadataContent="v1"
                            :filterDate = "selectedDateFilter">
                        </MetadataBarChart>
                      </v-flex>
                    </v-row>
                  </v-layout>

                  <v-layout wrap align-center justify-center v-else>
                    <v-flex class="no-horizontal-padding xs6 d-flex">
                      <MetadataPieChart
                          :nameMetadata="v2"
                          :metadataContent="v1">
                      </MetadataPieChart>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs6 d-flex">
                      <MetadataBarChart
                          :nameMetadata="v2+v2"
                          :metadataContent="v1">
                      </MetadataBarChart>
                    </v-flex>
                  </v-layout>
                 </v-card>
                </v-flex>

            </v-layout>
          </v-container>

        </v-card-text>
      </v-card>
    </v-row>
    </v-container>

    <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import MetadataPieChart from "./MetadataPieChart";
import MetadataBarChart from "./MetadataBarChart";

export default {
  name: "MetadataPage",
  components: {MetadataBarChart, MetadataPieChart},
  data(){
    return{
      overlay: false,
      possibleDateFilter: ['Day', 'Month', 'Year'],
      selectedDateFilter: 'Day',
    }
  },
  computed: {
    ...mapState(['fileFASTA', 'fileCSV', 'allMetadata', 'htmlAttached']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations(['setLoadPage', 'setMetadataPage', 'setStatisticsPage', 'setAllResultTable',
       'setAllResultTableHeaders', 'setHtmlAttached', 'setAllResultTableFixed']),
    ...mapActions([]),
    apply(){
       this.overlay = true;
       let url = '/analyze_file/secondAnalysis'
      let to_send = {'fileCSV': this.fileCSV, 'fileFASTA': this.fileFASTA}
      axios.post(url, to_send)
      .then((res) => {
          return res.data;
      })
      .then((res) => {
          let res_table = res['table'];
          let res_html = res['html'];

          this.setHtmlAttached(res_html);

          let single_line = res_table[0];
          let headers = [];
          Object.keys(single_line).forEach(key => {
              let single_header = {};
              single_header['text'] = key;

              if(key === 'sequences'){
                single_header['value'] = 'sequences_count';
              }
              else{
                single_header['value'] = key;
              }

              single_header['sortable'] = !(key === 'epi_seq' || key === 'pubs linear' || key === 'pubs non-linear');

              single_header['show'] = true;
              single_header['align'] = 'center';
              single_header['width'] = '15vh';

              if (key === 'cluster'){
                single_header['sort'] = (a, b) => {
                  let num1 = a.match(/\d+/g);
                  let num2 = b.match(/\d+/g);
                  return num1[0] - num2[0];
                };
              }
              else if (key === 'mutation'){
                single_header['sort'] = (a, b) => {
                  if (a[0] === b[0]) {
                    if (a[1] === b[1]) {
                      if(a[2] === "-"){
                        return 1;
                      }
                      else if(b[2] === "-"){
                        return -1;
                      }
                      else {
                        return a[2] > b[2] ? 1 : -1;
                      }
                    }
                    else{
                      if(a[1] === "-"){
                        return 1;
                      }
                      else if(b[1] === "-"){
                        return -1;
                      }
                      else {
                        return a[1] > b[1] ? 1 : -1;
                      }
                    }
                  }
                  else {
                    return parseInt(a[0],10) > parseInt(b[0], 10) ? 1 : -1;
                  }
                };
              }

              let len = res_table.length;
              let i = 0;

              while (i < len){
                res_table[i]['sequences_count'] = res_table[i]['sequences'].length;
                i = i + 1;
              }

              headers.push(single_header);
          })

          res_table = res_table.sort(function(a, b){
            let num1 = a['cluster'].match(/\d+/g);
            let num2 = b['cluster'].match(/\d+/g);
            return num1[0] - num2[0];
          });

          this.setAllResultTableHeaders(headers);
          this.setAllResultTable(res_table);
          this.setAllResultTableFixed(res_table);

          this.overlay = false;
      });
    },
  },
  watch: {
    overlay(){
      if(!this.overlay){
        this.setStatisticsPage();
      }
    }
  }
}
</script>

<style scoped>

</style>