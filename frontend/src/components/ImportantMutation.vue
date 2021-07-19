<template>
  <div>
    <v-btn @click="dialogImportantMutation = true"
           class="white--text"
           color="blue">
      Important Mutation (Spike)</v-btn>

      <v-dialog
      persistent
      v-model="dialogImportantMutation"
      width="800"
      >
        <v-card>
          <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
            Important Mutation (Spike)
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
               <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center; " v-for="(category, key, index) in importantMutation" v-bind:key="index">
                  <v-card width="100%" color="#F0E68C">
                    <v-card-title class="justify-center">
                      {{key.replaceAll("_", " ").toUpperCase()}}
                    </v-card-title>
                    <v-card-text style="text-align: center;">
                      <span v-for="mutation in category" v-bind:key="mutation">
                        <span>{{mutation}}</span><br>
                      </span>
                    </v-card-text>
                  </v-card>
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
    importantMutation: {required: true,},
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