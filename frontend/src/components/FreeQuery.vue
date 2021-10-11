<template>
  <div style="margin-bottom: 100px">
    <v-layout row wrap justify-center style="padding: 30px;">
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
         <h2>PICK LINEAGE AND PLACE</h2>
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
         <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
              <v-radio-group
                v-model="radio_group_lineage"
                row
              >
                <v-radio
                  label="Only Lineage"
                  value="only_lineage"
                ></v-radio>
                <v-radio
                  label="Lineage + Set of Mutations"
                  value="lineage_and_mutations"
                ></v-radio>
                <v-radio
                  label="Only Set of Mutations"
                  value="only_mutations"
                ></v-radio>
              </v-radio-group>
            </v-flex>
           <v-flex class="no-horizontal-padding xs12 lg6 xl3 d-flex" style="justify-content: center;">
             <SelectorsQueryFree
              field = 'lineage'
              :type = 'type'
              :radio_select = "radio_group_lineage">
             </SelectorsQueryFree>
           </v-flex>
           <v-flex class="no-horizontal-padding xs12 lg12 xl12 d-flex" style="justify-content: center;">
             <SetMutationPanel
             :type = 'type'
             :radio_group_lineage = "radio_group_lineage">
             </SetMutationPanel>
           </v-flex>
         </v-layout>
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 lg6 xl3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'geo_group'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 lg6 xl3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'country'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 lg6 xl3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'region'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
       <v-flex class="no-horizontal-padding xs12 lg6 xl3 d-flex" style="justify-content: center;">
         <SelectorsQueryFree
          field = 'province'
          :type = 'type'>
         </SelectorsQueryFree>
       </v-flex>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px;">
        <h3>Exclude one or more places</h3>
      </v-flex>
      <v-flex class="no-horizontal-padding xs12 md4 d-flex" style="justify-content: center;">
          <SelectorQueryToExclude
          :mode="'free' + type"
          :field="fieldToExclude">
          </SelectorQueryToExclude>
      </v-flex>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
      </v-flex>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
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
import SetMutationPanel from "./SetMutationPanel";
export default {
name: "FreeQuery",
  components: {SetMutationPanel, SelectorQueryToExclude, TimeSelectorQueryFree, SelectorsQueryFree},
  props: {
    type: {required: true,},
  },
  data(){
    return {
      radio_group_lineage: 'only_lineage',

      fieldToExclude: null,
    }
  },
  computed: {
    ...mapState(['queryFreeTarget', 'queryFreeBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryFreeTarget', 'setQueryFreeBackground']),
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
    radio_group_lineage(){
      if(this.radio_group_lineage === 'only_lineage'){
        if(this.type === 'target') {
          this.setQueryFreeTarget({field: 'mutations', list: null});
        }
        else if(this.type === 'background'){
          this.setQueryFreeBackground({field: 'mutations', list: null});
        }
      }
    },
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