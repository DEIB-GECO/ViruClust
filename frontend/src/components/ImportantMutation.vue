<template>
  <div>
    <span>Check <a @click="dialogImportantMutation = true">here</a> the important changes.</span>

      <v-dialog
      persistent
      v-model="dialogImportantMutation"
      width="800"
      >
        <v-card>
          <v-card-title class="headline" style="background-color: #A8DADC;">
            Important Changes Of Target Lineage
            <v-spacer></v-spacer>
            <v-btn
                style="background-color: rgb(122, 139, 157)"
                slot="activator"
                icon
                small
              color="white"
              @click="dialogImportantMutation = !dialogImportantMutation"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text style="padding: 50px">
            <v-layout row wrap justify-space-around>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 20px; margin-bottom: 10px">
                <h3> Legend: </h3>
              </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 50px">
                <span>
                  <v-icon
                    text icon
                    slot="activator"
                    color="green"
                    class="white--text info-button-green" >mdi-circle</v-icon>
                  All targets have the related change<br>
                  <v-icon
                    text icon
                    slot="activator"
                    color="orange"
                    class="white--text info-button-green" >mdi-circle</v-icon>
                  Only some of the targets have the related change (click to see which ones)<br>
                  <v-icon
                    text icon
                    slot="activator"
                    color='red'
                    class="white--text info-button-green" >mdi-circle</v-icon>
                  None of the targets have the related change<br>
                </span>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                <v-layout row wrap justify-space-around v-if="importantMutationECDC['mutation'].length > 0 || importantMutationECDC['additional_mutation'].length > 0">
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 20px; margin-bottom: 50px">
                      <h2>ECDC changes (Spike): </h2>
                    </v-flex>
                   <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center; " v-for="(category, key, index) in importantMutationECDC" v-bind:key="index">
                      <v-card width="100%" color="#F1FAEE">
                        <v-card-title class="justify-center">
                          <span v-if="key.toLowerCase() === 'mutation'" style="padding: 5px; background-color: red; color: white">
                            CORE CHANGES
                          </span>
                          <span v-else-if="key.toLowerCase() === 'additional_mutation'" style="padding: 5px; background-color: orange; color: white">
                            ADDITIONAL CHANGES
                          </span>
                        </v-card-title>
                        <v-card-text style="text-align: center;">
                          <span v-for="mutation in category" v-bind:key="mutation">
                            <span>{{mutation}}</span>
                            <span v-if="checkAllMutations[mutation] === totalTargets" style=" display:inline; margin-left: 5px;">
                                  <v-icon
                                      text icon
                                      slot="activator"
                                      color="green"
                                      class="white--text info-button-green" >mdi-circle</v-icon>
                            </span>
                            <span v-else-if="checkAllMutations[mutation] === 0" style="display:inline; margin-left: 5px">
                                  <v-icon
                                      text icon
                                      slot="activator"
                                      color="red"
                                      class="white--text info-button-green" >mdi-circle</v-icon>
                            </span>
                            <span v-else style="display:inline; margin-left: 5px">
                                <v-dialog width="500">
                                  <template v-slot:activator="{ on }">
                                    <v-btn
                                          v-on="on"
                                          small
                                          text icon
                                          slot="activator"
                                          color="orange"
                                          class="white--text info-button"
                                          >
                                      <v-icon >mdi-circle</v-icon>
                                     </v-btn>
                                  </template>
                                  <v-card width="500" >
                                    <v-card-title  class="headline" style="background-color: #A8DADC ; color: white">TARGET WITH THE CHANGE: </v-card-title>
                                    <v-card-text style="margin-top: 30px; text-align: center">
                                      <span v-for="target in checkTargetsForAllMutations[mutation]" v-bind:key="target">
                                         {{target}} <br><br>
                                      </span>
                                    </v-card-text>
                                  </v-card>
                              </v-dialog>
                            </span>
                            <br>
                          </span>
                        </v-card-text>
                      </v-card>
                   </v-flex>
                </v-layout>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                <v-layout row wrap justify-space-around v-if="importantMutation75Percentage['mutation'].length > 0 || importantMutation75Percentage['additional_mutation'].length > 0">
                  <v-flex class="no-horizontal-padding xs12 d-flex" v-if="importantMutationECDC['mutation'].length > 0 || importantMutationECDC['additional_mutation'].length > 0" style="justify-content: center; margin-top: 100px;">
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; text-align: center; margin-bottom: 50px">
                    <h2 v-if="rowsTable[0][0] && rowsTable[0][0]['lineage'] === 'empty'"> All lineages characteristic changes (present in 75% of sequences): </h2>
                    <h2 v-else-if="rowsTable[0][0]"> Lineage {{rowsTable[0][0]['lineage']}} characteristic changes (present in 75% of lineage sequences): </h2>
                    <h2 v-else>Changes present in 75% of sequences of the selected lineages: </h2>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                    <v-layout row wrap justify-space-around>
                       <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center; ">
                          <v-card width="100%" color="#F1FAEE">
                            <v-card-title class="justify-center">
                              <span style="padding: 5px; background-color: red; color: white">CHANGES</span>
                            </v-card-title>
                            <v-card-text style="text-align: center;">
                              <span v-for="mutation in importantMutation75Percentage['mutation']" v-bind:key="mutation">
                                <span>{{mutation}}</span>
                                <span v-if="checkAllMutations[mutation] === totalTargets" style=" display:inline; margin-left: 5px;">
                                      <v-icon
                                          text icon
                                          slot="activator"
                                          color="green"
                                          class="white--text info-button-green" >mdi-circle</v-icon>
                                </span>
                                <span v-else-if="checkAllMutations[mutation] === 0" style="display:inline; margin-left: 5px">
                                      <v-icon
                                          text icon
                                          slot="activator"
                                          color="red"
                                          class="white--text info-button-green" >mdi-circle</v-icon>
                                </span>
                                <span v-else style="display:inline; margin-left: 5px">
                                    <v-dialog width="500">
                                      <template v-slot:activator="{ on }">
                                        <v-btn
                                              v-on="on"
                                              small
                                              text icon
                                              slot="activator"
                                              color="orange"
                                              class="white--text info-button"
                                              >
                                          <v-icon >mdi-circle</v-icon>
                                         </v-btn>
                                      </template>
                                      <v-card width="500" >
                                        <v-card-title  class="headline" style="background-color: #A8DADC ; color: white">TARGET WITH THE CHANGE: </v-card-title>
                                        <v-card-text style="margin-top: 30px; text-align: center">
                                          <span v-for="target in checkTargetsForAllMutations[mutation]" v-bind:key="target">
                                             {{target}} <br><br>
                                          </span>
                                        </v-card-text>
                                      </v-card>
                                  </v-dialog>
                                </span>
                                <br>
                              </span>
                            </v-card-text>
                          </v-card>
                       </v-flex>
                    </v-layout>
                   </v-flex>
                </v-layout>
               </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-dialog>
  </div>
