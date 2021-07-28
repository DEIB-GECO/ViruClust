<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#A8DADC">
          <v-card-title class="justify-center">
            <h1>COUNTRY (TARGET) vs LINEAGE (BACKGROUND)</h1>
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                 <h2>SELECT LINEAGE (BACKGROUND) AND MIN % TO FILTER THE COUNTRIES (TARGET) OF INTEREST</h2>
               </v-flex>
                <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                  <v-autocomplete
                    v-model="selectedLineage"
                    :items="possibleLineage"
                    label="Lineage"
                    solo
                    hide-details
                    :item-text="getFieldText"
                  >
                    <template slot="item" slot-scope="data">
                        <span class="item-value-span">{{getFieldText(data.item)}}</span>
                        <span class="item-count-span">{{data.item.count}}</span>
                    </template>
                  </v-autocomplete>
                </v-flex>
                <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                  <v-text-field v-model.number="selectedMinNumCase" min="0" max="100" solo type="number" hide-details></v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyLoadCountry()"
                         color="#E63946"
                         class="white--text"
                         :disabled="selectedLineage === null"
                  >
                      APPLY
                  </v-btn>
                </v-flex>
             </v-layout>

             <v-layout row wrap justify-center v-if="countryReceived">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h2>SELECT COUNTRY (TARGET) OF INTEREST</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-bottom: 0"
               v-if="possibleCountry.length === 0">
                 <h3 style="color: white; background-color: red">NO COUNTRY TO ANALYZE PLEASE CHANGE LINEAGE OR %</h3>
               </v-flex>
                <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                  <v-autocomplete
                    v-model="selectedCountry"
                    :items="possibleCountry"
                    label="Country"
                    solo
                    hide-details
                    multiple
                  >
                  </v-autocomplete>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 30px">
                 <h2>SELECT PROTEINS TO ANALYZE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h4>(no selection means "all protein")</h4>
               </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                   <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                      <v-autocomplete
                        v-model="selectedProtein"
                        :items="possibleProtein"
                        label="Protein"
                        solo
                        hide-details
                        multiple
                      >
                      </v-autocomplete>
                    </v-flex>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                        :disabled="possibleCountry.length === 0"
                         @click="applySingleLineageAnalysis()"
                         color="#E63946"
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
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#A8DADC">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <h2>APPLY FILTERS TO TABLE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F1FAEE">
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
                  <v-card width="500px" color="#F1FAEE">
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
                  <v-card width="500px" color="#F1FAEE">
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
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>NUMERATOR BACKGROUND:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinBackgroundNumerator"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxBackgroundNumerator"
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
                              <v-text-field v-model.number="selectedMaxBackgroundNumerator"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinBackgroundNumerator"
                                            :max = "totalMaxBackgroundNumerator"
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
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>NUMERATOR TARGET:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinTargetNumerator"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxTargetNumerator"
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
                              <v-text-field v-model.number="selectedMaxTargetNumerator"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinTargetNumerator"
                                            :max = "totalMaxTargetNumerator"
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
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>ODDS RATIO:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinOddsRatio"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxOddsRatio"
                                            step = "0.1"
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
                              <v-text-field v-model.number="selectedMaxOddsRatio"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinOddsRatio"
                                            :max = "totalMaxOddsRatio"
                                            step = "0.1"
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
                         color="#E63946"
                         class="white--text"
                  >
                      APPLY FILTERS
                  </v-btn>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 80px">
                 <h2>TABLE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center" v-if="rowsAnalyzeMutation.length !== 0">
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-card width="500px" color="#F1FAEE">
                        <v-card-title class="justify-center">
                          <h5>INFO:</h5>
                        </v-card-title>
                        <v-card-text>
                          <span>
                            <b> - TARGET: </b>
                            <span>{{rowsAnalyzeMutation[0]['background']}} in {{rowsAnalyzeMutation[0]['target']}}</span>
                            <br>
                          </span>
                          <span>
                            <b> - TOT NUM SEQ IN TARGET: </b>
                            <span>{{rowsAnalyzeMutation[0]['denominator_target']}}</span>
                            <br>
                          </span>
                          <br>
                          <span>
                            <b> - BACKGROUND: </b>
                            <span>{{rowsAnalyzeMutation[0]['background']}}</span>
                            <br>
                          </span>
                          <span>
                            <b> - TOT NUM SEQ IN BACKGROUND: </b>
                            <span>{{rowsAnalyzeMutation[0]['denominator_background']}}</span>
                            <br>
                          </span>
                        </v-card-text>
                     </v-card>
                   </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-card width="500px" color="#F1FAEE">
                        <v-card-title class="justify-center">
                          <h5>FILTER PROTEIN:</h5>
                        </v-card-title>
                        <v-card-text style="margin-top: 30px">
                          <v-autocomplete
                            v-model="selectedProteinForTable"
                            :items="possibleProteinForTable"
                            label="Protein"
                            solo
                            clearable
                            hide-details
                          >
                          </v-autocomplete>
                        </v-card-text>
                     </v-card>
                   </v-flex>
                 </v-layout>
               </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-data-table
                        :headers="headerAnalyzeMutation"
                        :items="rowsAnalyzeMutation"
                        class="data-table table_analyze_mutation"
                        style="width: 90%; border: grey solid 1px"
                        multi-sort
                        :sort-by.sync="sortByAnalyzeMutation"
                        :sort-desc.sync="sortDescAnalyzeMutation"
                  >
                      <template v-slot:item ="{ item }">
                        <tr>
                          <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerAnalyzeMutation"
                              :key="header.value" v-show="header.show">
                                <span v-if="header.value === 'mutation_position'"> {{item['mutation']}}</span>
                                <span v-else-if="header.value === 'p_value'">{{item['p_value'].toFixed(5)}}</span>
                                <span v-else-if="header.value === 'odd_ratio'">
                                  <span v-if="item['percentage_background'] === 0"> INF </span>
                                  <span v-else>{{item['odd_ratio'].toFixed(5)}}</span>
                                </span>
                                <span v-else-if="header.value === 'percentage_target'">{{item['percentage_target'].toFixed(5)}} % ({{item['numerator_target']}})</span>
                                <span v-else-if="header.value === 'percentage_background'">{{item['percentage_background'].toFixed(5)}} % ({{item['numerator_background']}})</span>
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
                 <v-card width="500px" color="#F1FAEE">
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
                 <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>FILTER PROTEIN:</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-autocomplete
                        v-model="selectedProteinForPValue"
                        :items="possibleProteinForPValue"
                        label="Protein"
                        solo
                        hide-details
                      >
                      </v-autocomplete>
                    </v-card-text>
                 </v-card>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <v-btn
                         @click="applyFilterPValueChart()"
                         color="#E63946"
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
      sortByAnalyzeMutation: ['odd_ratio'],
      sortDescAnalyzeMutation: [true],
      maxNumeratorTarget: 100,
      maxDenominatorTarget: 100,
      tableApplied: false,
      pValueName: 'p_value_country_lineage',
      pValueContent: [],
      pValueBarChartApplied: false,
      selectedProtein: [],
      possibleProtein: [],

      selectedProteinForPValue: null,
      possibleProteinForPValue: [],

      selectedProteinForTable: null,
      possibleProteinForTable: [],

      selectedMinBackgroundFrequency: 0,
      selectedMaxBackgroundFrequency: 100,
      selectedMinTargetFrequency: 0,
      selectedMaxTargetFrequency: 100,
      selectedMinPValue: 0,
      selectedMaxPValue: 1,
      selectedMinBackgroundNumerator: 0,
      selectedMaxBackgroundNumerator: 100,
      selectedMinTargetNumerator: 0,
      selectedMaxTargetNumerator: 100,
      selectedMinOddsRatio: 0,
      selectedMaxOddsRatio: 100,
      selectedMinPValueBarChart: 0,
      selectedMaxPValueBarChart: 1,

      totalMaxTargetNumerator: 0,
      totalMaxBackgroundNumerator: 0,
      totalMaxOddsRatio: 0,
    }
  },
  computed: {
    ...mapState(['all_protein', 'all_lineages']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
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
      let name = '';
      name = item['value'];
      return name;
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
        if(res[0] === "\n"){
          this.possibleCountry = [];
        }
        else {
          this.possibleCountry = res;
        }
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
              //{'text': 'target', 'value': 'target', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'background', 'value': 'background', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'odds_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'numerator_background', 'value': 'numerator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'denominator_background', 'value': 'denominator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'numerator_target', 'value': 'numerator_target', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'denominator_target', 'value': 'denominator_target', 'show': true, 'align': 'center', 'width': '23vh'},
          ];
          this.headerAnalyzeMutation = headers;
          this.rowsAnalyzeMutation = res;
          this.fixedRowAnalyzeMutation = res;

          let copy = JSON.parse(JSON.stringify(this.rowsAnalyzeMutation));
          this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];
          this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];

          let rowTable = JSON.parse(JSON.stringify(this.rowsAnalyzeMutation));
          this.totalMaxTargetNumerator = Math.max.apply(Math, rowTable.map(function(o) { return o['numerator_target']; }))
          this.selectedMaxTargetNumerator = this.totalMaxTargetNumerator;
          this.totalMaxBackgroundNumerator = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_target']; }))
          this.selectedMaxBackgroundNumerator = this.totalMaxBackgroundNumerator;
          this.totalMaxOddsRatio = Math.ceil(Math.max.apply(Math, rowTable.map(function(o) { return o['odd_ratio']; })));
          this.selectedMaxOddsRatio = Math.ceil(this.totalMaxOddsRatio);

          this.tableApplied = true;
          this.overlay = false;
        });
    },
    applyFilterOnTable(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeMutation));
      var that = this;
      result = result.filter(function (i){
          let background_frequency = JSON.parse(JSON.stringify(i['percentage_background']));
          let target_frequency = JSON.parse(JSON.stringify(i['percentage_target']));
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          let background_numerator = JSON.parse(JSON.stringify(i['numerator_background']));
          let target_numerator = JSON.parse(JSON.stringify(i['numerator_target']));
          let odds_ratio = JSON.parse(JSON.stringify(i['odd_ratio']));
          return (background_frequency >= that.selectedMinBackgroundFrequency
              && background_frequency <= that.selectedMaxBackgroundFrequency
              && target_frequency >= that.selectedMinTargetFrequency
              && target_frequency <= that.selectedMaxTargetFrequency
              && p_value >= that.selectedMinPValue
              && p_value <= that.selectedMaxPValue
              && p_value <= that.selectedMaxPValue
              && background_numerator >= that.selectedMinBackgroundNumerator
              && background_numerator <= that.selectedMaxBackgroundNumerator
              && target_numerator >= that.selectedMinTargetNumerator
              && target_numerator <= that.selectedMaxTargetNumerator
              && odds_ratio >= that.selectedMinOddsRatio
              && odds_ratio <= that.selectedMaxOddsRatio);
        })
      this.rowsAnalyzeMutation = result;

      let copy = JSON.parse(JSON.stringify(this.rowsAnalyzeMutation));
      this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];
    },
    applyFilterPValueChart(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeMutation));
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
      this.pValueName = 'p_value_country_lineage';
      this.pValueBarChartApplied = true;
    },
    createPossibleLineageObject(){
      let all_lin = this.all_lineages;
      let i = 0;
      let len = all_lin.length;
      let arr_all_lin = [];
      while(i < len){
        let elem = { 'count' : all_lin[i]['cnt'], 'value': all_lin[i]['lineage']};
        if(all_lin[i]['lineage'] !== null){
          arr_all_lin.push(elem);
        }
        i = i + 1;
      }
      this.possibleLineage = arr_all_lin;
    }
  },
  watch: {
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    all_lineages(){
      this.createPossibleLineageObject();
    },
    selectedLineage(){
       this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.tableApplied = false;
       this.countryReceived = false;
       this.selectedProteinTable = null;
    },
    selectedCountry(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.tableApplied = false;
      this.selectedProteinTable = null;
    },
    selectedProtein(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.tableApplied = false;
      this.selectedProteinTable = null;
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
    selectedMinBackgroundNumerator(){
      if (this.selectedMinBackgroundNumerator < 0 ){
        this.selectedMinBackgroundNumerator= 0;
      }
      else if (this.selectedMinBackgroundNumerator > this.selectedMaxBackgroundNumerator){
        this.selectedMinBackgroundNumerator = this.selectedMaxBackgroundNumerator;
      }
    },
    selectedMaxBackgroundNumerator(){
      if (this.selectedMaxBackgroundNumerator < this.selectedMinBackgroundNumerator ){
        this.selectedMaxBackgroundNumerator = this.selectedMinBackgroundNumerator;
      }
      else if (this.selectedMaxBackgroundNumerator > this.totalMaxBackgroundNumerator){
        this.selectedMaxBackgroundNumerator = this.totalMaxBackgroundNumerator;
      }
    },
    selectedMinTargetNumerator(){
      if (this.selectedMinTargetNumerator < 0 ){
        this.selectedMinTargetNumerator = 0;
      }
      else if (this.selectedMinTargetNumerator > this.selectedMaxTargetNumerator){
        this.selectedMinTargetNumerator = this.selectedMaxTargetNumerator;
      }
    },
    selectedMaxTargetNumerator(){
      if (this.selectedMaxTargetNumerator < this.selectedMinTargetNumerator ){
        this.selectedMaxTargetNumerator = this.selectedMinTargetNumerator;
      }
      else if (this.selectedMaxTargetNumerator > this.totalMaxTargetNumerator){
        this.selectedMaxTargetNumerator = this.totalMaxTargetNumerator;
      }
    },
    selectedMinOddsRatio(){
      if (this.selectedMinOddsRatio < 0 ){
        this.selectedMinOddsRatio = 0;
      }
      else if (this.selectedMinOddsRatio > this.selectedMaxOddsRatio){
        this.selectedMinOddsRatio = this.selectedMaxOddsRatio;
      }
    },
    selectedMaxOddsRatio(){
      if (this.selectedMaxOddsRatio < this.selectedMinOddsRatio ){
        this.selectedMaxOddsRatio = this.selectedMinOddsRatio;
      }
      else if (this.selectedMaxOddsRatio > this.totalMaxOddsRatio){
        this.selectedMaxOddsRatio = this.totalMaxOddsRatio;
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
    selectedMinNumCase(){
       this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.tableApplied = false;
       this.countryReceived = false;
      if(this.selectedMinNumCase < 0){
        this.selectedMinNumCase = 0;
      }
      else if(this.selectedMinNumCase > 100){
        this.selectedMinNumCase = 100;
      }
    },
    selectedProteinForTable(){
      let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeMutation));
      if(this.selectedProteinForTable !== null) {
        let that = this;
        result = result.filter(function (i){
            let background_frequency = JSON.parse(JSON.stringify(i['percentage_background']));
            let target_frequency = JSON.parse(JSON.stringify(i['percentage_target']));
            let p_value = JSON.parse(JSON.stringify(i['p_value']));
            let background_numerator = JSON.parse(JSON.stringify(i['numerator_background']));
            let target_numerator = JSON.parse(JSON.stringify(i['numerator_target']));
            let odds_ratio = JSON.parse(JSON.stringify(i['odd_ratio']));
            let product = JSON.parse(JSON.stringify(i['product']));
            return (background_frequency >= that.selectedMinBackgroundFrequency
                && background_frequency <= that.selectedMaxBackgroundFrequency
                && target_frequency >= that.selectedMinTargetFrequency
                && target_frequency <= that.selectedMaxTargetFrequency
                && p_value >= that.selectedMinPValue
                && p_value <= that.selectedMaxPValue
                && background_numerator >= that.selectedMinBackgroundNumerator
                && background_numerator <= that.selectedMaxBackgroundNumerator
                && target_numerator >= that.selectedMinTargetNumerator
                && target_numerator <= that.selectedMaxTargetNumerator
                && odds_ratio >= that.selectedMinOddsRatio
                && odds_ratio <= that.selectedMaxOddsRatio
                && product === that.selectedProteinForTable);
          })
      }
      else{
        var that = this;
        result = result.filter(function (i){
          let background_frequency = JSON.parse(JSON.stringify(i['percentage_background']));
          let target_frequency = JSON.parse(JSON.stringify(i['percentage_target']));
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          let background_numerator = JSON.parse(JSON.stringify(i['numerator_background']));
          let target_numerator = JSON.parse(JSON.stringify(i['numerator_target']));
          let odds_ratio = JSON.parse(JSON.stringify(i['odd_ratio']));
          return (background_frequency >= that.selectedMinBackgroundFrequency
              && background_frequency <= that.selectedMaxBackgroundFrequency
              && target_frequency >= that.selectedMinTargetFrequency
              && target_frequency <= that.selectedMaxTargetFrequency
              && p_value >= that.selectedMinPValue
              && p_value <= that.selectedMaxPValue
              && background_numerator >= that.selectedMinBackgroundNumerator
              && background_numerator <= that.selectedMaxBackgroundNumerator
              && target_numerator >= that.selectedMinTargetNumerator
              && target_numerator <= that.selectedMaxTargetNumerator
              && odds_ratio >= that.selectedMinOddsRatio
              && odds_ratio <= that.selectedMaxOddsRatio);
        })
      }
      this.rowsAnalyzeMutation = result;
    }
  },
  mounted() {
    this.createPossibleLineageObject();
    this.possibleProtein = this.all_protein;
  }
}
</script>

<style scoped>

  .table_analyze_mutation table > tbody > tr > td:nth-child(1),
  .table_analyze_mutation table > tbody > tr > td:nth-child(3),
  .table_analyze_mutation table > tbody > tr > td:nth-child(4){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

  .centered-input >>> input {
    text-align: center
  }

  .item-value-span {
      padding-right: 3.5em;
  }

  .item-count-span {
      /*float:right;*/
      position: absolute;
      right: 0.5em;
  }

</style>