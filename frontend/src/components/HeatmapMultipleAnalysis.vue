<template>
  <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px; position:relative;">
    <v-layout row wrap justify-center>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 50px">
      <h2>HEATMAP
        <v-btn @click="download" x-small icon v-if="my_chart !== null"
            style="margin-left: 20px; margin-bottom: 5px">
              <v-icon size="23">
                mdi-download-circle-outline
              </v-icon>
         </v-btn>
      </h2>
     </v-flex>
     <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
      <v-autocomplete
              v-model="heatmapMode"
              :items="possibleHeatmapMode"
              label="Heatmap mode"
              solo
              hide-details
            >
      </v-autocomplete>
     </v-flex>
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

      <div v-else-if="errorNoData" style="position: absolute; top: 50px; width: 500px; height: 200px">
          <v-layout wrap justify-center style=" height: 100%">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: relative">
              <h1 style="position: absolute; top: 10%; text-align: center; z-index: 1">NO DATA</h1>
              <h3 style="position: absolute; top:40%; text-align: center; z-index: 1">No data to show</h3>
            </v-flex>
          </v-layout>
        </div>
      </v-flex>

      <v-flex v-if="!errorShow && !errorNoData && heatmapMode === 'Odds ratio'" class="no-horizontal-padding xs12 d-flex" style="justify-content: center; position: absolute; right: 40%; bottom: 90px; z-index: 1;">
          <v-dialog width="500">
            <template v-slot:activator="{ on }">
              <v-btn
                    v-on="on"
                      slot="activator"
                      class="info-button"
                      x-small
                      text icon color="grey"
                      style="margin-bottom: 5px; margin-left: 20px">
                  <v-icon class="info-icon">mdi-information</v-icon>
              </v-btn>
            </template>
            <v-card>
                <v-card-title
                        class="headline grey lighten-2"
                        primary-title
                >
                  {{heatmapMode}}
                </v-card-title>
                <v-card-text style="margin-top: 10px">
                    <span v-if="heatmapMode === 'Odds ratio'">
                        Minimum value is 0. Maximum value is the maximum number that the odds ratio reaches, before becoming infinite.
                    </span>
                </v-card-text>
            </v-card>
      </v-dialog>
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
    maxOddsRatio: {required: true,},
    importantMutation: {required: true,}
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
      errorNoData: false,

      heatmapMode: '% Target',
      possibleHeatmapMode: ['% Target', '% Target - % Background', 'Odds ratio'],

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
            formatter: (value, index)=> `{${index}|${value}}`,
            rich: {},
          }
        },
        visualMap: {
          min: 0,
          max: 100,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '0px',
          inRange: {
              color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
          }
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
    download(){
      let url = this.my_chart.getConnectedDataURL({
          pixelRatio: 2,
          backgroundColor: 'white'
      });
      let $a = document.createElement('a');
      let type = 'png';
      $a.download = 'graph.' + type;
      $a.target = '_blank';
      $a.href = url;
      if (typeof MouseEvent === 'function') {
        let evt = new MouseEvent('click', {
          view: window,
          bubbles: true,
          cancelable: false
        });
        $a.dispatchEvent(evt);
      }
      else {
        let html = '<body style="margin:0;">![](' + url + ')</body>';
        let tab = window.open();
        tab.document.write(html);
      }
    },
    renderGraph(){
      this.x_axis = [];
      this.y_axis = [];
      let rows = [];
      let stop = false;
      let rich = {};
      for(let i = 0; i < this.contentHeatmap.length; i = i + 1){
        this.x_axis.push(this.fixedContent[i][0]['target'].replace("//", ' // '));
        for(let k = 0; k < this.contentHeatmap[i].length; k = k + 1){
          if(this.contentHeatmap[i].length > 500){
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

      this.errorShow = false;
      this.errorNoData = false;

      rows = rows.sort(function (a, b) {
        let pos_a = parseInt(a['mutation_position']);
        let pos_b = parseInt(b['mutation_position']);
        return pos_a > pos_b ? -1 : 1;
      });

      for (let j = 0; j < rows.length; j = j + 1) {
        this.y_axis.push(rows[j]['mutation']);
        if (this.importantMutation['mutation'].includes(rows[j]['mutation'])) {
            rich[j] = {'backgroundColor': 'red', 'color': 'white', 'padding': 3};
        }
        else if (this.importantMutation['additional_mutation'].includes(rows[j]['mutation'])) {
            rich[j] = {'backgroundColor': 'orange', 'color': 'white', 'padding': 3};
        }
        else {
            rich[j] = {'backgroundColor': 'transparent', 'color': 'rgb(104,104,104)'};
        }
      }

      this.data_inside_heatmap = [];
      for (let i = 0; i < this.contentHeatmap.length; i = i + 1) {
        for (let j = 0; j < this.y_axis.length; j = j + 1) {
          let mutation = this.y_axis[j];
          let content = this.contentHeatmap[i];
          let target_info;
          let heatmap_value;
          let index = content.findIndex(function (item) {
            return item['mutation'] === mutation;
          });

          if (index !== -1) {
            if(this.heatmapMode === '% Target') {
              target_info = this.contentHeatmap[i][index]['numerator_target'];
              heatmap_value = this.contentHeatmap[i][index]['percentage_target'];
              this.heatmap.visualMap.min = 0;
              this.heatmap.visualMap.max = 100;
              this.heatmap.tooltip.formatter = function formatter(params){
                let lineage =  `<div style="text-align: center; padding: 0; margin: 0;"><b>${params.data[3]}</b></div>`
                return `${lineage}<br>
                        <b>${params.name}</b><br>
                         <b>num sequences target:</b> ${params.data[2]}<br>
                         <b>% target:</b> ${params.data[4]}%<br />`;
              }
            }
            else if(this.heatmapMode === '% Target - % Background') {
              target_info = this.contentHeatmap[i][index]['percentage_target'];
              heatmap_value = this.contentHeatmap[i][index]['percentage_target'] - this.contentHeatmap[i][index]['percentage_background'];
              this.heatmap.visualMap.min = -10;
              this.heatmap.visualMap.max = 10;
              this.heatmap.tooltip.formatter = function formatter(params){
                let lineage =  `<div style="text-align: center; padding: 0; margin: 0;"><b>${params.data[3]}</b></div>`
                return `${lineage}<br>
                        <b>${params.name}</b><br>
                        <b>% target - % background:</b> ${params.data[4]}%<br>
                        <b>% target:</b> ${params.data[2]}%<br />`;
              }
            }
            else if(this.heatmapMode === 'Odds ratio') {
              target_info = this.contentHeatmap[i][index]['percentage_target'];
              heatmap_value = this.contentHeatmap[i][index]['odd_ratio'];
              this.heatmap.visualMap.min = 0;
              this.heatmap.visualMap.max = this.maxOddsRatio;
              this.heatmap.tooltip.formatter = function formatter(params){
                let lineage =  `<div style="text-align: center; padding: 0; margin: 0;"><b>${params.data[3]}</b></div>`
                return `${lineage}<br>
                        <b>${params.name}:</b><br>
                        <b>odds ratio:</b> ${params.data[4]} <br>
                        <b>% target:</b> ${params.data[2]}%<br />`;
              }
            }
          } else {
            target_info = '-';
            heatmap_value = '-';
          }

          let single_cell = [i, j, target_info, mutation, heatmap_value];
          this.data_inside_heatmap.push(single_cell);
        }
      }

      this.heatmap.yAxis.axisLabel.rich = rich;

      let elem = document.getElementById(this.nameHeatmap);
      let height = (this.y_axis.length * 20 + 300);
      elem.style['height'] = (height + 100).toString() + 'px';
      elem.style['width'] = '100%';

      this.heatmap.xAxis.data = this.x_axis;
      this.heatmap.yAxis.data = this.y_axis;
      this.heatmap.series[0].data = this.data_inside_heatmap;


      // if(this.nameHeatmap === 'multipleAnalysisHeatmapTime') {
      //   let array_to_exclude = [];
      //   for (let i = 0; i < this.y_axis.length; i = i + 1) {
      //     let exclude = true;
      //     let count_exclude = 0;
      //     for (let j = 0; j < this.x_axis.length; j = j + 1) {
      //       if (j < this.x_axis.length - 1 && this.data_inside_heatmap[i + (j * (this.y_axis.length))][4] === '-') {
      //         exclude = true;
      //       }
      //       else if (j < this.x_axis.length - 1 && this.data_inside_heatmap[i + (j * (this.y_axis.length))][4] !== '-') {
      //         count_exclude = count_exclude + 1;
      //         exclude = false;
      //       }
      //       else if (j >= this.x_axis.length - 1 && this.data_inside_heatmap[i + (j * (this.y_axis.length))][4] !== '-') {
      //         exclude = false;
      //       }
      //     }
      //
      //     if (count_exclude <= 1 && exclude) {
      //       array_to_exclude.push(i);
      //     }
      //   }
      //
      //   let array_inside_heatmap_to_exclude = [];
      //
      //   for (let i = array_to_exclude.length -1; i >= 0; i = i - 1) {
      //     // this.y_axis.splice(array_to_exclude[i], 1);
      //     for (let j = this.x_axis.length - 1; j >= 0; j = j - 1) {
      //       array_inside_heatmap_to_exclude.push(array_to_exclude[i] + (j * (this.y_axis.length)));
      //       // this.data_inside_heatmap.splice((array_to_exclude[i] + (j * (this.y_axis.length))), 1);
      //     }
      //   }
      //
      //   array_inside_heatmap_to_exclude.sort(function(a, b){
      //     let num1 = parseInt(a);
      //     let num2 = parseInt(b);
      //     return num1 - num2;
      //   });
      //   // console.log("qui", array_inside_heatmap_to_exclude);
      //
      //   for (let j = array_inside_heatmap_to_exclude.length -1; j >= 0; j = j - 1) {
      //     console.log("qui", this.data_inside_heatmap[array_inside_heatmap_to_exclude[j]]);
      //     // this.data_inside_heatmap.splice(array_inside_heatmap_to_exclude[j], 1);
      //   }
      //
      // }

      if(this.y_axis.length > 150){
        stop = true;
      }


      if(!stop && rows.length !== 0) {
        if (this.my_chart === null) {
          this.my_chart = echarts.init(document.getElementById(this.nameHeatmap), null, {height: height});
        }
        this.heatmap.grid.height = (this.y_axis.length * 20);
        this.my_chart.setOption(this.heatmap, true);
      }
      else if(rows.length === 0){
        let elem = document.getElementById(this.nameHeatmap);
        elem.style['height'] = '200px';
        elem.style['width'] = '500px';
        this.errorShow = false;
        this.errorNoData = true;
      }
      else{
        let elem = document.getElementById(this.nameHeatmap);
        elem.style['height'] = '200px';
        elem.style['width'] = '500px';
        this.errorShow = true;
        this.errorNoData = false;
      }
    },
  },
  mounted() {
    this.renderGraph();
  },
  watch: {
    contentHeatmap(){
      this.renderGraph();
    },
    heatmapMode(){
      this.renderGraph();
    },
    importantMutation(){
      this.renderGraph();
    }
  }
}

</script>

<style scoped>

</style>