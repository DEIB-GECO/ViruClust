<template>
  <v-container fluid grid-list-xl style="justify-content: center; padding: 0; margin-top: 10px">

    <v-tabs v-model="selectedTabAnalyze"
            background-color="#800000"
            dark
            show-arrows
            slider-color="orange"
            slider-size="6"
            height="60">

      <v-tab id="tab0" style="border-right: black solid 1px; width: 20%">
         ANALYZE DISTRIBUTION LINEAGE IN GEO
      </v-tab>

      <v-tab id="tab1" style="border-right: black solid 1px; width: 20%">
         TEMPORAL ANALYSIS
      </v-tab>

      <!--<v-tab id="tab2"  style="border-right: black solid 1px; width: 20%">
         COUNTRY VS LINEAGE
      </v-tab>-->

      <v-tab id="tab2"  style="border-right: black solid 1px; width: 20%">
         SPATIAL ANALYSIS
      </v-tab>

      <v-tab id="tab3"  style="border-right: black solid 1px; width: 20%">
         FREE TARGET VS BACKGROUND
      </v-tab>

      <v-tab-item>
        <AnalyzeDistributionLineageInGeo></AnalyzeDistributionLineageInGeo>
      </v-tab-item>

      <v-tab-item>
        <AnalyzeTimeLinCou></AnalyzeTimeLinCou>
      </v-tab-item>

      <!--<v-tab-item>
        <AnalyzeLineageAndCountry></AnalyzeLineageAndCountry>
      </v-tab-item>-->

      <v-tab-item>
         <AnalyzeProvinceRegion></AnalyzeProvinceRegion>
      </v-tab-item>

      <v-tab-item>
        <FreeTargetVsBackground></FreeTargetVsBackground>
      </v-tab-item>

    </v-tabs>

    <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>


  </v-container>
</template>

<script>
import AnalyzeDistributionLineageInGeo from "./AnalyzeDistributionLineageInGeo";
import AnalyzeProvinceRegion from "./AnalyzeProvinceRegion";
import AnalyzeTimeLinCou from "./AnalyzeTimeLinCou";
import axios from "axios";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import FreeTargetVsBackground from "./FreeTargetVsBackground";

export default {
  name: "AnalyzePage",
  components: {FreeTargetVsBackground, AnalyzeTimeLinCou, AnalyzeProvinceRegion, AnalyzeDistributionLineageInGeo},
  data() {
    return {
      selectedTabAnalyze: 0,
      overlay: true,
      finished_api: 0,
    }
  },
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllProtein', 'setAllLineages', 'setAllGeo']),
    ...mapActions([]),
  },
  watch:{
    finished_api(){
      if(this.finished_api === 3){
        this.overlay = false;
      }
    },
    selectedTabAnalyze(){
      let i = 0;
      while(i < 4){
        let id = 'tab' + i;
        if (i === this.selectedTabAnalyze){
          let elem = document.getElementById(id);
          //elem.style.fontSize = '15px';
          elem.style['font-weight'] = 'bold';
        }
        else{
          let elem = document.getElementById(id);
          //elem.style.fontSize = '12px';
          elem.style['font-weight'] = 'normal';
        }
        i = i + 1;
      }
    }
  },
  mounted() {
    let i = 0;
    while(i < 3){
      let id = 'tab' + i;
      if (i === this.selectedTabAnalyze){
        let elem = document.getElementById(id);
        //elem.style.fontSize = '15px';
        elem.style['font-weight'] = 'bold';
      }
      else{
        let elem = document.getElementById(id);
        //elem.style.fontSize = '12px';
        elem.style['font-weight'] = 'normal';
      }
      i = i + 1;
    }

    let url = `/analyze/allProtein`;
    let to_send = {'gcm': {'taxon_name':["severe acute respiratory syndrome coronavirus 2"]}};
    axios.post(url, to_send)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      this.setAllProtein(res);
    });

    let url2 = `/analyze/allLineages`;
    axios.get(url2)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      this.possibleLineage = res;
      this.setAllLineages(res);
    });

    let url3 = `/analyze/allGeo`;
    axios.get(url3)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      this.setAllGeo(res);
    });
  }
}
</script>

<style scoped>


</style>