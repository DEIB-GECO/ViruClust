<template>
  <v-container fluid grid-list-xl style="justify-content: center;">

    <AnalyzeDistributionLineageInGeo></AnalyzeDistributionLineageInGeo>

    <AnalyzeTimeLinCou></AnalyzeTimeLinCou>

    <AnalyzeLineageAndCountry></AnalyzeLineageAndCountry>

    <AnalyzeProvinceRegion></AnalyzeProvinceRegion>

  </v-container>
</template>

<script>
import AnalyzeDistributionLineageInGeo from "./AnalyzeDistributionLineageInGeo";
import AnalyzeLineageAndCountry from "./AnalyzeLineageAndCountry";
import AnalyzeProvinceRegion from "./AnalyzeProvinceRegion";
import AnalyzeTimeLinCou from "./AnalyzeTimeLinCou";
import axios from "axios";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "AnalyzePage",
  components: {AnalyzeTimeLinCou, AnalyzeProvinceRegion, AnalyzeLineageAndCountry, AnalyzeDistributionLineageInGeo},
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllProtein']),
    ...mapActions([]),
  },
  mounted() {
    let url = `/analyze/allProtein`;
    let to_send = {'gcm': {'taxon_name':["severe acute respiratory syndrome coronavirus 2"]}};
    axios.post(url, to_send)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.setAllProtein(res);
    });
  }
}
</script>

<style scoped>


</style>