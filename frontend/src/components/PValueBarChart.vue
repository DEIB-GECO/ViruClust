<template>
  <v-container fluid grid-list-xl style="justify-content: center; width: 1500px">
    <v-row justify="center" align="center">
      <div :id="namePValue" style="width: 1200px; height: 500px; user-select: none;
      -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
       background-color: white; margin-top: 50px">
      </div>
    </v-row>
  </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "PValueBarChart",
  props: {
    namePValue: {required: true,},
    pValueContent: {required: true,},
  },
  data(){
    return {
      barChart: {
        title: {
        },
        tooltip: {
            trigger: 'item'
        },
        series: [
            {
                type: 'bar',
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
        ],
        xAxis: {
            type: 'category',
            data: []
        },
        yAxis: {
            type: 'value'
        },
        dataZoom: [
            {
                type: 'inside',
            },
          ],
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

      let len = met.length;
      let i = 0;
      let arrX = [];
      let arrY = [];
      while (i < len){
        let single_line = met[i];
        arrX.push(single_line['name']);
        arrY.push(single_line['value']);
        i = i + 1;
      }

      this.barChart.series[0].data = arrY;
      this.barChart.xAxis.data = arrX;

      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.namePValue));
      }
      this.my_chart.setOption(this.barChart, true);
    }
  },
  mounted() {
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      this.renderGraph(met);
  },
  watch: {
    metadataContent(){
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      this.renderGraph(met);
    },
  }
}
</script>

<style scoped>

</style>