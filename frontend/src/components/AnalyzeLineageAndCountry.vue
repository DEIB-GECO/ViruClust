<template>
  <div>
    <v-card width="100%" color="#F0E68C" style="margin-bottom: 50px; margin-top: 50px; padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="600px" style="padding: 50px" color="#DAA520">
          <v-card-title class="justify-center">
            COUNTRY (TARGET) vs LINEAGE (BACKGROUND)
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
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
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                  <v-text-field v-model="selectedMinNumCase" solo type="number"></v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyLoadCountry()"
                         color="red"
                         class="white--text"
                         :disabled="selectedLineage === null"
                  >
                      APPLY
                  </v-btn>
                </v-flex>
             </v-layout>

             <v-layout row wrap justify-center style="padding: 30px;" v-if="countryReceived">
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                  <v-select
                    v-model="selectedCountry"
                    :items="possibleCountry"
                    label="Country"
                    solo
                    hide-details
                    multiple
                  >
                  </v-select>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                   <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
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
           </v-card-text>
        </v-card>
      </v-row>
      <v-row justify="center" align="center" v-if="tableApplied">
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#DAA520">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>Numerator_target:  (greater than)</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-slider
                        v-model="sliderNumeratorTarget"
                        always-dirty
                        persistent-hint
                        thumb-label="always"
                        min = "0"
                        :max = "maxNumeratorTarget"
                        color="#191970"
                        track-color="#191970"
                        thumb-color="#191970"
                      ></v-slider>
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>% background: (less than)</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-slider
                        v-model="sliderBackgroundFrequency"
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
               <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>Denominator_target:  (greater than)</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-slider
                        v-model="sliderDenominatorTarget"
                        always-dirty
                        persistent-hint
                        thumb-label="always"
                        min = "0"
                        :max = "maxDenominatorTarget"
                        color="#191970"
                        track-color="#191970"
                        thumb-color="#191970"
                      ></v-slider>
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>% target: (greater than)</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-slider
                        v-model="sliderTargetFrequency"
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
               <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>p-value: (less than)</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-slider
                        v-model="sliderPValue"
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
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <v-btn
                         @click="applyFilterOnTable()"
                         color="red"
                         class="white--text"
                  >
                      APPLY
                  </v-btn>
               </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-data-table
                        :headers="headerAnalyzeMutation"
                        :items="rowsAnalyzeMutation"
                        class="data-tabl table_analyze_mutation"
                        style="width: 90%; margin-bottom: 50px; border: grey solid 1px"
                        multi-sort
                        :sort-by.sync="sortByAnalyzeMutation"
                        :sort-desc.sync="sortDescAnalyzeMutation"
                  >
                      <template v-slot:item ="{ item }">
                        <tr>
                          <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerAnalyzeMutation"
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
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 30px">
                 <h1> BAR CHART based on P-VALUE</h1>
               </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                 <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>p-value: (less than)</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-slider
                        v-model="sliderPValueBarChart"
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
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                 <v-card width="500px" color="#A9A9A9">
                    <v-card-title>
                      <h5>Select protein:</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 5px">
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