</template>

<script>
export default {
  name: "ImportantMutation",
  props: {
    importantMutationECDC: {required: true,},
    importantMutation75Percentage: {required: true,},
    rowsTable: {required: true,},
  },
  methods: {
    analyzeMissingMutations(){
      this.totalTargets = this.rowsTable.length;
      this.checkAllMutations = {};
      this.checkTargetsForAllMutations = {};

      for(let k = 0; k < 4; k = k + 1) {

        let all_mutations;
        if(k === 0){
          all_mutations = this.importantMutationECDC['mutation'];
        }
        else if(k === 1){
          all_mutations = this.importantMutationECDC['additional_mutation'];
        }
        else if(k === 2){
          all_mutations = this.importantMutation75Percentage['mutation'];
        }
        else if(k === 3){
          all_mutations = this.importantMutation75Percentage['additional_mutation'];
        }

        for (let j = 0; j < all_mutations.length; j = j + 1) {
          for (let i = 0; i < this.totalTargets; i = i + 1) {
            let mutation = all_mutations[j];
            let index = this.rowsTable[i].findIndex(function (item) {
              return item['mutation'] === all_mutations[j];
            });
            if (index !== -1) {
              if (this.checkAllMutations[mutation]) {
                if(!this.checkTargetsForAllMutations[mutation].includes(this.rowsTable[i][index]['target'])) {
                  this.checkAllMutations[mutation] = this.checkAllMutations[mutation] + 1;
                  this.checkTargetsForAllMutations[mutation].push(this.rowsTable[i][index]['target']);
                }
              } else {
                this.checkAllMutations[mutation] = 1;
                this.checkTargetsForAllMutations[mutation] = [];
                this.checkTargetsForAllMutations[mutation].push(this.rowsTable[i][index]['target']);
              }
            } else {
              if (!this.checkAllMutations[mutation]) {
                this.checkAllMutations[mutation] = 0;
                if(!this.checkTargetsForAllMutations[mutation]) {
                  this.checkTargetsForAllMutations[mutation] = [];
                }
              }
            }
          }
        }
      }
    }
  },
  data() {
    return {
      dialogImportantMutation: false,
      totalTargets: 0,
      checkAllMutations: {},
      checkTargetsForAllMutations: {},
    }
  },
  mounted() {
    this.analyzeMissingMutations();
  },
  watch: {
    rowsTable(){
      this.analyzeMissingMutations();
    },
    importantMutationECDC(){
      this.analyzeMissingMutations();
    },
    importantMutation75Percentage(){
      this.analyzeMissingMutations();
    },
  }
}
</script>

<style scoped>

</style>