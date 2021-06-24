<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#DAA520">
          <v-card-title class="justify-center">
            <h1>TIME (TARGET) vs TIME (BACKGROUND) in LINEAGE & COUNTRY</h1>
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                 <h2>SELECT LINEAGE AND COUNTRY OF INTEREST</h2>
               </v-flex>
               <!--<v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h4>(both fields can be empty, meaning that all lineages/countries are interesting)</h4>
               </v-flex>-->
                <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                  <v-select
                    v-model="selectedLineage"
                    :items="possibleLineage"
                    label="Lineage"
                    solo
                    hide-details
                    :item-text="getFieldText"
                  >
                  </v-select>
                </v-flex>
                <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                  <v-select
                    v-model="selectedCountry"
                    :items="possibleCountry"
                    label="Country"
                    solo
                    hide-details
                  >
                  </v-select>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyChosenLineageCountry()"
                         color="red"
                         class="white--text"
                  >
                      CHOSEN
                  </v-btn>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <TimeDistributionChart
                     v-if="chosenApplied && timeContent.length !== 0"
                     :timeName="timeName"
                     :timeContent="timeContent"
                     :filterDate="filterDate"
                     style="width: 80%"
                 ></TimeDistributionChart>
               </v-flex>
             </v-layout>

             <v-layout row wrap justify-center style="padding: 30px;" v-if="chosenApplied && timeContent.length !== 0">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h2>SELECT PROTEINS TO ANALYZE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h4>(no selection means "all protein")</h4>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                    <v-select
                      v-model="selectedProtein"
                      :items="possibleProtein"
                      label="Protein"
                      solo
                      hide-details
                      multiple
                    >
                    </v-select>
                  </v-flex>
               </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applySingleLineageAnalysis()"
                         color="red"
                         class="white--text"
                  >
                      APPLY
                  </v-btn>
                </v-flex>
             </v-layout>

             <v-layout row wrap justify-center v-if="chosenApplied && timeContent.length === 0">
               <v-row justify="center" align="center">
                <span style="background-color: #F0E68C;
                         width: 60%; height: 100px; border-radius: 10%; border: darkred solid 10px">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                      <span style="font-size: 50px; color: red; margin-top: 30px">NO DATA TO SHOW</span>
                    </v-flex>
                  </v-layout>
                </span>
              </v-row>
             </v-layout>
           </v-card-text>
        </v-card>
      </v-row>
      <v-row justify="center" align="center" v-if="tableApplied">
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#DAA520">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <h2>APPLY FILTERS TO TABLE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>% BACKGROUND:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinBackgroundFrequency"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxBackgroundFrequency"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MAX</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMaxBackgroundFrequency"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinBackgroundFrequency"
                                            max = "100"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                  </v-card>
                </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>% TARGET:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinTargetFrequency"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxTargetFrequency"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MAX</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMaxTargetFrequency"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinTargetFrequency"
                                            max = "100"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                  </v-card>
                </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>P-VALUE:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinPValue"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxPValue"
                                            step = "0.01"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MAX</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMaxPValue"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinPValue"
                                            max = "1"
                                            step = "0.01"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                  </v-card>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <v-btn
                         @click="applyFilterOnTable()"
                         color="red"
                         class="white--text"
                  >
                      APPLY FILTERS
                  </v-btn>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 80px">
                 <h2>TABLE</h2>
               </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-data-table
                        :headers="headerAnalyzeTime"
                        :items="rowsAnalyzeTime"
                        class="data-table table_analyze_time"
                        style="width: 90%; border: grey solid 1px"
                        multi-sort
                        :sort-by.sync="sortByAnalyzeTime"
                        :sort-desc.sync="sortDescAnalyzeTime"
                  >
                      <template v-slot:item ="{ item }">
                        <tr>
                          <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerAnalyzeTime"
                              :key="header.value" v-show="header.show">
                                <span v-if="header.value === 'mutation_position'"> {{item['mutation']}}</span>
                                <span v-else>{{item[header.value]}}</span>
                          </td>
                        </tr>
                      </template>
                  </v-data-table>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                  <v-btn @click="downloadTable('analyze_mutation')"
                         class="white--text"
                         small
                         color="rgb(122, 139, 157)">
                    Download Table</v-btn>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 80px">
                 <h2> BAR CHART based on P-VALUE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>P-VALUE:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinPValueBarChart"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxPValueBarChart"
                                            step = "0.01"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MAX</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMaxPValueBarChart"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinPValueBarChart"
                                            max = "1"
                                            step = "0.01"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                  </v-card>
                </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                 <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>SELECT PROTEIN:</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-select
                        v-model="selectedProteinForPValue"
                        :items="possibleProteinForPValue"
                        label="Lineage"
                        solo
                        hide-details
                      >
                      </v-select>
                    </v-card-text>
                 </v-card>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <v-btn
                         @click="applyFilterPValueChart()"
                         color="red"
                         class="white--text"
                         :disabled="selectedProteinForPValue === null"
                  >
                      APPLY
                 </v-btn>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <PValueBarChart
                     v-if="pValueBarChartApplied"
                     :namePValue="pValueName"
                     :pValueContent="pValueContent">
                 </PValueBarChart>
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
import PValueBarChart from "./PValueBarChart";
import TimeDistributionChart from "./TimeDistributionChart";

