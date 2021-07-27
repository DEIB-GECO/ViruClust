<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px; min-height: 83.5vh">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#FFBA08">
          <v-card-title class="justify-center">
            <h1>GEOGRAPHICAL DISTRIBUTION OF LINEAGES</h1>
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
               <h2>SELECT GEO-GRANULARITY AND LOCATION</h2>
              </v-flex>
              <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                <v-select
                  v-model="selectedGeoToChange"
                  :items="possibleGeo"
                  label="Granularity"
                  solo
                  hide-details
                ></v-select>
              </v-flex>
              <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                <v-autocomplete
                  v-model="selectedSpecificGeo"
                  :items="possibleSpecificGeo"
                  label="Specific Locality"
                  solo
                  hide-details
                  :item-text="getFieldText"
                  :disabled="selectedGeo === null || selectedGeo === 'world'"
                >
                  <template slot="item" slot-scope="data">
                        <span class="item-value-span">{{getFieldText(data.item)}}</span>
                        <span class="item-count-span">{{data.item.count}}</span>
                    </template>
                </v-autocomplete>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyChosen()"
                         color="#D00000"
                         class="white--text"
                         :disabled="(selectedGeo !== 'world' && this.selectedSpecificGeo === null) || selectedGeo === null"
                  >
                      APPLY
                  </v-btn>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="chosenApplied">
                  <TimeSelectorDistributionLineageInGeo
                  timeName = "distributionAnalyzeLineageInGeo"
                  :geoGranularity = "selectedGeo"
                  :geoSpecific = "selectedSpecificGeo">
                  </TimeSelectorDistributionLineageInGeo>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px" v-if="chosenApplied">
               <h2>MIN %</h2>
              </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0" v-if="chosenApplied">
               <h4>(The minimum percentage is used to filter the list of lineages in the result. Only the lineages
                 with at least the min % of the total number of sequences fulfilling all filters will appear)</h4>
              </v-flex>
               <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;"  v-if="chosenApplied">
                  <v-text-field v-model.number="selectedGeoCount" min="0" max="100" step = "0.1"  solo type="number" hide-details></v-text-field>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="chosenApplied">
                 <v-btn
                         @click="applyTableLineageCountry()"
                         color="#D00000"
                         class="white--text"
                         :disabled="selectedGeo !== 'world' && (selectedGeo === null || selectedSpecificGeo === null)"
                  >
                      APPLY
                  </v-btn>
               </v-flex>
             </v-layout>
           </v-card-text>
        </v-card>
      </v-row>
      <v-row justify="center" align="center" v-if="tableApplied">
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#FFBA08">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <h2>LINEAGES AND THEIR PRESENCE IN THE SELECTED LOCATION</h2>
                <v-btn @click="downloadTable('table_geo')" x-small icon
                style="margin-left: 20px;">
                  <v-icon size="23">
                    mdi-download-circle-outline
                  </v-icon>
                </v-btn>
               </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-data-table
                        :headers="headerTableLineageCountry"
                        :items="rowsTableLineageCountry"
                        class="data-table table_distribution_lineage_geo"
                        style="width: 90%; border: grey solid 1px"
                        :sort-by.sync="sortByTableLineageCountry"
                        :sort-desc.sync="sortDescTableLineageCountry"
                        hide-default-header
                        :custom-sort="customSort"
                  >
                    <template v-slot:header="{ props }">
                      <tr style="height: 50px;">
                        <th style="text-align: center"
                            v-bind:key="head.value"
                          v-for="head in props.headers"
                          :class="['header']"
                          @click="changeSort(head.value)"
                          @mouseover="selectHoverHeaderValue(head.value)"
                          @mouseout="deselectHoverHeaderValue(head.value)">
                              <span>{{ head.text.toUpperCase() }}</span>
                              <span v-if="head.value === hoverHeaderValue && head.value !== sortByTableLineageCountry[0]">
                                <v-icon class="icon_header" small>mdi-arrow-up</v-icon>
                              </span>
                              <span v-if="head.value === sortByTableLineageCountry[0]
                                  && sortDescTableLineageCountry[0] === false">
                                <v-icon class="icon_header" color="black" small>mdi-arrow-up</v-icon>
                              </span>
                              <span v-if="head.value === sortByTableLineageCountry[0]
                                  && sortDescTableLineageCountry[0] === true">
                                <v-icon class="icon_header" color="black" small>mdi-arrow-down</v-icon>
                              </span>
                          </th>
                      </tr>
                    </template>

                      <template v-slot:item ="{ item }">
                        <tr>
                          <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerTableLineageCountry"
                              :key="header.value" v-show="header.show" :title="item['lineage']">
                                <div v-if="header.value === 'lineage'" @click="orderColumn(item);" class="row-pointer"
                                @mouseover="selectHoverItemValue(item[header.value])"
                                @mouseout="deselectHoverItemValue(item[header.value])">
                                  <span>{{item[header.value]}}</span>
                                  <span v-if="item[header.value] === hoverItemValue && item !== selectedItem">
                                    <v-icon class="icon_header" small>mdi-arrow-up</v-icon>
                                  </span>
                                  <v-icon style="margin-left: 10px; color: black;" v-else-if="selectedItem === item && order_by_row_desc" small flat>mdi-arrow-up</v-icon>
                                  <v-icon style="margin-left: 10px; color: black;" v-else-if="selectedItem === item && !order_by_row_desc" small flat>mdi-arrow-down</v-icon>
                                </div>
                                <span v-else>{{item[header.value]}}</span>
                          </td>
                        </tr>
                      </template>
                  </v-data-table>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <HeatmapAnalyzeDistribution
                  nameHeatmap = "heatmap"
                  :headerTable = "headerTableLineageCountry"
                  :rowTable = "rowsTableLineageCountry"
                  :sortColumn = "sortByTableLineageCountry"
                  :descColumn = "sortDescTableLineageCountry"
                  :numSequences = "numberOfSequencesGeo"
                  :geoGranularity = "selectedGeo"
                  :denominators = "denominators">
                 </HeatmapAnalyzeDistribution>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 20px">
                 <ModifyColumnsHeatmap
                 :headerTable = "headerTableLineageCountry"
                 :rowTable = "rowsTableLineageCountry"
                 :denominators = "denominators"></ModifyColumnsHeatmap>
               </v-flex>
             </v-layout>
           </v-card-text>
        </v-card>
      </v-row>
    </v-card>

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
import HeatmapAnalyzeDistribution from "./HeatmapAnalyzeDistribution";
import TimeSelectorDistributionLineageInGeo from "./TimeSelectorDistributionLineageInGeo";
import ModifyColumnsHeatmap from "./ModifyColumnsHeatmap";

