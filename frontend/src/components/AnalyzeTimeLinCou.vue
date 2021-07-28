<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#A8DADC">
          <v-card-title class="justify-center">
            <h1>TEMPORAL ANALYSIS</h1>
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                 <h2>SELECT LINEAGE AND LOCATION OF INTEREST</h2>
               </v-flex>
               <!--<v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h4>(both fields can be empty, meaning that all lineages/countries are interesting)</h4>
               </v-flex>-->
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryTime
                  field = 'lineage'>
                 </SelectorsQueryTime>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryTime
                  field = 'geo_group'>
                 </SelectorsQueryTime>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryTime
                  field = 'country'>
                 </SelectorsQueryTime>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryTime
                  field = 'region'>
                 </SelectorsQueryTime>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                 <SelectorsQueryTime
                  field = 'province'>
                 </SelectorsQueryTime>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px;">
                <h3>Select location to exclude from the one selected</h3>
              </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; padding: 0; margin: 0;">
                <SelectorQueryToExclude
                  mode="time"
                  :field="fieldToExclude">
                  </SelectorQueryToExclude>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyChosenLineageCountry()"
                         color="#E63946"
                         class="white--text"
                  >
                      APPLY
                  </v-btn>
                </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 50px;"
                        v-if = "chosenApplied && timeContent.length !== 0">
                 <h2>SELECT TARGET AND BACKGROUND:</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" v-if="chosenApplied && timeContent.length !== 0">
                <v-container fluid grid-list-xl style="justify-content: center; padding: 0; margin-top: 10px;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                      <v-btn id="two_comparison" large color="#457B9D" @click="selectedTabSelectTargetBackground = 0" style="margin-right: 10px; width: 400px; height: 70px;"> TWO-PERIOD COMPARISON </v-btn>
                      <v-btn id="n_comparison" large color="#457B9D" @click="selectedTabSelectTargetBackground = 1" style="margin-left: 10px; width: 400px; height: 70px;"> N-PERIOD ANALYSIS </v-btn>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                      <div v-if="selectedTabSelectTargetBackground === 0">
                        <TimeDistributionChart
                           :timeName="timeName"
                           :timeContent="timeContent"
                           :filterDate="filterDate"
                           style="width: 100%"
                       ></TimeDistributionChart>
                      </div>
                      <div v-if="selectedTabSelectTargetBackground === 1">
                       <TimeDistributionChartWeekMonth
                           :timeName="timeName + timeName"
                           :timeContent="timeContent"
                           :filterDate="filterDate"
                           style="width: 100%"></TimeDistributionChartWeekMonth>
                      </div>
                    </v-flex>
                  </v-layout>
                </v-container>
               </v-flex>
             </v-layout>

             <v-layout row wrap justify-center style="padding: 30px;" v-if="chosenApplied && timeContent.length !== 0">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h2>SELECT PROTEINS TO ANALYZE</h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                 <h4>(selecting none is equivalent to "all proteins")</h4>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
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
               v-if="errorNumSeqQueryTime">
                 <span style="color: red"> number of sequences selected is too low (minimum 10 for both target and background)</span>
               </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applySingleLineageAnalysis()"
                         color="#E63946"
                         class="white--text"
                         :disabled="errorNumSeqQueryTime"
                  >
                      APPLY
                  </v-btn>
                </v-flex>
             </v-layout>

             <v-layout row wrap justify-center v-if="chosenApplied && timeContent.length === 0">
               <v-row justify="center" align="center">
                <span style="background-color: #F1FAEE;
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
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#A8DADC">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                  <h2>APPLY FILTERS FOR SELECTING THE CHANGES IN THE TABLE<span v-if="fixedRowAnalyzeTime.length > 1">S AND HEATMAP</span><span>  BELOW</span></h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center">
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>% BACKGROUND:</h5>
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
                                % BACKGROUND
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
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5># SEQUENCES IN BACKGROUND:</h5>
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
                                # SEQUENCES IN BACKGROUND
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
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>% TARGET:</h5>
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
                                % TARGET
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
                  <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5># SEQUENCES IN TARGET:</h5>
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
                                # SEQUENCES IN TARGET
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
                  <v-card width="500px" color="#F1FAEE">
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
                  <v-card width="500px" color="#F1FAEE">
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
                     <v-card width="500px" color="#F1FAEE">
                        <v-card-title class="justify-center">
                          <h5>FILTER PROTEIN:</h5>
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
                                FILTER PROTEIN
                            </v-card-title>
                            <v-card-text>
                             ...
                            </v-card-text>
                        </v-card>
                    </v-dialog>
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
                         color="#E63946"
                         class="white--text"
                  >
                      APPLY
                  </v-btn>
               </v-flex>
               <v-card width="1000px" color="#F1FAEE" style="margin-top: 50px; padding: 10px" v-if="queryTime['lineage']">
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center; margin-top: 12px" v-if="rowsAnalyzeTime.length !== 0">
                     <h3>IMPORTANT CHANGES OF TARGET LINEAGE:</h3>
                   </v-flex>
                   <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center" v-if="rowsAnalyzeTime.length !== 0">
                     <v-select
                      v-model="selectedTypeImportantMutation"
                      :items="possibleTypeImportantMutation"
                      label="Type Important Change"
                      solo
                      hide-details>
                     </v-select>
                   </v-flex>
                   <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center; margin-top: 12px" v-if="rowsAnalyzeTime.length !== 0">
                     <ImportantMutation
                     :importantMutationECDC="importantMutationECDC"
                     :importantMutation75Percentage="importantMutation75Percentage"
                     :rowsTable = "fixedRowAnalyzeTime">
                     </ImportantMutation>
                   </v-flex>
                 </v-layout>
               </v-card>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 30px" v-if="rowsAnalyzeTime.length > 1">
                 <HeatmapMultipleAnalysis
                 nameHeatmap = "multipleAnalysisHeatmapTime"
                 :contentHeatmap = "rowsAnalyzeTime"
                 :fixedContent = "fixedRowAnalyzeTime"
                 :maxOddsRatio = "totalMaxOddsRatio"
                 :importantMutation = "importantMutation">
                 </HeatmapMultipleAnalysis>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 50px">
                 <h2>CHANGES IN TARGET vs BACKGROUND PERIOD</h2><h2 v-if="rowsAnalyzeTime.length > 1">S</h2>
               </v-flex>
              <v-tabs v-model="selectedTabTable"
              background-color="#457B9D"
              dark
              vertical
              show-arrows
              slider-color="#E63946"
              slider-size="6">

                <v-tab style="border-bottom: black solid 1px; width: 200px" v-for="(rows ,index) in rowsAnalyzeTime" v-bind:key="index">
                  <span>{{ fixedRowAnalyzeTime[index][0]['target'].split(' / ')[0] }}<br>
                    {{ fixedRowAnalyzeTime[index][0]['target'].split(' / ')[1] }}
                  </span>
                </v-tab>

                <v-tabs-items v-model="selectedTabTable" style="background: #F1FAEE;">
                  <v-tab-item style="padding: 20px; background-color: #F1FAEE" v-for="(rowsAnalTime ,index) in rowsAnalyzeTime" v-bind:key="index">
                    <v-layout row wrap justify-space-around style="margin-top: 10px">
                      <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                         <v-card width="500px" color="#F1FAEE" style="border: black solid 1px">
                            <v-card-title class="justify-center">
                              <h5>INFO:</h5>
                            </v-card-title>
                            <v-card-text>
                              <span>
                                <b> - TARGET: </b>
                                <span>{{fixedRowAnalyzeTime[index][0]['target']}}</span>
                                <br>
                              </span>
                              <span>
                                <b> - TOT NUM SEQ IN TARGET: </b>
                                <span>{{fixedRowAnalyzeTime[index][0]['denominator_target']}}</span>
                                <br>
                              </span>
                              <br>
                              <span>
                                <b> - BACKGROUND: </b>
                                <span>{{fixedRowAnalyzeTime[index][0]['background']}}</span>
                                <br>
                              </span>
                              <span>
                                <b> - TOT NUM SEQ IN BACKGROUND: </b>
                                <span>{{fixedRowAnalyzeTime[index][0]['denominator_background']}}</span>
                                <br>
                              </span>
                            </v-card-text>
                         </v-card>
                       </v-flex>
                      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                          <h2>TABLE<v-btn @click="downloadTable('analyze_mutation', rowsAnalTime)" x-small icon
                                  style="margin-left: 20px; margin-bottom: 5px">
                                    <v-icon size="23">
                                      mdi-download-circle-outline
                                    </v-icon>
                                </v-btn>
                          </h2>
                      </v-flex>
                      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                        <v-data-table
                              :headers="headerAnalyzeTime"
                              :items="rowsAnalTime"
                              class="data-table table_analyze_time"
                              style="width: 98%; border: grey solid 1px"
                              multi-sort
                              :sort-by.sync="sortByAnalyzeTime"
                              :sort-desc.sync="sortDescAnalyzeTime"
                        >
                            <template v-slot:item ="{ item }">
                              <tr>
                                <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center; align-content: center" v-for="header in headerAnalyzeTime"
                                    :key="header.value" v-show="header.show">
                                      <span style="color: white; font-weight: 900; background-color: #1D3557; padding: 5px" v-if="header.value === 'mutation_position' && importantMutation['mutation'].includes(item['mutation'])">{{item['mutation']}}</span>
                                      <span style="color: white; font-weight: 900; background-color: #457B9D; padding: 5px" v-else-if="header.value === 'mutation_position' && importantMutation['additional_mutation'].includes(item['mutation'])">{{item['mutation']}}</span>
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
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#A8DADC">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 <h2>TARGET SEQUENCES BAR CHART</h2>
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
                 <v-card width="500px" color="#F1FAEE">
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
                         color="#E63946"
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
                           <v-card width="400px" color="#F1FAEE">
                              <v-card-title class="justify-center">
                                <h5>HIGHLIGHT DOMAINS:</h5>
                              </v-card-title>
                              <v-card-text>
                                <v-autocomplete
                                  v-model="selectedDomainForPValue"
                                  :items="possibleDomainForPValue"
                                  label="Sites, family, and domains"
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
                           <v-card width="400px" color="#F1FAEE">
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
                           <v-card width="400px" color="#F1FAEE">
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
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}}</h5>
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
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}}</h5>
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
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}}</h5>
                              </v-card>
                            </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                 </v-layout>
                 <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                 </v-flex>
                 <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-for="(rowsAnalTime ,index) in rowsAnalyzeTime" v-bind:key="'pValue' + index">
                  <v-layout row wrap justify-space-between>
                    <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: left;">
                       <v-card width="500px" color="#F1FAEE" style="height: 250px">
                          <v-card-text style="text-align: center; padding-top: 22%">
                            <span>
                              <b> TARGET: </b>
                              <br>
                            </span>
                            <span>
                              <span>{{fixedRowAnalyzeTime[index][0]['target']}}</span>
                              <br>
                            </span>
                            <span> NUM SEQ:
                              <span>{{fixedRowAnalyzeTime[index][0]['denominator_target']}}</span>
                              <br>
                            </span>
                            <br>
                            <span>
                              <b> BACKGROUND: </b>
                              <br>
                            </span>
                            <span>
                              <span>{{fixedRowAnalyzeTime[index][0]['background']}}</span>
                              <br>
                            </span>
                            <span> NUM SEQ:
                              <span>{{fixedRowAnalyzeTime[index][0]['denominator_background']}}</span>
                              <br>
                            </span>
                          </v-card-text>
                       </v-card>
                     </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center;">
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
                           type="time">
                       </PValueBarChart>
                     </v-flex>
                  </v-layout>
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
        <v-card-title class="headline" style="background-color: #A8DADC ; color: white">
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
import TimeDistributionChart from "./TimeDistributionChart";
import SelectorsQueryTime from "./SelectorsQueryTime";
import TimeDistributionChartWeekMonth from "./TimeDistributionChartWeekMonth";
import HeatmapMultipleAnalysis from "./HeatmapMultipleAnalysis";
import SelectorQueryToExclude from "./SelectorQueryToExclude";
import ImportantMutation from "./ImportantMutation";

