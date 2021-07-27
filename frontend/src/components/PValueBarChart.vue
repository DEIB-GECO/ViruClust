<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center; width: 1300px">
      <v-layout row wrap justify-center>
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin: 0; padding: 0">
          <div :id="namePValue" style="width: 1000px; height: 250px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white;">
          </div>
           <v-btn @click="download" x-small icon v-if="my_chart !== null"
            style="margin-left: 20px; margin-top: 110px">
              <v-icon size="23">
                mdi-download-circle-outline
              </v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
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
    selectedDomainForPValueMutagenesis: {required: true,},
    possibleDomainForPValueMutagenesis: {required: true,},
    selectedDomainForPValueAaModifications: {required: true,},
    possibleDomainForPValueAaModifications: {required: true,},
    type: {required: true,},
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
                type: 'slider',
            },
          ],
      },
      my_chart: null,
    }
  },
  computed: {
    ...mapState(['colorPValueChart', 'startValuePValueBarChartTime', 'endValuePValueBarChartTime',
                 'startValuePValueBarChartGeo', 'endValuePValueBarChartGeo',
                 'startValuePValueBarChartFree', 'endValuePValueBarChartFree',
                 'color_1', 'color_2', 'color_3']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setStartValuePValueBarChartTime', 'setEndValuePValueBarChartTime',
                     'setStartValuePValueBarChartGeo', 'setEndValuePValueBarChartGeo',
                     'setStartValuePValueBarChartFree', 'setEndValuePValueBarChartFree']),
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
            color = '#3C99DC';
          }
          else{
            color = '#0F5298';
          }
          let series = {
                type: 'bar',
                radius: '50%',
                data: arr_of_arrY[ii],
                itemStyle: {color: color},
                large: true,
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

          let colors = this.color_1;

          let num_color = k%colors.length;
          let color = colors[num_color];
          color = color + '80'

          let singleMarkArea = [{
            xAxis: min - 1,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max - 1
          }];

          this.barChart.series[0].markArea.data.push(singleMarkArea);

        }
      }

      if(this.selectedDomainForPValueMutagenesis.length > 0){
        for(let k = 0; k < this.selectedDomainForPValueMutagenesis.length; k = k + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValueMutagenesis.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValueMutagenesis[k];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValueMutagenesis[index]['Begin'];
            max = this.possibleDomainForPValueMutagenesis[index]['End'];
          }

          let colors = this.color_2;

          let num_color = k%colors.length;
          let color = colors[num_color];
          color = color + '80'

          let singleMarkArea = [{
            xAxis: min - 1,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max - 1
          }];

          this.barChart.series[0].markArea.data.push(singleMarkArea);
        }
      }

      if(this.selectedDomainForPValueAaModifications.length > 0){
        for(let k = 0; k < this.selectedDomainForPValueAaModifications.length; k = k + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValue.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValueAaModifications[k];
          });
          if (index !== -1) {
            min = this.possibleDomainForPValueAaModifications[index]['Begin'];
            max = this.possibleDomainForPValueAaModifications[index]['End'];
          }

          let colors = this.color_3;

          let num_color = k%colors.length;
          let color = colors[num_color];
          color = color + '80'

          let singleMarkArea = [{
            xAxis: min - 1,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max - 1
          }];

          this.barChart.series[0].markArea.data.push(singleMarkArea);

        }
      }

      this.barChart.xAxis.data = arrX;

      if(this.type === 'time'){
        this.setStartValuePValueBarChartTime(0);
        this.setEndValuePValueBarChartTime(arrX.length);
      }
      else if(this.type === 'geo'){
        this.setStartValuePValueBarChartGeo(0);
        this.setEndValuePValueBarChartGeo(arrX.length);
      }
      else if(this.type === 'free'){
        this.setStartValuePValueBarChartFree(0);
        this.setEndValuePValueBarChartFree(arrX.length);
      }

      this.barChart.dataZoom[0].startValue = 0;
      this.barChart.dataZoom[0].endValue = arrX.length;

      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.namePValue));
      }
      this.my_chart.setOption(this.barChart, true);

      let that = this;
      this.my_chart.on('dataZoom', function (params) {
        if(that.type === 'time') {
          that.setStartValuePValueBarChartTime(params.start / 100 * arrX.length);
          that.setEndValuePValueBarChartTime(params.end / 100 * arrX.length);
        }
        else if(that.type === 'geo') {
          that.setStartValuePValueBarChartGeo(params.start / 100 * arrX.length);
          that.setEndValuePValueBarChartGeo(params.end / 100 * arrX.length);
        }
        else if(that.type === 'free') {
          that.setStartValuePValueBarChartFree(params.start / 100 * arrX.length);
          that.setEndValuePValueBarChartFree(params.end / 100 * arrX.length);
        }
      });
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
    },
    selectedDomainForPValueMutagenesis(){
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      let delayInMilliseconds = 2000;

      let that = this;
      setTimeout(function() {
        that.renderGraph(met);
      }, delayInMilliseconds);
    },
    selectedDomainForPValueAaMutations(){
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      let delayInMilliseconds = 2000;

      let that = this;
      setTimeout(function() {
        that.renderGraph(met);
      }, delayInMilliseconds);
    },
    startValuePValueBarChartTime(){
      if(this.type === 'time') {
        if (this.barChart.dataZoom[0].startValue !== this.startValuePValueBarChartTime ||
            this.barChart.dataZoom[0].endValue !== this.endValuePValueBarChartTime) {
          this.barChart.dataZoom[0].startValue = this.startValuePValueBarChartTime;
          this.barChart.dataZoom[0].endValue = this.endValuePValueBarChartTime;

          if (this.my_chart === null) {
            this.my_chart = echarts.init(document.getElementById(this.namePValue));
          }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    },
    endValuePValueBarChartTime(){
      if(this.type === 'time') {
        if (this.barChart.dataZoom[0].startValue !== this.startValuePValueBarChartTime ||
            this.barChart.dataZoom[0].endValue !== this.endValuePValueBarChartTime) {
          this.barChart.dataZoom[0].startValue = this.startValuePValueBarChartTime;
          this.barChart.dataZoom[0].endValue = this.endValuePValueBarChartTime;

          if (this.my_chart === null) {
            this.my_chart = echarts.init(document.getElementById(this.namePValue));
          }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    },
    startValuePValueBarChartGeo(){
      if(this.type === 'geo') {
        if (this.barChart.dataZoom[0].startValue !== this.startValuePValueBarChartGeo ||
            this.barChart.dataZoom[0].endValue !== this.endValuePValueBarChartGeo) {
          this.barChart.dataZoom[0].startValue = this.startValuePValueBarChartGeo;
          this.barChart.dataZoom[0].endValue = this.endValuePValueBarChartGeo;

          if (this.my_chart === null) {
            this.my_chart = echarts.init(document.getElementById(this.namePValue));
          }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    },
    endValuePValueBarChartGeo(){
      if(this.type === 'geo') {
        if (this.barChart.dataZoom[0].startValue !== this.startValuePValueBarChartGeo ||
            this.barChart.dataZoom[0].endValue !== this.endValuePValueBarChartGeo) {
          this.barChart.dataZoom[0].startValue = this.startValuePValueBarChartGeo;
          this.barChart.dataZoom[0].endValue = this.endValuePValueBarChartGeo;

          if (this.my_chart === null) {
            this.my_chart = echarts.init(document.getElementById(this.namePValue));
          }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    },
    startValuePValueBarChartFree(){
      if(this.type === 'time') {
        if (this.barChart.dataZoom[0].startValue !== this.startValuePValueBarChartFree ||
            this.barChart.dataZoom[0].endValue !== this.endValuePValueBarChartFree) {
          this.barChart.dataZoom[0].startValue = this.startValuePValueBarChartFree;
          this.barChart.dataZoom[0].endValue = this.endValuePValueBarChartFree;

          if (this.my_chart === null) {
            this.my_chart = echarts.init(document.getElementById(this.namePValue));
          }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    },
    endValuePValueBarChartFree(){
      if(this.type === 'time') {
        if (this.barChart.dataZoom[0].startValue !== this.startValuePValueBarChartFree ||
            this.barChart.dataZoom[0].endValue !== this.endValuePValueBarChartFree) {
          this.barChart.dataZoom[0].startValue = this.startValuePValueBarChartFree;
          this.barChart.dataZoom[0].endValue = this.endValuePValueBarChartFree;

          if (this.my_chart === null) {
            this.my_chart = echarts.init(document.getElementById(this.namePValue));
          }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    }
  }
}
</script>

<style scoped>

</style>