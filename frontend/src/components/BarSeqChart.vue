<template>
  <v-card color="#DAA520">
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <div @click="filterPoint()" id="chart2" style="width: 1200px; height: 500px; user-select: none;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
         background-color: white; margin: 50px; margin-bottom: 0px!important;">
        </div>
        <v-container id="image2" fluid grid-list-xl style="justify-content: center; margin-bottom: 20px; background-color: white;">
          <v-row justify="center" align="center" v-if="proteinSelected === 'Spike (surface glycoprotein)'">
            <img alt= "" style="width: 80%; margin-left: 0.6%; align-items: center;" id="regionSVG" src="../images/image_2697049_spike.svg">
          </v-row>
        </v-container>
      </v-row>
      <v-row justify="center" align="center">
        <v-btn @click="replotChart()" color="blue" class="white--text" style="margin-bottom: 20px; margin-right: 10px">
          RE-PLOT
        </v-btn>
        <v-btn @click="zoomOut()" color="blue" class="white--text" style="margin-bottom: 20px; margin-left: 10px">
          ZOOM OUT
        </v-btn>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from 'echarts';

export default {
  name: 'BarSeqChart',
  data() {
    return {
      params: null,
      selectedPosition: null,
      firstUpdate: true,
      allResultTableThisInstance: [],
      listResThisInstance: [],
      sequenceBarChart: {
          title: {
            textStyle: {
              fontSize: 15,
            },
            text: 'Seq Bar Chart',
            left: 'center'
          },
          tooltip: {},
          xAxis: {
            type: 'value',
            min: 'dataMin',
            max: 'dataMax',
            minInterval: 1,
            splitLine: {
                show: false
            },
            splitNumber: 10
          },
          yAxis: {
            type: 'value',
            min: 'dataMin',
            minInterval: 1,
            splitLine: {
                show: true
            }
          },
          series: [{
            name: 'seq mutated',
            type: 'bar',
            data: [],
            selectedMode: 'single',
            barMinWidth: '5px',
            emphasis: {
              label:{
                show: true,
                position: 'top',
                formatter: '{@[0]}',
                color: 'orange',
              },
              itemStyle: {
                 borderColor: 'orange',
                color: 'orange',
              }
            },
          }],
          dataZoom: [
            {
                type: 'slider',
                show: true,
                start: 0,
                end: 100,
                handleSize: '100%',
                xAxisIndex: [0],
            },
            {
                type: 'inside',
                start: 0,
                end: 100
            },
          ],
          selectedMode: 'single',
          select: {
            label: {
              show: true,
              position: 'top',
              color: 'red',
              formatter: '{@[0]} : {@[1]}'
            },
            itemStyle:{
              color: 'red',
              borderColor: 'red',
              borderWidth: '1px',
              borderType: 'solid',
            },
          }
      },
      my_chart: null,
      my_chart2: null,
    }
  },
  computed: {
    ...mapState(['xAxisBarSeqChart', 'yAxisBarSeqChart', 'allResultTable', 'listRes', 'proteinSelected']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllResultTable', 'setListRes']),
    ...mapActions([]),
    zoomOut() {
       this.my_chart2.dispatchAction({
        type: 'dataZoom',
            startValue: 1,
            endValue: this.yAxisBarSeqChart.length
        });

    },
    filterPoint(){
        var that = this;
        this.my_chart2.on('click', function (params) {
          that.params = params;
        });
    },
    renderGraph(re_init = false) {
      let gLabel = document.getElementById("chart2");
      let style = window.getComputedStyle(gLabel , null);
      document.getElementById('image2').style.width = style.getPropertyValue("width");

      this.allResultTableThisInstance = this.allResultTable;
      this.listResThisInstance = this.listRes;
      this.sequenceBarChart.series[0].data = this.yAxisBarSeqChart;
      if(re_init) {
        this.my_chart2 = echarts.init(document.getElementById('chart2'));
      }
      this.my_chart2.setOption(this.sequenceBarChart, true);
      this.firstUpdate = false;
      let my_c = document.getElementById('chart2');
      my_c.click();
    },
    replotChart(){
      this.my_chart2.dispose();
      this.setAllResultTable(this.allResultTableThisInstance);
      this.setListRes(this.listResThisInstance);
      this.selectedPosition = null;
      this.renderGraph(true);
    },
    onResize() {
      this.my_chart2.dispose();
      this.renderGraph(true);
    }
  },
  mounted() {
    this.renderGraph(true);
    /*this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    })*/
  },
  watch: {
    allResultTable() {
      if(this.firstUpdate) {
        this.renderGraph(false);
      }
      else{
        this.zoomOut();
      }
    },
    params(){
      if(this.params !== null){
        if(this.params.data[0] !== this.selectedPosition){
          this.selectedPosition = this.params.data[0];
          this.setAllResultTable(this.allResultTableThisInstance);
          this.setListRes(this.listResThisInstance);
          var that = this;
          this.setAllResultTable(this.allResultTable.filter(function (i){
              let mut = i['mutation'];
              return mut[0] === that.selectedPosition;
            })
          );
          this.setListRes(this.listRes.filter(function (i){
              let mut = i['mutation_name'];
              return mut[0] === that.selectedPosition;
            })
          );
        }
        else{
          this.selectedPosition = null;
          this.setAllResultTable(this.allResultTableThisInstance);
          this.setListRes(this.listResThisInstance);
        }
      }
    }
  }
}
</script>

<style scoped>

</style>