export default {
  name: "AnalyzeTimeLinCou",
  components: {
    ImportantMutation,
    SelectorQueryToExclude,
    HeatmapMultipleAnalysis,
    TimeDistributionChartWeekMonth, SelectorsQueryTime, TimeDistributionChart, PValueBarChart},
  data() {
    return {
      overlay: false,
      rowsAnalyzeTime: [],
      fixedRowAnalyzeTime: [],
      headerAnalyzeTime: [],
      sortByAnalyzeTime: ['odd_ratio'],
      sortDescAnalyzeTime: [true],
      maxNumeratorTarget: 100,
      maxDenominatorTarget: 100,
      tableApplied: false,
      pValueName: [],
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

      selectedTabSelectTargetBackground: 0,
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

      selectedMinPercentageMutationPValue: 0,
      selectedMaxPercentageMutationPValue: 80,

      fieldToExclude: null,

      selectedTabTable: 0,

      importantMutationECDC: {},
      importantMutation75Percentage: {},
      importantMutation: {},

      selectedTypeImportantMutation: 'ECDC',
      possibleTypeImportantMutation: ['ECDC', 'Present in 75% of the lineage (worldwide)'],
    }
  },
  computed: {
    ...mapState(['all_protein', 'timeRangesTargetAndBackground', 'queryTime', 'errorNumSeqQueryTime'
                , 'toExcludeTime', 'timeDivisionAcceptable', 'colorPValueInfoBox'
                , 'color_1', 'color_2', 'color_3']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryTime']),
    computeFieldToExclude(){
      if (!this.queryTime['geo_group']) {
        this.fieldToExclude = 'geo_group';
      } else if (!this.queryTime['country']) {
        this.fieldToExclude = 'country';
      } else if (!this.queryTime['region']) {
        this.fieldToExclude = 'region';
      } else if (!this.queryTime['province']) {
        this.fieldToExclude = 'province';
      } else {
        this.fieldToExclude = null;
      }
    },
    filter(){
      let arr_row_an_time = [];
      for(let i = 0; i < this.rowsAnalyzeTime.length; i = i + 1) {
        let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeTime[i]));
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
      this.rowsAnalyzeTime = arr_row_an_time;
    },
    getDaysArray(start, end) {
      for (var arr = [], dt = new Date(start); dt <= end; dt.setDate(dt.getDate() + 1)) {
        let date = new Date(dt).toISOString().slice(0, 10);
        if(!arr.includes(date)) {
          arr.push(date);
        }
        if( date.indexOf('-10-24') !== -1){
          let date2 = new Date(date);
          date2.setDate(date2.getDate() + 1)
          let date3 = new Date(date2).toISOString().slice(0, 10);
          arr.push(date3);
        }
      }
      return arr;
    },
    downloadTable(table, rowAnalyzeTime){
      let text = "";
      let result_sorted = this.sortResults(table, rowAnalyzeTime);
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
    sortResults(table, rowAnalyzeTime){
      let len;
      let sortBy;
      let sortDesc;
      let results;
       if(table === 'analyze_mutation'){
        len = this.sortByAnalyzeTime.length;
        sortBy = this.sortByAnalyzeTime;
        sortDesc = this.sortDescAnalyzeTime;
        results = JSON.parse(JSON.stringify(rowAnalyzeTime));
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
    getFieldTextDomain(item){
      return `${item['Description']}` + ' / (' + `${item['Begin']}` + ' , ' + `${item['End']}` + ')';
    },
    applySingleLineageAnalysis(){
      let url = `/analyze/analyzeMutationCountryLineageInTime`;
      this.overlay = true;

      this.importantMutation = {};
      this.importantMutationECDC = {};
      let queryTime = JSON.parse(JSON.stringify(this.queryTime));
      let url_important_mutation = `/analyze/getImportantMutation`;
      let lineage_to_send = null;
      if(queryTime['lineage']){
        lineage_to_send = queryTime['lineage'];
      }
      let to_send_important_mutation = {'lineage': lineage_to_send}

      axios.post(url_important_mutation, to_send_important_mutation)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          this.importantMutationECDC = res;
          if(this.selectedTypeImportantMutation === 'ECDC'){
            if(queryTime['lineage']) {
              this.importantMutation = res;
            }
            else{
              this.importantMutation = {'mutation': [], 'additional_mutation': []};
            }
          }
        })

      let array_protein = [];
      if(this.selectedProtein.length === 0){
        array_protein = this.possibleProtein;
      }
      else{
        array_protein = this.selectedProtein;
      }

      let to_send_all_important_mutation_per_lineage= {'lineage': lineage_to_send, 'proteins': array_protein};
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


      this.possibleProteinForTable = [];
      this.possibleProteinForPValue = [];
      this.headerAnalyzeTime = [];
      this.rowsAnalyzeTime = [];
      this.fixedRowAnalyzeTime = [];

      if(this.selectedTabSelectTargetBackground === 0) {

        let query = JSON.parse(JSON.stringify(this.queryTime));
        query['toExclude'] = this.toExcludeTime;

        let start_target_time = this.timeRangesTargetAndBackground['start_target_time'];
        let end_target_time = this.timeRangesTargetAndBackground['end_target_time'];
        let start_background_time = this.timeRangesTargetAndBackground['start_background_time'];
        let end_background_time = this.timeRangesTargetAndBackground['end_background_time'];
        let array_protein = [];

        if (this.selectedProtein === null) {
          array_protein = [];
        } else {
          array_protein = this.selectedProtein;
        }

        let to_send = {
          'start_target': start_target_time,
          'end_target': end_target_time, 'start_background': start_background_time,
          'end_background': end_background_time, 'protein': array_protein
        }

        to_send['query'] = query;

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.headerAnalyzeTime = [
                {'text': 'mutation', 'value': 'mutation_position', 'show': true, 'align': 'center', 'width': '23vh'},
                {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
                {'text': 'odds_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
                {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
                {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
              ];

              this.rowsAnalyzeTime[0] = res;
              this.fixedRowAnalyzeTime[0] = res;

              let copy = JSON.parse(JSON.stringify(this.rowsAnalyzeTime[0]));
              this.possibleProteinForPValue = [...new Set(copy.map(elem => elem.product))];
              this.possibleProteinForTable = [...new Set(copy.map(elem => elem.product))];

              let rowTable = JSON.parse(JSON.stringify(this.rowsAnalyzeTime[0]));
              this.totalMaxTargetNumerator = Math.max.apply(Math, rowTable.map(function (o) {
                return o['denominator_target'];
              }))
              this.selectedMaxTargetNumerator = this.totalMaxTargetNumerator;
              this.totalMaxBackgroundNumerator = Math.max.apply(Math, rowTable.map(function (o) {
                return o['denominator_background'];
              }))
              this.selectedMaxBackgroundNumerator = this.totalMaxBackgroundNumerator;
              let rowTable2 = JSON.parse(JSON.stringify(this.rowsAnalyzeTime[0]));
              rowTable2 = rowTable2.filter(function (i) {
                    let perc = i['percentage_background'];
                    return perc !== 0;
                  }
              );
              this.totalMaxOddsRatio = Math.ceil(Math.max.apply(Math, rowTable2.map(function (o) {
                return o['odd_ratio'];
              })));
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
      }
      else if(this.selectedTabSelectTargetBackground === 1){
        let len = this.timeDivisionAcceptable.length - 1;
        let i = 0;
        this.headerAnalyzeTime = [
          {'text': 'mutation', 'value': 'mutation_position', 'show': true, 'align': 'center', 'width': '23vh'},
          {'text': 'p_value', 'value': 'p_value', 'show': true, 'align': 'center', 'width': '23vh'},
          {'text': 'odds_ratio', 'value': 'odd_ratio', 'show': true, 'align': 'center', 'width': '23vh'},
          {'text': '%_target', 'value': 'percentage_target', 'show': true, 'align': 'center', 'width': '23vh'},
          {'text': '%_background', 'value': 'percentage_background', 'show': true, 'align': 'center', 'width': '23vh'},
        ];
        if(i < len) {
          this.applyAnalysisTimeDivisions(i, len);
        }
      }
    },
    applyAnalysisTimeDivisions(i, len){
      let url = `/analyze/analyzeMutationCountryLineageInTime`;

      let query = JSON.parse(JSON.stringify(this.queryTime));
      query['toExclude'] = this.toExcludeTime;

      let period_1 = this.timeDivisionAcceptable[i];
      let period_2 = this.timeDivisionAcceptable[i+1];

      let start_target_time = period_2[0];
      let end_target_time = period_2[1];
      let start_background_time = period_1[0];
      let end_background_time = period_1[1];
      let array_protein = [];

      let date1 = new Date(start_target_time);
      let date2 = new Date(end_background_time);
      date1.setDate(date1.getDate() - 1);
      let date3 = new Date(date1).toISOString().slice(0, 10);
      let date4 = new Date(date2).toISOString().slice(0, 10);

      if(date3 === date4) {

        if (this.selectedProtein === null) {
          array_protein = [];
        } else {
          array_protein = this.selectedProtein;
        }

        let to_send = {
          'start_target': start_target_time,
          'end_target': end_target_time, 'start_background': start_background_time,
          'end_background': end_background_time, 'protein': array_protein
        }

        to_send['query'] = query;

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.rowsAnalyzeTime.push(res);
              this.fixedRowAnalyzeTime.push(res);

              let copy = JSON.parse(JSON.stringify(this.rowsAnalyzeTime[this.rowsAnalyzeTime.length - 1]));
              this.possibleProteinForPValue = [...new Set([...this.possibleProteinForPValue, ...copy.map(elem => elem.product)])];
              this.possibleProteinForTable = [...new Set([...this.possibleProteinForTable, ...copy.map(elem => elem.product)])];

              let rowTable = JSON.parse(JSON.stringify(this.rowsAnalyzeTime[this.rowsAnalyzeTime.length - 1]));

              let totalMaxTargetNum = Math.max.apply(Math, rowTable.map(function (o) {
                return o['denominator_target'];
              }))
              if (totalMaxTargetNum > this.totalMaxTargetNumerator) {
                this.totalMaxTargetNumerator = totalMaxTargetNum;
                this.selectedMaxTargetNumerator = totalMaxTargetNum;
              }

              let totalMaxBackNum = Math.max.apply(Math, rowTable.map(function (o) {
                return o['denominator_background'];
              }))
              if (totalMaxBackNum > this.totalMaxBackgroundNumerator) {
                this.totalMaxBackgroundNumerator = totalMaxBackNum;
                this.selectedMaxBackgroundNumerator = totalMaxBackNum;
              }

              let rowTable2 = JSON.parse(JSON.stringify(this.rowsAnalyzeTime[this.rowsAnalyzeTime.length - 1]));
              rowTable2 = rowTable2.filter(function (i) {
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

              i = i + 1;
              if (i < len) {
                this.applyAnalysisTimeDivisions(i, len);
              } else {
                this.tableApplied = true;
                this.overlay = false;
              }
            });
      }
      else{
        i = i + 1;
        if (i < len) {
          this.applyAnalysisTimeDivisions(i, len);
        } else {
          this.tableApplied = true;
          this.overlay = false;
        }
      }
    },
    applyFilterOnTable(){
      this.filter();
    },
    applyFilterPValueChart(){
      this.overlay = true;
      this.selectedDomainForPValue = [];
      this.selectedDomainForPValueMutagenesis = [];
      this.selectedDomainForPValueAaModifications = [];
      this.pValueContent = [];
      this.pValueName = [];

      for(let i = 0; i < this.rowsAnalyzeTime.length; i = i + 1) {
        let result = JSON.parse(JSON.stringify(this.fixedRowAnalyzeTime[i]));
        var that = this;
        result = result.filter(function (i){
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
        this.pValueName[i] = 'p_value_time' + i;
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
                  });

                  this.overlay = false;
                  this.pValueBarChartApplied = true;
              });
        });
    },
    applyChosenLineageCountry(){
      let url = `/analyze/analyzeTimeDistributionCountryLineage`;
      this.overlay = true;

      let query = JSON.parse(JSON.stringify(this.queryTime));
      query['toExclude'] = this.toExcludeTime;

      let to_send = {'query': query};

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

            let delayInMilliseconds = 500;
            let that = this;
            setTimeout(function() {
              that.selectedTabSelectTargetBackground = 0;
              let id1 = 'two_comparison';
              let id2 = 'n_comparison';
              let elem1 = document.getElementById(id1);
              elem1.style['color'] = 'white';
              elem1.style['font-weight'] = 'bold';
              let elem2 = document.getElementById(id2);
              elem2.style['color'] = '#FFFFFF80';
              elem2.style['font-weight'] = 'normal';
            }, delayInMilliseconds);
        });
    },
    openDialogAccession(type, item){
      let url = `/analyze/getAccessionIds`;
      this.overlay = true;
      this.listAccessionIds = [];

      let query = JSON.parse(JSON.stringify(this.queryTime));
      let query_false = '';
      if(type === 'target'){
        query['lineage'] = item['lineage'];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        query['minDateTarget'] = item['target'].split("//")[0];
        query['maxDateTarget'] = item['target'].split("//")[1];
        query['product'] = item['product'];
      }
      else if(type === 'background'){
        query['lineage'] = item['lineage'];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        query['minDateBackground'] = item['background'].split("//")[0];
        query['maxDateBackground'] = item['background'].split("//")[1];
        query['product'] = item['product'];
      }

      query['toExclude'] = this.toExcludeTime;

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
    }
  },
  watch: {
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
            return item['Description'] === that.selectedDomainForPValue[i].split(' / ')[0];
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
            return item['Description'] === that.selectedDomainForPValueMutagenesis[i].split(' / ')[0];
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
            return item['Description'] === that.selectedDomainForPValueAaModifications[i].split(' / ')[0];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValueAaModifications[index]['Begin'];
            max = this.possibleDomainForPValueAaModifications[index]['End'];
          }
          this.begin_value_domain_aa_modifications.push(min);
          this.end_value_domain_aa_modifications.push(max);
      }
    },
    'queryTime.geo_group': function (){
        this.setQueryTime({field: 'country', list: null});
        this.setQueryTime({field: 'region', list: null});
        this.setQueryTime({field: 'province', list: null});
    },
    'queryTime.country': function (){
        this.setQueryTime({field: 'region', list: null});
        this.setQueryTime({field: 'province', list: null});
    },
    'queryTime.region': function (){
        this.setQueryTime({field: 'province', list: null});
    },
    all_protein(){
      this.possibleProtein = this.all_protein;
    },
    queryTime(){
       this.computeFieldToExclude();
       this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.selectedProteinForTable = null;
       this.tableApplied = false;
       this.chosenApplied = false;
    },
    toExcludeTime(){
      this.pValueBarChartApplied = false;
       this.selectedProteinForPValue = null;
       this.selectedProteinForTable = null;
       this.tableApplied = false;
       this.chosenApplied = false;
    },
    selectedProtein(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProteinForTable = null;
      this.tableApplied = false;
    },
    timeRangesTargetAndBackground(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProteinForTable = null;
      this.tableApplied = false;
    },
    selectedTabSelectTargetBackground(){
      if(this.selectedTabSelectTargetBackground === 0){
        let id1 = 'two_comparison';
        let id2 = 'n_comparison';
        let elem1 = document.getElementById(id1);
        elem1.style['color'] = 'white';
        elem1.style['font-weight'] = 'bold';
        let elem2 = document.getElementById(id2);
        elem2.style['color'] = '#FFFFFF80';
        elem2.style['font-weight'] = 'normal';
      }
      else{
        let id1 = 'two_comparison';
        let id2 = 'n_comparison';
        let elem1 = document.getElementById(id1);
        elem1.style['color'] = '#FFFFFF80';
        elem1.style['font-weight'] = 'normal';
        let elem2 = document.getElementById(id2);
        elem2.style['color'] = 'white';
        elem2.style['font-weight'] = 'bold';
      }
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProteinForTable = null;
      this.tableApplied = false;
    },
    timeDivisionAcceptable(){
      this.pValueBarChartApplied = false;
      this.selectedProteinForPValue = null;
      this.selectedProteinForTable = null;
      this.tableApplied = false;
    },
    selectedProteinForPValue(){
      this.pValueBarChartApplied = false;
    },
    selectedMinPercentageMutationPValue(){
      this.pValueBarChartApplied = false;
    },
    selectedMaxPercentageMutationPValue(){
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
    // selectedProteinForTable(){
    //   this.filter();
    // }
  },
  mounted() {
      this.computeFieldToExclude();
      this.possibleProtein = this.all_protein;
  }
}
</script>

<style scoped>

  .table_analyze_time table > tbody > tr > td:nth-child(1),
  .table_analyze_time table > tbody > tr > td:nth-child(3),
  .table_analyze_time table > tbody > tr > td:nth-child(4){
    box-shadow: inset -0.5px 0 0 0 grey;
  }

  .centered-input >>> input {
    text-align: center
  }

</style>