<template>
  <v-container fluid grid-list-xl style="justify-content: center; padding: 0;">
    <v-layout wrap align-center style="margin: 0; padding: 0">
          <v-flex md12 sm12 class=" no-horizontal-padding" style="text-align: right; padding: 0; margin-right: 10px">
              Last update date: {{update_date}}
          </v-flex>
    </v-layout>

    <v-tabs v-model="selectedTabAnalyze"
            background-color="#457B9D"
            dark
            show-arrows
            slider-color="#E63946"
            slider-size="6"
            class="containTabs"
            height="60">

      <v-tab id="tab0"  style="border-right: black solid 1px; width: 5%" @click="setSelectedTabAnalyzeFromHome(0);">
        <div>
          <v-icon>mdi-home</v-icon>
        </div>
      </v-tab>

      <v-tab id="tab1" style="border-right: black solid 1px; width: 20%">
         PREVALENCE OF LINEAGES
      </v-tab>

      <v-tab id="tab2" style="border-right: black solid 1px; width: 20%">
         EVOLUTION IN TIME
      </v-tab>

      <!--<v-tab id="tab2"  style="border-right: black solid 1px; width: 20%">
         COUNTRY VS LINEAGE
      </v-tab>-->

      <v-tab id="tab3"  style="border-right: black solid 1px; width: 20%">
         EVOLUTION IN SPACE
      </v-tab>

      <v-tab id="tab4"  style="border-right: black solid 1px; width: 20%">
         CUSTOM ANALYSIS
      </v-tab>

      <v-tab-item class="lol">
        <HomePage></HomePage>
      </v-tab-item>

      <v-tab-item class="lol">
        <AnalyzeDistributionLineageInGeo></AnalyzeDistributionLineageInGeo>
      </v-tab-item>

      <v-tab-item class="lol">
        <AnalyzeTimeLinCou></AnalyzeTimeLinCou>
      </v-tab-item>

      <v-tab-item class="lol">
         <AnalyzeProvinceRegion></AnalyzeProvinceRegion>
      </v-tab-item>

      <v-tab-item class="lol">
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
import HomePage from "./HomePage";

export default {
  name: "AnalyzePage",
  components: {
    HomePage,
    FreeTargetVsBackground, AnalyzeTimeLinCou, AnalyzeProvinceRegion, AnalyzeDistributionLineageInGeo},
  data() {
    return {
      selectedTabAnalyze: 0,
      overlay: true,
      finished_api: 0,
      update_date: null,
    }
  },
  computed: {
    ...mapState(['selectedTabAnalyzeFromHome']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllProtein', 'setAllGeo', 'setHomePage', 'setColor1', 'setColor2', 'setColor3', 'setSelectedTabAnalyzeFromHome']),
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
      while(i < 5){
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
    },
    selectedTabAnalyzeFromHome(){
      this.selectedTabAnalyze = this.selectedTabAnalyzeFromHome;
    }
  },
  mounted() {
    this.selectedTabAnalyze = this.selectedTabAnalyzeFromHome;

    let colormap = require('colormap')

    let color_1 = colormap({
        colormap: 'freesurface-red',
        nshades: 9,
        format: 'hex',
        alpha: 1
    })

    let color_2 = colormap({
        colormap: 'freesurface-blue',
        nshades: 9,
        format: 'hex',
        alpha: 1
    })

    let color_3 = colormap({
        colormap: 'chlorophyll',
        nshades: 9,
        format: 'hex',
        alpha: 1
                  })

    this.setColor1(color_1);
    this.setColor2(color_2);
    this.setColor3(color_3);

    let i = 0;
    while(i < 5){
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

    let url2 = `/analyze/updateDate`;
    axios.get(url2)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      console.log("qui", res);
      this.update_date = res;
    });

    let url = `/analyze/allProtein`;
    axios.get(url)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      this.setAllProtein(res);
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

.lol {
    height: 83.5vh;
    width: 100%;
    overflow-y:auto;
		float:left;
		position:relative;
}

.containTabs{
  width: 100%;
  float:left;
  position:relative;
}

</style>