<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <v-layout row wrap justify-center>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">

            <div :id="nameField" style="width: 100%; height: 400px; user-select: none;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0;
             background-color: white; margin-bottom: 30px; border: black solid 1px">
            </div>

            <div v-if="chartBlocked" style="position: absolute; top: 100px; width: 200px; height: 200px">
                <v-layout wrap justify-center style=" height: 100%">
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
                    <h1 style="position: absolute; top: 80%; text-align: center">MULTI TARGET</h1>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
                    <h3 style="position: absolute; top: 20%; text-align: center">A multiple target has already been selected</h3>
                  </v-flex>
                </v-layout>
              </div>
            <div v-else-if="isLoading" style="position: absolute; top: 100px; width: 200px; height: 200px">
                <v-img
                    src="../images/loading.gif"
                    style="z-index: 1;"
                />
              </div>
              <div v-else-if="checkNoDataOrSelectLevelAbove()" style="position: absolute; top: 100px; width: 200px; height: 200px">
                <v-layout wrap justify-center style=" height: 100%">
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
                    <h1 style="position: absolute; top: 80%; text-align: center">WAITING DATA</h1>
                  </v-flex>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
                    <h3 style="position: absolute; top: 20%; text-align: center">Please select the previous location level</h3>
                  </v-flex>
                </v-layout>
              </div>
              <div v-else-if="fieldContent.length === 0" style="position: absolute; top: 100px; width: 200px; height: 200px">
                <v-img
                    src="../images/no_data.png"
                    style="z-index: 1;"
                />
              </div>

          </v-flex>
        </v-layout>
      </v-row>
    </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "SelectorsPieChart",
  props: {
    nameField: {required: true,},
    field: {required: true,},
    nameQuery: {required: true,},
    fieldContent: {required: true,},
    isLoading: {required: true,},
    pieChartBlocked: {required: false},
  },
  data(){
    return {
      chartBlocked: false,
      pieChart: {
        title: {
        },
        tooltip: {
            trigger: 'item'
        },
        series: [
            {
                type: 'pie',
                radius: '50%',
                data: [],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
      },
      my_chart: null,
    }
  },
  computed: {
    ...mapState(['queryGeo', 'queryTime', 'queryFreeTarget', 'queryFreeBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    renderGraph(met){

      this.chartBlocked = !!this.pieChartBlocked;

      if(!this.chartBlocked) {

        this.pieChart.series[0].data = met.sort(function (a, b) {
          let num1 = a['value'];
          let num2 = b['value'];
          return num1 - num2;
        });
        if (this.my_chart === null) {
          this.my_chart = echarts.init(document.getElementById(this.nameField));
        }
        this.my_chart.setOption(this.pieChart, true);
      }
      else {
        if (this.my_chart !== null) {
          this.my_chart = echarts.dispose(document.getElementById(this.nameField));
          this.my_chart = null;
        }
      }
    },
    checkNoDataOrSelectLevelAbove(){
      if(this.nameQuery === 'time'){
        if(this.nameField === 'country'){
          return !this.queryTime['geo_group'];
        }
        else if(this.nameField === 'region'){
          return !this.queryTime['country'];
        }
        else if(this.nameField === 'province'){
          return !this.queryTime['region'];
        }
      }
      else if(this.nameQuery === 'geo'){
        if(this.field === 'country'){
          return !this.queryGeo['geo_group'];
        }
        else if(this.field === 'region'){
          return !this.queryGeo['country'];
        }
        else if(this.field === 'province'){
          return !this.queryGeo['region'];
        }
      }
      else if(this.nameQuery === 'freetarget'){
        if(this.field === 'country'){
          return !this.queryFreeTarget['geo_group'];
        }
        else if(this.field === 'region'){
          return !this.queryFreeTarget['country'];
        }
        else if(this.field === 'province'){
          return !this.queryFreeTarget['region'];
        }
      }
      else if(this.nameQuery === 'freebackground'){
        if(this.field === 'country'){
          return !this.queryFreeBackground['geo_group'];
        }
        else if(this.field === 'region'){
          return !this.queryFreeBackground['country'];
        }
        else if(this.field === 'province'){
          return !this.queryFreeBackground['region'];
        }
      }
    },
  },
  mounted() {
    let contentGraph = [];
    let i = 0;
    let len = this.fieldContent.length;
    while(i < len){
      let elem = {'name': this.fieldContent[i]['value'], 'value': this.fieldContent[i]['count']};
      contentGraph.push(elem);
      i = i + 1;
    }
    let met =  JSON.parse(JSON.stringify(contentGraph));
    if(met.length > 0){
        this.renderGraph(met);
    }
    else{
      if(this.my_chart !== null) {
        this.my_chart = echarts.dispose(document.getElementById(this.nameField));
        this.my_chart = null;
      }
    }
  },
  watch: {
    pieChartBlocked(){
      this.chartBlocked = !!this.pieChartBlocked;
    },
    fieldContent(){
      let contentGraph = [];
      let i = 0;
      let len = this.fieldContent.length;
      while(i < len){
        let elem = {'name': this.fieldContent[i]['value'], 'value': this.fieldContent[i]['count']};
        contentGraph.push(elem);
        i = i + 1;
      }
      let met =  JSON.parse(JSON.stringify(contentGraph));
      if(met.length > 0){
        this.renderGraph(met);
      }
      else{
        if(this.my_chart !== null) {
          this.my_chart = echarts.dispose(document.getElementById(this.nameField));
          this.my_chart = null;
        }
      }
    },
  }
}
</script>

<style scoped>

</style>