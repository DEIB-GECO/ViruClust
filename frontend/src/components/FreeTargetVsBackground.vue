<template>
  <v-card width="100%" color="white" style="padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="1600px" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" color="#A8DADC">
          <v-card-title class="justify-center">
            <h1>CUSTOM ANALYSIS</h1>
          </v-card-title>
          <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs12 d-flex">
              <v-container fluid grid-list-xl style="justify-content: center; padding: 0; margin-top: 10px;">
                <v-tabs v-model="selectedTabFreeQuery"
                        background-color="#A8DADC"
                        dark
                        show-arrows
                        slider-color="#E63946"
                        slider-size="6"
                        height="60"
                        centered>

                  <v-tab id="tabFree1" style="border: black solid 1px; width: 40%; background-color: #457B9D">
                     DEFINE YOUR TARGET
                  </v-tab>

                  <v-tab id="tabFree2" style="border: black solid 1px; border-left: 0!important; width: 40%; background-color: #457B9D">
                     DEFINE YOUR BACKGROUND
                  </v-tab>

                  <v-tab style="border: black solid 1px; width: 20%; border-left: 0!important; background-color: #457B9D">
                     SUMMARY
                  </v-tab>

                  <v-tabs-items v-model="selectedTabFreeQuery" style="background: transparent;">

                    <v-tab-item style="background-color: #A8DADC; padding-top: 40px">

                      <v-container fluid grid-list-xl style="justify-content: center; padding: 0; margin-top: 10px;">

                        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                          <v-btn id="tabTargetFree1" large color="#457B9D" @click="selectedTabTargetFreeQuery = 0" style="margin-right: 10px; width: 400px; height: 70px;"> USE METADATA SEARCH </v-btn>
                          <v-btn id="tabTargetFree2" large color="#457B9D" @click="selectedTabTargetFreeQuery = 1;" style="margin-left: 10px; width: 400px; height: 70px;"> USE IDS </v-btn>
                        </v-flex>

                        <v-layout row wrap justify-center v-if="selectedTabTargetFreeQuery === 0">
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="!(listAccIdsTarget.length > 0)">
                            <FreeQuery
                              type="target">
                            </FreeQuery>
                           </v-flex>
                        </v-layout>


                        <v-layout row wrap justify-center v-if="selectedTabTargetFreeQuery === 1">
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                            <h2>INSERT ACCESSION IDs</h2>
                            <v-dialog width="500">
                                <template v-slot:activator="{ on }">
                                  <v-btn
                                        v-on="on"
                                          slot="activator"
                                          class="info-button"
                                          x-small
                                          text icon color="grey"
                                          style="margin-top: 10px; margin-left: 20px">
                                      <v-icon class="info-icon">mdi-information</v-icon>
                                  </v-btn>
                                </template>
                                <v-card>
                                    <v-card-title
                                            class="headline grey lighten-2"
                                            primary-title
                                    >
                                        INSERT ACCESSION IDs:
                                    </v-card-title>
                                    <v-card-text style="text-align: center;">
                                     <span>
                                       <br>
                                        For statistical significance you need to provide at least 50 valid ids not overlapping with the background.
                                       <br>
                                     </span>
                                    </v-card-text>
                                </v-card>
                            </v-dialog>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                            <v-card color="#F1FAEE" width="100%" style="padding: 11px">
                              <v-card-title class="justify-center">
                                <h5>ADD ACCESSION IDs:</h5>
                              </v-card-title>
                              <v-card-text>
                                <v-layout row wrap justify-center>
                                  <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                                    <v-text-field
                                      v-model = "accession_id_target"
                                      solo
                                      hide-details
                                      style="margin-right: 10px"
                                    ></v-text-field>
                                  </v-flex>
                                  <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                                    <v-btn
                                        class="white--text"
                                         small
                                         color="#E63946"
                                         style="margin-top: 10px"
                                        @click="addAccessionIdTarget()"
                                    >
                                      ADD
                                    </v-btn>
                                  </v-flex>
                                  <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                                    <v-dialog width="500" v-model="dialogAccIdsTargetInserted">
                                        <template v-slot:activator="{ on }">
                                          <v-btn
                                              v-on="on"
                                              slot="activator"
                                              class="white--text"
                                               small
                                               color="#1D3557"
                                               style="margin-top: 10px"
                                              :disabled="!(listAccIdsTargetInserted.length > 0)"
                                          >
                                            SHOW LIST ({{listAccIdsTargetInserted.length}})
                                          </v-btn>
                                        </template>
                                        <v-card>
                                            <v-card-title
                                                    class="headline"
                                                    style="background-color: #A8DADC"
                                            >
                                                ACCESSION IDs ADDED:
                                              <v-spacer></v-spacer>
                                              <v-btn
                                                color="black"
                                                text
                                                @click="deleteAllAccIdsTargetInserted();"
                                              >
                                                DELETE ALL
                                              </v-btn>
                                            </v-card-title>
                                            <v-card-text style="text-align: center;">
                                              <span><br>
                                                <span v-for="(acc_id, index) in listAccIdsTargetInserted" v-bind:key="acc_id">
                                                  {{acc_id}}
                                                  <v-btn
                                                        style="background-color: red; margin-left: 20px"
                                                        icon
                                                        width="15px"
                                                        height="15px"
                                                      color="white"
                                                        @click="deleteAccIdsTargetInserted(index)"
                                                    >
                                                      <v-icon size="12">mdi-close</v-icon>
                                                    </v-btn>
                                                  <br>
                                                </span>
                                              </span>
                                            </v-card-text>
                                        </v-card>
                                    </v-dialog>
                                  </v-flex>
                                </v-layout>
                              </v-card-text>
                              <v-card-title class="justify-center">
                                <h5>UPLOAD LIST OF ACCESSION IDs:</h5>
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
                                            UPLOAD LIST OF ACCESSION IDs:
                                        </v-card-title>
                                        <v-card-text style="text-align: center;">
                                         <span>
                                          <br><br>
                                         </span>
                                          <span><b>EXAMPLE OF FILE</b> <v-btn @click="downloadExampleListAccessionIds('target')" x-small icon
                                            style="margin-left: 20px;">
                                              <v-icon size="18">
                                                mdi-download-circle-outline
                                              </v-icon>
                                          </v-btn></span>
                                        </v-card-text>
                                    </v-card>
                                </v-dialog>
                              </v-card-title>
                              <v-card-text>
                                <v-layout row wrap justify-space-around>
                                  <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                                    <input id="inputAccIdsTarget" type="file" style="display:none"
                                                 v-on:change="loadAccIdsTarget()" accept=".txt"
                                                 onclick="document.getElementById('inputAccIdsTarget').value = ''"
                                          />
                                    <v-btn
                                           onclick="document.getElementById('inputAccIdsTarget').click()"
                                           class="white--text"
                                           small
                                           color="#E63946"
                                           style="margin-top: 10px"
                                    >
                                        Upload Target Accession IDs
                                    </v-btn>
                                  </v-flex>
                                  <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                                   <v-text-field
                                    :value = this.nameFileAccIdsTarget
                                    solo
                                    readonly
                                    hide-details
                                    style="margin-right: 10px"
                                  ></v-text-field>
                                   <v-btn
                                      style="background-color: red; margin-top: 10px;"
                                      icon
                                      x-small
                                    color="white"
                                      @click="deleteAccIdsTarget()"
                                  >
                                    <v-icon size="18">mdi-close</v-icon>
                                  </v-btn>
                                 </v-flex>
                                </v-layout>
                              </v-card-text>
                            </v-card>
                          </v-flex>
                        </v-layout>
                      </v-container>
                    </v-tab-item>

                    <v-tab-item style="background-color: #A8DADC; padding-top: 40px">

                      <v-container fluid grid-list-xl style="justify-content: center; padding: 0; margin-top: 10px;">

                        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                          <v-btn id="tabBackgroundFree1" large color="#457B9D" @click="selectedTabBackgroundFreeQuery = 0" style="margin-right: 10px; width: 400px; height: 70px;"> USE METADATA SEARCH </v-btn>
                          <v-btn id="tabBackgroundFree2" large color="#457B9D" @click="selectedTabBackgroundFreeQuery = 1;" style="margin-left: 10px; width: 400px; height: 70px;"> USE IDS </v-btn>
                        </v-flex>

                          <v-layout row wrap justify-center v-if="selectedTabBackgroundFreeQuery === 0">
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="!(listAccIdsBackground.length > 0)">
                            <FreeQuery
                              type="background">
                            </FreeQuery>
                           </v-flex>
                          </v-layout>

                          <v-layout row wrap justify-center v-if="selectedTabBackgroundFreeQuery === 1">
                            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                            <h2>INSERT ACCESSION IDs</h2>
                            <v-dialog width="500">
                                <template v-slot:activator="{ on }">
                                  <v-btn
                                        v-on="on"
                                          slot="activator"
                                          class="info-button"
                                          x-small
                                          text icon color="grey"
                                          style="margin-top: 10px; margin-left: 20px">
                                      <v-icon class="info-icon">mdi-information</v-icon>
                                  </v-btn>
                                </template>
                                <v-card>
                                    <v-card-title
                                            class="headline grey lighten-2"
                                            primary-title
                                    >
                                        INSERT ACCESSION IDs:
                                    </v-card-title>
                                    <v-card-text style="text-align: center;">
                                     <span>
                                       <br>
                                        For statistical significance you need to provide at least 50 valid ids not overlapping with the target.
                                       <br>
                                     </span>
                                    </v-card-text>
                                </v-card>
                            </v-dialog>
                          </v-flex>
                            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                              <v-card color="#F1FAEE" width="100%" style="padding: 11px">
                                <v-card-title class="justify-center">
                                  <h5>ADD ACCESSION IDs:</h5>
                                </v-card-title>
                                <v-card-text>
                                  <v-layout row wrap justify-center>
                                    <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                                      <v-text-field
                                        v-model = "accession_id_background"
                                        solo
                                        hide-details
                                        style="margin-right: 10px"
                                      ></v-text-field>
                                    </v-flex>
                                    <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                                      <v-btn
                                          class="white--text"
                                           small
                                           color="#E63946"
                                           style="margin-top: 10px"
                                          @click="addAccessionIdBackground()"
                                      >
                                        ADD
                                      </v-btn>
                                    </v-flex>
                                    <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                                      <v-dialog width="500"  v-model="dialogAccIdsBackgroundInserted">
                                          <template v-slot:activator="{ on }">
                                            <v-btn
                                                v-on="on"
                                                slot="activator"
                                                class="white--text"
                                                 small
                                                 color="#1D3557"
                                                 style="margin-top: 10px"
                                                :disabled="!(listAccIdsBackgroundInserted.length > 0)"
                                            >
                                              SHOW LIST ({{listAccIdsBackgroundInserted.length}})
                                            </v-btn>
                                          </template>
                                          <v-card>
                                              <v-card-title
                                                      class="headline"
                                                      style="background-color: #A8DADC"
                                              >
                                                  ACCESSION IDs ADDED:
                                                <v-spacer></v-spacer>
                                                <v-btn
                                                  color="black"
                                                  text
                                                  @click="deleteAllAccIdsBackgroundInserted();"
                                                >
                                                  DELETE ALL
                                                </v-btn>
                                              </v-card-title>
                                              <v-card-text style="text-align: center;">
                                                <span><br>
                                                  <span v-for="(acc_id, index) in listAccIdsBackgroundInserted" v-bind:key="acc_id">
                                                    {{acc_id}}
                                                    <v-btn
                                                          style="background-color: red; margin-left: 20px"
                                                          icon
                                                          width="15px"
                                                          height="15px"
                                                        color="white"
                                                          @click="deleteAccIdsBackgroundInserted(index)"
                                                      >
                                                        <v-icon size="12">mdi-close</v-icon>
                                                      </v-btn>
                                                    <br>
                                                  </span>
                                                </span>
                                              </v-card-text>
                                          </v-card>
                                      </v-dialog>
                                    </v-flex>
                                  </v-layout>
                                </v-card-text>
                                <v-card-title class="justify-center">
                                  <h5>UPLOAD LIST OF ACCESSION IDs:</h5>
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
                                              UPLOAD LIST OF ACCESSION IDs:
                                          </v-card-title>
                                          <v-card-text style="text-align: center;">
                                           <span>
                                            <br><br>
                                           </span>
                                            <span><b>EXAMPLE OF FILE</b> <v-btn @click="downloadExampleListAccessionIds('background')" x-small icon
                                              style="margin-left: 20px;">
                                                <v-icon size="18">
                                                  mdi-download-circle-outline
                                                </v-icon>
                                            </v-btn></span>
                                          </v-card-text>
                                      </v-card>
                                  </v-dialog>
                                </v-card-title>
                                <v-card-text>
                                  <v-layout row wrap justify-space-around>
                                    <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                                      <input id="inputAccIdsBackground" type="file" style="display:none"
                                                   v-on:change="loadAccIdsBackground()" accept=".txt"
                                                   onclick="document.getElementById('inputAccIdsBackground').value = ''"
                                            />
                                      <v-btn
                                             onclick="document.getElementById('inputAccIdsBackground').click()"
                                             class="white--text"
                                             small
                                             color="#E63946"
                                             style="margin-top: 10px"
                                      >
                                          Upload Background Accession IDs
                                      </v-btn>
                                    </v-flex>
                                    <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                                     <v-text-field
                                      :value = this.nameFileAccIdsBackground
                                      solo
                                      readonly
                                      hide-details
                                      style="margin-right: 10px"
                                    ></v-text-field>
                                     <v-btn
                                        style="background-color: red; margin-top: 10px;"
                                        icon
                                        x-small
                                      color="white"
                                        @click="deleteAccIdsBackground()"
                                    >
                                      <v-icon size="18">mdi-close</v-icon>
                                    </v-btn>
                                   </v-flex>
                                  </v-layout>
                                </v-card-text>
                              </v-card>
                            </v-flex>
                          </v-layout>
                      </v-container>
                    </v-tab-item>

                    <v-tab-item style="background-color: #A8DADC; padding-top: 40px">
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
              <h3> Remove overlapping data from </h3>
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
               <h2>SELECT THE PROTEINS TO COMPARE</h2>
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
                 <span style="color: red"> The number of currently selected genomic sequences is too low. A minimum of 50 non-overlapping sequences must be selected for both the target and background. Please change your setting.</span><br>
                 <span style="color: red"> (Please be aware that overlapping entries are removed from {{selectRemoveOverlapping.toLowerCase()}})</span>
              </span>
               </v-flex>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-btn
                         @click="applyFreeQueryAnalysis()"
                         color="#E63946"
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
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#A8DADC">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                  <h2>ADVANCED FILTERS</h2>
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
               <v-card width="1000px" color="#F1FAEE" style="margin-top: 50px; padding: 10px" v-if="queryFreeTarget['lineage']">
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; margin-top: 12px" v-if="fixedRowsTable.length !== 0">
                     <h3>CHANGES TO HIGHLIGHT:</h3>
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
                slider-color="#E63946"
                slider-size="6">

                <v-tabs-items v-model="selectedTabTable" style="background: #F1FAEE;">
                  <v-tab-item style="padding: 20px; background-color: #F1FAEE" v-for="(rows ,index) in rowsTable" v-bind:key="index">
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
                                                      style="background-color: #A8DADC ; color: white;"
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
                                        <span v-else-if="header.value === 'p_value' && item['p_value'] >= 0.00001">{{item['p_value'].toFixed(5)}}</span>
                                        <span v-else-if="header.value === 'p_value' && item['p_value'] > 0 && item['p_value'] < 0.00001">{{item['p_value']}}</span>
                                        <span v-else-if="header.value === 'p_value' && item['p_value'] === 0">{{p_value_lower}}</span>
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
                <h2> TARGET SEQUENCES BAR CHART </h2>
               </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                 <v-card width="500px" color="#F1FAEE">
                    <v-card-title class="justify-center">
                      <h5>P-VALUE:</h5>
                    </v-card-title>
                    <v-card-text >
                      <v-layout row wrap justify-space-around>
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
                    <v-card-text style="margin-top: 10px">
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
                        <h5>PREVALENCE RANGE OF AA CHANGES:</h5>
                    </v-card-title>
                    <v-card-text style="padding-top: 0; margin-top: 0">
                      <v-layout row wrap justify-space-around style="margin-top: 0; padding: 0">
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
                                <h5>HIGHLIGHT FUNCTIONALLY CHARACTERISED<br> SITES:</h5>
                              </v-card-title>
                              <v-card-text>
                                <v-autocomplete
                                  v-model="selectedDomainForPValueMutagenesis"
                                  :items="possibleDomainForPValueMutagenesis"
                                  label="Functionally Characterised Sites"
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
                                  v-model="selectedDomainForPValueAaModificationsFake"
                                  :items="possibleDomainForPValueAaModifications"
                                  label="Glycosylation Sites"
                                  solo
                                  hide-details
                                  :item-text="getFieldTextDomain"
                                >
                                </v-autocomplete>
                                <v-layout row wrap justify-center style="padding: 0; margin: 0">
                                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin: 0">
                                    <v-checkbox v-model="selectedAllAaModifications"
                                    label="Select All"
                                    input-value="true"
                                    hide-details>
                                    </v-checkbox>
                                  </v-flex>
                                </v-layout>
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
                              <v-card color="#FFA50080" height="100%">
                                <h5 style="text-align: center; color: black ">{{domain.toUpperCase()}}</h5>
                              </v-card>
                            </v-card>
                         </v-flex>
                     </v-layout>
                    </v-flex>
                 </v-layout>
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                     <v-card width="400px" color="#F1FAEE">
                        <v-card-title class="justify-center">
                          <h5>UPLOAD YOUR REGIONS:</h5>
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
                                      UPLOAD YOUR REGIONS:
                                  </v-card-title>
                                  <v-card-text style="text-align: center;">
                                   <span>
                                    <br><br>
                                   </span>
                                    <span><b>EXAMPLE OF FILE</b> <v-btn @click="downloadExampleCSV()" x-small icon
                                      style="margin-left: 20px;">
                                        <v-icon size="18">
                                          mdi-download-circle-outline
                                        </v-icon>
                                    </v-btn></span>
                                  </v-card-text>
                              </v-card>
                          </v-dialog>
                        </v-card-title>
                        <v-card-text>
                           <v-layout wrap justify-space-around>
                              <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                                <input id="inputDomainCSVFree" type="file" style="display:none"
                                             v-on:change="loadDomainCSV()" accept=".csv"
                                             onclick="document.getElementById('inputDomainCSVFree').value = ''"
                                      />
                                <v-btn
                                       onclick="document.getElementById('inputDomainCSVFree').click()"
                                       class="white--text"
                                       small
                                       color="#E63946"
                                       style="margin-top: 10px"
                                >
                                    Upload CSV
                                </v-btn>
                              </v-flex>
                             <v-flex class="no-horizontal-padding xs8 d-flex" style="justify-content: center;">
                               <v-text-field
                                :value = this.nameFileDomainCSV
                                solo
                                readonly
                                hide-details
                                style="margin-right: 10px"
                              ></v-text-field>
                               <v-btn
                                  style="background-color: red; margin-top: 10px;"
                                  icon
                                  x-small
                                color="white"
                                  @click="deleteDomainCSV()"
                              >
                                <v-icon size="18">mdi-close</v-icon>
                              </v-btn>
                             </v-flex>
                           </v-layout>
                        </v-card-text>
                     </v-card>
                   </v-flex>
                 </v-layout>
                 <v-layout row wrap justify-center>
                   <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-center>
                         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; padding-bottom: 5px!important;" v-for="(domain, idx) in selectedDomainForPValueUploaded" v-bind:key="idx">
                            <v-card style="width: 400px;" color="white" v-if="selectedDomainForPValueUploaded.length > 0">
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
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-for="(rows ,index) in rowsTable" v-bind:key="'pValue' + index">
                <v-layout row wrap justify-space-around style="margin: 10px; padding: 10px">
                   <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                     <v-layout row wrap justify-space-between>
                        <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: left;">
                           <v-card width="500px" color="#F1FAEE" style="height: 250px">
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
                             :selectedDomainForPValueUploaded="selectedDomainForPValueUploaded"
                             :possibleDomainForPValueUploaded="possibleDomainForPValueUploaded"
                             type="free"
                             :rowsAnalTime = rows
                             :protein = selectedProteinForPValue
                             :nameFileAccIdsTarget = nameFileAccIdsTarget
                             :nameFileAccIdsBackground = nameFileAccIdsBackground
                             :listAccIdsTargetInserted = listAccIdsTargetInserted
                             :listAccIdsBackgroundInserted = listAccIdsBackgroundInserted>
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
        <v-card-title class="headline" style="background-color: #A8DADC ;">
          Accession IDs
          <v-spacer></v-spacer>
          <v-btn
            color="rgb(122, 139, 157)"
            text
            @click="downloadAccessionIds()"
          >
            DOWNLOAD
          </v-btn>
          <v-btn
            color="rgb(122, 139, 157)"
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
      min_num_seq_target: 50,
      min_num_seq_background: 50,
      min_num_seq_target_acc_ids: 50,
      min_num_seq_background_acc_ids: 50,

      selectedTabTargetFreeQuery: 0,
      selectedTabBackgroundFreeQuery: 0,

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
      p_value_lower: '<0.00001',

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

      selectedAllAaModifications: false,
      selectedDomainForPValueAaModificationsFake: [],
      selectedDomainForPValueAaModifications: [],
      possibleDomainForPValueAaModifications: [],
      begin_value_domain_aa_modifications: [],
      end_value_domain_aa_modifications: [],

      possibleDomainForPValueUploaded: [],
      selectedDomainForPValueUploaded: [],

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

      fileDomainCSV: null,
      nameFileDomainCSV: null,

      accessionIdsTargetOrBackground: null,
      accessionIdsSingleMutation: null,

      listAccIdsTarget: [],
      listAccIdsBackground: [],

      fileAccIdsTarget: null,
      nameFileAccIdsTarget: null,
      listAccIdsTargetFile: [],
      fileAccIdsBackground: null,
      nameFileAccIdsBackground: null,
      listAccIdsBackgroundFile: [],

      accession_id_target: null,
      accession_id_background: null,
      listAccIdsTargetInserted: [],
      listAccIdsBackgroundInserted: [],

      dialogAccIdsTargetInserted: false,
      dialogAccIdsBackgroundInserted: false,
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
    ...mapMutations(['setStartDateQueryFreeTarget', 'setStartDateQueryFreeBackground',
                     'setStopDateQueryFreeTarget', 'setStopDateQueryFreeBackground', 'setNumSequencesQueryFreeTarget',
                     'setNumSequencesQueryFreeBackground']),
    ...mapActions(['setQueryFreeTarget', 'setQueryFreeBackground']),
    deleteAllAccIdsTargetInserted(){
      this.listAccIdsTargetInserted = [];
      this.dialogAccIdsTargetInserted = false;
    },
    deleteAllAccIdsBackgroundInserted(){
      this.listAccIdsBackgroundInserted = [];
      this.dialogAccIdsBackgroundInserted = false;
    },
    deleteAccIdsTargetInserted(index){
      let array = JSON.parse(JSON.stringify(this.listAccIdsTargetInserted));
      array.splice(index, 1);
      this.listAccIdsTargetInserted = array;
    },
    deleteAccIdsBackgroundInserted(index){
      let array = JSON.parse(JSON.stringify(this.listAccIdsBackgroundInserted));
      array.splice(index, 1);
      this.listAccIdsBackgroundInserted = array;
    },
    addAccessionIdTarget(){
      let arr_acc_ids = this.accession_id_target.split(/(?:,|;|\t|\n| )+/);
      for(let i = 0; i < arr_acc_ids.length; i = i + 1) {
        if (arr_acc_ids[i] !== null && arr_acc_ids[i] !== '') {
          let url = `/analyze/checkAccessionId`;
          let to_send = {'accession_id': arr_acc_ids[i]}
          axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              if(res === true && !this.listAccIdsTargetInserted.includes(arr_acc_ids[i])){
                this.listAccIdsTargetInserted.push(arr_acc_ids[i]);
              }
            })
          // this.listAccIdsTargetInserted.push(arr_acc_ids[i]);
        }
      }
      this.accession_id_target = null;
    },
    addAccessionIdBackground(){
      let arr_acc_ids = this.accession_id_background.split(/(?:,|;|\t|\n| )+/);
      for(let i = 0; i < arr_acc_ids.length; i = i + 1) {
        if (arr_acc_ids[i] !== null && arr_acc_ids[i] !== '') {
          let url = `/analyze/checkAccessionId`;
          let to_send = {'accession_id': arr_acc_ids[i]}
          axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              if(res === true && !this.listAccIdsBackgroundInserted.includes(arr_acc_ids[i])){
                this.listAccIdsBackgroundInserted.push(arr_acc_ids[i]);
              }
            })
          //this.listAccIdsBackgroundInserted.push(arr_acc_ids[i]);
        }
      }
      this.accession_id_background = null;
    },
    downloadExampleListAccessionIds(type){
      let text;
      if(type === 'target'){
        text = 'EPI_ISL_3039500;  EPI_ISL_3039501;  EPI_ISL_3039502;  EPI_ISL_3039503;  EPI_ISL_3039504;  ' +
          ' EPI_ISL_3039505; EPI_ISL_3039506; EPI_ISL_3039507; EPI_ISL_3039508; EPI_ISL_3039509; EPI_ISL_3039510;' +
          ' EPI_ISL_3039511; EPI_ISL_3039512; EPI_ISL_3039513; EPI_ISL_3039514; EPI_ISL_3039515; EPI_ISL_3039516;' +
          ' EPI_ISL_3039517; EPI_ISL_3039518; EPI_ISL_3039519; EPI_ISL_3039520; EPI_ISL_3039521; EPI_ISL_3039522;' +
          ' EPI_ISL_3039523; EPI_ISL_3039524; EPI_ISL_3039525; EPI_ISL_3039526; EPI_ISL_3039527; EPI_ISL_3039528;' +
          ' EPI_ISL_3039529; EPI_ISL_3039530; EPI_ISL_3039531; EPI_ISL_3039532; EPI_ISL_3039533; EPI_ISL_3039534;' +
          ' EPI_ISL_3039535; EPI_ISL_3039536; EPI_ISL_3039537; EPI_ISL_3039538; EPI_ISL_3039539; EPI_ISL_3039540;' +
          ' EPI_ISL_3039541; EPI_ISL_3039542; EPI_ISL_3039543; EPI_ISL_3039544; EPI_ISL_3039545; EPI_ISL_3039546;' +
          ' EPI_ISL_3039547; EPI_ISL_3039548; EPI_ISL_3039549;';
      }
      else{
        text = 'EPI_ISL_3039300;  EPI_ISL_3039301;  EPI_ISL_3039302;  EPI_ISL_3039303;  EPI_ISL_3039304;  ' +
          ' EPI_ISL_3039305; EPI_ISL_3039306; EPI_ISL_3039307; EPI_ISL_3039308; EPI_ISL_3039309; EPI_ISL_3039310;' +
          ' EPI_ISL_3039311; EPI_ISL_3039312; EPI_ISL_3039313; EPI_ISL_3039314; EPI_ISL_3039315; EPI_ISL_3039316;' +
          ' EPI_ISL_3039317; EPI_ISL_3039318; EPI_ISL_3039319; EPI_ISL_3039320; EPI_ISL_3039321; EPI_ISL_3039322;' +
          ' EPI_ISL_3039323; EPI_ISL_3039324; EPI_ISL_3039325; EPI_ISL_3039326; EPI_ISL_3039327; EPI_ISL_3039328;' +
          ' EPI_ISL_3039329; EPI_ISL_3039330; EPI_ISL_3039331; EPI_ISL_3039332; EPI_ISL_3039333; EPI_ISL_3039334;' +
          ' EPI_ISL_3039335; EPI_ISL_3039336; EPI_ISL_3039337; EPI_ISL_3039338; EPI_ISL_3039339; EPI_ISL_3039340;' +
          ' EPI_ISL_3039341; EPI_ISL_3039342; EPI_ISL_3039343; EPI_ISL_3039344; EPI_ISL_3039345; EPI_ISL_3039346;' +
          ' EPI_ISL_3039347; EPI_ISL_3039348; EPI_ISL_3039349; EPI_ISL_3039350;';
      }
      let filename = 'exampleListAccessionIds.txt';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    loadAccIdsTarget(){
      let reader = new FileReader();
      let selectedFile = document.getElementById ('inputAccIdsTarget'). files[0];
      this.nameFileAccIdsTarget = selectedFile.name;
      let that = this;
      reader.onload = function() {
        let arrayIds = reader.result.replaceAll(" ", "").split(/(?:,|;|\t|\n| )+/);
        let arrayAllIds = [];
        console.log("quiqui", arrayIds);
        for(let i = 0; i < arrayIds.length; i = i + 1) {
          if (arrayIds[i] !== null && arrayIds[i] !== undefined) {
            let url = `/analyze/checkAccessionId`;
            let to_send = {'accession_id': arrayIds[i]}
            axios.post(url, to_send)
                .then((res) => {
                  return res.data;
                })
                .then((res) => {
                  if (res === true) {
                    arrayAllIds.push(arrayIds[i]);
                  }
                  if(i === arrayIds.length - 1){
                    that.fileAccIdsTarget = arrayAllIds;
                  }
                })
          }
        }
      }
      reader.readAsText(selectedFile);
    },
    deleteAccIdsTarget(){
      this.fileAccIdsTarget = null;
      this.nameFileAccIdsTarget = null;
      this.listAccIdsTargetFile = [];
    },
    loadAccIdsBackground(){
      let reader = new FileReader();
      let selectedFile = document.getElementById ('inputAccIdsBackground'). files[0];
      this.nameFileAccIdsBackground = selectedFile.name;
      let that = this;
      reader.onload = function() {
        let arrayIds = reader.result.replaceAll(" ", "").split(/(?:,|;|\t|\n| )+/);
        let arrayAllIds = [];
        for(let i = 0; i < arrayIds.length; i = i + 1) {
          if (arrayIds[i] !== null && arrayIds[i] !== undefined) {
            let url = `/analyze/checkAccessionId`;
            let to_send = {'accession_id': arrayIds[i]}
            axios.post(url, to_send)
                .then((res) => {
                  return res.data;
                })
                .then((res) => {
                  if (res === true) {
                    arrayAllIds.push(arrayIds[i]);
                  }
                  if (i === arrayIds.length - 1) {
                    that.fileAccIdsBackground = arrayAllIds;
                  }
                })
          }
        }
      }
      reader.readAsText(selectedFile);
    },
    deleteAccIdsBackground(){
      this.fileAccIdsBackground = null;
      this.nameFileAccIdsBackground = null;
      this.listAccIdsBackgroundFile = [];
    },
    loadDomainCSV(){
      this.fileDomainCSV = null;
      this.nameFileDomainCSV = null;
      this.selectedDomainForPValueUploaded = [];
      this.possibleDomainForPValueUploaded = [];
      let reader = new FileReader();
      let selectedFile = document.getElementById ('inputDomainCSVFree'). files[0];
      this.nameFileDomainCSV = selectedFile.name;
      let that = this;
      reader.onload = function() {
        let fileDomain = reader.result.replaceAll('"', '');
        let jsonTranslate = that.CSVToJson(fileDomain);
        localStorage.setItem('uploadedDomainsFree', jsonTranslate);
        localStorage.setItem('uploadedFileNameFree', that.nameFileDomainCSV);
        that.calculateUploadedDomains();
      }
      reader.readAsText(selectedFile);
    },
    CSVToJson(file){
      let lines= file.split("\r\n");
      let result = [];
      let headers = lines[0].split(",");

      for(let i=1;i<lines.length;i++){
          let obj = {};
          let currentline=lines[i].split(",");
          for(let j=0;j<headers.length;j++){
              if(headers[j] === 'Begin' || headers[j] === 'End'){
                obj[headers[j]] = parseInt(currentline[j]);
              }
              else{
                obj[headers[j]] = currentline[j];
              }
          }
          result.push(obj);
      }
      return JSON.stringify(result);
    },
    deleteDomainCSV(){
      this.fileDomainCSV = null;
      this.nameFileDomainCSV = null;
      this.selectedDomainForPValueUploaded = [];
      this.possibleDomainForPValueUploaded = [];
      localStorage.setItem('uploadedDomainsFree', JSON.stringify([]));
      localStorage.setItem('uploadedFileNameFree', null);
      this.calculateUploadedDomains();
    },
    calculateUploadedDomains() {
      let name = localStorage.getItem('uploadedFileNameFree');
      if( name === null || name === 'null'){
        this.fileDomainCSV = null;
        this.nameFileDomainCSV = null;
      }
      else{
        this.fileDomainCSV = JSON.parse(localStorage.getItem('uploadedDomainsFree'));
        this.nameFileDomainCSV = localStorage.getItem('uploadedFileNameFree');
        if(this.pValueBarChartApplied){
          this.calculatePossibleAndSelectedUploadedDomain();
        }
      }
    },
    calculatePossibleAndSelectedUploadedDomain(){
      let that = this;
      this.possibleDomainForPValueUploaded = this.fileDomainCSV.filter(function (dom){
        return dom['Protein'] === that.selectedProteinForPValue;
      })

      for(let i = 0; i < this.possibleDomainForPValueUploaded.length; i = i + 1){
         let single_domain = this.possibleDomainForPValueUploaded[i]['Description'] + ' / (' +
                             this.possibleDomainForPValueUploaded[i]['Begin'] + ' , ' +
                             this.possibleDomainForPValueUploaded[i]['End'] + ')';
         this.selectedDomainForPValueUploaded.push(single_domain);
      }
    },
    downloadExampleCSV(){
      let text = "";
      let result_sorted = [{'Protein': 'Spike (surface glycoprotein)', 'Description': 'Receptor-binding Domain (RBD)', 'Begin': 319, 'End': 541},
                           {'Protein': 'Spike (surface glycoprotein)', 'Description': 'Receptor-binding Motif (RBM)', 'Begin': 438, 'End': 506},
                           {'Protein': 'M (membrane glycoprotein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 222},
                           {'Protein': 'E (envelope protein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 75},
                           {'Protein': 'N (nucleocapsid phosphoprotein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 419},
                           {'Protein': 'ORF10 protein', 'Description': 'Whole protein', 'Begin': 1, 'End': 38},
                           {'Protein': "NSP16 (2'-O-ribose methyltransferase)", 'Description': 'Whole protein', 'Begin': 1, 'End': 298},
                           {'Protein': 'NSP3', 'Description': 'Whole protein', 'Begin': 1, 'End': 1945},
                           {'Protein': 'NSP4', 'Description': 'Whole protein', 'Begin': 1, 'End': 500},
                           {'Protein': 'NSP15 (endoRNAse)', 'Description': 'Whole protein', 'Begin': 1, 'End': 346},
                           {'Protein': 'NSP5 (3C-like proteinase)', 'Description': 'Whole protein', 'Begin': 1, 'End': 306},
                           {'Protein': "NSP14 (3'-to-5' exonuclease)", 'Description': 'Whole protein', 'Begin': 1, 'End': 527},
                           {'Protein': 'NSP11', 'Description': 'Whole protein', 'Begin': 1, 'End': 13},
                           {'Protein': 'NSP13 (helicase)', 'Description': 'Whole protein', 'Begin': 1, 'End': 601},
                           {'Protein': 'NSP6', 'Description': 'Whole protein', 'Begin': 1, 'End': 290},
                           {'Protein': 'NSP7', 'Description': 'Whole protein', 'Begin': 1, 'End': 84},
                           {'Protein': 'NSP8', 'Description': 'Whole protein', 'Begin': 1, 'End': 198},
                           {'Protein': 'NSP9', 'Description': 'Whole protein', 'Begin': 1, 'End': 113},
                           {'Protein': 'NSP12 (RNA-dependent RNA polymerase)', 'Description': 'Whole protein', 'Begin': 1, 'End': 932},
                           {'Protein': 'ORF1ab polyprotein', 'Description': 'Whole protein', 'Begin': 1, 'End': 7096},
                           {'Protein': 'NSP10', 'Description': 'Whole protein', 'Begin': 1, 'End': 138},
                           {'Protein': 'NSP1 (leader protein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 180},
                           {'Protein': 'ORF1a polyprotein', 'Description': 'Whole protein', 'Begin': 1, 'End': 4405},
                           {'Protein': 'NSP2', 'Description': 'Whole protein', 'Begin': 1, 'End': 638},
                           {'Protein': 'NS3 (ORF3a protein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 275},
                           {'Protein': 'NS6 (ORF6 protein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 61},
                           {'Protein': 'NS7a (ORF7a protein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 121},
                           {'Protein': 'NS7b (ORF7b)', 'Description': 'Whole protein', 'Begin': 1, 'End': 43},
                           {'Protein': 'NS8 (ORF8 protein)', 'Description': 'Whole protein', 'Begin': 1, 'End': 121},
      ];
      let headers = [{'text': 'Protein', 'value': 'Protein'},
                     {'text': 'Description', 'value': 'Description'},
                     {'text': 'Begin', 'value': 'Begin'},
                     {'text': 'End', 'value': 'End'}];
      text = this.json2csvDomains(result_sorted, headers);
      let filename = 'exampleDomain.csv';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    getFieldTextDomain(item){
      return `${item['Description']}` + ' / (' + `${item['Begin']}` + ' , ' + `${item['End']}` + ')';
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
      let filename = 'open_analysis_table_' + '(';
      if(this.listAccIdsTarget.length === 0) {
        if (this.queryFreeTarget['lineage']) {
          filename += this.queryFreeTarget['lineage'] + '_';
        }
        if (!this.queryFreeTarget['geo_group']) {
          filename += 'World';
        } else if (!this.queryFreeTarget['country']) {
          if(this.queryFreeTarget['geo_group'].length > 2){
            filename += this.queryFreeTarget['geo_group'][0] + '_etc';
          }
          else {
            filename += this.queryFreeTarget['geo_group'];
          }
        } else if (!this.queryFreeTarget['region']) {
          if(this.queryFreeTarget['country'].length > 2){
            filename += this.queryFreeTarget['country'][0] + '_etc';
          }
          else{
            filename += this.queryFreeTarget['country'];
          }
        } else if (!this.queryFreeTarget['province']) {
          if(this.queryFreeTarget['region'].length > 2){
            filename += this.queryFreeTarget['region'][0] + '_etc';
          }
          else{
            filename += this.queryFreeTarget['region'];
          }
        } else {
          if(this.queryFreeTarget['province'].length > 2){
            filename += this.queryFreeTarget['province'][0] + '_etc';
          }
          else{
            filename += this.queryFreeTarget['province'];
          }
        }
        filename += '_' + this.startDateQueryFreeTarget + '_' + this.stopDateQueryFreeTarget;
      }
      else{
        if(this.listAccIdsTargetFile.length > 0) {
          filename += this.nameFileAccIdsTarget.split('.txt')[0];
        }
        if(this.listAccIdsTargetInserted.length > 0){
          if(this.listAccIdsTargetFile.length > 0) {
            filename += '_';
          }
          filename += 'userSelectedIds';
        }
      }
      filename += ')' + '_vs_(';
      if(this.listAccIdsBackground.length === 0) {
        if (this.queryFreeBackground['lineage']) {
          filename += this.queryFreeBackground['lineage'] + '_';
        }
        if (!this.queryFreeBackground['geo_group']) {
          filename += 'World';
        } else if (!this.queryFreeBackground['country']) {
          if(this.queryFreeBackground['geo_group'].length > 2){
            filename += this.queryFreeBackground['geo_group'][0] + '_etc';
          }
          else{
            filename += this.queryFreeBackground['geo_group'];
          }
        } else if (!this.queryFreeBackground['region']) {
          if(this.queryFreeBackground['country'].length > 2){
            filename += this.queryFreeBackground['country'][0] + '_etc';
          }
          else{
            filename += this.queryFreeBackground['country'];
          }
        } else if (!this.queryFreeBackground['province']) {
          if(this.queryFreeBackground['region'].length > 2){
            filename += this.queryFreeBackground['region'][0] + '_etc';
          }
          else{
            filename += this.queryFreeBackground['region'];
          }
        } else {
          if(this.queryFreeBackground['province'].length > 2){
            filename += this.queryFreeBackground['province'][0] + '_etc';
          }
          else{
            filename += this.queryFreeBackground['province'];
          }
        }
        filename += '_' + this.startDateQueryFreeBackground + '_' + this.stopDateQueryFreeBackground;
      }
      else{
        if(this.listAccIdsBackgroundFile.length > 0) {
          filename += this.nameFileAccIdsBackground.split('.txt')[0];
        }
        if(this.listAccIdsBackgroundInserted.length > 0){
          if(this.listAccIdsBackgroundFile.length > 0) {
            filename += '_';
          }
          filename += 'userSelectedIds';
        }
      }
      filename += ')';
      filename += '.csv';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    json2csvDomains(input, selected_headers) {
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
                  string_val = row['mutation'];
                  if(typeof string_val === 'string' || string_val instanceof String) {
                    string_val = string_val.replaceAll("\n", " ");
                  }
                }
                else {
                  string_val = row[fieldName];
                  if(typeof string_val === 'string' || string_val instanceof String) {
                    string_val = string_val.replaceAll("\n", " ");
                  }
                }
                return string_val;
            }).join(',')
        });
        csv.unshift(fields.join(','));
        return csv.join('\r\n')
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
            if(queryFree['lineage']) {
              this.importantMutation = res;
            }
            else{
              this.importantMutation = {'mutation': [], 'additional_mutation': []};
            }
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
      this.selectedDomainForPValueMutagenesis = [];
      this.selectedDomainForPValueAaModifications = [];
      this.selectedDomainForPValueUploaded = [];
      this.possibleDomainForPValueUploaded = [];
      this.selectedAllAaModifications = false;
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
                    a['disabled'] = true;
                    b['disabled'] = true;
                    let value_a = a['Description'].toLowerCase();
                    let value_b = b['Description'].toLowerCase();
                    return value_a > value_b ? 1 : -1;
                  })

                  if(this.fileDomainCSV !== null) {
                    let that = this;
                    this.possibleDomainForPValueUploaded = this.fileDomainCSV.filter(function (dom) {
                      return dom['Protein'] === that.selectedProteinForPValue;
                    })

                    for (let i = 0; i < this.possibleDomainForPValueUploaded.length; i = i + 1) {
                      let single_domain = this.possibleDomainForPValueUploaded[i]['Description'] + ' / (' +
                          this.possibleDomainForPValueUploaded[i]['Begin'] + ' , ' +
                          this.possibleDomainForPValueUploaded[i]['End'] + ')';
                      this.selectedDomainForPValueUploaded.push(single_domain);
                    }
                  }

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
        this.accessionIdsTargetOrBackground = type;
        this.accessionIdsSingleMutation = '(' + item['product'] + '_' + item['sequence_aa_original'] + item['start_aa_original'] + item['sequence_aa_alternative'] + ')';
        query['lineage'] = item['lineage_target'];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        if(this.startDateQueryFreeTarget !== null) {
          query['minDateBackground'] = this.startDateQueryFreeTarget;
        }
        if(this.stopDateQueryFreeTarget !== null) {
          query['maxDateBackground'] = this.stopDateQueryFreeTarget;
        }
        if(this.selectRemoveOverlapping === 'Both' || this.selectRemoveOverlapping === 'Target') {
          query_target = JSON.parse(JSON.stringify(this.queryFreeBackground));
        }
        query['product'] = item['product'];
      }
      else if(type === 'background'){
        this.accessionIdsTargetOrBackground = type;
        this.accessionIdsSingleMutation = '(' + item['product'] + '_' + item['sequence_aa_original'] + item['start_aa_original'] + item['sequence_aa_alternative'] + ')';
        query['lineage'] = item['lineage_background'];
        query['start_aa_original'] = item['start_aa_original'];
        query['sequence_aa_original'] = item['sequence_aa_original'];
        query['sequence_aa_alternative'] = item['sequence_aa_alternative'];
        if(this.startDateQueryFreeBackground !== null) {
          query['minDateBackground'] = this.startDateQueryFreeBackground;
        }
        if(this.stopDateQueryFreeBackground !== null) {
          query['maxDateBackground'] = this.stopDateQueryFreeBackground;
        }
        query['product'] = item['product'];
        if(this.selectRemoveOverlapping === 'Both' || this.selectRemoveOverlapping === 'Background') {
          query_target = JSON.parse(JSON.stringify(this.queryFreeTarget));
        }
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
      let filename = 'open_analysis_' + this.accessionIdsSingleMutation + '_';
      if(this.accessionIdsTargetOrBackground === 'target') {
        if(this.listAccIdsTarget.length === 0) {
          if (this.queryFreeTarget['lineage']) {
            filename += this.queryFreeTarget['lineage'] + '_';
          }
          if (!this.queryFreeTarget['geo_group']) {
            filename += 'World';
          } else if (!this.queryFreeTarget['country']) {
            if(this.queryFreeTarget['geo_group'].length > 2){
              filename += this.queryFreeTarget['geo_group'][0] + '_etc';
            }
            else{
              filename += this.queryFreeTarget['geo_group'];
            }
          } else if (!this.queryFreeTarget['region']) {
            if(this.queryFreeTarget['country'].length > 2){
              filename += this.queryFreeTarget['country'][0] + '_etc';
            }
            else{
              filename += this.queryFreeTarget['country'];
            }
          } else if (!this.queryFreeTarget['province']) {
            if(this.queryFreeTarget['region'].length > 2){
              filename += this.queryFreeTarget['region'][0] + '_etc';
            }
            else{
              filename += this.queryFreeTarget['region'];
            }
          } else {
            if(this.queryFreeTarget['province'].length > 2){
              filename += this.queryFreeTarget['province'][0] + '_etc';
            }
            else{
              filename += this.queryFreeTarget['province'];
            }
          }
          filename += '_' + this.startDateQueryFreeTarget + '_' + this.stopDateQueryFreeTarget;
        }
        else{
          if(this.listAccIdsTargetFile.length > 0) {
            filename += this.nameFileAccIdsTarget.split('.txt')[0];
          }
          if(this.listAccIdsTargetInserted.length > 0){
            if(this.listAccIdsTargetFile.length > 0) {
              filename += '_';
            }
            filename += 'userSelectedIds';
          }
        }
      }
      else {
        if(this.listAccIdsBackground.length === 0) {
          if (this.queryFreeBackground['lineage']) {
            filename += this.queryFreeBackground['lineage'] + '_';
          }
          if (!this.queryFreeBackground['geo_group']) {
            filename += 'World';
          } else if (!this.queryFreeBackground['country']) {
            if(this.queryFreeBackground['geo_group'].length > 2){
              filename += this.queryFreeBackground['geo_group'][0] + '_etc';
            }
            else{
              filename += this.queryFreeBackground['geo_group'];
            }
          } else if (!this.queryFreeBackground['region']) {
            if(this.queryFreeBackground['country'].length > 2){
              filename += this.queryFreeBackground['country'][0] + '_etc';
            }
            else{
              filename += this.queryFreeBackground['country'];
            }
          } else if (!this.queryFreeBackground['province']) {
            if(this.queryFreeBackground['region'].length > 2){
              filename += this.queryFreeBackground['region'][0] + '_etc';
            }
            else{
              filename += this.queryFreeBackground['region'];
            }
          } else {
            if(this.queryFreeBackground['province'].length > 2){
              filename += this.queryFreeBackground['province'][0] + '_etc';
            }
            else{
              filename += this.queryFreeBackground['province'];
            }
          }
          filename += '_' + this.startDateQueryFreeBackground + '_' + this.stopDateQueryFreeBackground;
        }
        else{
          if(this.listAccIdsBackgroundFile.length > 0) {
            filename += this.nameFileAccIdsBackground.split('.txt')[0];
          }
          if(this.listAccIdsBackgroundInserted.length > 0){
            if(this.listAccIdsBackgroundFile.length > 0) {
              filename += '_';
            }
            filename += 'userSelectedIds';
          }
        }
      }
      filename += '.txt'
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

      if(Object.keys(query_target).length > 1 && Object.keys(query_background).length > 1) {

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
    },
    checkErrorNumSeqFreeQuery(){
      this.errorNumSeqFreeQuery = (
          (this.selectedTabTargetFreeQuery === 0 && this.numSequencesQueryFreeTarget < this.min_num_seq_target)
          ||
          (this.selectedTabTargetFreeQuery === 1 && this.numSequencesQueryFreeTarget < this.min_num_seq_target_acc_ids)
          ||
          (this.selectedTabBackgroundFreeQuery === 0 && this.numSequencesQueryFreeBackground < this.min_num_seq_background)
          ||
          (this.selectedTabBackgroundFreeQuery === 1 && this.numSequencesQueryFreeBackground < this.min_num_seq_background_acc_ids)
          ||
          (this.selectRemoveOverlapping === 'Target'
              &&
              (
                  (this.selectedTabTargetFreeQuery === 0 && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
                  ||
                  (this.selectedTabTargetFreeQuery === 1 && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target_acc_ids)
              )
          )
          ||
          (this.selectRemoveOverlapping === 'Background'
              &&
              (
                  (this.selectedTabBackgroundFreeQuery === 0 && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
                  ||
                  (this.selectedTabBackgroundFreeQuery === 1 && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background_acc_ids)
              )
          )
          ||
          (this.selectRemoveOverlapping === 'Both' && (
              (this.selectedTabTargetFreeQuery === 0 && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target)
              ||
              (this.selectedTabTargetFreeQuery === 1 && this.numSequencesQueryFreeTarget - this.num_overlapping_sequences < this.min_num_seq_target_acc_ids)
              ||
              (this.selectedTabBackgroundFreeQuery === 0 && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background)
              ||
              (this.selectedTabBackgroundFreeQuery === 1 && this.numSequencesQueryFreeBackground - this.num_overlapping_sequences < this.min_num_seq_background_acc_ids)
              )
          )
      );
    }
  },
  watch:{
    selectedTabTargetFreeQuery(){
      if(this.selectedTabTargetFreeQuery === 1){
        let id1 = 'tabTargetFree2';
        let id2 = 'tabTargetFree1';
        let elem1 = document.getElementById(id1);
        elem1.style['color'] = 'white';
        elem1.style['font-weight'] = 'bold';
        let elem2 = document.getElementById(id2);
        elem2.style['color'] = '#FFFFFF80';
        elem2.style['font-weight'] = 'normal';
        this.setQueryFreeTarget({field: 'accession_id', list: null});
        this.setQueryFreeTarget({field: 'lineage', list: null});
        this.setQueryFreeTarget({field: 'geo_group', list: null});
        this.setQueryFreeTarget({field: 'country', list: null});
        this.setQueryFreeTarget({field: 'region', list: null});
        this.setQueryFreeTarget({field: 'province', list: null});
        this.setStartDateQueryFreeTarget(null);
        this.setStopDateQueryFreeTarget(null);
        // this.setQueryFreeBackground({field: 'accession_id', list: this.listAccIdsTarget});
        this.setNumSequencesQueryFreeTarget(0);
      }
      else{
        let id1 = 'tabTargetFree2';
        let id2 = 'tabTargetFree1';
        let elem1 = document.getElementById(id1);
        elem1.style['color'] = '#FFFFFF80';
        elem1.style['font-weight'] = 'normal';
        let elem2 = document.getElementById(id2);
        elem2.style['color'] = 'white';
        elem2.style['font-weight'] = 'bold';
        this.listAccIdsTarget = [];
        this.listAccIdsTargetInserted = [];
        this.nameFileAccIdsTarget = null;
        this.fileAccIdsTarget = null;
        this.setQueryFreeTarget({field: 'accession_id', list: null});
      }
    },
    selectedTabBackgroundFreeQuery(){
      if(this.selectedTabBackgroundFreeQuery === 1){
        let id1 = 'tabBackgroundFree2';
        let id2 = 'tabBackgroundFree1';
        let elem1 = document.getElementById(id1);
        elem1.style['color'] = 'white';
        elem1.style['font-weight'] = 'bold';
        let elem2 = document.getElementById(id2);
        elem2.style['color'] = '#FFFFFF80';
        elem2.style['font-weight'] = 'normal';
        this.setQueryFreeBackground({field: 'accession_id', list: null});
        this.setQueryFreeBackground({field: 'lineage', list: null});
        this.setQueryFreeBackground({field: 'geo_group', list: null});
        this.setQueryFreeBackground({field: 'country', list: null});
        this.setQueryFreeBackground({field: 'region', list: null});
        this.setQueryFreeBackground({field: 'province', list: null});
        this.setStartDateQueryFreeBackground(null);
        this.setStopDateQueryFreeBackground(null);
        this.setNumSequencesQueryFreeBackground(0);
      }
      else{
        let id1 = 'tabBackgroundFree2';
        let id2 = 'tabBackgroundFree1';
        let elem1 = document.getElementById(id1);
        elem1.style['color'] = '#FFFFFF80';
        elem1.style['font-weight'] = 'normal';
        let elem2 = document.getElementById(id2);
        elem2.style['color'] = 'white';
        elem2.style['font-weight'] = 'bold';
        this.listAccIdsBackground = [];
        this.listAccIdsBackgroundInserted = [];
        this.nameFileAccIdsBackground = null;
        this.fileAccIdsBackground = null;
        this.setQueryFreeBackground({field: 'accession_id', list: null});
      }
    },
    listAccIdsTargetInserted(){
      this.listAccIdsTarget = [];
      let arrayFull = [];
      this.setQueryFreeTarget({field: 'accession_id', list: null});
      this.setQueryFreeTarget({field: 'lineage', list: null});
      this.setQueryFreeTarget({field: 'geo_group', list: null});
      this.setQueryFreeTarget({field: 'country', list: null});
      this.setQueryFreeTarget({field: 'region', list: null});
      this.setQueryFreeTarget({field: 'province', list: null});
      this.setStartDateQueryFreeTarget(null);
      this.setStopDateQueryFreeTarget(null);
      if(this.listAccIdsTargetFile.length > 0){
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsTargetFile));
        for(let i = 0; i < this.listAccIdsTargetInserted.length; i = i + 1){
          if(!arrayFull.includes(this.listAccIdsTargetInserted[i])){
            arrayFull.push(this.listAccIdsTargetInserted[i]);
          }
        }
      }
      else{
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsTargetInserted));
      }
      this.listAccIdsTarget = arrayFull;
      if(arrayFull.length === 0){
        this.setQueryFreeTarget({field: 'accession_id', list: null});
      }
      else{
        this.setQueryFreeTarget({field: 'accession_id', list: arrayFull});
      }
      this.setNumSequencesQueryFreeTarget(arrayFull.length);
      this.checkErrorNumSeqFreeQuery();
    },
    listAccIdsBackgroundInserted(){
      this.listAccIdsBackground = [];
      let arrayFull = [];
      this.setQueryFreeBackground({field: 'accession_id', list: null});
      this.setQueryFreeBackground({field: 'lineage', list: null});
      this.setQueryFreeBackground({field: 'geo_group', list: null});
      this.setQueryFreeBackground({field: 'country', list: null});
      this.setQueryFreeBackground({field: 'region', list: null});
      this.setQueryFreeBackground({field: 'province', list: null});
      this.setStartDateQueryFreeBackground(null);
      this.setStopDateQueryFreeBackground(null);
      if(this.listAccIdsBackgroundFile.length > 0){
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsBackgroundFile));
        for(let i = 0; i < this.listAccIdsBackgroundInserted.length; i = i + 1){
          if(!arrayFull.includes(this.listAccIdsBackgroundInserted[i])){
            arrayFull.push(this.listAccIdsBackgroundInserted[i]);
          }
        }
      }
      else{
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsBackgroundInserted));
      }
      this.listAccIdsBackground = arrayFull;
      if(arrayFull.length === 0){
        this.setQueryFreeBackground({field: 'accession_id', list: null});
      }
      else{
        this.setQueryFreeBackground({field: 'accession_id', list: arrayFull});
      }
      this.setNumSequencesQueryFreeBackground(arrayFull.length);
      this.checkErrorNumSeqFreeQuery();
    },
    fileAccIdsTarget(){
      this.listAccIdsTarget = [];
      this.listAccIdsTargetFile = [];
      this.setQueryFreeTarget({field: 'accession_id', list: null});
      this.setQueryFreeTarget({field: 'lineage', list: null});
      this.setQueryFreeTarget({field: 'geo_group', list: null});
      this.setQueryFreeTarget({field: 'country', list: null});
      this.setQueryFreeTarget({field: 'region', list: null});
      this.setQueryFreeTarget({field: 'province', list: null});
      this.setStartDateQueryFreeTarget(null);
      this.setStopDateQueryFreeTarget(null);
      if(this.fileAccIdsTarget !== null) {
        this.listAccIdsTargetFile = this.fileAccIdsTarget;
        for(let i = 0; i < this.listAccIdsTargetFile.length; i = i + 1){
          if(this.listAccIdsTargetFile[i] === ''){
            this.listAccIdsTargetFile.splice(i, 1);
          }
        }
      }
      let arrayFull = [];
      if(this.listAccIdsTargetInserted.length > 0){
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsTargetFile));
        for(let i = 0; i < this.listAccIdsTargetInserted.length; i = i + 1){
          if(!arrayFull.includes(this.listAccIdsTargetInserted[i])){
            arrayFull.push(this.listAccIdsTargetInserted[i]);
          }
        }
      }
      else{
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsTargetFile));
      }
      this.listAccIdsTarget = arrayFull;
      if(arrayFull.length === 0){
        this.setQueryFreeTarget({field: 'accession_id', list: null});
      }
      else{
        this.setQueryFreeTarget({field: 'accession_id', list: arrayFull});
      }
      this.setNumSequencesQueryFreeTarget(arrayFull.length);
      this.checkErrorNumSeqFreeQuery();
    },
    fileAccIdsBackground(){
      this.listAccIdsBackground = [];
      this.listAccIdsBackgroundFile = [];
      this.setQueryFreeBackground({field: 'accession_id', list: null});
      this.setQueryFreeBackground({field: 'lineage', list: null});
      this.setQueryFreeBackground({field: 'geo_group', list: null});
      this.setQueryFreeBackground({field: 'country', list: null});
      this.setQueryFreeBackground({field: 'region', list: null});
      this.setQueryFreeBackground({field: 'province', list: null});
      this.setStartDateQueryFreeBackground(null);
      this.setStopDateQueryFreeBackground(null);
      if(this.fileAccIdsBackground !== null){
        this.listAccIdsBackgroundFile = this.fileAccIdsBackground;
        for(let i = 0; i < this.listAccIdsBackgroundFile.length; i = i + 1){
          if(this.listAccIdsBackgroundFile[i] === ''){
            this.listAccIdsBackgroundFile.splice(i, 1);
          }
        }
      }
      let arrayFull = [];
      if(this.listAccIdsBackgroundInserted.length > 0){
        arrayFull = JSON.parse(JSON.stringify(this.listAccIdsBackgroundFile));
        for(let i = 0; i < this.listAccIdsBackgroundInserted.length; i = i + 1){
          if(!arrayFull.includes(this.listAccIdsBackgroundInserted[i])){
            arrayFull.push(this.listAccIdsBackgroundInserted[i]);
          }
        }
      }
      else{
        JSON.parse(JSON.stringify(arrayFull = this.listAccIdsBackgroundFile));
      }
      this.listAccIdsBackground = arrayFull;
      if(arrayFull.length === 0){
        this.setQueryFreeBackground({field: 'accession_id', list: null});
      }
      else{
        this.setQueryFreeBackground({field: 'accession_id', list: arrayFull});
      }
      this.setNumSequencesQueryFreeBackground(arrayFull.length);
      this.checkErrorNumSeqFreeQuery();
    },
    selectedAllAaModifications(){
      this.selectedDomainForPValueAaModifications = [];
      if(this.selectedAllAaModifications){
        for(let i = 0; i < this.possibleDomainForPValueAaModifications.length; i = i + 1){
          let selected = this.possibleDomainForPValueAaModifications[i]['Description']  + ' / (' +
                         this.possibleDomainForPValueAaModifications[i]['Begin'] + ' , ' +
                         this.possibleDomainForPValueAaModifications[i]['End'] + ')';
          this.selectedDomainForPValueAaModifications.push(selected);
        }
      }
    },
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
    selectedMinPercentageMutationPValue(){
      this.pValueBarChartApplied = false;
    },
    selectedMaxPercentageMutationPValue(){
      this.pValueBarChartApplied = false;
    },
    selectRemoveOverlapping(){
      this.resetApplied();
      this.checkErrorNumSeqFreeQuery();
    },
    selectedTabFreeQuery(){
      this.boldTabs();
      if(this.selectedTabFreeQuery === 0 && this.selectedTabTargetFreeQuery === 0){
        let delayInMilliseconds = 500;
        setTimeout(function() {
          let id1 = 'tabTargetFree1';
          let id2 = 'tabTargetFree2';
          let elem1 = document.getElementById(id1);
          elem1.style['color'] = 'white';
          elem1.style['font-weight'] = 'bold';
          let elem2 = document.getElementById(id2);
          elem2.style['color'] = '#FFFFFF80';
          elem2.style['font-weight'] = 'normal';
        }, delayInMilliseconds);
      }
      else if(this.selectedTabFreeQuery === 1 && this.selectedTabBackgroundFreeQuery === 0){
        let delayInMilliseconds = 500;
        setTimeout(function() {
          let id3 = 'tabBackgroundFree1';
          let id4 = 'tabBackgroundFree2';
          let elem3 = document.getElementById(id3);
          elem3.style['color'] = 'white';
          elem3.style['font-weight'] = 'bold';
          let elem4 = document.getElementById(id4);
          elem4.style['color'] = '#FFFFFF80';
          elem4.style['font-weight'] = 'normal';
        }, delayInMilliseconds);
      }
    },
    'queryFreeTarget.geo_group': function (){
      if(!this.queryFreeTarget['geo_group'] || this.queryFreeTarget['geo_group'].length === 0) {
        this.setQueryFreeTarget({field: 'country', list: []});
        this.setQueryFreeTarget({field: 'region', list: []});
        this.setQueryFreeTarget({field: 'province', list: []});
      }
    },
    'queryFreeTarget.country': function (){
      if(!this.queryFreeTarget['country'] || this.queryFreeTarget['country'].length === 0) {
        this.setQueryFreeTarget({field: 'region', list: []});
        this.setQueryFreeTarget({field: 'province', list: []});
      }
    },
    'queryFreeTarget.region': function (){
      if(!this.queryFreeTarget['region'] || this.queryFreeTarget['region'].length === 0) {
        this.setQueryFreeTarget({field: 'province', list: []});
      }
    },
    'queryFreeBackground.geo_group': function (){
      if(!this.queryFreeBackground['geo_group'] || this.queryFreeBackground['geo_group'].length === 0) {
        this.setQueryFreeBackground({field: 'country', list: []});
        this.setQueryFreeBackground({field: 'region', list: []});
        this.setQueryFreeBackground({field: 'province', list: []});
      }
    },
    'queryFreeBackground.country': function (){
      if(!this.queryFreeBackground['country'] || this.queryFreeBackground['country'].length === 0) {
        this.setQueryFreeBackground({field: 'region', list: []});
        this.setQueryFreeBackground({field: 'province', list: []});
      }
    },
    'queryFreeBackground.region': function (){
      if(!this.queryFreeBackground['region'] || this.queryFreeBackground['region'].length === 0) {
        this.setQueryFreeBackground({field: 'province', list: []});
      }
    },
    numSequencesQueryFreeTarget(){
      this.checkErrorNumSeqFreeQuery();
    },
    numSequencesQueryFreeBackground(){
      this.checkErrorNumSeqFreeQuery();
    },
    num_overlapping_sequences(){
      this.checkErrorNumSeqFreeQuery();
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
    let id1 = 'tabTargetFree1';
    let id2 = 'tabTargetFree2';
    let elem1 = document.getElementById(id1);
    elem1.style['color'] = 'white';
    elem1.style['font-weight'] = 'bold';
    let elem2 = document.getElementById(id2);
    elem2.style['color'] = '#FFFFFF80';
    elem2.style['font-weight'] = 'normal';

    this.calculateUploadedDomains();
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