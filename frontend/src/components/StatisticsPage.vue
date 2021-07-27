<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
      <v-card width="95%" style="margin-top:50px; margin-bottom: 50px; padding: 50px" color="#F0E68C">
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
              <v-card width="500px" color="#FFBA08">
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
              <v-card width="500px" color="#FFBA08">
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
              <v-card width="500px" color="#FFBA08">
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
          <v-layout row wrap justify-center style="margin-top: 50px">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <v-card width="500px" color="#FFBA08">
                <v-layout row wrap justify-center style="padding: 30px;">
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                    <h3>Filter graph on cluster and lineages:</h3>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                    <v-select
                      v-model="selectedClusters"
                      :items="possibleClusters"
                      label="Clusters"
                      multiple
                      solo
                      hide-details
                    ></v-select>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                    <v-select
                      v-model="selectedLineages"
                      :items="possibleLineages"
                      label="Lineages"
                      multiple
                      solo
                      hide-details
                    ></v-select>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                    <div v-if="selectedClusters.length > 0 || selectedLineages.length > 0" style="text-align: center">
                      <h4>Filters:</h4>
                      <span v-if="selectedClusters.length > 0">
                        <span>CLUSTERS: </span>
                        <span v-for="(cluster,index) in selectedClusters" v-bind:key="cluster">
                          <span v-if="index !== 0">, </span>
                          <span>{{cluster}}</span>
                        </span>
                      </span>
                      <span v-if="selectedLineages.length > 0">
                        <br>
                        <span>LINEAGES: </span>
                        <span v-for="(lineage, index) in selectedLineages" v-bind:key="lineage">
                          <span v-if="index !== 0">, </span>
                          <span>{{lineage}}</span>
                        </span>
                      </span>
                    </div>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                    <v-btn
                           @click="removeClusterLineageFilter()"
                           color="red"
                           class="white--text"
                           small
                           :disabled="selectedClusters.length === 0 && selectedLineages.length === 0"
                    >
                        REMOVE FILTERS
                    </v-btn>
                  </v-flex>
               </v-layout>
              </v-card>
            </v-flex>
          </v-layout>
          <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <v-btn
                     @click="apply(); $vuetify.goTo(1200, {duration: 1000, offset: 0, easing: 'easeInOutQuart'})"
                     color="red"
                     class="white--text"
              >
                  APPLY
              </v-btn>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>

      <v-card width="95%" style="margin-top:50px; padding: 50px" color="#F0E68C" v-if="applied">
        <v-card-text>

          <v-layout row wrap justify-center style="padding: 30px; margin-bottom: 50px">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <div style="width:80%; background-color: white">
                <BarSeqChart></BarSeqChart>
              </div>
            </v-flex>
          </v-layout>

          <v-card color="#FFBA08" style="padding-bottom: 50px">
            <v-layout wrap align-center justify-center>
              <v-data-table
                      :headers="allResultTableHeaders"
                      :items="results"
                      class="data-table"
                      style="width: 90%; margin-top: 50px; margin-bottom: 50px"
                      multi-sort
                      :sort-by.sync="sortBy"
                      :sort-desc.sync="sortDesc"
                      :custom-sort="customSort"
              >
                <!--height="650"
                      fixed-header-->
                  <template v-slot:item ="{ item }">
                    <tr>
                      <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in allResultTableHeaders"
                          :key="header.value" v-show="header.show">

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
                                          style="background-color: #FFBA08 ; color: white;"
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

                            <span v-else-if="header.value === 'annotations'">
                              <v-dialog width="800" scrollable>
                                <template v-slot:activator="{ on }">
                                  <v-btn
                                    v-on="on"
                                    slot="activator"
                                    color="rgb(122, 139, 157)"
                                    small
                                    class="white--text">
                                    <span>
                                      Annotations
                                    </span>
                                  </v-btn>
                                </template>
                                <v-card>
                                  <v-card-title
                                          style="background-color: #FFBA08 ; color: white;"
                                          class="justify-center"
                                  >
                                    <span>
                                      Annotations
                                    </span>
                                  </v-card-title>
                                  <v-card-text style="margin-top: 20px;">
                                    <span v-for="(annotation, index) in item[header.value]" v-bind:key="index">
                                      <v-layout row wrap justify-center>
                                        <v-card style=" padding: 20px; margin-bottom: 20px; margin-top: 20px; border: darkgrey solid 1px; border-radius: 15px" width="500">
                                          <span v-for="(value, key) in annotation" v-bind:key="key">
                                            <span><b> - {{key}}: </b>
                                              <span v-if="key !== 'EvidenceUrls'">
                                                {{value}}
                                              </span>
                                              <span v-else>
                                                <div style="display: inline-grid; vertical-align: central;">
                                                  <span v-for="link in value.slice(1,-1).replaceAll('\'', '').split(',')" v-bind:key="link" style="word-wrap:break-word; max-width: 400px">
                                                    <span v-if="link !== ''">
                                                      <a :href="link" target="_blank"> {{link}}</a>
                                                      <br>
                                                    </span>
                                                    <span v-else>
                                                      N/D
                                                    </span>
                                                  </span>
                                                </div>
                                              </span>
                                            </span>
                                            <br>
                                          </span>
                                        </v-card>
                                      </v-layout>
                                    </span>
                                  </v-card-text>
                                </v-card>
                              </v-dialog>
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
            <v-layout wrap align-center justify-center>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                <v-btn @click="downloadTable()"
                     class="white--text" small
                     color="rgb(122, 139, 157)">
                Download Result Table</v-btn>
              </v-flex>
            </v-layout>
          </v-card>

        </v-card-text>
      </v-card>
    </v-row>

    <div v-if = "applied">
      <ListResults
      :sortBy = sortBy
      :sortDesc = sortDesc>
      </ListResults>
    </div>

    </v-container>

    <v-dialog
      persistent
    v-model="inputStatsDialog"
    width="1500"
  >
    <v-card>
      <v-card-title class="headline" style="background-color: #FFBA08 ; color: white">
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
      },
      sortBy: [],
      sortDesc: [],
      selectedClusters: [],
      selectedLineages: [],
      possibleClusters: [],
      possibleLineages: [],
      resultsInstance: null,
      listResultsInstance: null,
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
    customSort(){
         let len = this.sortBy.length;
         let results = JSON.parse(JSON.stringify(this.results));
         let that = this;
         return results.sort(function(a1, b1) {
              let i = 0;
              while(i < len) {
                let a = a1[that.sortBy[i]];
                let b = b1[that.sortBy[i]];
                let is_same = false;
                if (Array.isArray(a)){
                  is_same = (a.length === b.length) && a.every(function(element, index) {
                      return element === b[index];
                  });
                }
                else{
                  if(a === b){
                    is_same = true;
                  }
                }
                if(is_same && (i+1) < len){
                  i = i + 1;
                }
                else if (is_same && (i+1) >= len){
                  let a2 = a1['cluster'];
                  let b2 = b1['cluster'];
                  if (a2 === b2){
                    let a = a1['mutation'];
                    let b = b1['mutation'];
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
                  }
                  else {
                    let num11 = a2.match(/\d+/g);
                    let num22 = b2.match(/\d+/g);
                    return num11[0] - num22[0];
                  }
                }
                else{
                  if(that.sortDesc[i] === false) {
                    if (that.sortBy[i] === 'cluster'){
                      let num1 = a.match(/\d+/g);
                      let num2 = b.match(/\d+/g);
                      return num1[0] - num2[0];
                    }
                    else if (that.sortBy[i] === 'mutation'){
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
                    }
                    else {
                      return a > b ? 1 : -1;
                    }
                  }
                  else{
                    if (that.sortBy[i] === 'cluster'){
                      let num1 = a.match(/\d+/g);
                      let num2 = b.match(/\d+/g);
                      return num2[0] - num1[0];
                    }
                    else if (that.sortBy[i] === 'mutation'){
                      if (a[0] === b[0]) {
                        if (a[1] === b[1]) {
                          if(a[2] === "-"){
                            return -1;
                          }
                          else if(b[2] === "-"){
                            return 1;
                          }
                          else {
                            return a[2] < b[2] ? 1 : -1;
                          }
                        }
                        else{
                          if(a[1] === "-"){
                            return -1;
                          }
                          else if(b[1] === "-"){
                            return 1;
                          }
                          else {
                            return a[1] < b[1] ? 1 : -1;
                          }
                        }
                      }
                      else {
                        return parseInt(a[0],10) < parseInt(b[0], 10) ? 1 : -1;
                      }
                    }
                    else {
                      return a < b ? 1 : -1;
                    }
                  }
                }
              }
         });
    },
    downloadTable(){
      let result_sorted = this.sortResults();
      let text = this.json2csv(result_sorted, this.allResultTableHeaders);
      let filename = 'result.csv';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    json2csv(input, selected_headers) {
        var json = input;
        var fields = [];
        var fields2 = [];
        selected_headers.forEach(function (el) {
          if (el.value !== 'sequences_count') {
            fields.push(el.text);
          }
          else{
            fields.push('sequences');
          }
        });
        selected_headers.forEach(function (el) {
          if (el.value !== 'sequences_count') {
            fields2.push(el.text);
          }
          else{
            fields2.push('sequences');
          }
        });
        var csv = json.map(function (row) {
            return fields2.map(function (fieldName) {
                let string_val ;
                let val ;
                if(fieldName.includes('%') && row[fieldName]!== null){
                  val = (row[fieldName]*100);
                  string_val = String(val);
                }
                else if (fieldName === 'FC' && row[fieldName]!== null){
                  val = row[fieldName];
                  string_val = String(val);
                }
                else if (fieldName === 'annotations' && row[fieldName]!== null){
                  json = JSON.parse(JSON.stringify(row[fieldName]));
                  let i = 0;
                  while (i < json.length) {
                    if(json[i]['Description'].indexOf('\'') > -1){
                      json[i]['Description'] = json[i]['Description'].replaceAll('\'', '°');
                    }
                    json[i]['EvidenceUrls'] =  json[i]['EvidenceUrls'].slice(1,-1).replaceAll('\'', '').split(',');
                    i = i + 1;
                  }
                  val = JSON.stringify(json);
                  val = String(val);
                  val = val.replaceAll("\"", "'");
                  string_val = val;
                }
                else {
                  if (row[fieldName] === null || (Array.isArray(row[fieldName]) && row[fieldName].length === 0)){
                    string_val = 'N/D';
                  }
                  else {
                    string_val = String(row[fieldName]);
                  }
                }
                string_val = string_val.replaceAll("\n", " ");
                return JSON.stringify(string_val);
            }).join(',')
        });
        csv.unshift(fields.join(','));

        return csv.join('\r\n')
    },
    sortResults(){
       if(this.sortBy.length > 0) {
         return this.customSort();
       }
       else{
         return this.results;
       }
    },
    apply(){
      this.sortBy = [];
      this.sortDesc = [];
      this.setAllResultTable(this.allResultTableFixed);
      var that = this;
      this.setAllResultTable(this.allResultTable.filter(function (i){
          let freq = JSON.parse(JSON.stringify(i['% lineage']));
          let cluster = i['cluster'];
          let lineage = i['lineage'];
          if (freq === -1 || freq === null){
            i['% lineage'] = null;
            i['FC'] = null;
            freq = 100;
          }
          else{
            freq = freq * 100;
          }
          let num_clust = i['# cluster']
        if(that.selectedClusters.length > 0 && that.selectedLineages.length > 0) {
            return (that.selectedClusters.includes(cluster) && that.selectedLineages.includes(lineage)
              && freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
          }
          else if (that.selectedClusters.length > 0){
            return (that.selectedClusters.includes(cluster) && freq <= that.sliderLineageFrequency
                && num_clust >= that.sliderClusterCount);
          }
          else if (that.selectedLineages.length > 0) {
            return (that.selectedLineages.includes(lineage) && freq <= that.sliderLineageFrequency
                && num_clust >= that.sliderClusterCount);
          }
          else{
            return (freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
          }
        })
      );

      this.setListRes(this.listResFixed);
      this.setListRes(this.listRes.filter(function (i){
          let freq = JSON.parse(JSON.stringify(i['% lineage']));
          let cluster = i['cluster'];
          let lineage = i['lineage'];
          if (freq === -1 || freq === null){
            i['% lineage'] = null;
            i['FC'] = null;
            freq = 100;
          }
          else{
            freq = freq * 100;
          }
          let num_clust = i['# cluster']
          if(that.selectedClusters.length > 0 && that.selectedLineages.length > 0) {
            return (that.selectedClusters.includes(cluster) && that.selectedLineages.includes(lineage)
              && freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
          }
          else if (that.selectedClusters.length > 0){
            return (that.selectedClusters.includes(cluster) && freq <= that.sliderLineageFrequency
                && num_clust >= that.sliderClusterCount);
          }
          else if (that.selectedLineages.length > 0) {
            return (that.selectedLineages.includes(lineage) && freq <= that.sliderLineageFrequency
                && num_clust >= that.sliderClusterCount);
          }
          else{
            return (freq <= that.sliderLineageFrequency && num_clust >= that.sliderClusterCount);
          }
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

      this.resultsInstance = JSON.parse(JSON.stringify(this.allResultTable));
      this.listResultsInstance = JSON.parse(JSON.stringify(this.listRes));

    },
    removeClusterLineageFilter(){
       this.applied = false;
       this.selectedClusters = [];
       this.selectedLineages = [];
    }
  },
  mounted() {
    this.possibleClusters = [];
    this.possibleLineages = [];
    this.allResultTable.forEach(elem => {
      if(!this.possibleClusters.includes(elem['cluster'])){
        this.possibleClusters.push(elem['cluster']);
      }
      if(!this.possibleLineages.includes(elem['lineage'])){
        this.possibleLineages.push(elem['lineage']);
      }
    })
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
    },
    selectedClusters(){
      this.applied = false;
    },
    selectedLineages(){
      this.applied = false;
    }
  }
}
</script>

<style scoped>

</style>