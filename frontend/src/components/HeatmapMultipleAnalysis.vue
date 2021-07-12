<template>
  <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
    <v-layout row wrap justify-center>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="nameHeatmap" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; z-index: 1">
          </div>
        </v-row>

        <div v-if="errorShow" style="position: absolute; top: 50px; width: 500px; height: 200px">
          <v-layout wrap justify-center style=" height: 100%">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
              <h1 style="position: absolute; top: 10%; text-align: center; z-index: 1">TOO MANY DATA</h1>
              <h3 style="position: absolute; top:40%; text-align: center; z-index: 1">Please select some filter to reduce the number of rows</h3>
            </v-flex>
          </v-layout>
        </div>
      </v-flex>
    </v-layout>

  </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "HeatmapMultipleAnalysis",
  props: {
    nameHeatmap: {required: true,},
    contentHeatmap: {required: true,},
    fixedContent: {required: true,},
  },
  data(){
    return {
      overlay: false,
      x_axis: [],
      y_axis: [],
      data_inside_heatmap: [],
      array_values: [],
      row: [],
      header: [],
      errorShow: false,

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
          max: 80,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '0px'
        },
        series: [{
          name: 'Distribution',
          type: 'heatmap',
          data: this.data_inside_heatmap,
          itemStyle: {
              borderColor: 'white',
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            }
          },
        }]
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
    renderGraph(){
      this.x_axis = [];
      this.y_axis = [];
      let rows = [];
      let stop = false;
      for(let i = 0; i < this.contentHeatmap.length; i = i + 1){
        this.x_axis.push(this.fixedContent[i][0]['target'].replace("//", '\n \n'));
        for(let k = 0; k < this.contentHeatmap[i].length; k = k + 1){
          if(this.contentHeatmap[i].length > 100){
            stop = true;
            break;
          }
          let that = this;
          let index = rows.findIndex(function(item){
            return item['mutation'] === that.contentHeatmap[i][k]['mutation'];
          });
          if(index === -1){
            let single_line = {'mutation': this.contentHeatmap[i][k]['mutation'], 'mutation_position': this.contentHeatmap[i][k]['mutation_position']}
            rows.push(single_line);
          }
        }
      }

      this.my_chart = echarts.dispose(document.getElementById(this.nameHeatmap));
      this.my_chart = null;

      if(!stop && rows.length < 100 && rows.length !== 0) {
        this.errorShow = false;

        rows = rows.sort(function (a, b) {
          let pos_a = parseInt(a['mutation_position']);
          let pos_b = parseInt(b['mutation_position']);
          return pos_a > pos_b ? -1 : 1;
        });

        for (let j = 0; j < rows.length; j = j + 1) {
          this.y_axis.push(rows[j]['mutation']);
        }

        this.data_inside_heatmap = [];
        for (let i = 0; i < this.contentHeatmap.length; i = i + 1) {
          for (let j = 0; j < this.y_axis.length; j = j + 1) {
            let mutation = this.y_axis[j];
            let content = this.contentHeatmap[i];
            let value;
            let percentage;
            let index = content.findIndex(function (item) {
              return item['mutation'] === mutation;
            });

            if (index !== -1) {
              value = this.contentHeatmap[i][index]['numerator_target'];
              percentage = this.contentHeatmap[i][index]['percentage_target'];
            } else {
              value = '-';
              percentage = '-';
            }

            let single_cell = [i, j, value, mutation, percentage];
            this.data_inside_heatmap.push(single_cell);
          }
        }

        let elem = document.getElementById(this.nameHeatmap);
        let height = (this.y_axis.length * 20 + 300);
        elem.style['height'] = (height + 100).toString() + 'px';
        elem.style['width'] = '100%';

        this.heatmap.xAxis.data = this.x_axis;
        this.heatmap.yAxis.data = this.y_axis;
        this.heatmap.series[0].data = this.data_inside_heatmap;

        if (this.my_chart === null) {
          this.my_chart = echarts.init(document.getElementById(this.nameHeatmap), null, {height: height});
          // this.my_chart = echarts.init(document.getElementById(this.nameHeatmap));

        }
        this.heatmap.grid.height = (this.y_axis.length * 20);
        this.my_chart.setOption(this.heatmap, true);
      }
      else{
        let elem = document.getElementById(this.nameHeatmap);
        elem.style['height'] = '200px';
        elem.style['width'] = '500px';
        this.errorShow = true;
      }
    },
  },
  mounted() {
    this.renderGraph();
  },
  watch: {
    contentHeatmap(){
      this.renderGraph();
    }
  }
}

</script>

<style scoped>

</style>