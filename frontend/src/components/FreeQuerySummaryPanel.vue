<template>
  <div>
    <v-row justify="center" align="center">
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
          <h2>SUMMARY</h2>
        </v-flex>
        <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
          <v-card style="width: 80%; margin: 20px" color="rgba(0, 0, 255, 0.5)">
            <v-card-title class="justify-center">
              TARGET
            </v-card-title>
            <v-card-text>
              <v-layout row wrap justify-center style="padding: 20px;">
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3>INFO: </h3>
                </v-flex>
                <v-card color="white" width="60%" style="margin-bottom: 20px; padding: 20px">
                  <span v-for="(info, key) in arrayQueryFreeTarget" v-bind:key="key"><b>- {{key}} :</b> {{info}}<br></span>
                </v-card>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3>LOCATION EXCLUDED: </h3>
                </v-flex>
                <v-card color="white" width="60%" style="margin-bottom: 20px;">
                  <v-card-text style="text-align: center; color: black">
                    <span v-for="(info, key) in toExcludeFreeTarget" v-bind:key="key"><b>{{key.toUpperCase()}} :</b><br><br>
                      <span v-for="(location, idx) in info" v-bind:key="idx">{{location}}<br>
                      </span>
                    </span>
                  </v-card-text>
                </v-card>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3>NUM SEQUENCES: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    :value = "numSequencesQueryFreeTarget"
                    solo
                    readonly
                    hide-details
                    class = "centered-input"
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
          <v-card style="width: 80%; margin: 20px" color="rgba(255, 0, 0, 0.5)">
            <v-card-title class="justify-center">
              BACKGROUND
            </v-card-title>
            <v-card-text>
              <v-layout row wrap justify-center style="padding: 20px;">
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3>INFO: </h3>
                </v-flex>
                <v-card color="white" width="60%" style="margin-bottom: 20px; padding: 20px">
                  <span v-for="(info, key) in arrayQueryFreeBackground" v-bind:key="key"><b>- {{key}} :</b> {{info}}<br></span>
                </v-card>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3>LOCATION EXCLUDED: </h3>
                </v-flex>
                <v-card color="white" width="60%" style="margin-bottom: 20px;">
                  <v-card-text style="text-align: center; color: black">
                    <span v-for="(info, key) in toExcludeFreeBackground" v-bind:key="key"><b>{{key.toUpperCase()}} :</b><br><br>
                      <span v-for="(location, idx) in info" v-bind:key="idx">{{location}}<br>
                      </span>
                    </span>
                  </v-card-text>
                </v-card>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3>NUM SEQUENCES: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    :value = "numSequencesQueryFreeBackground"
                    solo
                    readonly
                    hide-details
                    class = "centered-input"
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-row>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "FreeQuerySummaryPanel",
  data() {
    return {

    }
  },
  computed: {
    ...mapState(['queryFreeTarget', 'queryFreeBackground', 'numSequencesQueryFreeBackground',
                 'numSequencesQueryFreeTarget', 'startDateQueryFreeTarget', 'stopDateQueryFreeTarget',
                 'startDateQueryFreeBackground', 'stopDateQueryFreeBackground',
                 'toExcludeFreeTarget', 'toExcludeFreeBackground']),
    ...mapGetters({}),
    arrayQueryFreeTarget(){
      let array = {};
      let array_keys = ['lineage', 'geo_group', 'country', 'region', 'province'];
      for(let i = 0; i < array_keys.length; i = i + 1){
        let key = array_keys[i];
        let key_to_use;
        if(key === 'geo_group'){
          key_to_use = 'continent';
        }
        else{
          key_to_use = key;
        }
        if(this.queryFreeTarget[key]){
          array[key_to_use] = this.queryFreeTarget[key];
        }
        else{
          array[key_to_use] = 'N/D';
        }
      }
      if(this.startDateQueryFreeTarget){
        array['start date'] = this.startDateQueryFreeTarget;
      }
      else{
         array['start date'] = 'N/D';
      }
      if(this.stopDateQueryFreeTarget){
        array['stop date'] = this.stopDateQueryFreeTarget;
      }
      else{
         array['stop date'] = 'N/D';
      }
      return array;
    },
    arrayQueryFreeBackground(){
      let array = {};
      let array_keys = ['lineage', 'geo_group', 'country', 'region', 'province'];
      for(let i = 0; i < array_keys.length; i = i + 1){
        let key = array_keys[i];
        let key_to_use;
        if(key === 'geo_group'){
          key_to_use = 'continent';
        }
        else{
          key_to_use = key;
        }
        if(this.queryFreeBackground[key]){
          array[key_to_use] = this.queryFreeBackground[key];
        }
        else{
          array[key_to_use] = 'N/D';
        }
      }
      if(this.startDateQueryFreeBackground){
        array['start date'] = this.startDateQueryFreeBackground;
      }
      else{
         array['start date'] = 'N/D';
      }
      if(this.stopDateQueryFreeBackground){
        array['stop date'] = this.stopDateQueryFreeBackground;
      }
      else{
         array['stop date'] = 'N/D';
      }
      return array;
    }
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
  }
}
</script>

<style scoped>

  /deep/ .centered-input input {
    text-align: center
  }

</style>