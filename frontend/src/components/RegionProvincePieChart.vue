<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <div :id="nameGeo" style="width: 600px; height: 500px; user-select: none;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
         background-color: white; margin-top: 30px; margin-bottom: 30px">
        </div>
      </v-row>
    </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "RegionProvincePieChart",
  props: {
    nameGeo: {required: true,},
    geoContent: {required: true,},
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
        this.my_chart = echarts.init(document.getElementById(this.nameGeo));
      }
      else{
        this.my_chart.dispose();
        this.my_chart = echarts.init(document.getElementById(this.nameGeo));
      }
      this.my_chart.setOption(this.pieChart, true);
    },
  },
  mounted() {
    let met =  JSON.parse(JSON.stringify(this.geoContent));
    this.renderGraph(met);
  },
  watch: {
    geoContent(){
      let met =  JSON.parse(JSON.stringify(this.geoContent));
      this.renderGraph(met);
    },
  }
}
</script>

<style scoped>

</style>