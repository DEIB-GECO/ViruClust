<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
      <v-card width="1800px" style="margin-top:50px; margin-bottom: 50px; padding: 50px" color="#F0E68C">
        <v-card-title class="justify-center"><h1>METADATA</h1></v-card-title>
        <v-card-text>
           <v-card color="#DAA520" style="margin-top: 50px">
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <h3>SELECTED FILTER</h3>
               </v-flex>

               <v-layout row wrap justify-center style="padding: 30px;">
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center"
                  v-for="(item, field, index) in selectedFilters" v-bind:key="index">
                      <v-row align="center" justify="center" style="background-color:#800000; color: white; height: 60px; margin-bottom: 10px; padding-left: 20px">
                        <span><pre><b>{{field.toUpperCase()}} :  </b></pre></span>
                        <span v-if="field !== 'date'">
                          <span v-for="(singleIt, index) in item" v-bind:key="singleIt">
                            <span v-if="index !== 0"> , </span>
                            <span>{{singleIt}}</span>
                          </span>
                        </span>
                        <span v-else>
                          <span v-for="singleIt in item" v-bind:key="singleIt['min_val'] + singleIt['max_val']">
                              <span v-if="singleIt['min_val'] !== null">
                                from = {{singleIt['min_val']}}
                              </span>
                              <span v-if="singleIt['max_val'] !== null">
                                to = {{singleIt['max_val']}}
                              </span>
                          </span>
                        </span>
                        <v-spacer></v-spacer>
                        <v-btn icon @click="deleteFilter(field)"><v-icon color="white">mdi-close-circle</v-icon></v-btn>
                      </v-row>
                  </v-flex>
                </v-layout>

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
           </v-card>
             <v-tabs v-model="selectedTab"
                  vertical style="margin-top: 50px;" dark
                  background-color="#800000"
                  show-arrows>
               <v-tabs-slider color="" style="width: 500%"></v-tabs-slider>

               <v-tab style="border-bottom: orangered solid 1px">
                 <b><u>SELECT METADATA:</u></b>
               </v-tab>
              <v-tab v-for="(v1, v2) in allMetadata" v-bind:key="v2" style="border-bottom: orange solid 1px">
                {{v2.toUpperCase()}}
              </v-tab>

               <v-tab-item>
                 <v-card color="#DAA520" style="padding: 50px; border-radius: 0px" height="500">
                   <v-container fluid grid-list-xl style="justify-content: center;">
                      <v-row justify="center" align="center">
                       <h2>SELECT ONE METADATA FROM LIST</h2>
                      </v-row>
                    </v-container>
                 </v-card>
               </v-tab-item>

              <v-tab-item v-for="(v1, v2) in allMetadata" v-bind:key="v2" style="background-color: red">
                  <v-card color="#DAA520" style="padding: 50px; border-radius: 0px">
                    <v-container fluid grid-list-xl style="justify-content: center;">
                      <v-row justify="center" align="center">
                       <h2>{{v2.toUpperCase()}}</h2>
                      </v-row>
                    </v-container>
                    <v-container fluid grid-list-xl style="justify-content: center; margin-top: 50px;" v-if="v1.length === 0">
                      <v-row justify="center" align="center">
                       <h1>NOTHING TO SHOW</h1>
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
                      <v-row justify="center" align="center" style="width: 90%">
                        <v-flex class="xs6 d-flex">
                          <MetadataPieChart
                              :nameMetadata="v2"
                              :metadataContent="v1"
                              :filterDate = "selectedDateFilter">
                          </MetadataPieChart>
                        </v-flex>
                        <v-spacer></v-spacer>
                        <v-flex class="xs6 d-flex">
                          <MetadataBarChart
                              :nameMetadata="v2+v2"
                              :metadataContent="v1"
                              :filterDate = "selectedDateFilter">
                          </MetadataBarChart>
                        </v-flex>
                      </v-row>
                    </v-layout>

                    <v-layout wrap align-center justify-center v-else>
                      <v-flex class="xs6 d-flex">
                        <MetadataPieChart
                            :nameMetadata="v2"
                            :metadataContent="v1">
                        </MetadataPieChart>
                      </v-flex>
                      <v-spacer></v-spacer>
                      <v-flex class="xs6 d-flex">
                        <MetadataBarChart
                            :nameMetadata="v2+v2"
                            :metadataContent="v1">
                        </MetadataBarChart>
                      </v-flex>
                    </v-layout>

                    <v-layout row align-center justify-center v-if="v2 === 'date'">
                       <v-flex class="no-horizontal-padding xs12 d-flex">
                        <SelectorFilter
                            :nameMetadata="v2"
                            :metadataContent="v1"
                            :filterDate = "selectedDateFilter"></SelectorFilter>
                       </v-flex>
                    </v-layout>
                    <v-layout row align-center justify-center v-else>
                       <v-flex class="no-horizontal-padding xs6 d-flex">
                          <SelectorFilter
                            :nameMetadata="v2"
                            :metadataContent="v1"></SelectorFilter>
                       </v-flex>
                    </v-layout>
                  </v-card>
              </v-tab-item>
            </v-tabs>

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

    <v-overlay :value="overlay2">
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
import SelectorFilter from "./SelectorFilter";

