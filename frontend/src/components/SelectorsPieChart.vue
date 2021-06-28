<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <v-layout row wrap justify-center>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">

            <div :id="nameField" style="width: 100%; height: 400px; user-select: none;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0;
             background-color: white; margin-bottom: 30px; border: black solid 1px">
            </div>

            <div v-if="isLoading" style="position: absolute; top: 100px; width: 200px; height: 200px">
                <v-img
                    src="../images/loading.gif"
                    style="z-index: 1;"
                />
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
    fieldContent: {required: true,},
    isLoading: {required: true,},
  },
  data(){
    return {
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
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    renderGraph(met){
      this.pieChart.series[0].data = met.sort(function(a, b){
        let num1 = a['value'];
        let num2 = b['value'];
        return num1 - num2;
      });
      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.nameField));
      }
      this.my_chart.setOption(this.pieChart, true);
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