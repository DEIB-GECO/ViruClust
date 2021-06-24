<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#DAA520">
          <v-card-title class="justify-center">
            <h1>REGION (TARGET) vs COUNTRY (BACKGROUND)</h1>
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
               <h2>SELECT SPECIFIC GEO LOCALITY (until REGION is selected)</h2>
              </v-flex>
              <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                <v-select
                  v-model="selectedContinent_forProvReg"
                  :items="possibleContinent_forProvReg"
                  label="Continent"
                  solo
                  hide-details
                ></v-select>
              </v-flex>
              <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                <v-select
                  v-model="selectedCountry_forProvReg"
                  :items="possibleCountry_forProvReg"
                  label="Country"
                  solo
                  hide-details
                  :disabled="selectedContinent_forProvReg === null"
                ></v-select>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"
               v-if="selectedCountryToLower !== 'usa'">
                <RegionProvincePieChart
                  v-if="selectedCountry_forProvReg !== null && selectedCountryToLower !== 'usa'"
                  :nameGeo="geoSelectedName"
                  :geoContent="geoSelectedContent">
                </RegionProvincePieChart>
              </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px"
              v-if="selectedCountryToLower !== 'usa'">
                 <h2>SELECT REGION (TARGET) THAT WILL BE ANALYZED AGAINST ITS COUNTRY (BACKGROUND)</h2>
              </v-flex>
              <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                <v-select
                  v-model="selectedRegion_forProvReg"
                  :items="possibleRegion_forProvReg"
                  label="Region"
                  solo
                  hide-details
                  :disabled="selectedCountry_forProvReg === null"
                ></v-select>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"
               v-if="selectedCountryToLower === 'usa'">
                <RegionProvincePieChart
                  v-if="selectedRegion_forProvReg !== null && selectedCountryToLower === 'usa'"
                  :nameGeo="geoSelectedName"
                  :geoContent="geoSelectedContent">
                </RegionProvincePieChart>
               </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px"
              v-if="selectedCountryToLower === 'usa'">
                 <h2>SELECT REGION (TARGET) THAT WILL BE ANALYZED AGAINST ITS COUNTRY (BACKGROUND)</h2>
              </v-flex>
              <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;"
                      v-if="(selectedCountryToLower === 'usa')">
                <v-select
                  v-model="selectedProvince_forProvReg"
                  :items="possibleProvince_forProvReg"
                  label="Province"
                  solo
                  hide-details
                  :disabled="(selectedCountryToLower !== 'usa' || selectedRegion_forProvReg === null)"
                ></v-select>
              </v-flex>
             </v-layout>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 20px">
               <h2>SELECT PROTEINS TO ANALYZE</h2>
             </v-flex>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
               <h4>(no selection means "all protein")</h4>
             </v-flex>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
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
                       @click="applyTableProvReg()"
                       color="red"
                       class="white--text"
                       style="margin-top: 20px"
                       :disabled="!((selectedCountryToLower === 'usa' && selectedProvince_forProvReg !== null)
                              || (selectedCountryToLower !== 'usa' && selectedRegion_forProvReg !== null))"
                >
                    APPLY
                </v-btn>
             </v-flex>
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
                         @click="applyFilterOnTableProvReg()"
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
                        :headers="headerTableProvReg"
                        :items="rowsTableProvReg"
                        class="data-table table_prov_reg"
                        style="width: 90%; border: grey solid 1px"
                        multi-sort
                        :sort-by.sync="sortByTableProvReg"
                        :sort-desc.sync="sortDescTableProvReg"
                  >
                      <template v-slot:item ="{ item }">
                        <tr>
                          <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerTableProvReg"
                              :key="header.value" v-show="header.show">
                                <span v-if="header.value === 'lineage'">
                                  <v-dialog width="800" scrollable>
                                    <template v-slot:activator="{ on }">
                                      <v-btn
                                        v-on="on"
                                        slot="activator"
                                        color="rgb(122, 139, 157)"
                                        small
                                        class="white--text">
                                        <span>
                                          Lineages
                                        </span>
                                      </v-btn>
                                    </template>
                                    <v-card>
                                      <v-card-title
                                              style="background-color: #DAA520 ; color: white;"
                                              class="justify-center"
                                      >
                                        <span>
                                          Lineages
                                        </span>
                                      </v-card-title>
                                      <v-card-text style="margin-top: 20px;">
                                        <span v-for="lineage in item[header.value]" v-bind:key="lineage">
                                            <span>{{lineage}}</span>
                                            <br>
                                        </span>
                                      </v-card-text>
                                    </v-card>
                                  </v-dialog>
                                </span>
                                <span v-else-if="header.value === 'mutation_position'"> {{item['mutation']}}</span>
                                <span v-else>{{item[header.value]}}</span>
                          </td>
                        </tr>
                      </template>
                  </v-data-table>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                  <v-btn @click="downloadTable('table_prov_reg')"
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
import RegionProvincePieChart from "./RegionProvincePieChart";
import PValueBarChart from "./PValueBarChart";

