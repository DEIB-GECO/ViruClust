<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; margin-top: 50px;  z-index: 1">
          </div>
        </v-row>
    </v-container>
    <!--<v-container fluid grid-list-xl style="justify-content: center;
    background-color: white; z-index: 3; width: 100%; position: relative">
      <v-row justify="center" align="center" style="z-index: 3">
        <div id="background_slider" style="width: 60%; height:30px; background-color: red;
        position: absolute; top: -20px; left: 10%; opacity: 50%; z-index: 3">
        </div>
        <div id="target_slider" style="width: 20%; height:30px; background-color: blue;
        position: absolute; top: -20px; left: 70%; opacity: 50%; z-index: 3">
        </div>
      </v-row>
    </v-container> -->
    <v-container fluid grid-list-xl style="justify-content: center;
    background-color: white; width: 100%">
      <v-row justify="center" align="center">
<!--        <v-flex class="no-horizontal-padding xs1 d-flex" style="justify-content: center;">-->
<!--          <v-btn-->
<!--                style="margin-bottom: 20px; margin-left: 50px"-->
<!--                class="white&#45;&#45;text"-->
<!--                x-small-->
<!--                color="red"-->
<!--                :disabled="background_slider[0] === 0"-->
<!--                @click="addSubSliders('background_slider', 'minus')"-->
<!--            >-->
<!--              <v-icon>mdi-minus</v-icon>-->
<!--            </v-btn>-->
<!--        </v-flex>-->
        <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0">
          <div style="width: 100%; ; z-index: 3">
            <v-range-slider
                v-model="background_slider"
                min = "0"
                :max = "max_range"
                color="red"
                track-color="grey"
                height="2px"
              >
            </v-range-slider>
          </div>
        </v-flex>
        <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0; margin-top: 20px">
          <div style="width: 100%; ; z-index: 3;">
            <v-range-slider
              v-model="target_slider"
              min = "0"
              :max = "max_range"
              color="blue"
              track-color="grey"
              height="2px"
            >
            </v-range-slider>
          </div>
        </v-flex>
      </v-row>
    </v-container>
    <v-container fluid grid-list-xl style="justify-content: center;
  background-color: white; width: 100%">
      <v-row justify="center" align="center">
        <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
          <v-card style="width: 80%; margin: 20px" color="rgba(255, 0, 0, 0.5)">
            <v-card-title class="justify-center">
              BACKGROUND
            </v-card-title>
            <v-card-text>
              <v-layout row wrap justify-center style="padding: 30px;">
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3># SEQUENCES: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    :value = "num_sequences_background"
                    solo
                    readonly
                    hide-details
                    class = "centered-input"
                  ></v-text-field>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 20px">
                  <h3>START BACKGROUND: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;
                 padding: 0; position: relative">
                  <v-text-field
                    v-model = "startBackgroundField"
                    solo
                    hide-details
                    class = "centered-input"
                  >
                    <template v-slot:append>
                      <v-icon v-if="wrongDateStartBackground"
                              color="red">
                        mdi-close-circle
                      </v-icon>
                      <v-icon v-else
                              color="green">
                        mdi-checkbox-marked-circle
                      </v-icon>
                    </template>
                  </v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <span> (write correct date in correct format YYYY-MM-DD) </span>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 20px">
                  <h3>STOP BACKGROUND: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    v-model = "stopBackgroundField"
                    solo
                    hide-details
                    class = "centered-input"
                  >
                    <template v-slot:append>
                      <v-icon v-if="wrongDateStopBackground"
                              color="red">
                        mdi-close-circle
                      </v-icon>
                      <v-icon v-else
                              color="green">
                        mdi-checkbox-marked-circle
                      </v-icon>
                    </template>
                  </v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <span> (write correct date in correct format YYYY-MM-DD) </span>
                </v-flex>

              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
          <v-card style="width: 80%; margin: 20px" color="rgba(0, 0, 255, 0.5)">
            <v-card-title class="justify-center">
              TARGET
            </v-card-title>
            <v-card-text>
                      <v-layout row wrap justify-center style="padding: 30px;">
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3># SEQUENCES: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    :value = "num_sequences_target"
                    solo
                    readonly
                    hide-details
                    class = "centered-input"
                  ></v-text-field>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 20px">
                  <h3>START TARGET: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    v-model = "startTargetField"
                    solo
                    hide-details
                    class = "centered-input"
                  >
                    <template v-slot:append>
                      <v-icon v-if="wrongDateStartTarget"
                              color="red">
                        mdi-close-circle
                      </v-icon>
                      <v-icon v-else
                              color="green">
                        mdi-checkbox-marked-circle
                      </v-icon>
                    </template>
                  </v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <span> (write correct date in correct format YYYY-MM-DD) </span>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin-top: 20px">
                  <h3>STOP TARGET: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    v-model = "stopTargetField"
                    solo
                    hide-details
                    class = "centered-input"
                  >
                    <template v-slot:append>
                      <v-icon v-if="wrongDateStopTarget"
                              color="red">
                        mdi-close-circle
                      </v-icon>
                      <v-icon v-else
                              color="green">
                        mdi-checkbox-marked-circle
                      </v-icon>
                    </template>
                  </v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <span> (write correct date in correct format YYYY-MM-DD) </span>
                </v-flex>

              </v-layout>

            </v-card-text>
          </v-card>
        </v-flex>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "TimeDistributionChart",
  props: {
    timeName: {required: true,},
    timeContent: {required: true,},
    filterDate: {required: true},
  },
  data(){
    return {
      background_slider: [0, 500],
      target_slider: [500, 1500],
      left_ranges_width:  10,
      total_ranges_width: 80,
      max_range: 0,
      num_sequences_background: 0,
      num_sequences_target: 0,
      startBackgroundField: 0,
      stopBackgroundField: 0,
      startTargetField: 0,
      stopTargetField: 0,
      wrongDateStartBackground: false,
      wrongDateStopBackground: false,
      wrongDateStartTarget: false,
      wrongDateStopTarget: false,

      options_slider: {
        enableCross: false
      },
      barChart: {
        title: {
        },
        tooltip: {
            trigger: 'item',
        },
        series: [
            {
                type: 'bar',
                radius: '50%',
                data: [],
                itemStyle: {color: 'rgb(72,72,72)'},
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
                            color: 'rgba(255, 0, 0, 0.5)',
                        },
                    }, {
                        xAxis: 0
                    }], [{
                        xAxis: 0,
                        itemStyle: {
                            color: 'rgba(0, 0, 255, 0.5)'
                        },
                    }, {
                        xAxis: 0
                    }] ]
                }
            }
        ],
        xAxis: {
            type: 'category',
            data: [],
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
    ...mapMutations(['setTimeRangesTargetAndBackground']),
    ...mapActions([]),
    renderGraphFilterDate(){
      if(this.filterDate === 'Month'){
        let met =  JSON.parse(JSON.stringify(this.timeContent));
        let new_met = [];

        let len = met.length;
        let i = 0;

        while(i < len){
          let single_line = met[i];
          let dt1 = single_line['name'];
          let p1 = dt1.split("-");
          let date2 = p1[0] + "-" + p1[1];
          let found = false;

          for(let j in new_met){
              let line_new = new_met[j];
              if(line_new['name'] === date2){
                found = true;
                line_new['value'] = line_new['value'] + single_line['value'];
              }
          }

          if(!found){
            let line = {'name': date2, 'value':single_line['value']};
            new_met.push(line);
          }

          i = i + 1;
        }
        this.renderGraph(new_met);
      }
      else if(this.filterDate === 'Year') {
        let met =  JSON.parse(JSON.stringify(this.timeContent));
        let new_met = [];

        let len = met.length;
        let i = 0;

        while(i < len){
          let single_line = met[i];
          let dt1 = single_line['name'];
          let p1 = dt1.split("-");
          let date2 = p1[0];
          let found = false;

          for(let j in new_met){
              let line_new = new_met[j];
              if(line_new['name'] === date2){
                found = true;
                line_new['value'] = line_new['value'] + single_line['value'];
              }
          }

          if(!found){
            let line = {'name': date2, 'value':single_line['value']};
            new_met.push(line);
          }

          i = i + 1;
        }
        this.renderGraph(new_met);

      }
      else if(this.filterDate === 'Day') {
        let met =  JSON.parse(JSON.stringify(this.timeContent));
        this.renderGraph(met);
      }
    },
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
        this.my_chart = echarts.init(document.getElementById(this.timeName));
      }
      this.my_chart.setOption(this.barChart, true);
    },
    changeMarkerAndRender(min1, max1, min2, max2){
      this.barChart.series[0].markArea.data[0][0].xAxis = min1;
      this.barChart.series[0].markArea.data[0][1].xAxis = max1;
      this.barChart.series[0].markArea.data[1][0].xAxis = min2;
      this.barChart.series[0].markArea.data[1][1].xAxis = max2;

      this.startBackgroundField = this.translateIndexToDate(min1);
      this.stopBackgroundField = this.translateIndexToDate(max1);
      this.startTargetField= this.translateIndexToDate(min2);
      this.stopTargetField= this.translateIndexToDate(max2);

      let lenXAxis = this.timeContent.length;
      let i = 0;
      this.num_sequences_background = 0;
      this.num_sequences_target = 0;

      while(i < lenXAxis){
        if( i >= min1 && i <= max1 ){
          this.num_sequences_background = this.num_sequences_background + this.timeContent[i].value;
        }
        else if( i > min2 && i <= max2 ){
          this.num_sequences_target = this.num_sequences_target + this.timeContent[i].value;
        }
        i = i + 1;
      }

      this.renderGraphFilterDate();
    },
    translateIndexToDate(index){
      return this.timeContent[index].name;
    },
    translateDateToIndex(date){
      let index = this.timeContent.findIndex(function(item){
        return item.name === date;
      });
      return index;
    },
  },
  watch: {
    timeContent(){
      this.renderGraphFilterDate();
    },
    filterDate(){
      this.renderGraphFilterDate();
    },
    startBackgroundField(){
      this.wrongDateStartBackground = false;
      let start = this.translateDateToIndex(this.startBackgroundField);
      if (start === -1 || start > this.background_slider[1]){
        this.wrongDateStartBackground  = true;
      }
      else {
        let stop = this.background_slider[1];
        this.background_slider = [start, stop];
      }
    },
    stopBackgroundField(){
      this.wrongDateStopBackground = false;
      let stop = this.translateDateToIndex(this.stopBackgroundField);
      if (stop === -1 || stop < this.background_slider[0] || stop > this.target_slider[0]){
        this.wrongDateStopBackground = true;
      }
      else {
        let start = this.background_slider[0];
        this.background_slider = [start, stop];
      }
    },
    startTargetField(){
      this.wrongDateStartTarget = false;
      let start = this.translateDateToIndex(this.startTargetField);
      if (start === -1 || start < this.background_slider[1] || start > this.target_slider[1]){
        this.wrongDateStartTarget = true;
      }
      else {
        let stop = this.target_slider[1];
        this.target_slider = [start, stop];
      }
    },
    stopTargetField(){
      this.wrongDateStopTarget = false;
      let stop = this.translateDateToIndex(this.stopTargetField);
      if (stop === -1 || stop < this.target_slider[0]){
        this.wrongDateStopTarget = true;
      }
      else {
        let start = this.target_slider[0];
        this.target_slider = [start, stop];
      }
    },
    background_slider(){
      if(this.target_slider[0] < this.background_slider[1]){
        this.background_slider[1] = this.target_slider[0];
      }
      // let elem = document.getElementById('background_slider');
      //
      // let min_value = this.background_slider[0];
      // let max_value = this.background_slider[1];
      //
      // let min = (100 * min_value) / this.max_range;
      // let max = (100 * max_value) / this.max_range;
      //
      // let start_background = ((min*this.total_ranges_width)/ 100) + this.left_ranges_width;
      // let stop_background = ((max-min)*this.total_ranges_width)/ 100;
      // elem.style.width = stop_background + "%";
      // elem.style.left = start_background + "%";

      this.changeMarkerAndRender(this.background_slider[0], this.background_slider[1],
          this.target_slider[0], this.target_slider[1]);

      let timeRanges = {
        'start_background_time': this.timeContent[this.background_slider[0]].name,
        'end_background_time': this.timeContent[this.background_slider[1]].name,
        'start_target_time': this.timeContent[this.target_slider[0]].name,
        'end_target_time': this.timeContent[this.target_slider[1]].name,
      }
      this.setTimeRangesTargetAndBackground(timeRanges);
    },
    target_slider(){
      if(this.background_slider[1] > this.target_slider[0]){
        this.target_slider[0] = this.background_slider[1];
      }
      // let elem = document.getElementById('target_slider');
      //
      // let min_value = this.target_slider[0];
      // let max_value = this.target_slider[1];
      //
      // let min = (100 * min_value) / this.max_range;
      // let max = (100 * max_value) / this.max_range;
      //
      // let start_target = ((min*this.total_ranges_width)/ 100) + this.left_ranges_width;
      // let stop_target = ((max-min)*this.total_ranges_width)/ 100;
      // elem.style.width = stop_target + "%";
      // elem.style.left = start_target + "%";

       this.changeMarkerAndRender(this.background_slider[0], this.background_slider[1],
          this.target_slider[0], this.target_slider[1]);

       let timeRanges = {
        'start_background_time': this.timeContent[this.background_slider[0]].name,
        'end_background_time': this.timeContent[this.background_slider[1]].name,
        'start_target_time': this.timeContent[this.target_slider[0]].name,
        'end_target_time': this.timeContent[this.target_slider[1]].name,
      }
      this.setTimeRangesTargetAndBackground(timeRanges);
    }
  },
  mounted() {

      this.max_range = this.timeContent.length - 1;

      let val = "2021-03-31"
      let index = this.timeContent.findIndex(function(item){
        return item.name === val
      });
      if (index === -1){
        index = Math.floor(this.max_range / 2);
      }

      this.background_slider[0] = 0;
      this.background_slider[1] = index;
      this.target_slider[0] = index;
      this.target_slider[1] = this.max_range;

      this.changeMarkerAndRender(0, index, index, this.max_range);
  },
}
</script>

<style scoped>

  /deep/ .centered-input input {
    text-align: center
  }
</style>