<template>
  <div style="width: 95%">
    <v-container fluid grid-list-xl style="justify-content: center; text-align: center; z-index: 1;">
        <v-layout row wrap justify-center>
           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 50px;">
                <h2 style="text-align: center"># GENOMES BY COLLECTION DATE </h2>
                <v-btn @click="download" x-small icon
                      style="margin-left: 20px; margin-bottom: 5px">
                        <v-icon size="23">
                          mdi-download-circle-outline
                        </v-icon>
               </v-btn>
           </v-flex>
        </v-layout>
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; margin-top: 50px; z-index: 1">
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
<!--                color="#E63946"-->
<!--                :disabled="background_slider[0] === 0"-->
<!--                @click="addSubSliders('background_slider', 'minus')"-->
<!--            >-->
<!--              <v-icon>mdi-minus</v-icon>-->
<!--            </v-btn>-->
<!--        </v-flex>-->
        <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0">
          <div style="width: 100%; z-index: 3">
            <v-range-slider
                v-model="background_slider"
                min = "0"
                :max = "max_range"
                color="#F48C0680"
                track-color="grey"
                height="2px"
                hide-details
              >
            </v-range-slider>
          </div>
        </v-flex>
        <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0; margin-top: 30px">
          <div style="width: 100%; z-index: 3;">
            <v-range-slider
              v-model="target_slider"
              min = "0"
              :max = "max_range"
              color="#DC2F0280"
              track-color="grey"
              height="2px"
              hide-details
            >
            </v-range-slider>
          </div>
        </v-flex>
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0">
        </v-flex>
        <v-flex class="no-horizontal-padding xs12 md6 d-flex" style="justify-content: center; margin: 0; padding: 0">
            <v-checkbox v-model="isStartTargetStopBackground"
            label="Start Target = Stop Background + 1"
            input-value="true"
            hide-details>
            </v-checkbox>
        </v-flex>
      </v-row>
    </v-container>
    <v-container fluid grid-list-xl style="justify-content: center;
  background-color: white; width: 100%; padding-bottom: 50px;">
      <v-row justify="center" align="center">
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
          <v-card style="width: 80%;" color="#F48C0680">
            <v-card-text>
              <v-layout row wrap justify-center>
                <v-flex class="no-horizontal-padding xs12 md12 lg4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; margin-top: 10px;">
                      <h3 style="text-align: center">BACKGROUND NUM SEQUENCES: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "num_sequences_background"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <div style="color: #F48C0680 "> . </div>
                    </v-flex>
                  </v-layout>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 md6 lg4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; margin-top: 10px">
                      <h3 style="text-align: center">START BACKGROUND: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; position: relative">
                      <v-text-field
                        v-model = "startBackgroundField"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                        <template v-slot:append>
                          <v-icon v-if="wrongDateStartBackground"
                                  color="#E63946">
                            mdi-close-circle
                          </v-icon>
                          <v-icon v-else
                                  color="#1D3557">
                            mdi-checkbox-marked-circle
                          </v-icon>
                        </template>
                      </v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <span style="text-align: center"> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>


                <v-flex class="no-horizontal-padding xs12 md6 lg4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; margin-top: 10px">
                      <h3 style="text-align: center">END BACKGROUND: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        v-model = "stopBackgroundField"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                        <template v-slot:append>
                          <v-icon v-if="wrongDateStopBackground"
                                  color="#E63946">
                            mdi-close-circle
                          </v-icon>
                          <v-icon v-else
                                  color="#1D3557">
                            mdi-checkbox-marked-circle
                          </v-icon>
                        </template>
                      </v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <span style="text-align: center"> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>

              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
          <v-card style="width: 80%;" color="#DC2F0280">
            <v-card-text>
              <v-layout row wrap justify-center>
                <v-flex class="no-horizontal-padding xs12 md12 lg4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; margin-top: 10px;">
                      <h3 style="text-align: center">TARGET NUM SEQUENCES: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "num_sequences_target"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <div style="color: #DC2F0280 "> . </div>
                    </v-flex>
                  </v-layout>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 md6 lg4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; margin-top: 10px">
                      <h3 style="text-align: center">START TARGET: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        v-model = "startTargetField"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                        <template v-slot:append>
                          <v-icon v-if="wrongDateStartTarget"
                                  color="#E63946">
                            mdi-close-circle
                          </v-icon>
                          <v-icon v-else
                                  color="#1D3557">
                            mdi-checkbox-marked-circle
                          </v-icon>
                        </template>
                      </v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <span style="text-align: center"> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>

                <v-flex class="no-horizontal-padding xs12 md6 lg4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-center>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0; margin-top: 10px">
                      <h3 style="text-align: center">END TARGET: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        v-model = "stopTargetField"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                        <template v-slot:append>
                          <v-icon v-if="wrongDateStopTarget"
                                  color="#E63946">
                            mdi-close-circle
                          </v-icon>
                          <v-icon v-else
                                  color="#1D3557">
                            mdi-checkbox-marked-circle
                          </v-icon>
                        </template>
                      </v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <span style="text-align: center"> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
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

      min_num_seq_target: 50,
      min_num_seq_background: 50,
      isStartTargetStopBackground: false,

      options_slider: {
        enableCross: false
      },
      barChart: {
        title: {
        },
        tooltip: {
            trigger: 'item',
        },
        legend: {
          data: ['Time distribution', 'AVG of previous 7 days'],
          top: '20px',
          selectedMode: false,
          itemGap: 50,
        },
        series: [
            {
                name: 'Time distribution',
                type: 'bar',
                radius: '50%',
                data: [],
                itemStyle: {color: '#1D3557'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: '#1D3557'
                    }
                },
                markArea: {
                    tooltip: {
                        show: false,
                    },
                    data: [ [{
                        xAxis: 0,
                        itemStyle: {
                            color: '#F48C0680',
                        },
                    }, {
                        xAxis: 0
                    }], [{
                        xAxis: 0,
                        itemStyle: {
                            color: '#DC2F0280'
                        },
                    }, {
                        xAxis: 0
                    }] ]
                }
            },
            {
                name: 'AVG of previous 7 days',
                type: 'line',
                data: [],
                color: '#1D3557',
            },
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
    ...mapState(['queryTime']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setTimeRangesTargetAndBackground', 'setTrueErrorNumSeqQueryTime', 'setFalseErrorNumSeqQueryTime']),
    ...mapActions([]),
    download(){
      let url = this.my_chart.getConnectedDataURL({
          pixelRatio: 2,
          backgroundColor: 'white'
      });
      let $a = document.createElement('a');
      let type = 'png';
      let filename = 'temporal_analysis_timeDistribution2Periods';
        if(this.queryTime['lineage']){
          filename += '_' + this.queryTime['lineage'];
        }
        if (!this.queryTime['geo_group']) {
          filename += '_World';
        } else if (!this.queryTime['country']) {
          filename += '_' + this.queryTime['geo_group'];
        } else if (!this.queryTime['region']) {
          filename += '_' + this.queryTime['country'];
        } else if (!this.queryTime['province']) {
          filename += '_' + this.queryTime['region'];
        } else {
          filename += '_' + this.queryTime['province'];
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
      let arrYLine = [];
      while (i < len){
        let single_line = met[i];
        let sum = 0;
        if (i - 7 > 0){
          for (let j = 8; j > 0; j = j - 1){
            sum = sum + parseInt(met[i-j]['value']);
          }
        }
        arrYLine.push((sum/7).toFixed(3));
        arrX.push(single_line['name']);
        arrY.push(single_line['value']);
        i = i + 1;
      }

      this.barChart.series[0].data = arrY;
      this.barChart.series[1].data = arrYLine;
      this.barChart.xAxis.data = arrX;

      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.timeName));
      }
      else{
        this.my_chart.dispose();
        this.my_chart = echarts.init(document.getElementById(this.timeName));
      }
      this.my_chart.setOption(this.barChart, true);
    },
    changeMarkerAndRender(min1, max1, min2, max2){

      if(min1 === max1 || max1 === min2 - 1){
        if(max1 < this.max_range) {
          this.barChart.series[0].markArea.data[0][0].xAxis = min1;
          this.barChart.series[0].markArea.data[0][1].xAxis = max1 + 1;
        }
        else{
          this.barChart.series[0].markArea.data[0][0].xAxis = min1 - 1;
          this.barChart.series[0].markArea.data[0][1].xAxis = max1;
        }
      }
      else{
        this.barChart.series[0].markArea.data[0][0].xAxis = min1;
        this.barChart.series[0].markArea.data[0][1].xAxis = max1;
      }

      if(min2 === max2){
        if(max2 < this.max_range) {
          this.barChart.series[0].markArea.data[1][0].xAxis = min2;
          this.barChart.series[0].markArea.data[1][1].xAxis = max2 + 1;
        }
        else{
          this.barChart.series[0].markArea.data[1][0].xAxis = min2 - 1;
          this.barChart.series[0].markArea.data[1][1].xAxis = max2;
        }
      }
      else{
        this.barChart.series[0].markArea.data[1][0].xAxis = min2;
        this.barChart.series[0].markArea.data[1][1].xAxis = max2;
      }

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
        else if( i >= min2 && i <= max2 ){
          this.num_sequences_target = this.num_sequences_target + this.timeContent[i].value;
        }
        i = i + 1;
      }

      if (this.num_sequences_target < this.min_num_seq_target || this.num_sequences_background < this.min_num_seq_background){
        this.setTrueErrorNumSeqQueryTime();
      }
      else{
        this.setFalseErrorNumSeqQueryTime();
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
    isStartTargetStopBackground(){
      let start = this.translateDateToIndex(this.startTargetField);
      let startBackground = this.background_slider[0];
      this.background_slider = [startBackground, start - 1];
    },
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
      if (stop === -1 || stop < this.background_slider[0] || (stop >= this.target_slider[0] && !this.isStartTargetStopBackground)){
        this.wrongDateStopBackground = true;
      }
      else {
        let start = this.background_slider[0];
        this.background_slider = [start, stop];
        if(this.isStartTargetStopBackground) {
          let stopTarget = this.target_slider[1];
          this.target_slider = [stop + 1, stopTarget];
        }
      }
    },
    startTargetField(){
      this.wrongDateStartTarget = false;
      let start = this.translateDateToIndex(this.startTargetField);
      if (start === -1 || (start <= this.background_slider[1] && !this.isStartTargetStopBackground) || start > this.target_slider[1]){
        this.wrongDateStartTarget = true;
      }
      else {
        let stop = this.target_slider[1];
        this.target_slider = [start, stop];
        if(this.isStartTargetStopBackground) {
          let startBackground = this.background_slider[0];
          this.background_slider = [startBackground, start - 1];
        }
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
      if(this.target_slider[0] <= this.background_slider[1] && !this.isStartTargetStopBackground){
        this.background_slider[1] = this.target_slider[0] - 1;
      }

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
      if(this.background_slider[1] >= this.target_slider[0] && !this.isStartTargetStopBackground){
        this.target_slider[0] = this.background_slider[1] + 1;
      }

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
      this.setFalseErrorNumSeqQueryTime();
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
      this.target_slider[0] = index + 1;
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