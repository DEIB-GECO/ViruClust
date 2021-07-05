<template>
  <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="nameHeatmap" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; z-index: 1">
          </div>
        </v-row>
    </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "HeatmapAnalyzeDistribution",
  props: {
    nameHeatmap: {required: true,},
    headerTable: {required: true,},
    rowTable: {required: true,},
    sortColumn: {required: true,},
    descColumn: {required: true,},
    numSequences: {required: true,},
    geoGranularity: {required: true,},
    denominators: {required: true,},
  },
  x_axis: [],
  y_axis: [],
  data_inside_heatmap: [],
  data(){
    return {
      overlay: false,

      options_slider: {
        enableCross: false
      },
      heatmap: {
        tooltip: {
          position: 'top',
           trigger: 'item',
          formatter: function (params) {
            // let icon0 = `<span data-tooltip="minimum" style="border-left: 2px solid #fff;display: inline-block;height: 10px;margin-right: 5px;width: 10px;">
            //                 <span style="background-color:${params.color}; border-radius: 100%; display: block;height: 10px;width: 10px;">
            //                 </span>
            //               </span>`;
            let lineage =  `<div style="text-align: center; padding: 0; margin: 0;">${params.data[3]}</div>`
            return `${lineage}
                    ${params.name}: ${params.data[2]} (${params.data[4]}%)<br />`;
          },
          borderWidth: '6'
        },
        grid: {
          top: 100,
        },
        xAxis: {
          type: 'category',
          data: this.x_axis,
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: '0',
            rotate: '-90',
          }
        },
        yAxis: {
          type: 'category',
          data: this.y_axis,
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: '0',
          }
        },
        visualMap: {
          min: 0,
          max: 25,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '0px'
        },
        series: [{
          name: 'Distribution',
          type: 'heatmap',
          data: this.data_inside_heatmap,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
        }]
      },
      my_chart: null,
    }
  },
  computed: {
    ...mapState(['all_geo', 'startDateDistributionLineageInGeo', 'stopDateDistributionLineageInGeo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    renderGraph(){
      this.rowTable = this.customSort(this.rowTable, this.sortColumn, this.descColumn);

      this.x_axis = [];
      this.headerTable.forEach(elem => {
        if(elem['text'] !== 'lineage') {
          this.x_axis.push(elem['value']);
        }
      });

      this.y_axis = [];

      this.rowTable.forEach(elem2 => {
        this.y_axis.push(elem2['lineage']);
      });

      this.data_inside_heatmap = [];
      for (let i = 0; i < this.x_axis.length; i = i + 1){
        let denominator = this.denominators[this.x_axis[i]];
        for (let j = 0; j < this.rowTable.length; j = j + 1) {
            let value;
            let percentage;
            if(this.rowTable[j][this.x_axis[i]] === undefined ||  this.rowTable[j][this.x_axis[i]] === null){
              value = '-';
              percentage = '-';
            }
            else{
              value = parseInt(this.rowTable[j][this.x_axis[i]]);
              percentage = Math.ceil((value/denominator)*100);
            }
            let a = this.rowTable[j]['lineage'];
            let single_cell = [i, j, value, a, percentage];
            this.data_inside_heatmap.push(single_cell);
        }
      }

      this.heatmap.xAxis.data = this.x_axis;
      this.heatmap.yAxis.data = this.y_axis;
      this.heatmap.series[0].data = this.data_inside_heatmap;

      if(this.my_chart === null) {
        let height = (this.rowTable.length * 20 + 300);
        this.my_chart = echarts.init(document.getElementById(this.nameHeatmap), null, {height: height}); //, null, {height: height}
      }
      this.heatmap.grid.height =  (this.rowTable.length * 20);
      this.my_chart.setOption(this.heatmap, true);
    },
    customSort(items, index2, isDesc2) {
      let index = index2[0];
      let isDesc = isDesc2[0];
      items.sort((a, b) => {
        let count_a = '0';
        let count_b = '0';
        if(a[index] !== undefined && a[index] !== null){
          count_a = a[index].toString();
        }
        if(b[index] !== undefined && b[index] !== null){
          count_b = b[index].toString();
        }
        if (!isDesc) {
          if(count_a === count_b){
            return a['lineage'] < b['lineage'] ? 1 : -1;
          }
          else {
            return  parseInt(count_a, 10) > parseInt(count_b, 10)  ? 1 : -1;
          }
        } else {
          if(count_a === count_b){
            return a['lineage'] < b['lineage'] ? 1 : -1;
          }
          else {
            return  parseInt(count_a, 10) < parseInt(count_b, 10)  ? 1 : -1;
          }
        }
      });
      return items;
    },
    // countSpecificGeoSequence(location){
    //   let all_geo = this.all_geo;
    //   let i = 0;
    //   let len = all_geo.length;
    //   let total = 0;
    //   let locationToCheck;
    //   let granularity;
    //   if(this.geoGranularity === 'geo_group'){
    //     granularity = 'country';
    //   }
    //   else if(this.geoGranularity === 'country'){
    //     granularity = 'region';
    //   }
    //   else if(this.geoGranularity === 'region'){
    //     granularity = 'province';
    //   }
    //
    //   if(location === 'N/D'){
    //     locationToCheck = null;
    //   }
    //   else{
    //     locationToCheck = location;
    //   }
    //   while(i < len){
    //     if (all_geo[i][granularity] === locationToCheck) {
    //       total = total + all_geo[i]['count'];
    //     }
    //     i = i + 1;
    //   }
    //   return total;
    // },
  },
  mounted() {
    let elem = document.getElementById(this.nameHeatmap);
     elem.style['height'] = (this.rowTable.length * 20 + 400).toString()  + 'px';
    this.renderGraph();
  },
  watch: {
    headerTable(){
      this.renderGraph();
    },
    sortColumn(){
      if(this.descColumn[0]) {
        this.renderGraph();
      }
    },
    descColumn(){
      this.renderGraph();
    },
  }
}

</script>

<style scoped>

</style>