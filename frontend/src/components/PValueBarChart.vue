<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center; width: 1300px">
      <v-row justify="center" align="center">
        <div :id="namePValue" style="width: 1000px; height: 250px; user-select: none;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
         background-color: white;">
        </div>
      </v-row>
    </v-container>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "PValueBarChart",
  props: {
    namePValue: {required: true,},
    pValueContent: {required: true,},
    totalMaxOddsRatio: {required: true,},
    startStopProtein: {required: true,},
    selectedDomainForPValue: {required: true,},
    possibleDomainForPValue: {required: true,},
  },
  data(){
    return {
      begin_value_domain: 0,
      end_value_domain: 0,
      barChart: {
        title: {
        },
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            let icon0 = `<span data-tooltip="minimum" style="border-left: 2px solid #fff;display: inline-block;height: 10px;margin-right: 5px;width: 10px;">
                            <span style="background-color:${params.color}; border-radius: 100%; display: block;height: 10px;width: 10px;">
                            </span>
                          </span>`;
            let lineage =  `<span style="text-align: center; padding: 0; margin: 0;"><b>${params.data[4]}</b></span>`
            return `${icon0} ${lineage} <br /><br />
                    <span><b>p-value:</b> ${params.data[2]}</span><br />
                    <span><b>odds ratio:</b> ${params.data[3]}</span><br />
                    <span><b>num sequences:</b> ${params.data[1]}</span> <br />`;
          },
        },
        series: [
            {
                type: 'bar',
                radius: '50%',
                data: [],
                itemStyle: {color: 'blue'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                stack: 'one',
                markArea: {
                    tooltip: {
                        show: false,
                    },
                    data: [ [{
                        xAxis: 0,
                        itemStyle: {
                            color: 'rgba(50, 255, 50, 0.5)',
                        },
                    }, {
                        xAxis: 0
                    }]
                    ]
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
    ...mapState(['colorPValueChart']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    createArrayOfZeros(){
      let arrY = [];
      for (let j = 1; j <= this.startStopProtein['stop']; j = j + 1){
        arrY.push([j, 0, 0, 0]);
      }
      return arrY;
    },
    renderGraph(met){

      let len = met.length;
      let i = 0;
      let arrX = [];
      let arr_of_arrY = [];
      let arrY = [];
      for (let j = 1; j <= this.startStopProtein['stop']; j = j + 1){
        arrX.push(j);
        arrY.push([j, 0, 0, 0]);
      }
      arr_of_arrY.push(arrY);

      this.begin_value_domain = 0;
      this.end_value_domain = 0;

      while (i < len) {
        let single_line = met[i];
        // arrX.push(single_line['name']);
        let single_cell;
        if (single_line['odds_ratio'] > this.totalMaxOddsRatio) {
          single_cell = [single_line['position'] - 1, single_line['value'], single_line['p_value'], 'INF', single_line['name']];
        } else {
          single_cell = [single_line['position'] - 1, single_line['value'], single_line['p_value'], single_line['odds_ratio'], single_line['name']];
        }
        let while_condition = true;
        let k = 0;
        while (while_condition) {
          let arr = arr_of_arrY[k];
          if (JSON.stringify(arr[single_line['position'] - 1]) === JSON.stringify([single_line['position'], 0, 0, 0])) {
            arr[single_line['position'] - 1] = single_cell;
            while_condition = false;
          } else {
            if (k + 1 >= arr_of_arrY.length) {
              arr_of_arrY.push(this.createArrayOfZeros());
              let arr2 = arr_of_arrY[k + 1];
              arr2[single_line['position'] - 1] = single_cell;
              while_condition = false;
            }
          }
          k = k + 1;
        }
        i = i + 1;
      }

      this.barChart.series[0].markArea.data = [this.barChart.series[0].markArea.data[0]]
      this.barChart.series = [this.barChart.series[0]];
      this.barChart.series[0].markArea.data[0][0].xAxis = 0;
      this.barChart.series[0].markArea.data[0][1].xAxis = 0;

      for(let ii = 0; ii < arr_of_arrY.length; ii = ii + 1){
        if(ii === 0){
          this.barChart.series[ii].data = arr_of_arrY[ii];
        }
        else{
          let color ;
          if(ii %2 === 1){
            color = 'red';
          }
          else{
            color = 'blue';
          }
          let series = {
                type: 'bar',
                radius: '50%',
                data: arr_of_arrY[ii],
                itemStyle: {color: color},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                markArea: {
                        tooltip: {
                            show: false,
                        },
                        data: [ [{
                            xAxis: 0,
                            itemStyle: {
                                color: 'red',
                            },
                        }, {
                            xAxis: 0
                        }]
                        ]
                },
                stack: 'one',
            };
          this.barChart.series.push(series);
        }
      }

      if(this.selectedDomainForPValue.length > 0){
        for(let k = 0; k < this.selectedDomainForPValue.length; k = k + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValue.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValue[k];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValue[index]['Begin'];
            max = this.possibleDomainForPValue[index]['End'];
          }

          let num_color = k%this.colorPValueChart.length;

          if(k === 0) {
            this.barChart.series[0].markArea.data[0][0].xAxis = min - 1;
            this.barChart.series[0].markArea.data[0][1].xAxis = max - 1;
            this.barChart.series[0].markArea.data[0][0].itemStyle.color = this.colorPValueChart[num_color];
          }
          else{
            let singleMarkArea = [{
              xAxis: min,
              itemStyle: {
                color: this.colorPValueChart[num_color],
              },
            }, {
              xAxis: max
            }];

            this.barChart.series[0].markArea.data.push(singleMarkArea);
          }
        }
      }

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
    selectedDomainForPValue(){
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      let delayInMilliseconds = 2000;

      let that = this;
      setTimeout(function() {
        that.renderGraph(met);
      }, delayInMilliseconds);
    }
  }
}
</script>

<style scoped>

</style>