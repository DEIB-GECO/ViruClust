<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#DAA520">
          <v-card-title class="justify-center">
            <h1>SPATIAL ANALYSIS</h1>
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
               <h2>SELECT LINEAGE, TIME RANGE AND LOCATION (TARGET)</h2>
              </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryGeo
                  field = 'lineage'>
                 </SelectorsQueryGeo>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryGeo
                  field = 'geo_group'>
                 </SelectorsQueryGeo>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryGeo
                  field = 'country'>
                 </SelectorsQueryGeo>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryGeo
                  field = 'region'>
                 </SelectorsQueryGeo>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryGeo
                  field = 'province'>
                 </SelectorsQueryGeo>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <h3>Select "granularity" distance between target and background</h3>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center; padding: 0">
                 <v-select
                    v-model="selectedNumLevelAboveBackground"
                    :items="possibleNumLevelAboveBackground"
                    label="Background"
                    solo
                    :item-text="getFieldText"
                    hide-details
                    :disabled="possibleNumLevelAboveBackground.length === 0">
                   <template slot="item" slot-scope="data">
                        <span class="item-value-span">{{data.item.background}}</span>
                    </template>
                 </v-select>
               </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin: 0;"
                  v-if="this.queryGeo['geo_group'] === 'Europe'">
                  <!--(this.selectedNumLevelAboveBackground === 1 && this.queryGeo['country'] && !this.queryGeo['region']
                        || this.selectedNumLevelAboveBackground === 2 && this.queryGeo['region'] && !this.queryGeo['province']
                        || this.selectedNumLevelAboveBackground === 3 && this.queryGeo['province'])-->
                    <v-checkbox
                      v-model="includeUK"
                      hide-details
                      input-value="true"
                      label="Include UK in Background"
                      style="background-color: white; border: grey solid 1px; padding: 10px">
                    </v-checkbox>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <TimeSelectorQueryGeo
                    timeName="timeDistributionGeo"
                    filterDate = "Day">
                 </TimeSelectorQueryGeo>
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
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 20px"
             v-if="errorNumSeqQueryGeo">
               <span style="color: red"> number of sequences selected is too low (minimum 10)</span>
             </v-flex>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               <v-btn
                       @click="applyTableProvReg()"
                       color="red"
                       class="white--text"
                       style="margin-top: 20px"
                       :disabled="!(queryGeo['geo_group']) || errorNumSeqQueryGeo"
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
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F0E68C">
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
                  <v-card width="500px" color="#F0E68C">
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
                  <v-card width="500px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>ODDS RATIO:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around style="margin-top: 10px">
                        <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
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
                        <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
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
                        <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                          <v-layout row wrap justify-center>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                                <span>INF</span>
                            </v-flex>
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-bottom: 50px">
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
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center" v-if="rowsTableProvReg.length !== 0">
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-card width="500px" color="#F0E68C">
                        <v-card-title class="justify-center">
                          <h5>INFO:</h5>
                        </v-card-title>
                        <v-card-text>
                          <span>
                            <b> - TARGET: </b>
                            <span>{{rowsTableProvReg[0]['target']}}</span>
                            <br>
                          </span>
                          <span>
                            <b> - TOT NUM SEQ IN TARGET: </b>
                            <span>{{rowsTableProvReg[0]['denominator_target']}}</span>
                            <br>
                          </span>
                          <br>
                          <span>
                            <b> - BACKGROUND: </b>
                            <span>{{rowsTableProvReg[0]['background']}}</span>
                            <br>
                          </span>
                          <span>
                            <b> - TOT NUM SEQ IN BACKGROUND: </b>
                            <span>{{rowsTableProvReg[0]['denominator_background']}}</span>
                            <br>
                          </span>
                        </v-card-text>
                     </v-card>
                   </v-flex>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-card width="500px" color="#F0E68C">
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
                                <span v-if="header.value === 'mutation_position'"> {{item['mutation']}}</span>
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
                         color="red"
                         class="white--text"
                         :disabled="selectedProteinForPValue === null"
                  >
                      APPLY
                 </v-btn>
               </v-flex>
               <div v-if="pValueBarChartApplied">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 20px">
                 <v-card width="400px" color="#F0E68C">
                    <v-card-title class="justify-center">
                      <h5>HIGHLIGHTS DOMAIN:</h5>
                    </v-card-title>
                    <v-card-text style="margin-top: 30px">
                      <v-autocomplete
                        v-model="selectedDomainForPValue"
                        :items="possibleDomainForPValue"
                        label="Domain"
                        solo
                        :item-text="getFieldTextDomain"
                        hide-details
                      >
                        <template slot="item" slot-scope="data">
                            <span class="item-value-span">{{getFieldTextDomain(data.item)}}</span>
                        </template>
                      </v-autocomplete>
                    </v-card-text>
                 </v-card>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                 <PValueBarChart
                     :namePValue="pValueName"
                     :pValueContent="pValueContent"
                     :totalMaxOddsRatio="totalMaxOddsRatio"
                     :startStopProtein="startStopProtein"
                     :selectedDomainForPValue="selectedDomainForPValue"
                     :possibleDomainForPValue="possibleDomainForPValue">
                 </PValueBarChart>
               </v-flex>
               </div>
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

    <v-dialog
        persistent
        scrollable
      v-model="dialogAccessionIds"
      width="700"
    >
      <v-card>
        <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
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

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import PValueBarChart from "./PValueBarChart";
import SelectorsQueryGeo from "./SelectorsQueryGeo";
import TimeSelectorQueryGeo from "./TimeSelectorQueryGeo";

