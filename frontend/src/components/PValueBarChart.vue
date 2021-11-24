<template>
  <div style="width: 100%;">
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-layout row wrap justify-center>
        <v-flex class="no-horizontal-padding xs11 d-flex" style="justify-content: center; margin: 0; padding: 0">
          <div @click="filterPoint()" :id="namePValue" style="width: 100px; height: 250px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white;">
          </div>
        </v-flex>
        <v-flex class="no-horizontal-padding xs1 d-flex" style="justify-content: center; margin: 0; padding: 0">
           <v-btn @click="download" small icon v-if="my_chart !== null"
            style="margin-left: 20px; margin-top: 110px">
              <v-icon size="32">
                mdi-download-circle-outline
              </v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>

    <v-dialog
      persistent
      v-model="dialog_single_position"
      width="500"
      >
        <v-card>
          <v-card-title class="white--text" style="background-color: #457B9D;">
            SINGLE POSITION ({{single_position}})
            <v-spacer></v-spacer>
            <v-btn
                style="background-color: red"
                slot="activator"
                icon
                small
                color="white"
                @click="closeDialogSinglePosition()"
            >
              X
            </v-btn>
          </v-card-title>

          <v-card-text class="text-xs-center">
            <div :id="namePValue + '_single_position'" style="width: 50px; height: 250px; user-select: none;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
             background-color: white;">
            </div>
          </v-card-text>

        </v-card>
      </v-dialog>

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
    selectedDomainForPValueUploaded: {required: true,},
    possibleDomainForPValueUploaded: {required: true,},
    type: {required: true,},
    rowsAnalTime: {required: true,},
    protein: {required: true,},
    nameFileAccIdsTarget: {required: false,},
    nameFileAccIdsBackground: {required: false,},
    listAccIdsTargetInserted: {required: false,},
    listAccIdsBackgroundInserted: {required: false,},
  },
  data(){
    return {
      begin_value_domain: 0,
      end_value_domain: 0,
      params: null,
      dialog_single_position: false,
      single_position: null,
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
                    <span><b>log odds_ratio:</b> ${params.data[1]}</span> <br />
                    <span><b>p-value:</b> ${params.data[2]}</span><br />
                    <span><b>odds ratio:</b> ${params.data[3]}</span><br />
                    <span><b>num sequences:</b> ${params.data[5]}</span> <br />`;
          },
        },
        series: [
            {
                type: 'bar',
                radius: '50%',
                data: [],
                itemStyle: {color: '#457B9D'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: '#457B9D'
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
            // splitLine: {
            //    show: false
            // },
            // max: 0,
            // minInterval: 1,
        },
        yAxis: {
            type: 'value',
            // max: 0,
            name: 'log(odds_ratio)',
            nameTextStyle: {
              fontSize: 10,
            },
        },
        dataZoom: [
            {
                type: 'slider',
                // realtime: false,
                maxValueSpan: 398,
            },
          ],
      },
      barChartSinglePosition: {
        title: {
        },
        series: [
            {
                type: 'bar',
                radius: '50%',
                data: [],
                itemStyle: {color: '#457B9D'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: '#457B9D'
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
            axisTick: {
              interval: 0,
            },
            axisLabel: {
              interval: 0,
            },
        },
        yAxis: {
            type: 'value',
            name: 'log(odds_ratio)',
            nameTextStyle: {
              fontSize: 10,
            }
        },
      },
      my_chart: null,
      my_chart_single_position: null,
    }
  },
  computed: {
    ...mapState(['colorPValueChart', 'startValuePValueBarChartTime', 'endValuePValueBarChartTime',
                 'startValuePValueBarChartGeo', 'endValuePValueBarChartGeo',
                 'startValuePValueBarChartFree', 'endValuePValueBarChartFree',
                 'color_1', 'color_2', 'color_3',
                 'queryTime', 'startDateQueryGeo', 'stopDateQueryGeo',
                 'startDateQueryFreeTarget', 'stopDateQueryFreeTarget',
                 'startDateQueryFreeBackground', 'stopDateQueryFreeBackground',
                 'queryFreeTarget', 'queryFreeBackground', 'queryGeo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setStartValuePValueBarChartTime', 'setEndValuePValueBarChartTime',
                     'setStartValuePValueBarChartGeo', 'setEndValuePValueBarChartGeo',
                     'setStartValuePValueBarChartFree', 'setEndValuePValueBarChartFree']),
    ...mapActions([]),
    closeDialogSinglePosition(){
      this.dialog_single_position = false;
      this.params = null;
      this.single_position = null;
    },
    filterPoint(){
        let that = this;
        this.my_chart.on('click', function (params) {
          that.params = params;
        });
    },
    download(){
      let url = this.my_chart.getConnectedDataURL({
          pixelRatio: 2,
          backgroundColor: 'white'
      });
      let $a = document.createElement('a');
      let type = 'png';
      let filename = 'noResult';
      if(this.rowsAnalTime.length > 0) {
        if(this.type === 'time' || this.type === 'geo') {
          if(this.type === 'time') {
            filename = 'temporal_analysis_AaChanges_';
            if(this.queryTime['lineage']){
              filename += this.queryTime['lineage'] + '_';
            }
            filename += '(' + this.rowsAnalTime[0]['target'] + ')' + '_vs_' + '(' + this.rowsAnalTime[0]['background'] + ')';
            if (!this.queryTime['geo_group']) {
              filename += '_World.csv';
            } else if (!this.queryTime['country']) {
              filename += '_' + this.queryTime['geo_group'];
            } else if (!this.queryTime['region']) {
              filename += '_' + this.queryTime['country'];
            } else if (!this.queryTime['province']) {
              filename += '_' + this.queryTime['region'];
            } else {
              filename += '_' + this.queryTime['province'];
            }
          }
          else{
            filename = 'spatial_analysis_AaChanges_';
            if(this.queryGeo['lineage']){
              filename += this.queryGeo['lineage']  + '_';
            }
            filename += '(' + this.rowsAnalTime[0]['target'] + ')' + '_vs_' + '(' + this.rowsAnalTime[0]['background'] + ')';
            filename += '_' + this.startDateQueryGeo + '_' + this.stopDateQueryGeo;
          }
        }
        else{
          filename = 'open_analysis_AaChanges_' + '(';
          if(this.nameFileAccIdsTarget === null && this.listAccIdsTargetInserted.length === 0) {
            if (this.queryFreeTarget['lineage']) {
              filename += this.queryFreeTarget['lineage'] + '_';
            }
            if (!this.queryFreeTarget['geo_group']) {
              filename += 'World';
            } else if (!this.queryFreeTarget['country']) {
              if(this.queryFreeTarget['geo_group'].length > 2){
                filename += this.queryFreeTarget['geo_group'][0] + '_etc';
              }
              else {
                filename += this.queryFreeTarget['geo_group'];
              }
            } else if (!this.queryFreeTarget['region']) {
              if(this.queryFreeTarget['country'].length > 2){
                filename += this.queryFreeTarget['country'][0] + '_etc';
              }
              else{
                filename += this.queryFreeTarget['country'];
              }
            } else if (!this.queryFreeTarget['province']) {
              if(this.queryFreeTarget['region'].length > 2){
                filename += this.queryFreeTarget['region'][0] + '_etc';
              }
              else{
                filename += this.queryFreeTarget['region'];
              }
            } else {
              if(this.queryFreeTarget['province'].length > 2){
                filename += this.queryFreeTarget['province'][0] + '_etc';
              }
              else{
                filename += this.queryFreeTarget['province'];
              }
            }
            filename += '_' + this.startDateQueryFreeTarget + '_' + this.stopDateQueryFreeTarget;
          }
          else{
            if(this.nameFileAccIdsTarget !== null) {
              filename += this.nameFileAccIdsTarget.split('.txt')[0];
            }
            if(this.listAccIdsTargetInserted.length > 0){
              if(this.nameFileAccIdsTarget !== null) {
                filename += '_';
              }
              filename += 'userSelectedIds';
            }
          }
          filename += ')' + '_vs_(';
          if(this.nameFileAccIdsBackground === null && this.listAccIdsBackgroundInserted.length === 0 ) {
            if (this.queryFreeBackground['lineage']) {
              filename += this.queryFreeBackground['lineage'] + '_';
            }
            if (!this.queryFreeBackground['geo_group']) {
              filename += 'World';
            } else if (!this.queryFreeBackground['country']) {
              if(this.queryFreeBackground['geo_group'].length > 2){
                filename += this.queryFreeBackground['geo_group'][0] + '_etc';
              }
              else{
                filename += this.queryFreeBackground['geo_group'];
              }
            } else if (!this.queryFreeBackground['region']) {
              if(this.queryFreeBackground['country'].length > 2){
                filename += this.queryFreeBackground['country'][0] + '_etc';
              }
              else{
                filename += this.queryFreeBackground['country'];
              }
            } else if (!this.queryFreeBackground['province']) {
              if(this.queryFreeBackground['region'].length > 2){
                filename += this.queryFreeBackground['region'][0] + '_etc';
              }
              else{
                filename += this.queryFreeBackground['region'];
              }
            } else {
              if(this.queryFreeBackground['province'].length > 2){
                filename += this.queryFreeBackground['province'][0] + '_etc';
              }
              else{
                filename += this.queryFreeBackground['province'];
              }
            }
            filename += '_' + this.startDateQueryFreeBackground + '_' + this.stopDateQueryFreeBackground;
          }
          else{
            if(this.nameFileAccIdsBackground !== null) {
              filename += this.nameFileAccIdsBackground.split('.txt')[0];
            }
            if(this.listAccIdsBackgroundInserted.length > 0){
              if(this.nameFileAccIdsBackground !== null) {
                filename += '_';
              }
              filename += 'userSelectedIds';
            }
          }
          filename += ')';
        }
        filename += '_' + this.protein;
      }
      $a.download = filename + '.' + type;
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
      for (let j = 0; j <= this.startStopProtein['stop']; j = j + 1){
        arrY.push([j.toString(), 0, 0, 0, 0]);
      }
      return arrY;
    },
    createArrayOfColor(toColor){
      let arrColor = [];
      for (let j = 0; j <= this.startStopProtein['stop']; j = j + 1){
        if(toColor[j]){
          arrColor.push(toColor[j]);
        }
        else {
          arrColor.push('transparent');
        }
      }
      return arrColor;
    },
    renderGraph(met){

      let width = window.innerWidth * 0.6;
      let elem = document.getElementById(this.namePValue);
      elem.style['width'] = width + 'px';

      let len = met.length;
      let i = 0;
      let arrX = [];
      let arr_of_arrY = [];
      let arrY = [];
      for (let j = 0; j <= this.startStopProtein['stop']; j = j + 1){
        arrX.push(j.toString());
        arrY.push([j.toString(), 0, 0, 0, 0]);
      }
      arr_of_arrY.push(arrY);

      this.begin_value_domain = 0;
      this.end_value_domain = 0;

      // let maxY = 0;

      while (i < len) {
        let single_line = met[i];
        // arrX.push(single_line['name']);
        let single_cell;
        if (single_line['odds_ratio'] > this.totalMaxOddsRatio) {
          // if(Math.log(single_line['odds_ratio']) > maxY){
          //   maxY = Math.log(single_line['odds_ratio']);
          // }
          single_cell = [single_line['position'].toString(), Math.log(single_line['odds_ratio']), single_line['p_value'], 'INF', single_line['name'], single_line['value']];
        } else {
          // if(Math.log(single_line['odds_ratio']) > maxY){
          //   maxY = Math.log(single_line['odds_ratio']);
          // }
          single_cell = [single_line['position'].toString(), Math.log(single_line['odds_ratio']), single_line['p_value'], single_line['odds_ratio'], single_line['name'], single_line['value']];
        }
        // if (single_line['odds_ratio'] > this.totalMaxOddsRatio) {
        //   if(single_line['value'] > maxY){
        //     maxY = single_line['value'];
        //   }
        //   single_cell = [single_line['position'] - 1, single_line['value'], single_line['p_value'], 'INF', single_line['name']];
        // } else {
        //   if(single_line['value'] > maxY){
        //     maxY = single_line['value'];
        //   }
        //   single_cell = [single_line['position'] - 1, single_line['value'], single_line['p_value'], single_line['odds_ratio'], single_line['name']];
        // }
        let while_condition = true;
        let k = 0;
        while (while_condition) {
          let arr = arr_of_arrY[k];
          if (JSON.stringify(arr[single_line['position']].toString()) === JSON.stringify([single_line['position'], 0, 0, 0].toString())) {
            arr[single_line['position']] = single_cell;
            while_condition = false;
          } else {
            if (k + 1 >= arr_of_arrY.length) {
              arr_of_arrY.push(this.createArrayOfZeros());
              let arr2 = arr_of_arrY[k + 1];
              arr2[single_line['position']] = single_cell;
              while_condition = false;
            }
          }
          k = k + 1;
        }
        i = i + 1;
      }

      let toColor = {};
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
            color = '#A8DADC'
          }
          else{
            color = '#457B9D';
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
            return item['Description'] === that.selectedDomainForPValue[k].split(' / ')[0]
                   && item['Begin'] === parseInt(that.selectedDomainForPValue[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[0])
                  && item['End'] === parseInt(that.selectedDomainForPValue[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[1]);


          });
          if (index !== -1) {
            min = this.possibleDomainForPValue[index]['Begin'];
            max = this.possibleDomainForPValue[index]['End'];
          }

          let colors = this.color_1;

          let num_color = k%colors.length;
          let color = colors[num_color];
          color = color + '80'

          if(min !== 0 && max !== 0){
            toColor[min-1] = color;
            toColor[max-1] = color;
          }

          let singleMarkArea = [{
            xAxis: min - 0.5,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max + 0.5
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
            return item['Description'] === that.selectedDomainForPValueMutagenesis[k].split(' / ')[0]
                   && item['Begin'] === parseInt(that.selectedDomainForPValueMutagenesis[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[0])
                   && item['End'] === parseInt(that.selectedDomainForPValueMutagenesis[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[1]);


          });
          if (index !== -1) {
            min = this.possibleDomainForPValueMutagenesis[index]['Begin'];
            max = this.possibleDomainForPValueMutagenesis[index]['End'];
          }

          let colors = this.color_2;

          let num_color = k%colors.length;
          let color = colors[num_color];
          color = color + '80'

          if(min !== 0 && max !== 0){
            toColor[min-1] = color;
            toColor[max-1] = color;
          }

          let singleMarkArea = [{
            xAxis: min - 0.5,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max + 0.5
          }];

          this.barChart.series[0].markArea.data.push(singleMarkArea);
        }
      }

      if(this.selectedDomainForPValueAaModifications.length > 0){
        for(let k = 0; k < this.selectedDomainForPValueAaModifications.length; k = k + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValueAaModifications.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValueAaModifications[k].split(' / ')[0]
                    && item['Begin'] === parseInt(that.selectedDomainForPValueAaModifications[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[0])
                    && item['End'] === parseInt(that.selectedDomainForPValueAaModifications[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[1]);

          });
          if (index !== -1) {
            min = this.possibleDomainForPValueAaModifications[index]['Begin'];
            max = this.possibleDomainForPValueAaModifications[index]['End'];
          }

          // let colors = this.color_3;
          //
          // let num_color = k%colors.length;
          // let color = colors[num_color];
          let color = '#FFA50080'

          if(min !== 0 && max !== 0){
            toColor[min-1] = color;
            toColor[max-1] = color;
          }

          let singleMarkArea = [{
            xAxis: min - 0.5,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max + 0.5
          }];

          this.barChart.series[0].markArea.data.push(singleMarkArea);

        }
      }

      if(this.selectedDomainForPValueUploaded.length > 0){
        for(let k = 0; k < this.selectedDomainForPValueUploaded.length; k = k + 1) {
          let that = this;
          let min = 0;
          let max = 0;
          let index = this.possibleDomainForPValueUploaded.findIndex(function (item) {
            return item['Description'] === that.selectedDomainForPValueUploaded[k].split(' / ')[0]
                    && item['Begin'] === parseInt(that.selectedDomainForPValueUploaded[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[0])
                    && item['End'] === parseInt(that.selectedDomainForPValueUploaded[k].split(' / ')[1].replace('(', '').replace(')', '').split(',')[1]);

          });
          if (index !== -1) {
            min = this.possibleDomainForPValueUploaded[index]['Begin'];
            max = this.possibleDomainForPValueUploaded[index]['End'];
          }

          let colors = this.color_3;

          let num_color = k%colors.length;
          let color = colors[num_color];
          color = color + '80';

          if(min !== 0 && max !== 0){
            toColor[min-1] = color;
            toColor[max-1] = color;
          }

          let singleMarkArea = [{
            xAxis: min - 0.5,
            itemStyle: {
              color: color,
            },
          }, {
            xAxis: max + 0.5
          }];

          this.barChart.series[0].markArea.data.push(singleMarkArea);

        }
      }

      // this.barChart.yAxis.max = maxY * 1.5;
      // this.barChart.xAxis.max = this.startStopProtein['stop'];
      // this.barChart.xAxis.data = arrX;
      // this.barChart.xAxis.splitArea.areaStyle.color = this.createArrayOfColor(toColor);

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
      else{
        this.my_chart.dispose();
        this.my_chart = echarts.init(document.getElementById(this.namePValue));
      }
      console.log("qui", this.barChart);
      this.my_chart.setOption(this.barChart, true);
      let my_c = document.getElementById(this.namePValue);
      my_c.click();

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
    },
    renderGraphSinglePosition(met){

      this.dialog_single_position = true;
      let elem = document.getElementById(this.namePValue + '_single_position');
      elem.style['width'] = 450 + 'px';

      let len = met.length;
      let arrX = [];
      let arrY = [];
      for (let j = 0; j < len; j++){
        arrX.push(met[j]['name'].split('_')[1]);
        // arrY.push([met[j]['name'], met[j]['odds_ratio'], met[j]['p_value']]);
        arrY.push(Math.log(met[j]['odds_ratio']));
      }

      this.barChartSinglePosition.series[0]['data'] = arrY;
      this.barChartSinglePosition.xAxis.data = arrX;

      if(this.my_chart_single_position === null) {
        this.my_chart_single_position = echarts.init(document.getElementById(this.namePValue + '_single_position'));
      }
      else{
        this.my_chart_single_position.dispose();
        this.my_chart_single_position = echarts.init(document.getElementById(this.namePValue + '_single_position'));
      }
      this.my_chart_single_position.setOption(this.barChartSinglePosition, true);
    }
  },
  mounted() {
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      this.renderGraph(met);
  },
  watch: {
    params(){
      if(this.params !== null) {
        this.dialog_single_position = true;
        this.single_position = this.params['data'][0];
        let filtered_value = this.pValueContent.filter(x => x.position === parseInt(this.params['data'][0]));

        let delayInMilliseconds = 100;
        let that = this;
        setTimeout(function() {
          that.renderGraphSinglePosition(filtered_value);
        }, delayInMilliseconds);
      }
    },
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
    selectedDomainForPValueAaModifications(){
      let met =  JSON.parse(JSON.stringify(this.pValueContent));
      let delayInMilliseconds = 2000;

      let that = this;
      setTimeout(function() {
        that.renderGraph(met);
      }, delayInMilliseconds);
    },
    selectedDomainForPValueUploaded(){
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
          // else{
          //   this.my_chart.dispose();
          //   this.my_chart = echarts.init(document.getElementById(this.namePValue));
          // }
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
          // else{
          //   this.my_chart.dispose();
          //   this.my_chart = echarts.init(document.getElementById(this.namePValue));
          // }
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
          // else{
          //   this.my_chart.dispose();
          //   this.my_chart = echarts.init(document.getElementById(this.namePValue));
          // }
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
          // else{
          //   this.my_chart.dispose();
          //   this.my_chart = echarts.init(document.getElementById(this.namePValue));
          // }
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
          // else{
          //   this.my_chart.dispose();
          //   this.my_chart = echarts.init(document.getElementById(this.namePValue));
          // }
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
          // else{
          //   this.my_chart.dispose();
          //   this.my_chart = echarts.init(document.getElementById(this.namePValue));
          // }
          this.my_chart.setOption(this.barChart, true);
        }
      }
    }
  }
}
</script>

<style scoped>

</style>