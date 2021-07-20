<template>
  <div>
    <v-btn @click="dialogImportantMutation = true"
           class="white--text"
           color="blue">
      Important Mutation</v-btn>

      <v-dialog
      persistent
      v-model="dialogImportantMutation"
      width="800"
      >
        <v-card>
          <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
            Important Mutation
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
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 20px; margin-bottom: 50px">
                <h2>ECDC mutations (Spike): </h2>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                <v-layout row wrap justify-space-around>
                   <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center; " v-for="(category, key, index) in importantMutationECDC" v-bind:key="index">
                      <v-card width="100%" color="#F0E68C">
                        <v-card-title class="justify-center">
                          <span v-if="key.toLowerCase() === 'mutation'" style="padding: 5px; background-color: red; color: white">
                            CORE MUTATIONS
                          </span>
                          <span v-else-if="key.toLowerCase() === 'additional_mutation'" style="padding: 5px; background-color: orange; color: white">
                            ADDITIONAL MUTATIONS
                          </span>
                        </v-card-title>
                        <v-card-text style="text-align: center;">
                          <span v-for="mutation in category" v-bind:key="mutation">
                            <span>{{mutation}}</span><br>
                          </span>
                        </v-card-text>
                      </v-card>
                   </v-flex>
                </v-layout>
               </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 100px; margin-bottom: 50px">
                <h2>Mutations present in 75% of sequences of the selected lineages: </h2>
              </v-flex>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                <v-layout row wrap justify-space-around>
                   <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center; ">
                      <v-card width="100%" color="#F0E68C">
                        <v-card-title class="justify-center">
                          <span style="padding: 5px; background-color: red; color: white">MUTATIONS</span>
                        </v-card-title>
                        <v-card-text style="text-align: center;">
                          <span v-for="mutation in importantMutation75Percentage['mutation']" v-bind:key="mutation">
                            <span>{{mutation}}</span><br>
                          </span>
                        </v-card-text>
                      </v-card>
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
  },
  data() {
    return {
      dialogImportantMutation: false,
    }
  }
}
</script>

<style scoped>

</style>