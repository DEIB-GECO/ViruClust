<template>
  <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#FFBA08">
          <v-card-title class="justify-center">
            <h1>FREE TARGET VS BACKGROUND</h1>
          </v-card-title>
          <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs12 d-flex">
              <v-container fluid grid-list-xl style="justify-content: center; padding: 0; margin-top: 10px;">
                <v-tabs v-model="selectedTabFreeQuery"
                        background-color="#FFBA08"
                        dark
                        show-arrows
                        slider-color="orange"
                        slider-size="6"
                        height="60"
                        centered>

                  <v-tab id="tabFree1" style="border: black solid 1px; border-left: 0!important; width: 40%; background-color: #6A040F">
                     DEFINE YOUR TARGET
                  </v-tab>

                  <v-tab id="tabFree2" style="border: black solid 1px; border-left: 0!important; width: 40%; background-color: #6A040F">
                     DEFINE YOUR BACKGROUND
                  </v-tab>

                  <v-tab style="border: black solid 1px; width: 20%; background-color: #6A040F">
                     SUMMARY
                  </v-tab>

                  <v-tabs-items v-model="selectedTabFreeQuery" style="background: transparent;">

                    <v-tab-item style="background-color: #FFBA08; padding-top: 40px">
                      <FreeQuery
                        type="target">
                      </FreeQuery>
                    </v-tab-item>

                    <v-tab-item style="background-color: #FFBA08; padding-top: 40px">
                      <FreeQuery
                        type="background">
                      </FreeQuery>
                    </v-tab-item>

                    <v-tab-item style="background-color: #FFBA08; padding-top: 40px">
                    </v-tab-item>

                  </v-tabs-items>
                </v-tabs>

              </v-container>
            </v-flex>

            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <FreeQuerySummaryPanel></FreeQuerySummaryPanel>
            </v-flex>

            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
              <h2> NUM OVERLAPPING SEQUENCES </h2>
            </v-flex>
            <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center; margin-bottom: 30px">
              <v-text-field
                :value = "num_overlapping_sequences"
                solo
                readonly
                hide-details
                class = "centered-input"
              ></v-text-field>
            </v-flex>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0" v-if="num_overlapping_sequences !== 0">
              <h3> Select from where the overlapping sequences should be removed </h3>
            </v-flex>
            <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center; margin-bottom: 30px" v-if="num_overlapping_sequences !== 0">
            <v-select
                    v-model="selectRemoveOverlapping"
                    :items="possibleRemoveOverlapping"
                    label="Remove Overlapping"
                    solo
                    hide-details
                  ></v-select>
            </v-flex>

            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 20px">
               <h2>SELECT PROTEINS TO ANALYZE</h2>
             </v-flex>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
               <h4>(selecting none is equivalent to "all proteins")</h4>
             </v-flex>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
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

            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"
               v-if="errorNumSeqFreeQuery">
              <span style="text-align: center">
                 <span style="color: red"> number of sequences selected is too low (minimum 10 for both target and background)</span><br>
                 <span style="color: red"> (the number of sequences in {{selectRemoveOverlapping.toLowerCase()}} is calculated taking care of the overlapping sequences)</span>
              </span>
               </v-flex>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyFreeQueryAnalysis()"
                         color="#D00000"
                         class="white--text"
                         :disabled="errorNumSeqFreeQuery"
                  >
                      APPLY
                  </v-btn>
                </v-flex>

          </v-layout>
        </v-card>
      </v-row>

      <v-row justify="center" align="center" v-if="tableApplied">
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#FFBA08">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <h2>APPLY FILTERS FOR TABLE ANALYSIS</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>% BACKGROUND:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
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
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>NUMERATOR BACKGROUND:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
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
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>% TARGET:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
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
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>NUMERATOR TARGET:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
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
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>P-VALUE:</h5>
                      <v-dialog width="500">
                        <template v-slot:activator="{ on }">
                          <v-btn
                                v-on="on"
                                  slot="activator"
                                  class="info-button"
                                  x-small
                                  text icon color="grey"
                                  style="margin-bottom: 5px; margin-left: 20px">
                              <v-icon class="info-icon">mdi-information</v-icon>
                          </v-btn>
                        </template>
                        <v-card>
                            <v-card-title
                                    class="headline grey lighten-2"
                                    primary-title
                            >
                                P-VALUE
                            </v-card-title>
                            <v-card-text>
                             ...
                            </v-card-text>
                        </v-card>
                    </v-dialog>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
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
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>ODDS RATIO:</h5>
                      <v-dialog width="500">
                        <template v-slot:activator="{ on }">
                          <v-btn
                                v-on="on"
                                  slot="activator"
                                  class="info-button"
                                  x-small
                                  text icon color="grey"
                                  style="margin-bottom: 5px; margin-left: 20px">
                              <v-icon class="info-icon">mdi-information</v-icon>
                          </v-btn>
                        </template>
                        <v-card>
                            <v-card-title
                                    class="headline grey lighten-2"
                                    primary-title
                            >
                                ODDS RATIO
                            </v-card-title>
                            <v-card-text>
                             ...
                            </v-card-text>
                        </v-card>
                    </v-dialog>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
                        <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
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
                                            hide-details
                                            step = "0.1"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MAX</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMaxOddsRatio"
                                            solo
                                            class="centered-input"
                                            hide-details
                                            :min = "selectedMinOddsRatio"
                                            :max = "totalMaxOddsRatio"
                                            step = "0.1"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                                <span>INF</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-bottom: 0">
                                <v-checkbox v-model="isInfinite"
                                hide-details
                                input-value="true">
                                </v-checkbox>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                  </v-card>
                </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                     <v-card width="500px" color="#F0E68C">
                        <v-card-title class="justify-center">
                          <h5>FILTER PROTEIN:</h5>
                        </v-card-title>
                        <v-card-text>
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
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <v-btn
                         @click="applyFilterOnTable()"
                         color="#D00000"
                         class="white--text"
                  >
                      APPLY
                  </v-btn>
               </v-flex>
               <v-card width="1000px" color="#F0E68C" style="margin-top: 50px; padding: 10px">
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; margin-top: 12px" v-if="fixedRowsTable.length !== 0">
                     <h3>IMPORTANT CHANGES:</h3>
                   </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center" v-if="fixedRowsTable.length !== 0">
                     <v-select
                      v-model="selectedTypeImportantMutation"
                      :items="possibleTypeImportantMutation"
                      label="Type Important Change"
                      solo
                      hide-details>
                     </v-select>
                   </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; margin-top: 12px" v-if="fixedRowsTable.length !== 0">
                     <ImportantMutation
                     :importantMutationECDC="importantMutationECDC"
                     :importantMutation75Percentage="importantMutation75Percentage"
                     :rowsTable = "fixedRowsTable">
                     </ImportantMutation>
                   </v-flex>
                 </v-layout>
               </v-card>

               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 80px">
                 <h2>CHANGES IN TARGET vs BACKGROUND LOCATION</h2>
               </v-flex>
               <v-tabs v-model="selectedTabTable"
                background-color="#6A040F"
                dark
                vertical
                show-arrows
                slider-color="orange"
                slider-size="6">

                <v-tabs-items v-model="selectedTabTable" style="background: #F0E68C;">
                  <v-tab-item style="padding: 20px; background-color: #F0E68C" v-for="(rows ,index) in rowsTable" v-bind:key="index">
                    <v-layout row wrap justify-space-around style="margin-top: 10px">
                      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                         <h2>TABLE
                           <v-btn @click="downloadTable('table', rows)" x-small icon
                              style="margin-left: 20px; margin-bottom: 5px">
                                <v-icon size="23">
                                  mdi-download-circle-outline
                                </v-icon>
                            </v-btn>
                         </h2>
                       </v-flex>
                      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                          <v-data-table
                                :headers="headerTable"
                                :items="rows"
                                class="data-table table_free"
                                style="width: 98%; border: grey solid 1px"
                                multi-sort
                                :sort-by.sync="sortByTable"
                                :sort-desc.sync="sortDescTable"
                          >
                              <template v-slot:item ="{ item }">
                                <tr>
                                  <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerTable"
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
                                                      style="background-color: #FFBA08 ; color: white;"
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
                                        <span style="color: white; font-weight: 900; background-color: red; padding: 5px" v-if="header.value === 'mutation_position' && importantMutation['mutation'].includes(item['mutation'])">{{item['mutation']}}</span>
                                        <span style="color: white; font-weight: 900; background-color: orange; padding: 5px" v-else-if="header.value === 'mutation_position' && importantMutation['additional_mutation'].includes(item['mutation'])">{{item['mutation']}}</span>
                                        <span v-else-if="header.value === 'mutation_position'">{{item['mutation']}}</span>
                                        <span v-else-if="header.value === 'p_value'">{{item['p_value'].toFixed(5)}}</span>
                                        <span v-else-if="header.value === 'odd_ratio'">
                                          <span v-if="item['percentage_background'] === 0"> INF </span>
                                          <span v-else>{{item['odd_ratio'].toFixed(5)}}</span>
                                        </span>
                                        <span v-else-if="header.value === 'percentage_target'">{{item['percentage_target'].toFixed(5)}} %  <a @click="openDialogAccession('target', item)">({{item['numerator_target']}})</a>
                                        </span>
                                        <span v-else-if="header.value === 'percentage_background'">{{item['percentage_background'].toFixed(5)}} %  <a @click="openDialogAccession('background', item)">({{item['numerator_background']}})</a>
                                        </span>
                                        <span v-else>{{item[header.value]}}</span>
                                  </td>
                                </tr>
                              </template>
                          </v-data-table>
                      </v-flex>
                    </v-layout>
                  </v-tab-item>
                </v-tabs-items>
               </v-tabs>
             </v-layout>
           </v-card-text>
        </v-card>
      </v-row>
    <v-row justify="center" align="center" v-if="tableApplied">
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#FFBA08">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                <h2> TARGET SEQUENCES BAR CHART </h2>
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
                      <h5>SELECT PROTEIN (mandatory):</h5>
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
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                 <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center" style="margin: 0; padding-bottom: 0">
                        <h5>INCLUDE CHANGES:</h5>
                    </v-card-title>
                    <v-card-text style="padding-top: 0; margin-top: 0">
                      <v-layout row wrap justify-space-around style="margin-top: 0; padding: 0">
                        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin: 0">
                          <h5 style="text-align: center;">Include the changes that appear in a % of the sequences between the 2 values below</h5>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                              <span>MIN</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex-" style="justify-content: center; padding: 0">
                              <v-text-field v-model.number="selectedMinPercentageMutationPValue"
                                            solo
                                            class="centered-input"
                                            min="0"
                                            :max="selectedMaxPercentageMutationPValue"
                                            step = "1"
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
                              <v-text-field v-model.number="selectedMaxPercentageMutationPValue"
                                            solo
                                            class="centered-input"
                                            :min = "selectedMinPercentageMutationPValue"
                                            max = "100"
                                            step = "1"
                                            type="number">
                              </v-text-field>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                 </v-card>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <v-btn
                         @click="applyFilterPValueChart()"
                         color="#D00000"
                         class="white--text"
                         :disabled="selectedProteinForPValue === null"
                  >
                      APPLY
                 </v-btn>
               </v-flex>
               <div v-if="pValueBarChartApplied">
               <v-layout row wrap justify-center style="margin-top: 30px">
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                           <v-card width="400px" color="#F0E68C">
                              <v-card-title class="justify-center">
                                <h5>HIGHLIGHTS DOMAIN:</h5>
                              </v-card-title>
                              <v-card-text>
                                <v-autocomplete
                                  v-model="selectedDomainForPValue"
                                  :items="possibleDomainForPValue"
                                  label="Sites ,family and domains"
                                  solo
                                  hide-details
                                  :item-text="getFieldTextDomain"
                                  multiple
                                >
                                </v-autocomplete>
                              </v-card-text>
                           </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                           <v-card width="400px" color="#F0E68C">
                              <v-card-title class="justify-center">
                                <h5>HIGHLIGHT MUTAGENESIS SITES:</h5>
                              </v-card-title>
                              <v-card-text>
                                <v-autocomplete
                                  v-model="selectedDomainForPValueMutagenesis"
                                  :items="possibleDomainForPValueMutagenesis"
                                  label="Mutagenesis Sites"
                                  solo
                                  hide-details
                                  :item-text="getFieldTextDomain"
                                  multiple
                                >
                                </v-autocomplete>
                              </v-card-text>
                           </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                           <v-card width="400px" color="#F0E68C">
                              <v-card-title class="justify-center">
                                <h5>HIGHLIGHT GLYCOSYLATION SITES:</h5>
                              </v-card-title>
                              <v-card-text>
                                <v-autocomplete
                                  v-model="selectedDomainForPValueAaModifications"
                                  :items="possibleDomainForPValueAaModifications"
                                  label="Glycosylation Sites"
                                  solo
                                  hide-details
                                  :item-text="getFieldTextDomain"
                                  multiple
                                >
                                </v-autocomplete>
                              </v-card-text>
                           </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                 </v-layout>
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; padding-bottom: 5px!important;" v-for="(domain, idx) in selectedDomainForPValue" v-bind:key="idx">
                            <v-card style="width: 400px;" color="white" v-if="selectedDomainForPValue.length > 0">
                              <v-card :color="color_1[idx%color_1.length] + 80" height="100%">
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}} ({{begin_value_domain[idx]}} , {{end_value_domain[idx]}}) </h5>
                              </v-card>
                            </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; padding-bottom: 5px!important;" v-for="(domain, idx) in selectedDomainForPValueMutagenesis" v-bind:key="idx">
                            <v-card style="width: 400px;" color="white" v-if="selectedDomainForPValueMutagenesis.length > 0">
                              <v-card :color="color_2[idx%color_2.length] + 80" height="100%">
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}} ({{begin_value_domain_mutagenesis[idx]}} , {{end_value_domain_mutagenesis[idx]}}) </h5>
                              </v-card>
                            </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; padding-bottom: 5px!important;" v-for="(domain, idx) in selectedDomainForPValueAaModifications" v-bind:key="idx">
                            <v-card style="width: 400px;" color="white" v-if="selectedDomainForPValueAaModifications.length > 0">
                              <v-card :color="color_3[idx%color_3.length] + 80" height="100%">
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}} ({{begin_value_domain_aa_modifications[idx]}} , {{end_value_domain_aa_modifications[idx]}}) </h5>
                              </v-card>
                            </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                 </v-layout>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-for="(rows ,index) in rowsTable" v-bind:key="'pValue' + index">
                <v-layout row wrap justify-space-around style="margin: 10px; padding: 10px">
                   <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-space-around style="margin: 10px; padding-top: 10px">
                      <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center">
                         <v-card width="500px" color="#F0E68C" style="height: 250px">
                            <v-card-text style="text-align: center; padding-top: 30%">
                              <span>
                                <b> TARGET: </b>
                                <br>
                              </span>
                              <span> NUM SEQ:
                                <span>{{fixedRowsTable[index][0]['denominator_target']}}</span>
                                <br>
                              </span>
                              <br>
                              <span>
                                <b> BACKGROUND: </b>
                                <br>
                              </span>
                              <span> NUM SEQ:
                                <span>{{fixedRowsTable[index][0]['denominator_background']}}</span>
                                <br>
                              </span>
                            </v-card-text>
                         </v-card>
                       </v-flex>
                      <v-flex class="no-horizontal-padding xs8 d-flex" style="justify-content: center;">
                         <PValueBarChart
                             :namePValue="pValueName[index]"
                             :pValueContent="pValueContent[index]"
                             :totalMaxOddsRatio="totalMaxOddsRatio"
                             :startStopProtein="startStopProtein"
                             :selectedDomainForPValue="selectedDomainForPValue"
                             :possibleDomainForPValue="possibleDomainForPValue"
                             :selectedDomainForPValueMutagenesis="selectedDomainForPValueMutagenesis"
                             :possibleDomainForPValueMutagenesis="possibleDomainForPValueMutagenesis"
                             :selectedDomainForPValueAaModifications="selectedDomainForPValueAaModifications"
                             :possibleDomainForPValueAaModifications="possibleDomainForPValueAaModifications"
                             type="free">
                         </PValueBarChart>
                       </v-flex>
                    </v-layout>
                   </v-flex>
                </v-layout>
               </v-flex>
               </div>
             </v-layout>
           </v-card-text>
        </v-card>
      </v-row>

    <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

    <v-dialog
        persistent
        scrollable
      v-model="dialogAccessionIds"
      width="700"
    >
      <v-card>
        <v-card-title class="headline" style="background-color: #FFBA08 ; color: white">
          Accession IDs
          <v-spacer></v-spacer>
          <v-btn
            color="rgb(122, 139, 157)"
            style="color:white;"
            text
            @click="downloadAccessionIds()"
          >
            DOWNLOAD
          </v-btn>
          <v-btn
            color="rgb(122, 139, 157)"
            style="color:white;"
            text
            @click="dialogAccessionIds = !dialogAccessionIds"
          >
            CLOSE
          </v-btn>
        </v-card-title>
        <v-card-text style="padding: 50px">
          <span v-for="acc_id in listAccessionIds" v-bind:key="acc_id">
            <span> - {{acc_id}}</span><br>
          </span>
        </v-card-text>
      </v-card>
    </v-dialog>

  </v-card>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import FreeQuery from "./FreeQuery";