export default {
  name: "AnalyzeDistributionLineageInGeo",
  components: {ModifyColumnsHeatmap, TimeSelectorDistributionLineageInGeo, HeatmapAnalyzeDistribution},
  data() {
    return {
      overlay: false,
      selectedGeo: null,
      selectedGeoToChange: null,
      possibleGeo: ['World', 'Continent', 'Country', 'Region'],
      selectedSpecificGeo: null,
      possibleSpecificGeo: [],
      selectedGeoCount: 5,
      headerTableLineageCountry: [],
      headerTableLineageCountryLength: 0,
      headerTableLineageCountryFixed: [],
      rowsTableLineageCountry: [],
      rowsTableLineageCountryFixed: [],
      sortByTableLineageCountry: [],
      sortDescTableLineageCountry: [],
      hoverHeaderValue: null,
      hoverItemValue: null,
      selectedItem: null,
      order_by_row_desc: true,
      numberOfSequencesGeo: 0,
      chosenApplied: false,
      tableApplied: false,

      denominators: [],
      denominatorsFixed: [],
    }
  },
  computed: {
    ...mapState(['all_geo', 'startDateDistributionLineageInGeo', 'stopDateDistributionLineageInGeo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllGeo']),
    ...mapActions([]),
    downloadTable(table){
      let text = "";
      let result_sorted = this.sortResults(table);
      if(table === 'table_geo'){
        text = this.json2csv(result_sorted, this.headerTableLineageCountry);
      }
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
            fields.push(el.text);
        });
        selected_headers.forEach(function (el) {
            fields2.push(el.value);
        });
        var csv = json.map(function (row) {
            return fields2.map(function (fieldName) {
                let string_val ;
                string_val = String(row[fieldName]);
                string_val = string_val.replaceAll("\n", " ");
                return JSON.stringify(string_val);
            }).join(',')
        });
        csv.unshift(fields.join(','));
        return csv.join('\r\n')
    },
    sortResults(table){
      let len;
      let sortBy;
      let sortDesc;
      let results;
      if(table === 'table_geo'){
        len = this.sortByTableLineageCountry.length;
        sortBy = this.sortByTableLineageCountry;
        sortDesc = this.sortDescTableLineageCountry;
        results = JSON.parse(JSON.stringify(this.rowsTableLineageCountry));
      }
      if(len > 0) {
         return results.sort(function(a1, b1) {
            let i = 0;
            let a = a1[sortBy[i]];
            let b = b1[sortBy[i]];
            if(sortDesc[i] === false) {
                return a > b ? 1 : -1;
            }
            else{
                return a < b ? 1 : -1;
            }
         });
       }
       else{
         return results;
       }
    },
    applyTableLineageCountry(){
      this.headerTableLineageCountry = [];
      this.rowsTableLineageCountry = [];
      this.overlay = true;
      let url = `/analyze/tableLineageCountry`;
      let to_send = {'type': this.selectedGeo,
        'value': this.selectedSpecificGeo,
        'minCountSeq': this.selectedGeoCount,
        'minDate': this.startDateDistributionLineageInGeo,
        'maxDate': this.stopDateDistributionLineageInGeo};
      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let seq_mut_arr = JSON.parse(JSON.stringify(res));
          this.headerTableLineageCountry = [];

          let i = 0;
          let len_arr = seq_mut_arr.length;
          let headers = [];
          let arr_name_headers = [];
          let header_empty = {};
          let empty_header_present = false;
          while (i < len_arr) {
            let single_line = seq_mut_arr[i];
            Object.keys(single_line).forEach(key => {
              if(!arr_name_headers.includes(key) && key !== 'lineage') {

                if(key === "" || key === null || key === ''){
                  seq_mut_arr[i]['N/D'] = seq_mut_arr[i][""];
                }

                let single_header = {};
                arr_name_headers.push(key);
                if (key !== null && key !== ''){
                  single_header['text'] = key;
                  single_header['value'] = key;

                  single_header['show'] = true;
                  single_header['align'] = 'center';
                  single_header['width'] = '20vh';

                  headers.push(single_header);
                }
                else{
                  header_empty['text'] = 'N/D';
                  header_empty['value'] = 'N/D';

                  header_empty['show'] = true;
                  header_empty['align'] = 'center';
                  header_empty['width'] = '20vh';
                  empty_header_present = true;
                }
              }
              else if (key !== 'lineage'){
                if(key === "" || key === null || key === ''){
                  seq_mut_arr[i]['N/D'] = seq_mut_arr[i][""];
                }
                if (single_line['lineage'] === null){
                  single_line['lineage'] = 'N/D';
                }
              }
            })
            i = i + 1;
          }

          headers.sort( function( a, b ) {
              a = a.value.toLowerCase();
              b = b.value.toLowerCase();

              return a < b ? -1 : a > b ? 1 : 0;
          });

          if(empty_header_present) {
            headers.unshift(header_empty);
          }

          let lineage_header = {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '20vh'};

          headers.unshift(lineage_header);

          this.headerTableLineageCountry = headers;
          this.headerTableLineageCountryFixed = headers;


          seq_mut_arr = seq_mut_arr.sort( function( a, b ) {
            let a_lin = a['lineage'].toLowerCase();
            let b_lin = b['lineage'].toLowerCase();
            if(a_lin === "n/d"){
              return 1;
            }
            if(b_lin === "n/d"){
              return -1;
            }
            return a_lin < b_lin ? -1 : 1;
          });

          this.rowsTableLineageCountry = seq_mut_arr;
          this.rowsTableLineageCountryFixed = seq_mut_arr;

          let url = `/analyze/denominatorLineageCountry`;

          let to_send = {'type': this.selectedGeo,
            'value': this.selectedSpecificGeo,
            'minDate': this.startDateDistributionLineageInGeo,
            'maxDate': this.stopDateDistributionLineageInGeo};

          axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.denominators = res;
              this.denominatorsFixed = res;
              this.tableApplied = true;
              this.overlay = false;
            });

        });
    },
    createPossibleSpecificGeoObject(){
      let all_geo = this.all_geo;
      let i = 0;
      let geo = this.selectedGeo;
      let len = all_geo.length;
      let arr_all_specific_geo = [];
      while(i < len){
        let idx = arr_all_specific_geo.findIndex(item => item['value'] === all_geo[i][geo]);
        if (idx === -1 && all_geo[i][geo] !== null) {
          let elem = {'count': all_geo[i]['count'], 'value': all_geo[i][geo]};
          arr_all_specific_geo.push(elem);
        }
        else if(all_geo[i][geo] !== null){
          arr_all_specific_geo[idx]['count'] = arr_all_specific_geo[idx]['count'] + all_geo[i]['count'];
        }
        i = i + 1;
      }
      arr_all_specific_geo.sort( function( a, b ) {
          a = a['value'].toLowerCase();
          b = b['value'].toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
        });
      this.possibleSpecificGeo = arr_all_specific_geo;
    },
    getFieldText(item){
      this.numberOfSequencesGeo = item['count'];
      let name = '';
      name = item['value'];
      return name;
    },
    changeSort(column){
      if(this.sortByTableLineageCountry[0] === column && this.sortDescTableLineageCountry[0] === true){
        this.sortByTableLineageCountry = [];
        this.sortDescTableLineageCountry = [];
      }
      else {
        if (this.sortByTableLineageCountry[0] === column) {
          if (this.sortDescTableLineageCountry[0] === true) {
            this.sortDescTableLineageCountry = [false];
          } else {
            this.sortDescTableLineageCountry = [true];
          }
        } else {
          this.sortByTableLineageCountry = [column];
          this.sortDescTableLineageCountry = [false];
        }
      }
    },
    selectHoverHeaderValue(column){
      this.hoverHeaderValue = column;
    },
    deselectHoverHeaderValue(column){
      if(this.hoverHeaderValue === column){
        this.hoverHeaderValue = "";
      }
    },
    selectHoverItemValue(column){
      this.hoverItemValue = column;
    },
    deselectHoverItemValue(column){
      if(this.hoverItemValue === column){
        this.hoverItemValue = "";
      }
    },
    orderColumn(lineage){

      if(lineage !== this.selectedItem ) {
          this.order_by_row_desc = true;
          this.selectedItem = lineage;

          let old_header = JSON.parse(JSON.stringify(this.headerTableLineageCountry));

          let new_headers = old_header.splice(0, 1);

          let ordered_header = old_header.sort(function (a, b) {
            let lineage_a = '0';
            let lineage_b = '0';
            if(lineage[a.value] !== undefined && lineage[a.value] !== null){
              lineage_a = lineage[a.value].toString();
            }
            if(lineage[b.value] !== undefined && lineage[b.value] !== null){
              lineage_b = lineage[b.value].toString();
            }
            if (lineage_a === lineage_b) {
              return a.value.toLowerCase() > b.value.toLowerCase() ? 1 : -1;
            } else {
              return parseInt(lineage_a, 10) < parseInt(lineage_b, 10) ? 1 : -1;
            }
          });

          this.headerTableLineageCountry = new_headers.concat(ordered_header);
      }
      else if((lineage === this.selectedItem && !this.order_by_row_desc)){
          this.order_by_row_desc = true;
          this.selectedItem = null;
          this.headerTableLineageCountry = this.headerTableLineageCountryFixed;
      }
      else if(lineage === this.selectedItem && this.order_by_row_desc){

        this.order_by_row_desc = false;
        this.selectedItem = lineage;

        let old_header = JSON.parse(JSON.stringify(this.headerTableLineageCountry));

        let new_headers = old_header.splice(0, 1);

        let ordered_header = old_header.sort(function (a, b) {
            let lineage_a = '0';
            let lineage_b = '0';
            if(lineage[a.value] !== undefined && lineage[a.value] !== null){
              lineage_a = lineage[a.value].toString();
            }
            if(lineage[b.value] !== undefined && lineage[b.value] !== null){
              lineage_b = lineage[b.value].toString();
            }
            if (lineage_a === lineage_b) {
              return a.value.toLowerCase() > b.value.toLowerCase() ? 1 : -1;
            } else {
              return parseInt(lineage_a, 10) > parseInt(lineage_b, 10) ? 1 : -1;
            }
          });

        this.headerTableLineageCountry = new_headers.concat(ordered_header);
      }

    },
    customSort(items, index2, isDesc2) {
      let index = index2[0];
      let isDesc = isDesc2[0];
      items.sort((a, b) => {
        let count_a = '0';
        let count_b = '0';
        if(a[index] !== undefined && a[index] !== null){
          count_a = a[index].toString();
        }
        if(b[index] !== undefined && b[index] !== null){
          count_b = b[index].toString();
        }
        if (!isDesc) {
          if(count_a === count_b){
            let a_lin = a['lineage'].toLowerCase();
            let b_lin = b['lineage'].toLowerCase();
            if(a_lin === "n/d"){
              return 1;
            }
            if(b_lin === "n/d"){
              return -1;
            }
            return a_lin < b_lin ? -1 : 1;
          }
          else {
            return  parseInt(count_a, 10) < parseInt(count_b, 10)  ? 1 : -1;
          }
        } else {
          if(count_a === count_b){
            let a_lin = a['lineage'].toLowerCase();
            let b_lin = b['lineage'].toLowerCase();
            if(a_lin === "n/d"){
              return 1;
            }
            if(b_lin === "n/d"){
              return -1;
            }
            return a_lin < b_lin ? -1 : 1;
          }
          else {
            return  parseInt(count_a, 10) > parseInt(count_b, 10)  ? 1 : -1;
          }
        }
      });
      return items;
    },
    applyChosen(){
      this.chosenApplied = true;
    }
  },
  watch: {
    headerTableLineageCountry(){
      this.headerTableLineageCountryLength = this.headerTableLineageCountry.length;
    },
    headerTableLineageCountryLength(){
      this.selectedItem = null;
      this.order_by_row_desc = true;
    },
    selectedGeo(){
      this.headerTableLineageCountry = [];
      this.rowsTableLineageCountry = [];
      if(this.selectedGeo !== null){
        this.createPossibleSpecificGeoObject();
        this.chosenApplied = false;
        this.tableApplied = false;
      }
    },
    selectedGeoToChange(){
      if(this.selectedGeoToChange === 'Continent'){
        this.selectedGeo = 'geo_group';
      }
      else{
        this.selectedGeo = this.selectedGeoToChange.toLowerCase();
      }
    },
    selectedSpecificGeo() {
      this.headerTableLineageCountry = [];
      this.rowsTableLineageCountry = [];
      this.chosenApplied = false;
      this.tableApplied = false;
    },
    selectedGeoCount(){
      if(this.selectedGeoCount < 0){
        this.selectedGeoCount = 0;
      }
      else if(this.selectedGeoCount > 100){
        this.selectedGeoCount = 100;
      }
      this.tableApplied = false;
    },
    startDateDistributionLineageInGeo(){
      this.tableApplied = false;
    },
    stopDateDistributionLineageInGeo(){
      this.tableApplied = false;
    }
  },
  mounted() {

  }
}
</script>

<style scoped>

  .table_distribution_lineage_geo table > tbody > tr > td:nth-child(1){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

  .table_distribution_lineage_geo table > tr > th:nth-child(1){
    box-shadow: inset -0.5px 0 0 0 grey;
  }
  /*position: sticky !important;*/
  /*  position: -webkit-sticky !important;*/
  /*  left: 0px;*/
  /*  z-index: 9998;*/
  /*  background: white;*/

  .item-value-span {
      padding-right: 3.5em;
  }

  .item-count-span {
      /*float:right;*/
      position: absolute;
      right: 0.5em;
  }

  .header {
    border-bottom: darkgrey solid 1px;
    min-width: 15vh;
  }

  .header:hover {
    cursor: pointer;
  }

  table > tbody > tr > td:nth-child(1),
  table > tr > th:nth-child(1){
    position: sticky !important;
    position: -webkit-sticky !important;
    left: 0;
    z-index: 1;
    background: white;
  }

  .row-pointer {
    cursor: pointer;
  }

</style>