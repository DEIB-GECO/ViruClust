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
export default {
name: "FreeQuery",
  components: {TimeSelectorQueryFree, SelectorsQueryFree},
  props: {
    type: {required: true,},
  },
}
</script>

<style scoped>

</style>