export default {
  name: "MetadataPage",
  components: {SelectorFilter, MetadataBarChart, MetadataPieChart},
  data(){
    return{
      overlay: false,
      overlay2: false,
      selectedTab: 0,
      possibleDateFilter: ['Day', 'Month', 'Year'],
      selectedDateFilter: 'Day',
    }
  },
  computed: {
    ...mapState(['fileFASTA', 'fileCSV', 'allMetadata', 'selectedFilters', 'mutDict', 'selectedFilters',
    'allPossibleMetadataField']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations(['setLoadPage', 'setMetadataPage', 'setStatisticsPage', 'setAllResultTable',
       'setAllResultTableHeaders', 'setAllResultTableFixed', 'setListRes', 'setListResFixed', 'setStatisticsInput',
     'setAllMetadata']),
    ...mapActions(['setSelectedFilter']),
    deleteFilter(value){
       let val = {field: value, list:[]};
       this.setSelectedFilter(val);
    },
    apply(){
       this.overlay = true;
       let url = '/analyze_file/secondAnalysis'
      let to_send = {'fileCSV': this.fileCSV, 'mutDict': this.mutDict, 'selectedFilters': this.selectedFilters}
      axios.post(url, to_send)
      .then((res) => {
          return res.data;
      })
      .then((res) => {
          let res_table = JSON.parse(JSON.stringify(res['table']));
          let res_html = JSON.parse(JSON.stringify(res['html']));
          let res_stats = JSON.parse(JSON.stringify(res['stats']));

          this.setStatisticsInput(res_stats);

          res_html = res_html.sort(function(a, b){
            let num1 = a['cluster_name'].match(/\d+/g);
            let num2 = b['cluster_name'].match(/\d+/g);
            return num1[0] - num2[0];
          });

          this.setListRes(res_html);
          this.setListResFixed(res_html);

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
    selectedFilters(){
      this.overlay2 = true;
      let url = '/analyze_file/firstAnalysis'
      let to_send = {'fileCSV': this.fileCSV, 'selectedFilters': this.selectedFilters}
      axios.post(url, to_send)
      .then((res) => {
          return res.data;
        })
        .then((res) => {
          let allMeta = JSON.parse(JSON.stringify(this.allMetadata));
          Object.keys(allMeta).forEach(key => {
            allMeta[key] = [];
          });
          Object.keys(res).forEach(key => {
            allMeta[key] = res[key];
          });
          this.setAllMetadata(allMeta);
          this.overlay2 = false;
        });
    },
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