export default {
  name: "AnalyzeLineageAndCountry",
  components: {PValueBarChart},
  data() {
    return {
      overlay: false,
      selectedMinNumCase: 5,
      selectedLineage: null,
      possibleLineage: [],
      selectedCountry: null,
      possibleCountry: [],
      countryReceived: false,
      rowsAnalyzeMutation: [],
      fixedRowAnalyzeMutation: [],
      headerAnalyzeMutation: [],
      sortByAnalyzeMutation: [],
      sortDescAnalyzeMutation: [],
      sliderNumeratorTarget: 0,
      sliderBackgroundFrequency: 100,
      sliderDenominatorTarget: 0,
      sliderTargetFrequency: 0,
      sliderPValue: 1,
      maxNumeratorTarget: 100,
      maxDenominatorTarget: 100,
      tableApplied: false,
      sliderPValueBarChart: 0.05,
      pValueName: 'p_value_country_lineage',
      pValueContent: [],
      pValueBarChartApplied: false,
      selectedProtein: [],
      possibleProtein: [],

      selectedProteinForPValue: null,
      possibleProteinForPValue: [],
    }
  },
  computed: {
    ...mapState(['all_protein']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllLineages']),
    ...mapActions([]),
    downloadTable(table){
      let text = "";
      let result_sorted = this.sortResults(table);
      if(table === 'analyze_mutation'){
        text = this.json2csv(result_sorted, this.headerAnalyzeMutation);
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
        len = this.sortByAnalyzeMutation.length;
        sortBy = this.sortByAnalyzeMutation;
        sortDesc = this.sortDescAnalyzeMutation;
        results = JSON.parse(JSON.stringify(this.rowsAnalyzeMutation));
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
    applyLoadCountry(){
      let url = `/analyze/possibleCountryLineage`;
      let to_send = {'lineage': this.selectedLineage, 'min_count': this.selectedMinNumCase};
      this.overlay = true;
      axios.post(url, to_send)
      .then((res) => {
        return res.data;
      })
      .then((res) => {
        this.possibleCountry = res;
        this.countryReceived = true;
        this.overlay = false;
      });
    },
    applySingleLineageAnalysis(){
      let url = `/analyze/analyzeMutationCountryLineage`;
      let array_country = [];
      this.overlay = true;
      if(this.selectedCountry === null){
        array_country = this.possibleCountry;
      }
      else{
        array_country = this.selectedCountry;
      }
      let array_protein = [];
      if(this.selectedProtein === null){
        array_protein = [];
      }
      else{
        array_protein = this.selectedProtein;
      }

      let to_send = {'lineage': this.selectedLineage, 'country': array_country, 'protein': array_protein};
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

          //     {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'country', 'value': 'country', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'count_seq', 'value': 'count_seq', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'product', 'value': 'product', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'start_aa_original', 'value': 'start_aa_original', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'sequence_aa_original', 'value': 'sequence_aa_original', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'sequence_aa_alternative', 'value': 'sequence_aa_alternative', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': '%', 'value': 'fraction', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'numerator', 'value': 'numerator', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'denominator', 'value': 'denominator', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': '%_country', 'value': 'fraction_country', 'show': true, 'align': 'center', 'width': '20vh'},
          //     {'text': 'denominator_country', 'value': 'denominator_country', 'show': true, 'align': 'center', 'width': '20vh'},
          ];
          this.headerAnalyzeMutation = headers;
          this.rowsAnalyzeMutation = res;
          this.fixedRowAnalyzeMutation = res;

          let copy = JSON.parse(JSON.stringify(this.rowsAnalyzeMutation));
          this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];

          let rowTable = JSON.parse(JSON.stringify(this.rowsAnalyzeMutation));
          this.maxNumeratorTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['numerator_target']; }))
          this.maxDenominatorTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_target']; }))

          this.tableApplied = true;
          this.overlay = false;
        });
    },
    applyFilterOnTable(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeMutation));
      var that = this;
      result = result.filter(function (i){
          let denominator_target = JSON.parse(JSON.stringify(i['denominator_background']));
          let numerator_target = JSON.parse(JSON.stringify(i['numerator_target']));
          let background_frequency = JSON.parse(JSON.stringify(i['percentage_background']));
          let target_frequency = JSON.parse(JSON.stringify(i['percentage_target']));
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          return (background_frequency <= that.sliderBackgroundFrequency
              && numerator_target >= that.sliderNumeratorTarget
              && denominator_target >= that.sliderDenominatorTarget
              && target_frequency >= that.sliderTargetFrequency
              && p_value <= that.sliderPValue);
        })
      this.rowsAnalyzeMutation = result;
    },
    applyFilterPValueChart(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeMutation));
      var that = this;
      result = result.filter(function (i){
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          let product = JSON.parse(JSON.stringify(i['product']));
          return (p_value <= that.sliderPValueBarChart
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
      this.pValueName = 'p_value_country_lineage';
      this.pValueBarChartApplied = true;
    }
  },
  watch: {
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    sliderPValueBarChart(){
      this.pValueBarChartApplied = false;
    },
    selectedLineage(){
       this.pValueBarChartApplied = false;
       this.tableApplied = false;
       this.countryReceived = false;
       this.selectedProtein = null;
    },
    selectedCountry(){
      this.pValueBarChartApplied = false;
      this.tableApplied = false;
      this.selectedProtein = null;
    },
    selectedProtein(){
      this.pValueBarChartApplied = false;
      this.tableApplied = false;
    },
    selectedProteinForPValue(){
      this.pValueBarChartApplied = false;
    },
  },
  mounted() {
    let url2 = `/analyze/allLineages`;
    axios.get(url2)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.possibleLineage = res;
      this.setAllLineages(res);
    });
  }
}
</script>

<style scoped>

  .table_analyze_mutation table > tbody > tr > td:nth-child(5),
  .table_analyze_mutation table > tbody > tr > td:nth-child(8),
  .table_analyze_mutation table > tbody > tr > td:nth-child(11){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

</style>