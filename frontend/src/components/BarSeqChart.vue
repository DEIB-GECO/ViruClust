<template>
  <v-card color="#DAA520">
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <div @click="filterPoint()" id="chart2" style="width: 1200px; height: 500px; user-select: none;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
         background-color: white; margin: 50px">
        </div>
      </v-row>
      <v-row justify="center" align="center">
        <v-btn @click="zoomOut()" color="blue" class="white--text" style="margin-bottom: 20px;">
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
    ...mapState(['xAxisBarSeqChart', 'yAxisBarSeqChart', 'allResultTable']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllResultTable']),
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
  },
  mounted() {
      this.allResultTableThisInstance = this.allResultTable;
      this.sequenceBarChart.series[0].data = this.yAxisBarSeqChart;
      this.my_chart2 = echarts.init(document.getElementById('chart2'));
      this.my_chart2.setOption(this.sequenceBarChart, true);
      this.firstUpdate = false;
      let my_c = document.getElementById('chart2');
      my_c.click();
  },
  watch: {
    allResultTable() {
      if(this.firstUpdate) {
        this.sequenceBarChart.series[0].data = this.yAxisBarSeqChart;
        this.my_chart2 = new echarts.init(document.getElementById('chart2'));
        this.my_chart2.setOption(this.sequenceBarChart, true);
        this.firstUpdate = false;
        let my_c = document.getElementById('chart2');
        my_c.click();
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
          var that = this;
          this.setAllResultTable(this.allResultTable.filter(function (i){
              let mut = i['mutation'];
              return mut[0] === that.selectedPosition;
            })
          );
        }
        else{
          this.selectedPosition = null;
          this.setAllResultTable(this.allResultTableThisInstance);
        }
      }
    }
  }
}
</script>

<style scoped>

</style>