export default {
  name: "AnalyzeProvinceRegion",
  components: {TimeSelectorQueryGeo, SelectorsQueryGeo, PValueBarChart},
  data() {
    return {
      overlay: false,
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
      sortByTableProvReg: ['odd_ratio'],
      sortDescTableProvReg: [true],
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

      possibleNumLevelAboveBackground: [],
      includeUK: true,
      startStopProtein: {},
      selectedDomainForPValue: null,
      possibleDomainForPValue: [],
    }
  },
  computed: {
    ...mapState(['all_geo', 'all_protein', 'queryGeo', 'startDateQueryGeo', 'stopDateQueryGeo', 'errorNumSeqQueryGeo',
      'numLevelAboveBackground', 'includeUKGeo']),
    ...mapGetters({}),
    selectedCountryToLower(){
      if(this.selectedCountry_forProvReg !== null){
        return this.selectedCountry_forProvReg.toLowerCase();
      }
      else{
        return this.selectedCountry_forProvReg;
      }
    },
    selectedNumLevelAboveBackground: {
      get() {
        return this.numLevelAboveBackground;
      },
      set(value){
        this.setNumLevelAboveBackground(value);
      }
    }
  },
  methods: {
    ...mapMutations(['setNumLevelAboveBackground', 'setIncludeUKGeo']),
    ...mapActions(['setQueryGeo']),
    filter(){
      let result = JSON.parse(JSON.stringify(this.fixedRowsTableProvReg));
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
                &&
                ((odds_ratio >= that.selectedMinOddsRatio
                  && odds_ratio <= that.selectedMaxOddsRatio) ||
                     (that.isInfinite
                  && odds_ratio > that.totalMaxOddsRatio)
                )
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
              &&
                 ((odds_ratio >= that.selectedMinOddsRatio
              && odds_ratio <= that.selectedMaxOddsRatio) ||
                 (that.isInfinite
              && odds_ratio > that.totalMaxOddsRatio)
              ));
        })
      }
      this.rowsTableProvReg = result;
    },
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
      this.filter();

      let copy = JSON.parse(JSON.stringify(this.rowsTableProvReg));
      this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];
    },
    applyTableProvReg(){
      let url = `/analyze/analyzeMutationProvinceRegion`;
      this.overlay = true;
      // let type_geo1;
      // let type_geo2;
      // let geo1;
      // let geo2;
      // this.overlay = true;
      // if(this.selectedProvince_forProvReg !== null){
      //   type_geo1 = 'region';
      //   type_geo2 = 'province';
      //   geo1 = this.selectedRegion_forProvReg;
      //   geo2 = this.selectedProvince_forProvReg;
      // }
      // else{
      //   type_geo1 = 'country';
      //   type_geo2 = 'region';
      //   geo1 = this.selectedCountry_forProvReg;
      //   geo2 = this.selectedRegion_forProvReg;
      // }
      let array_protein = [];
      if(this.selectedProtein === null){
        array_protein = [];
      }
      else{
        array_protein = this.selectedProtein;
      }

      let query = JSON.parse(JSON.stringify(this.queryGeo));
      if(this.startDateQueryGeo !== null){
        query['minDate'] = this.startDateQueryGeo;
      }
      if(this.stopDateQueryGeo !== null){
        query['maxDate'] = this.stopDateQueryGeo;
      }

      let query_false;
      if(!query['country']){
        query_false = 'geo_group'
      }
      else if(!query['region']){
        let arr_geo = ['geo_group'];
        let i = 0;
        let len = arr_geo.length;
        while (i<len && i<(this.numLevelAboveBackground-1)){
          delete query[arr_geo[i]];
          i = i + 1;
        }
        query_false = 'country'
      }
      else if(!query['province']){
        let arr_geo = ['country', 'geo_group'];
        let i = 0;
        let len = arr_geo.length;
        while (i<len && i<(this.numLevelAboveBackground-1)){
          delete query[arr_geo[i]];
          i = i + 1;
        }
        query_false = 'region'
      }
      else{
        let arr_geo = ['region', 'country', 'geo_group'];
        let i = 0;
        let len = arr_geo.length;
        while (i<len && i<(this.numLevelAboveBackground-1)){
          delete query[arr_geo[i]];
          i = i + 1;
        }
        query_false = 'province'
      }

      let to_send = {'query': query,
                     'protein': array_protein,
                    'query_false': query_false,
                    'includeUKBackground': this.includeUKGeo};
      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let headers = [
              {'text': 'mutation', 'value': 'mutation_position', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'target', 'value': 'target', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'background', 'value': 'background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': 'odds_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
              {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'numerator_background', 'value': 'numerator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'denominator_background', 'value': 'denominator_background', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'numerator_target', 'value': 'numerator_target', 'show': true, 'align': 'center', 'width': '23vh'},
              //{'text': 'denominator_target', 'value': 'denominator_target', 'show': true, 'align': 'center', 'width': '23vh'},
          ];
          this.headerTableProvReg = headers;
          this.rowsTableProvReg = res;
          this.fixedRowsTableProvReg = res;

          let copy = JSON.parse(JSON.stringify(this.rowsTableProvReg));
          this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];
          this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];

          let rowTable = JSON.parse(JSON.stringify(this.rowsTableProvReg));
          this.totalMaxTargetNumerator = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_target']; }))
          this.selectedMaxTargetNumerator = this.totalMaxTargetNumerator;
          this.totalMaxBackgroundNumerator = Math.max.apply(Math, rowTable.map(function(o) { return o['denominator_background']; }))
          this.selectedMaxBackgroundNumerator = this.totalMaxBackgroundNumerator;
          let rowTable2 = JSON.parse(JSON.stringify(this.rowsTableProvReg));
          rowTable2 = rowTable2.filter(function (i){
              let perc = i['percentage_background'];
              return perc !== 0;
            }
          );
          this.totalMaxOddsRatio = Math.ceil(Math.max.apply(Math, rowTable2.map(function(o) { return o['odd_ratio']; })));
          this.selectedMaxOddsRatio = Math.ceil(this.totalMaxOddsRatio);

          this.tableApplied = true;
          this.overlay = false;
        });
    },
    applyFilterPValueChart(){
      this.selectedDomainForPValue = null;
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
          let single_element = {'name': mutation, 'value': elem['numerator_target'], 'position': mutation_position
          , 'p_value': elem['p_value'], 'odds_ratio': elem['odd_ratio']};
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
                  this.possibleDomainForPValue = res;
                  this.overlay = false;
                  this.pValueBarChartApplied = true;
              });
        });
    },
    openDialogAccession(type, item){
      let url = `/analyze/getAccessionIds`;
      this.overlay = true;
      this.listAccessionIds = [];

      let query = JSON.parse(JSON.stringify(this.queryGeo));
      let query_false = '';
      if(type === 'target'){
        query['lineage'] = item['lineage'][0];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        query['minDateBackground'] = this.startDateQueryGeo;
        query['maxDateBackground'] = this.stopDateQueryGeo;
        query['product'] = item['product'];
        query['includeUK'] = true;
      }
      else if(type === 'background'){
        query['lineage'] = item['lineage'][0];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        query['minDateBackground'] = this.startDateQueryGeo;
        query['maxDateBackground'] = this.stopDateQueryGeo;
        query['product'] = item['product'];
        query['includeUK'] = this.includeUKGeo;

        if(!query['country']){
          query_false = 'geo_group'
        }
        else if(!query['region']){
          query_false = 'country'
        }
        else if(!query['province']){
          query_false = 'region'
        }
        else{
          query_false = 'province'
        }
      }

      let query_target = 'empty';
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
    modifyPossibleBackground() {
      let arrayPossibleBackground = [];
      this.possibleNumLevelAboveBackground = [];
      if (this.queryGeo['province']) {
        let possibleBackground1 = {'value': 1,
          'background': this.queryGeo['province'] + ' vs ' + this.queryGeo['region'] }
        let possibleBackground2 = {'value': 2,
          'background': this.queryGeo['province'] + ' vs ' + this.queryGeo['country'] }
        let possibleBackground3 = {'value': 3,
          'background': this.queryGeo['province'] + ' vs ' + this.queryGeo['geo_group'] }
        let possibleBackground4 = {'value': 4,
          'background': this.queryGeo['province'] + ' vs ' + 'World' }
        arrayPossibleBackground.push(possibleBackground1);
        arrayPossibleBackground.push(possibleBackground2);
        arrayPossibleBackground.push(possibleBackground3);
        arrayPossibleBackground.push(possibleBackground4);
      } else if (this.queryGeo['region']) {
        let possibleBackground2 = {'value': 1,
          'background': this.queryGeo['region'] + ' vs ' + this.queryGeo['country'] }
        let possibleBackground3 = {'value': 2,
          'background': this.queryGeo['region'] + ' vs ' + this.queryGeo['geo_group'] }
        let possibleBackground4 = {'value': 3,
          'background': this.queryGeo['region'] + ' vs ' + 'World' }
        arrayPossibleBackground.push(possibleBackground2);
        arrayPossibleBackground.push(possibleBackground3);
        arrayPossibleBackground.push(possibleBackground4);
      } else if (this.queryGeo['country']) {
        let possibleBackground3 = {'value': 1,
          'background': this.queryGeo['country'] + ' vs ' + this.queryGeo['geo_group'] }
        let possibleBackground4 = {'value': 2,
          'background': this.queryGeo['country'] + ' vs ' + 'World' }
        arrayPossibleBackground.push(possibleBackground3);
        arrayPossibleBackground.push(possibleBackground4);
      } else if (this.queryGeo['geo_group']) {
        let possibleBackground4 = {'value': 1,
          'background': this.queryGeo['geo_group'] + ' vs ' + 'World' }
        arrayPossibleBackground.push(possibleBackground4);
      }
      else {
        arrayPossibleBackground = [];
      }
      this.possibleNumLevelAboveBackground = arrayPossibleBackground;
    },
    getFieldText(item){
      let name = '';
      name = item['background'];
      return name;
    },
    getFieldTextDomain(item){
      return `${item['Description']}` //  ----- ${item['cnt']}
    },
  },
  watch: {
    includeUK(){
      this.setIncludeUKGeo(this.includeUK);
    },
    IncludeUKGeo(){
       this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.selectedProteinTable = null;
       this.tableApplied = false;
    },
    numLevelAboveBackground(){
      this.pValueBarChartApplied = false;
     this.selectedProteinForPValue = null;
     this.selectedProteinTable = null;
     this.tableApplied = false;
    },
    startDateQueryGeo(){
      this.pValueBarChartApplied = false;
     this.selectedProteinForPValue = null;
     this.selectedProteinTable = null;
     this.tableApplied = false;
    },
    stopDateQueryGeo(){
      this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.selectedProteinTable = null;
       this.tableApplied = false;
    },
    'queryGeo.geo_group': function (){
        this.modifyPossibleBackground();
        this.setQueryGeo({field: 'country', list: null});
        this.setQueryGeo({field: 'region', list: null});
        this.setQueryGeo({field: 'province', list: null});
    },
    'queryGeo.country': function (){
        this.modifyPossibleBackground();
        this.setQueryGeo({field: 'region', list: null});
        this.setQueryGeo({field: 'province', list: null});
    },
    'queryGeo.region': function (){
        this.modifyPossibleBackground();
        this.setQueryGeo({field: 'province', list: null});
    },
    'queryGeo.province': function (){
        this.modifyPossibleBackground();
    },
    queryGeo(){
       this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.selectedProteinTable = null;
       this.tableApplied = false;
    },
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    selectedContinent_forProvReg(){
      this.selectedProteinTable = null;
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
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
      this.selectedProteinTable = null;
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
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
      this.selectedProteinTable = null;
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
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
      this.selectedProteinTable = null;
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
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
      this.selectedProteinTable = null;
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
    selectedProteinForTable(){
      this.filter();
    }
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
  .table_prov_reg table > tbody > tr > td:nth-child(1),
  .table_prov_reg table > tbody > tr > td:nth-child(3),
  .table_prov_reg table > tbody > tr > td:nth-child(4){
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