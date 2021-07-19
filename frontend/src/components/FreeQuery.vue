<template>
  <div style="border: black solid 1px; margin-bottom: 100px">
    <v-layout row wrap justify-center style="padding: 30px;">
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
         <h2>SELECT</h2>
       </v-flex>
       <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'lineage'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
       </v-flex>
       <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'geo_group'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'country'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'region'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'province'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px;">
        <h3>Select location to exclude from the one selected</h3>
      </v-flex>
      <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
          <SelectorQueryToExclude
          :mode="'free' + type"
          :field="fieldToExclude">
          </SelectorQueryToExclude>
      </v-flex>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
      </v-flex>
      <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
         <TimeSelectorQueryFree
            :timeName = 'type + "timeDistribution"'
            :type = 'type'
         >
         </TimeSelectorQueryFree>
       </v-flex>
    </v-layout>

  </div>
</template>

<script>
import SelectorsQueryFree from "./SelectorsQueryFree";
import TimeSelectorQueryFree from "./TimeSelectorQueryFree";
import SelectorQueryToExclude from "./SelectorQueryToExclude";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
export default {
name: "FreeQuery",
  components: {SelectorQueryToExclude, TimeSelectorQueryFree, SelectorsQueryFree},
  props: {
    type: {required: true,},
  },
  data(){
    return {
      fieldToExclude: null,
    }
  },
  computed: {
    ...mapState(['queryFreeTarget', 'queryFreeBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    computeFieldToExclude() {
      let query ;
      if(this.type === 'target'){
        query = this.queryFreeTarget;
      }
      else{
        query = this.queryFreeBackground;
      }
      if (!query['geo_group']) {
        this.fieldToExclude = 'geo_group';
      } else if (!query['country']) {
        this.fieldToExclude = 'country';
      } else if (!query['region']) {
        this.fieldToExclude = 'region';
      } else if (!query['province']) {
        this.fieldToExclude = 'province';
      } else {
        this.fieldToExclude = null;
      }
    },
  },
  mounted() {
    this.computeFieldToExclude();
  },
  watch: {
    queryFreeTarget(){
      if(this.type === 'target'){
        this.computeFieldToExclude();
      }
    },
    queryFreeBackground(){
      if(this.type === 'background'){
        this.computeFieldToExclude();
      }
    }
  }
}
</script>

<style scoped>

</style>