export default {
  name: "AnalyzeTimeLinCou",
  components: {TimeDistributionChart, PValueBarChart},
  data() {
    return {
      overlay: false,
      selectedLineage: null,
      possibleLineage: [],
      selectedCountry: null,
      possibleCountry: [],
      rowsAnalyzeTime: [],
      fixedRowAnalyzeTime: [],
      headerAnalyzeTime: [],
      sortByAnalyzeTime: [],
      sortDescAnalyzeTime: [],
      maxNumeratorTarget: 100,
      maxDenominatorTarget: 100,
      tableApplied: false,
      pValueName: 'p_value_time',
      pValueContent: [],
      pValueBarChartApplied: false,

      timeContent: [],
      timeName: 'timeDistribution',
      filterDate: 'Day',
      chosenApplied: false,
      selectedProtein: [],
      possibleProtein: [],

      selectedProteinForPValue: null,
      possibleProteinForPValue: [],

      selectedMinBackgroundFrequency: 0,
      selectedMaxBackgroundFrequency: 100,
      selectedMinTargetFrequency: 0,
      selectedMaxTargetFrequency: 100,
      selectedMinPValue: 0,
      selectedMaxPValue: 1,
      selectedMinPValueBarChart: 0,
      selectedMaxPValueBarChart: 1,
    }
  },
  computed: {
    ...mapState(['all_lineages', 'all_geo', 'all_protein', 'timeRangesTargetAndBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    getDaysArray(start, end) {
      for (var arr = [], dt = new Date(start); dt <= end; dt.setDate(dt.getDate() + 1)) {
        arr.push(new Date(dt).toISOString().slice(0, 10));
      }
      return arr;
    },
    downloadTable(table){
      let text = "";
      let result_sorted = this.sortResults(table);
      if(table === 'analyze_mutation'){
        text = this.json2csv(result_sorted, this.headerAnalyzeTime);
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
                let string_val;
                if (fieldName === 'mutation_position'){
                  string_val = String(row['mutation']);
                  string_val = string_val.replaceAll("\n", " ");
                }
                else {
                  string_val = String(row[fieldName]);
                  string_val = string_val.replaceAll("\n", " ");
                }
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
       if(table === 'analyze_mutation'){
        len = this.sortByAnalyzeTime.length;
        sortBy = this.sortByAnalyzeTime;
        sortDesc = this.sortDescAnalyzeTime;
        results = JSON.parse(JSON.stringify(this.rowsAnalyzeTime));
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
    getFieldText(item){
      return `${item['lineage']}` //  ----- ${item['cnt']}
    },
    applySingleLineageAnalysis(){
      let url = `/analyze/analyzeMutationCountryLineageInTime`;
      this.overlay = true;

      let lineage ;
      let country ;
      if(this.selectedLineage === null){
        lineage = 'empty';
      }
      else{
        lineage = this.selectedLineage;
      }
      if(this.selectedCountry === null){
        country = 'empty';
      }
      else{
        country = this.selectedCountry;
      }
      let start_target_time = this.timeRangesTargetAndBackground['start_target_time'];
      let end_target_time = this.timeRangesTargetAndBackground['end_target_time'];
      let start_background_time = this.timeRangesTargetAndBackground['start_background_time'];
      let end_background_time = this.timeRangesTargetAndBackground['end_background_time'];
      let array_protein = [];

      if(this.selectedProtein === null){
        array_protein = [];
      }
      else{
        array_protein = this.selectedProtein;
      }

      let to_send = {'lineage': lineage, 'country': [country], 'start_target': start_target_time,
              'end_target': end_target_time, 'start_background': start_background_time,
              'end_background': end_background_time, 'protein': array_protein}

      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let headers = [
              {'text': 'mutation', 'value': 'mutation_position', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'target', 'value': 'target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'background', 'value': 'background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'odd_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'numerator_background', 'value': 'numerator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'denominator_background', 'value': 'denominator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'numerator_target', 'value': 'numerator_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'denominator_target', 'value': 'denominator_target', 'show': true, 'align': 'center', 'width': '23vh'},
          ];

          this.headerAnalyzeTime= headers;
          this.rowsAnalyzeTime = res;
          this.fixedRowAnalyzeTime = res;

          let copy = JSON.parse(JSON.stringify(this.rowsAnalyzeTime));
          this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];

          let rowTable = JSON.parse(JSON.stringify(this.rowsAnalyzeTime));
          this.maxNumeratorTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['numerator_target']; }))
          this.maxDenominatorTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_target']; }))

          this.tableApplied = true;
          this.overlay = false;
        });
    },
    applyFilterOnTable(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeTime));
      var that = this;
      result = result.filter(function (i){
          let background_frequency = JSON.parse(JSON.stringify(i['percentage_background']));
          let target_frequency = JSON.parse(JSON.stringify(i['percentage_target']));
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          return (background_frequency >= that.selectedMinBackgroundFrequency
              && background_frequency <= that.selectedMaxBackgroundFrequency
              && target_frequency >= that.selectedMinTargetFrequency
              && target_frequency <= that.selectedMaxTargetFrequency
              && p_value >= that.selectedMinPValue
              && p_value <= that.selectedMaxPValue);
        })
      this.rowsAnalyzeTime = result;
    },
    applyFilterPValueChart(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeTime));
      var that = this;
      result = result.filter(function (i){
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          let product = JSON.parse(JSON.stringify(i['product']));
          return (p_value >= that.selectedMinPValueBarChart
              && p_value <= that.selectedMaxPValueBarChart
              && that.selectedProteinForPValue === product);
        })

      let arrayToBarChart = [];

      result.forEach(elem => {
        let mutation = elem['mutation'];
        let mutation_position = elem['mutation_position'];
        let idx = arrayToBarChart.findIndex(item => item['name'] === mutation);
        if (idx === -1) {
          let single_element = {'name': mutation, 'value': elem['numerator_target'], 'position': mutation_position};
          arrayToBarChart.push(single_element);
        } else {
          arrayToBarChart[idx]['value'] = arrayToBarChart[idx]['value'] + elem['numerator_target'];
        }
      })

      arrayToBarChart = arrayToBarChart.sort(function(a, b){
        let mutation_position1 = a['position'];
        let mutation_position2 = b['position'];
         return mutation_position1 > mutation_position2 ? 1 : -1;
      });

      this.pValueContent = arrayToBarChart;
      this.pValueName = 'p_value_time';
      this.pValueBarChartApplied = true;
    },
    applyChosenLineageCountry(){
      let url = `/analyze/analyzeTimeDistributionCountryLineage`;
      this.overlay = true;

      let lineage ;
      let country ;
      if(this.selectedLineage === null){
        lineage = 'empty';
      }
      else{
        lineage = this.selectedLineage;
      }
      if(this.selectedCountry === null){
        country = 'empty';
      }
      else{
        country = this.selectedCountry;
      }

      let to_send = {'lineage': lineage, 'country': country};

      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
            this.chosenApplied = true;
            this.overlay = false;
            this.timeName = 'timeDistribution';
             let arrOfDates = [];
            if( res.length !== 0) {

              let first_date = new Date(res[0]['name']);
              // let len = res.length;
              // let last_date = new Date(res[len-1]['name']);
              let last_date = new Date();
              last_date.setDate(last_date.getDate() + 1)

              let dayList = this.getDaysArray(first_date, last_date);
              dayList.forEach(day => {
                let idx = res.findIndex(item => item['name'] === day);
                if (idx === -1) {
                  let single_element = {'name': day, 'value': 0};
                  arrOfDates.push(single_element);
                } else {
                  let single_element = {'name': day, 'value': res[idx]['value']};
                  arrOfDates.push(single_element);
                }
              })
            }
            this.timeContent = arrOfDates;
        });
    }
  },
  watch: {
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    all_lineages(){
      this.possibleLineage = this.all_lineages;
    },
    all_geo(){
      let array_specific_geo = [];
      this.all_geo.forEach(elem => {
        if(elem['country'] !== null) {
          if (!array_specific_geo.includes(elem['country'])) {
            array_specific_geo.push(elem['country']);
          }
        }
      })
      array_specific_geo.sort( function( a, b ) {
        a = a.toLowerCase();
        b = b.toLowerCase();
        return a < b ? -1 : a > b ? 1 : 0;
      });
      this.possibleCountry = array_specific_geo;
    },
    selectedLineage(){
       this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.tableApplied = false;
       this.chosenApplied = false;
       this.selectedProtein = null;
    },
    selectedCountry() {
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.tableApplied = false;
      this.chosenApplied = false;
      this.selectedProtein = null;
    },
    selectedProtein(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.tableApplied = false;
    },
    timeRangesTargetAndBackground(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.tableApplied = false;
    },
    selectedProteinForPValue(){
      this.pValueBarChartApplied = false;
    },
    selectedMinBackgroundFrequency(){
      if (this.selectedMinBackgroundFrequency < 0 ){
        this.selectedMinBackgroundFrequency= 0;
      }
      else if (this.selectedMinBackgroundFrequency > this.selectedMaxBackgroundFrequency){
        this.selectedMinBackgroundFrequency = this.selectedMaxBackgroundFrequency;
      }
    },
    selectedMaxBackgroundFrequency(){
      if (this.selectedMaxBackgroundFrequency < this.selectedMinBackgroundFrequency ){
        this.selectedMaxBackgroundFrequency = this.selectedMinBackgroundFrequency;
      }
      else if (this.selectedMaxBackgroundFrequency > 100){
        this.selectedMaxBackgroundFrequency = 100;
      }
    },
    selectedMinTargetFrequency(){
      if (this.selectedMinTargetFrequency < 0 ){
        this.selectedMinTargetFrequency= 0;
      }
      else if (this.selectedMinTargetFrequency > this.selectedMaxTargetFrequency){
        this.selectedMinTargetFrequency = this.selectedMaxTargetFrequency;
      }
    },
    selectedMaxTargetFrequency(){
      if (this.selectedMaxTargetFrequency < this.selectedMinTargetFrequency ){
        this.selectedMaxTargetFrequency = this.selectedMinTargetFrequency;
      }
      else if (this.selectedMaxTargetFrequency > 100){
        this.selectedMaxTargetFrequency = 100;
      }
    },
    selectedMinPValue(){
      if (this.selectedMinPValue < 0 ){
        this.selectedMinPValue = 0;
      }
      else if (this.selectedMinPValue > this.selectedMaxPValue){
        this.selectedMinPValue = this.selectedMaxPValue;
      }
    },
    selectedMaxPValue(){
      if (this.selectedMaxPValue < this.selectedMinPValue ){
        this.selectedMaxPValue = this.selectedMinPValue;
      }
      else if (this.selectedMaxPValue > 1){
        this.selectedMaxPValue = 1;
      }
    },
    selectedMinPValueBarChart(){
      this.pValueBarChartApplied = false;
      if (this.selectedMinPValueBarChart < 0 ){
        this.selectedMinPValueBarChart = 0;
      }
      else if (this.selectedMinPValueBarChart > this.selectedMaxPValueBarChart){
        this.selectedMinPValueBarChart = this.selectedMaxPValueBarChart;
      }
    },
    selectedMaxPValueBarChart(){
      this.pValueBarChartApplied = false;
      if (this.selectedMaxPValueBarChart < this.selectedMinPValueBarChart ){
        this.selectedMaxPValueBarChart = this.selectedMinPValueBarChart;
      }
      else if (this.selectedMaxPValueBarChart > 1){
        this.selectedMaxPValueBarChart = 1;
      }
    },
  },
  mounted() {

    let array_specific_geo = [];
      this.all_geo.forEach(elem => {
        if(elem['country'] !== null) {
          if (!array_specific_geo.includes(elem['country'])) {
            array_specific_geo.push(elem['country']);
          }
        }
      })
      array_specific_geo.sort( function( a, b ) {
        a = a.toLowerCase();
        b = b.toLowerCase();
        return a < b ? -1 : a > b ? 1 : 0;
      });
      this.possibleCountry = array_specific_geo;

      this.possibleProtein = this.all_protein;
      this.possibleLineage = this.all_lineages;
  }
}
</script>

<style scoped>

  .table_analyze_time table > tbody > tr > td:nth-child(5),
  .table_analyze_time table > tbody > tr > td:nth-child(8),
  .table_analyze_time table > tbody > tr > td:nth-child(11){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

  .centered-input >>> input {
    text-align: center
  }

</style>