export default {
  name: "AnalyzeProvinceRegion",
  components: {PValueBarChart, RegionProvincePieChart},
  data() {
    return {
      overlay: false,
      maxNumeratorTarget: 100,
      maxDenominatorTarget: 100,
      num_sequences_forProvReg: null,
      selectedContinent_forProvReg: null,
      possibleContinent_forProvReg: [],
      selectedCountry_forProvReg: null,
      possibleCountry_forProvReg: [],
      selectedRegion_forProvReg: null,
      possibleRegion_forProvReg: [],
      selectedProvince_forProvReg: null,
      possibleProvince_forProvReg: [],
      headerTableProvReg: [],
      rowsTableProvReg: [],
      fixedRowsTableProvReg: [],
      sortByTableProvReg: [],
      sortDescTableProvReg: [],
      geoSelectedName: '',
      geoSelectedContent: [],
      pValueName: 'p_value_province_region',
      pValueContent: [],
      tableApplied: false,
      pValueBarChartApplied: false,
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
    ...mapState(['all_geo', 'all_protein']),
    ...mapGetters({}),
    selectedCountryToLower(){
      if(this.selectedCountry_forProvReg !== null){
        return this.selectedCountry_forProvReg.toLowerCase();
      }
      else{
        return this.selectedCountry_forProvReg;
      }
    }
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    downloadTable(table){
      let text = "";
      let result_sorted = this.sortResults(table);
      if(table === 'table_prov_reg'){
        text = this.json2csv(result_sorted, this.headerTableProvReg);
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
      if(table === 'table_prov_reg'){
        len = this.sortByTableProvReg.length;
        sortBy = this.sortByTableProvReg;
        sortDesc = this.sortDescTableProvReg;
        results = JSON.parse(JSON.stringify(this.rowsTableProvReg));
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
    applyFilterOnTableProvReg(){
      let result = JSON.parse(JSON.stringify(this.fixedRowsTableProvReg));
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
      this.rowsTableProvReg = result;
    },
    applyTableProvReg(){
      let url = `/analyze/analyzeMutationProvinceRegion`;
      let type_geo1;
      let type_geo2;
      let geo1;
      let geo2;
      this.overlay = true;
      if(this.selectedProvince_forProvReg !== null){
        type_geo1 = 'region';
        type_geo2 = 'province';
        geo1 = this.selectedRegion_forProvReg;
        geo2 = this.selectedProvince_forProvReg;
      }
      else{
        type_geo1 = 'country';
        type_geo2 = 'region';
        geo1 = this.selectedCountry_forProvReg;
        geo2 = this.selectedRegion_forProvReg;
      }
      let array_protein = [];
      if(this.selectedProtein === null){
        array_protein = [];
      }
      else{
        array_protein = this.selectedProtein;
      }

      let to_send = {'type_geo1': type_geo1, 'geo1': geo1,
                     'type_geo2': type_geo2, 'geo2': geo2,
                     'protein': array_protein};
      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let headers = [
              {'text': 'mutation', 'value': 'mutation_position', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'target', 'value': 'target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'background', 'value': 'background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'product', 'value': 'product', 'show': true, 'align': 'center', 'width': '20vh'},
              //{'text': 'start_aa_original', 'value': 'start_aa_original', 'show': true, 'align': 'center', 'width': '20vh'},
              //{'text': 'sequence_aa_original', 'value': 'sequence_aa_original', 'show': true, 'align': 'center', 'width': '20vh'},
              //{'text': 'sequence_aa_alternative', 'value': 'sequence_aa_alternative', 'show': true, 'align': 'center', 'width': '20vh'},
              {'text': 'odd_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'numerator_background', 'value': 'numerator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'denominator_background', 'value': 'denominator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'numerator_target', 'value': 'numerator_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'denominator_target', 'value': 'denominator_target', 'show': true, 'align': 'center', 'width': '23vh'},
          ];
          this.headerTableProvReg = headers;
          this.rowsTableProvReg = res;
          this.fixedRowsTableProvReg = res;

          let copy = JSON.parse(JSON.stringify(this.rowsTableProvReg));
          this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];

          let rowTable = JSON.parse(JSON.stringify(this.rowsTableProvReg));
          this.maxNumeratorTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['numerator_target']; }))
          this.maxDenominatorTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_target']; }))

          this.tableApplied = true;
          this.overlay = false;
        });
    },
    applyFilterPValueChart(){
      let result = JSON.parse(JSON.stringify(this.fixedRowsTableProvReg));
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
      this.pValueName = 'p_value_province_region';
      this.pValueBarChartApplied = true;
    }
  },
  watch: {
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    selectedContinent_forProvReg(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProtein = null;
      this.tableApplied = false;
      this.headerTableProvReg = [];
      this.rowsTableProvReg = [];

      this.num_sequences_forProvReg = null;
      this.selectedCountry_forProvReg = null;
      this.possibleCountry_forProvReg = [];
      this.selectedRegion_forProvReg = null;
      this.possibleRegion_forProvReg = [];
      this.selectedProvince_forProvReg = null;
      this.possibleProvince_forProvReg = [];

      if(this.selectedContinent_forProvReg !== null) {
        let array_specific_geo = [];
        this.all_geo.forEach(elem => {
          if (elem['country'] !== null) {
            if (elem['geo_group'] === this.selectedContinent_forProvReg && !array_specific_geo.includes(elem['country'])) {
              array_specific_geo.push(elem['country']);
            }
          }
        })
        array_specific_geo.sort(function (a, b) {
          a = a.toLowerCase();
          b = b.toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
        });
        this.possibleCountry_forProvReg = array_specific_geo;
      }
    },
    selectedCountry_forProvReg(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProtein = null;
      this.tableApplied = false;
      this.headerTableProvReg = [];
      this.rowsTableProvReg = [];

      this.num_sequences_forProvReg = null;
      this.selectedRegion_forProvReg = null;
      this.possibleRegion_forProvReg = [];
      this.selectedProvince_forProvReg = null;
      this.possibleProvince_forProvReg = [];

      if(this.selectedCountry_forProvReg !== null) {
        let array_specific_geo = [];
        this.all_geo.forEach(elem => {
          if (elem['region'] !== null) {
            if (elem['country'] === this.selectedCountry_forProvReg && !array_specific_geo.includes(elem['region'])) {
              array_specific_geo.push(elem['region']);
            }
          }
        })
        array_specific_geo.sort(function (a, b) {
          a = a.toLowerCase();
          b = b.toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
        });
        this.possibleRegion_forProvReg = array_specific_geo;

        if(this.selectedCountryToLower !== 'usa') {
          this.geoSelectedName = this.selectedCountry_forProvReg;
          let arrayToPieChart = [];
          let all_geo2 = JSON.parse(JSON.stringify(this.all_geo));

          all_geo2.forEach(elem => {
            if(elem['country'] === this.selectedCountry_forProvReg) {
              let region = '';
              if(elem['region'] === null){
                region = 'N/D';
              }
              else{
                region = elem['region'];
              }
              let idx = arrayToPieChart.findIndex(item => item['name'] === region);
              if (idx === -1) {
                let single_element = {'name': region, 'value': elem['count']};
                arrayToPieChart.push(single_element);
              } else {
                arrayToPieChart[idx]['value'] = arrayToPieChart[idx]['value'] + elem['count'];
              }
            }
          })
          this.geoSelectedContent = arrayToPieChart;
        }
      }
    },
    selectedRegion_forProvReg(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProtein = null;
      this.tableApplied = false;
      this.headerTableProvReg = [];
      this.rowsTableProvReg = [];

      this.num_sequences_forProvReg = null;
      this.selectedProvince_forProvReg = null;
      this.possibleProvince_forProvReg = [];

      if(this.selectedRegion_forProvReg !== null) {
        let array_specific_geo = [];
        this.all_geo.forEach(elem => {
          if (elem['province'] !== null) {
            if (elem['region'] === this.selectedRegion_forProvReg && !array_specific_geo.includes(elem['province'])) {
              array_specific_geo.push(elem['province']);
            }
          }
        })
        array_specific_geo.sort(function (a, b) {
          a = a.toLowerCase();
          b = b.toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
        });
        this.possibleProvince_forProvReg = array_specific_geo;

       if(this.selectedCountryToLower === 'usa') {
          this.geoSelectedName = this.selectedRegion_forProvReg;
          let arrayToPieChart = [];
          let all_geo2 = JSON.parse(JSON.stringify(this.all_geo));

          all_geo2.forEach(elem => {
            if(elem['region'] === this.selectedRegion_forProvReg) {
              let province = '';
              if(elem['province'] === null){
                province = 'N/D';
              }
              else{
                province = elem['province'];
              }
              let idx = arrayToPieChart.findIndex(item => item['name'] === province);
              if (idx === -1) {
                let single_element = {'name': province, 'value': elem['count']};
                arrayToPieChart.push(single_element);
              } else {
                arrayToPieChart[idx]['value'] = arrayToPieChart[idx]['value'] + elem['count'];
              }
            }
          })
          this.geoSelectedContent = arrayToPieChart;
        }
      }
    },
    selectedProvince_forProvReg(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProtein = null;
      this.tableApplied = false;
      this.headerTableProvReg = [];
      this.rowsTableProvReg = [];

      if(this.selectedProvince_forProvReg !== null) {
        let array_specific_geo = [];
        this.all_geo.forEach(elem => {
          if (elem['province'] === this.selectedProvince_forProvReg) {
            array_specific_geo.push(elem['count']);
          }
        })
        this.num_sequences_forProvReg = array_specific_geo;
      }
    },
    all_geo(){
      let array_specific_geo = [];
      this.all_geo.forEach(elem => {
        if(elem['geo_group'] !== null) {
          if (!array_specific_geo.includes(elem['geo_group'])) {
            array_specific_geo.push(elem['geo_group']);
          }
        }
      })
      array_specific_geo.sort( function( a, b ) {
        a = a.toLowerCase();
        b = b.toLowerCase();
        return a < b ? -1 : a > b ? 1 : 0;
      });
      this.possibleContinent_forProvReg = array_specific_geo;
    },
    selectedProtein(){
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
        if(elem['geo_group'] !== null) {
          if (!array_specific_geo.includes(elem['geo_group'])) {
            array_specific_geo.push(elem['geo_group']);
          }
        }
      })
      array_specific_geo.sort( function( a, b ) {
        a = a.toLowerCase();
        b = b.toLowerCase();
        return a < b ? -1 : a > b ? 1 : 0;
      });
      this.possibleContinent_forProvReg = array_specific_geo;

    this.possibleProtein = this.all_protein;
  }
}
</script>

<style scoped>
  .table_prov_reg table > tbody > tr > td:nth-child(6),
  .table_prov_reg table > tbody > tr > td:nth-child(9),
  .table_prov_reg table > tbody > tr > td:nth-child(12){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

  .centered-input >>> input {
    text-align: center
  }

</style>