import FreeQuerySummaryPanel from "./FreeQuerySummaryPanel";
import axios from "axios";
import PValueBarChart from "./PValueBarChart";
import ImportantMutation from "./ImportantMutation";

export default {
  name: "FreeTargetVsBackground",
  components: {ImportantMutation, PValueBarChart, FreeQuerySummaryPanel, FreeQuery},
  data() {
    return {
      selectedTabFreeQuery: 0,
      errorNumSeqFreeQuery: false,
      min_num_seq_target: 10,
      min_num_seq_background: 10,

      num_overlapping_sequences: 0,

      selectedProtein: [],
      possibleProtein: [],

      selectRemoveOverlapping: 'Background',
      possibleRemoveOverlapping: ['Background', 'Target', 'Both'],

      overlay: false,
      tableApplied: false,
      headerTable: [],
      rowsTable: [],
      fixedRowsTable: [],
      sortByTable: ['odd_ratio'],
      sortDescTable: [true],

      pValueName: [],
      pValueContent: [],
      pValueBarChartApplied: false,

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
      isInfinite: true,

      listAccessionIds: [],
      dialogAccessionIds: false,
      startStopProtein: {},
      selectedDomainForPValue: [],
      possibleDomainForPValue: [],
      begin_value_domain: [],
      end_value_domain: [],

      selectedDomainForPValueMutagenesis: [],
      possibleDomainForPValueMutagenesis: [],
      begin_value_domain_mutagenesis: [],
      end_value_domain_mutagenesis: [],

      selectedDomainForPValueAaModifications: [],
      possibleDomainForPValueAaModifications: [],
      begin_value_domain_aa_modifications: [],
      end_value_domain_aa_modifications: [],

      selectedHeatmapMode: '% Target',
      possibleHeatmapMode: ['% Target', '% Target - % Background', 'Odds ratio'],

      selectedMinPercentageMutationPValue: 0,
      selectedMaxPercentageMutationPValue: 80,

      selectedTabTable: 0,

      importantMutationECDC: {},
      importantMutation75Percentage: {},
      importantMutation: {},

      selectedTypeImportantMutation: 'ECDC',
      possibleTypeImportantMutation: ['ECDC', 'Present in 75% of the lineage (worldwide)'],
    }
  },
  computed: {
    ...mapState(['queryFreeTarget', 'queryFreeBackground', 'numSequencesQueryFreeTarget',
      'numSequencesQueryFreeBackground', 'all_protein', 'startDateQueryFreeTarget', "stopDateQueryFreeTarget",
      'startDateQueryFreeBackground', 'stopDateQueryFreeBackground', 'toExcludeFreeTarget', 'toExcludeFreeBackground',
      'colorPValueInfoBox', 'color_1', 'color_2', 'color_3']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryFreeTarget', 'setQueryFreeBackground']),
    getFieldTextDomain(item){
      return `${item['Description']}` //  ----- ${item['cnt']}
    },
    filter(){
      let arr_row_an_time = [];
      for(let i = 0; i < this.rowsTable.length; i = i + 1) {
        let result = JSON.parse(JSON.stringify(this.fixedRowsTable[i]));
        if (this.selectedProteinForTable !== null) {
          let that = this;
          result = result.filter(function (i) {
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
                &&
                ((odds_ratio >= that.selectedMinOddsRatio
                        && odds_ratio <= that.selectedMaxOddsRatio) ||
                    (that.isInfinite
                        && odds_ratio > that.totalMaxOddsRatio)
                )
                && product === that.selectedProteinForTable);
          })
        } else {
          var that = this;
          result = result.filter(function (i) {
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
                &&
                ((odds_ratio >= that.selectedMinOddsRatio
                        && odds_ratio <= that.selectedMaxOddsRatio) ||
                    (that.isInfinite
                        && odds_ratio > that.totalMaxOddsRatio)
                ));
          })
        }
        arr_row_an_time[i] = result;
      }
      this.rowsTable = arr_row_an_time;
    },
    boldTabs(){
      let i = 0;
      while(i < 3){
        let id = 'tab' + i;
        if (i === this.selectedTabAnalyze){
          let elem = document.getElementById(id);
          elem.style['font-weight'] = 'bold';

        }
        else{
          let elem = document.getElementById(id);
          elem.style['font-weight'] = 'normal';
        }
        i = i + 1;
      }
    },
    downloadTable(table, rows){
      let text = "";
      let result_sorted = this.sortResults(table, rows);
      if(table === 'table'){
        text = this.json2csv(result_sorted, this.headerTable);
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
    sortResults(table, rows){
      let len;
      let sortBy;
      let sortDesc;
      let results;
      if(table === 'table'){
        len = this.sortByTable.length;
        sortBy = this.sortByTable;
        sortDesc = this.sortDescTable;
        results = JSON.parse(JSON.stringify(rows));
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
    applyFilterOnTable(){
      this.filter();

      // let copy = JSON.parse(JSON.stringify(this.rowsTable));
      // this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];
    },
    applyFreeQueryAnalysis(){
      let url = `/analyze/analyzeMutationTargetBackgroundFree`;
      this.overlay = true;

      this.importantMutation = {};
      this.importantMutationECDC = {};
      let queryFree = JSON.parse(JSON.stringify(this.queryFreeTarget));
      let url_important_mutation = `/analyze/getImportantMutation`;
      let lineage_to_send = null;
      if(queryFree['lineage']){
        lineage_to_send = queryFree['lineage'];
      }
      let to_send_important_mutation = {'lineage': lineage_to_send}

      axios.post(url_important_mutation, to_send_important_mutation)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          this.importantMutationECDC = res;
          if(this.selectedTypeImportantMutation === 'ECDC'){
            this.importantMutation = res;
          }
        })


      let array_protein2 = [];
      if(this.selectedProtein.length === 0){
        array_protein2 = this.possibleProtein;
      }
      else{
        array_protein2 = this.selectedProtein;
      }

      let to_send_all_important_mutation_per_lineage= {'lineage': lineage_to_send, 'proteins': array_protein2};
      let url_all_important_mutation_per_lineage = `/analyze/getAllImportantMutationPerLineage`;
      axios.post(url_all_important_mutation_per_lineage, to_send_all_important_mutation_per_lineage)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let json = {};
          json['mutation'] = res;
          json['additional_mutation'] = [];
          this.importantMutation75Percentage = json;
          if(this.selectedTypeImportantMutation === 'Present in 75% of the lineage (worldwide)'){
            this.importantMutation = json;
          }
        })

      let array_protein = [];
      this.possibleProteinForPValue = [];
      this.headerTable = [];
      this.rowsTable = [];
      this.fixedRowsTable = [];
      if(this.selectedProtein === null){
        array_protein = [];
      }
      else{
        array_protein = this.selectedProtein;
      }
      let query_target = JSON.parse(JSON.stringify(this.queryFreeTarget));
      let query_background = JSON.parse(JSON.stringify(this.queryFreeBackground));

      if(this.startDateQueryFreeTarget !== null){
        query_target['minDate'] = this.startDateQueryFreeTarget;
      }
      if(this.stopDateQueryFreeTarget !== null){
        query_target['maxDate'] = this.stopDateQueryFreeTarget;
      }
      if(this.startDateQueryFreeBackground !== null){
        query_background['minDate'] = this.startDateQueryFreeBackground;
      }
      if(this.stopDateQueryFreeBackground !== null){
        query_background['maxDate'] = this.stopDateQueryFreeBackground;
      }

      query_background['toExclude'] = this.toExcludeFreeBackground;
      query_target['toExclude'] = this.toExcludeFreeTarget;

      let to_send = {'query_target': query_target,
                     'query_background': query_background,
                     'protein': array_protein,
                     'removeOverlapping': this.selectRemoveOverlapping};
      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let headers = [
              {'text': 'mutation', 'value': 'mutation_position', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'odds_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
          ];
          this.headerTable = headers;
          this.rowsTable[0] = res;
          this.fixedRowsTable[0] = res;

          let copy = JSON.parse(JSON.stringify(this.rowsTable[0]));
          this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];
          this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];

          let rowTable = JSON.parse(JSON.stringify(this.rowsTable[0]));
          let totalMaxTarget = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_target']; }))
          if (totalMaxTarget < 0){
            this.totalMaxTargetNumerator = 0;
            this.selectedMaxTargetNumerator = 0;
          }
          else{
            this.totalMaxTargetNumerator = totalMaxTarget;
            this.selectedMaxTargetNumerator = totalMaxTarget;
          }

          let totalMaxBackground = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_background']; }))
          if (totalMaxBackground < 0){
            this.totalMaxBackgroundNumerator = 0;
            this.selectedMaxBackgroundNumerator = 0;
          }
          else{
            this.totalMaxBackgroundNumerator = totalMaxBackground;
            this.selectedMaxBackgroundNumerator = totalMaxBackground;
          }

          let rowTable2 = JSON.parse(JSON.stringify(this.rowsTable[0]));
          rowTable2 = rowTable2.filter(function (i){
              let perc = i['percentage_background'];
              return perc !== 0;
            }
          );
          let totalMaxOdds = Math.ceil(Math.max.apply(Math, rowTable2.map(function (o) {
            return o['odd_ratio'];
          })));
          if (totalMaxOdds > this.totalMaxOddsRatio) {
            this.totalMaxOddsRatio = totalMaxOdds;
            this.selectedMaxOddsRatio = totalMaxOdds;
          }

          this.tableApplied = true;
          this.overlay = false;
        });
    },
    applyFilterPValueChart(){
      this.selectedDomainForPValue = [];
      this.pValueContent = [];
      this.pValueName = [];

      for(let i = 0; i < this.rowsTable.length; i = i + 1) {
        let result = JSON.parse(JSON.stringify(this.fixedRowsTable[i]));
        var that = this;
        result = result.filter(function (i) {
          let p_value = JSON.parse(JSON.stringify(i['p_value']));
          let product = JSON.parse(JSON.stringify(i['product']));
          let percentage = JSON.parse(JSON.stringify(i['percentage_target']));
          return (p_value >= that.selectedMinPValueBarChart
              && p_value <= that.selectedMaxPValueBarChart
              && percentage <= that.selectedMaxPercentageMutationPValue
              && percentage >= that.selectedMinPercentageMutationPValue
              && that.selectedProteinForPValue === product);
        })

        let arrayToBarChart = [];

        result.forEach(elem => {
          let mutation = elem['mutation'];
          let mutation_position = elem['mutation_position'];
          let idx = arrayToBarChart.findIndex(item => item['name'] === mutation);
          if (idx === -1) {
            let single_element = {
              'name': mutation, 'value': elem['numerator_target'], 'position': mutation_position
              , 'p_value': elem['p_value'], 'odds_ratio': elem['odd_ratio']
            };
            arrayToBarChart.push(single_element);
          } else {
            arrayToBarChart[idx]['value'] = arrayToBarChart[idx]['value'] + elem['numerator_target'];
          }
        })

        arrayToBarChart = arrayToBarChart.sort(function (a, b) {
          let mutation_position1 = a['position'];
          let mutation_position2 = b['position'];
          return mutation_position1 > mutation_position2 ? 1 : -1;
        });

        this.pValueContent[i] = arrayToBarChart;
        this.pValueName[i] = 'p_value_free' + i;
      }

      let url = `/analyze/getProteinPosition`;

      let to_send = {'protein': this.selectedProteinForPValue};

      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
            this.startStopProtein = res;
            let url2 = `/analyze/getDomains`;

            let to_send2 = {'protein': this.selectedProteinForPValue};

            axios.post(url2, to_send2)
              .then((res) => {
                return res.data;
              })
              .then((res) => {
                 this.possibleDomainForPValue = res['sites_and_domains'].sort(function(a, b){
                    let value_a = a['Description'].toLowerCase();
                    let value_b = b['Description'].toLowerCase();
                    return value_a > value_b ? 1 : -1;
                  });
                 this.possibleDomainForPValueMutagenesis = res['mutagenesis'].sort(function(a, b){
                    let value_a = a['Description'].toLowerCase();
                    let value_b = b['Description'].toLowerCase();
                    return value_a > value_b ? 1 : -1;
                  });
                  this.possibleDomainForPValueAaModifications = res['aa_modifications'].sort(function(a, b){
                    let value_a = a['Description'].toLowerCase();
                    let value_b = b['Description'].toLowerCase();
                    return value_a > value_b ? 1 : -1;
                  })

                  this.overlay = false;
                  this.pValueBarChartApplied = true;
              });
        });
    },
    openDialogAccession(type, item){
      let url = `/analyze/getAccessionIds`;
      this.overlay = true;
      this.listAccessionIds = [];

      let query ;
      if(type === 'target') {
        query = JSON.parse(JSON.stringify(this.queryFreeTarget));
      }
      else if(type === 'background') {
        query = JSON.parse(JSON.stringify(this.queryFreeBackground));
      }

      let query_false = '';
      let query_target = 'empty';
      if(type === 'target'){
        query['lineage'] = item['lineage'][0];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        query['minDateBackground'] = this.startDateQueryFreeTarget;
        query['maxDateBackground'] = this.stopDateQueryFreeTarget;
        query['product'] = item['product'];
      }
      else if(type === 'background'){
        query['lineage'] = item['lineage'][0];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        query['minDateBackground'] = this.startDateQueryFreeBackground;
        query['maxDateBackground'] = this.stopDateQueryFreeBackground;
        query['product'] = item['product'];

        query_target = JSON.parse(JSON.stringify(this.queryFreeTarget));
      }

      if(type === 'target') {
        query['toExclude'] = this.toExcludeFreeTarget;
      }
      else if(type === 'background') {
        query['toExclude'] = this.toExcludeFreeBackground;
      }

      let to_send = {'query': query, 'query_false': query_false, 'query_target': query_target};

      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          this.listAccessionIds = res[0]['acc_ids'];
          this.overlay = false;
          if(this.listAccessionIds !== null && this.listAccessionIds.length > 0) {
            this.dialogAccessionIds = true;
          }
        })
    },
    downloadAccessionIds(){
      let text = "";
      for (let i=0; i<this.listAccessionIds.length; i=i+1){
        text = text + this.listAccessionIds[i] + ';  ';
      }
      let filename = 'accession_ids.txt';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    resetApplied(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProteinForTable = null;
      this.tableApplied = false;
    },
    countOverlappingSequenceTargetBackground(){
      let url = `/analyze/countOverlappingSequenceTargetBackground`;
      this.overlay = true;

      let query_target =  JSON.parse(JSON.stringify(this.queryFreeTarget));
      let query_background = JSON.parse(JSON.stringify(this.queryFreeBackground));

      if (this.startDateQueryFreeTarget !== null) {
        query_target['minDate'] = this.startDateQueryFreeTarget;
      }
      if (this.stopDateQueryFreeTarget !== null) {
        query_target['maxDate'] = this.stopDateQueryFreeTarget;
      }
      if (this.startDateQueryFreeBackground !== null) {
        query_background['minDate'] = this.startDateQueryFreeBackground;
      }
      if (this.stopDateQueryFreeBackground !== null) {
        query_background['maxDate'] = this.stopDateQueryFreeBackground;
      }

      query_background['toExclude'] = this.toExcludeFreeBackground;
      query_target['toExclude'] = this.toExcludeFreeTarget;

      let to_send = {
        'query_target': query_target,
        'query_background': query_background
      };

      this.num_overlapping_sequences = 0;

      if(Object.keys(query_target).length > 0 && Object.keys(query_background).length > 0) {

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.num_overlapping_sequences = res[0]['count'];
              this.overlay = false;
              // if(this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < 10){
              //   this.errorNumSeqFreeQuery = true;
              // }
            });
      }
      else {
        this.overlay = false;
      }
    }
  },
  watch:{
    selectedTypeImportantMutation(){
      if(this.selectedTypeImportantMutation === 'ECDC'){
        this.importantMutation = this.importantMutationECDC;
      }
      else if(this.selectedTypeImportantMutation === 'Present in 75% of the lineage (worldwide)'){
        this.importantMutation = this.importantMutation75Percentage;
      }
    },
    selectedDomainForPValue(){
      this.begin_value_domain = [];
      this.end_value_domain = [];

      for(let i = 0; i < this.selectedDomainForPValue.length; i = i + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValue.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValue[i];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValue[index]['Begin'];
            max = this.possibleDomainForPValue[index]['End'];
          }
          this.begin_value_domain.push(min);
          this.end_value_domain.push(max);
      }
    },
    selectedDomainForPValueMutagenesis(){
      this.begin_value_domain_mutagenesis = [];
      this.end_value_domain_mutagenesis = [];

      for(let i = 0; i < this.selectedDomainForPValueMutagenesis.length; i = i + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValueMutagenesis.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValueMutagenesis[i];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValueMutagenesis[index]['Begin'];
            max = this.possibleDomainForPValueMutagenesis[index]['End'];
          }
          this.begin_value_domain_mutagenesis.push(min);
          this.end_value_domain_mutagenesis.push(max);
      }
    },
    selectedDomainForPValueAaModifications(){
      this.begin_value_domain_aa_modifications = [];
      this.end_value_domain_aa_modifications = [];

      for(let i = 0; i < this.selectedDomainForPValueAaModifications.length; i = i + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValueAaModifications.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValueAaModifications[i];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValueAaModifications[index]['Begin'];
            max = this.possibleDomainForPValueAaModifications[index]['End'];
          }
          this.begin_value_domain_aa_modifications.push(min);
          this.end_value_domain_aa_modifications.push(max);
      }
    },
    selectedMinPercentageMutationPValue(){
      this.pValueBarChartApplied = false;
    },
    selectedMaxPercentageMutationPValue(){
      this.pValueBarChartApplied = false;
    },
    selectRemoveOverlapping(){
      this.resetApplied();
      this.errorNumSeqFreeQuery = (this.numSequencesQueryFreeTarget < this.min_num_seq_target
          || this.numSequencesQueryFreeBackground < this.min_num_seq_background
          || (this.selectRemoveOverlapping === 'Target'
              && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
          || (this.selectRemoveOverlapping === 'Background'
              && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          || (this.selectRemoveOverlapping === 'Both' &&
              (this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
              || (this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          )
      );
    },
    selectedTabFreeQuery(){
      this.boldTabs();
    },
    'queryFreeTarget.geo_group': function (){
        this.setQueryFreeTarget({field: 'country', list: null});
        this.setQueryFreeTarget({field: 'region', list: null});
        this.setQueryFreeTarget({field: 'province', list: null});
    },
    'queryFreeTarget.country': function (){
        this.setQueryFreeTarget({field: 'region', list: null});
        this.setQueryFreeTarget({field: 'province', list: null});
    },
    'queryFreeTarget.region': function (){
        this.setQueryFreeTarget({field: 'province', list: null});
    },
    'queryFreeBackground.geo_group': function (){
        this.setQueryFreeBackground({field: 'country', list: null});
        this.setQueryFreeBackground({field: 'region', list: null});
        this.setQueryFreeBackground({field: 'province', list: null});
    },
    'queryFreeBackground.country': function (){
        this.setQueryFreeBackground({field: 'region', list: null});
        this.setQueryFreeBackground({field: 'province', list: null});
    },
    'queryFreeBackground.region': function (){
        this.setQueryFreeBackground({field: 'province', list: null});
    },
    numSequencesQueryFreeTarget(){
      this.errorNumSeqFreeQuery = (this.numSequencesQueryFreeTarget < this.min_num_seq_target
          || this.numSequencesQueryFreeBackground < this.min_num_seq_background
          || (this.selectRemoveOverlapping === 'Target'
              && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
          || (this.selectRemoveOverlapping === 'Background'
              && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          || (this.selectRemoveOverlapping === 'Both' &&
              (this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
              || (this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          )
      );
    },
    numSequencesQueryFreeBackground(){
      this.errorNumSeqFreeQuery = (this.numSequencesQueryFreeTarget < this.min_num_seq_target
          || this.numSequencesQueryFreeBackground < this.min_num_seq_background
          || (this.selectRemoveOverlapping === 'Target'
              && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
          || (this.selectRemoveOverlapping === 'Background'
              && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          || (this.selectRemoveOverlapping === 'Both' &&
              (this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
              || (this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          )
      );
    },
    num_overlapping_sequences(){
      this.errorNumSeqFreeQuery = (this.numSequencesQueryFreeTarget < this.min_num_seq_target
          || this.numSequencesQueryFreeBackground < this.min_num_seq_background
          || (this.selectRemoveOverlapping === 'Target'
              && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
          || (this.selectRemoveOverlapping === 'Background'
              && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          || (this.selectRemoveOverlapping === 'Both' &&
              (this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
              || (this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
          )
      );
    },
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    startDateQueryFreeTarget(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    stopDateQueryFreeTarget(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    startDateQueryFreeBackground(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    stopDateQueryFreeBackground(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    queryFreeTarget(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    queryFreeBackground(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    toExcludeFreeTarget(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    toExcludeFreeBackground(){
      this.resetApplied();
      this.countOverlappingSequenceTargetBackground();
    },
    selectedProtein(){
      this.selectedProteinForTable = null;
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
      if(this.selectedMaxOddsRatio !== '-Infinity') {
        if (this.selectedMaxOddsRatio < this.selectedMinOddsRatio) {
          this.selectedMaxOddsRatio = this.selectedMinOddsRatio;
        } else if (this.selectedMaxOddsRatio > this.totalMaxOddsRatio) {
          this.selectedMaxOddsRatio = this.totalMaxOddsRatio;
        }
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
    // selectedProteinForTable(){
    //   this.filter();
    // }

  },
  mounted() {
    this.possibleProtein = this.all_protein;
    this.boldTabs();
    this.errorNumSeqFreeQuery = (this.numSequencesQueryFreeTarget < this.min_num_seq_target
          || this.numSequencesQueryFreeBackground < this.min_num_seq_background);
  }
}
</script>

<style scoped>

  .table_free table > tbody > tr > td:nth-child(1),
  .table_free table > tbody > tr > td:nth-child(3),
  .table_free table > tbody > tr > td:nth-child(4){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

  .centered-input >>> input {
    text-align: center
  }


</style>