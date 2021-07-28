<template>
  <div style="position: relative;">
    <v-container fluid grid-list-xl style="justify-content: center; text-align: center; z-index: 1; width: 1500px">
        <h2 style="margin-top: 50px;">TIME DISTRIBUTION <v-btn @click="download" x-small icon
            style="margin-left: 20px; margin-bottom: 5px">
              <v-icon size="23">
                mdi-download-circle-outline
              </v-icon>
         </v-btn></h2>
        <v-layout row wrap justify-center style="background-color: white; margin-top: 30px; padding-top: 30px; padding-left: 15%; padding-right: 15%;">

          <v-btn-toggle v-model="perc_or_absolute_num_exclusive" mandatory color="black">
            <v-btn small>
              <span>NUM SEQUENCES</span>
            </v-btn>

            <v-btn small>
              <span>% SEQUENCES</span>
            </v-btn>
          </v-btn-toggle>

          <v-spacer></v-spacer>

          <v-btn-toggle v-model="view_exclusive" mandatory color="black">
            <v-btn small>
              <span>SHOW <span style="color: #323F8B">TARGET</span></span>
            </v-btn>

            <v-btn small>
              <span>SHOW <span style="color: #9F3255">BACKGROUND</span></span>
            </v-btn>

            <v-btn small>
              <span>SHOW <span style="color: #323F8B">BO</span><span style="color: #9F3255">TH</span></span>
            </v-btn>
          </v-btn-toggle>

        </v-layout>
        <v-row justify="center" align="center" style="z-index: 1; margin-top: 0">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; margin-top: 0; z-index: 1">
          </div>
        </v-row>
    </v-container>


    <div v-if="overlay" style="position: absolute; top: 200px; left:40%; width: 20%; height: 20%">
      <v-img
          src="../images/loading.gif"
          style="z-index: 1;"
      />
    </div>

    <v-container fluid grid-list-xl style="justify-content: center;
    background-color: white; width: 100%">
      <v-row justify="center" align="center">
        <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0">
          <div style="width: 100%; ; z-index: 3">
            <v-range-slider
                v-model="slider"
                min = "0"
                :max = "max_range"
                color="#F48C06"
                track-color="grey"
                height="2px"
              >
            </v-range-slider>
          </div>
        </v-flex>
        <v-flex class="no-horizontal-padding xs8 d-flex" style="justify-content: center;">
          <v-layout row wrap justify-center style="">
            <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
              <v-select
                v-model="selectedTarget"
                :items="possibleTarget"
                label="Target"
                solo
                hide-details>
             </v-select>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-row>
    </v-container>
    <v-container fluid grid-list-xl style="justify-content: center;
  background-color: white; width: 100%">
      <v-row justify="center" align="center">
        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;">
          <v-card style="width: 100%; margin-bottom: 20px" color="#F48C0680">
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 20px; padding-top: 5px">
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <h3>TARGET: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "target_name"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <h3>NUM SEQUENCES TARGET: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "num_sequences_target[targetIndex]"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>


        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;">
          <v-card style="width: 100%; margin-bottom: 20px" color="#F48C0680">
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 20px; padding-top: 5px">
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <h3>BACKGROUND: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "background_name"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <h3>NUM SEQUENCES BACKGROUND: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "num_sequences_background[targetIndex]"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin: 0; padding: 0" v-if="listLocationExcluded.length > 0">
                  * Location excluded from background : {{listLocationExcluded}}
                </v-flex>
            </v-card-text>
          </v-card>
        </v-flex>


        <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;">
          <v-card style="width: 100%; margin-bottom: 20px" color="#F48C0680">
            <v-card-title class="justify-center" style="margin: 0; padding: 0; margin-top: 5px !important;">
              TIME FILTER
            </v-card-title>
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 10px;">
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <h3>START: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <v-text-field
                        v-model = "last_start_date"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                         <template v-slot:append>
                            <v-icon v-if="wrong_last_start_date"
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
                      <span> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <h3>END: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <v-text-field
                        v-model = "last_stop_date"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                        <template v-slot:append>
                            <v-icon v-if="wrong_last_stop_date"
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
                      <span> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>

      </v-row>
    </v-container>

<!--    <v-overlay :value="overlay">-->
<!--      <v-progress-circular-->
<!--        indeterminate-->
<!--        size="64"-->
<!--      ></v-progress-circular>-->
<!--    </v-overlay>-->

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";
import axios from "axios";

export default {
  name: "TimeSelectorQueryGeo",
  props: {
    timeName: {required: true,},
    filterDate: {required: true},
  },
  data(){
    return {
      targetIndex: 0,
      possibleTarget: [],
      selectedTarget: null,

      view_exclusive: 2,
      perc_or_absolute_num_exclusive: 0,

      startDateMultiMinor: null,
      locationToExclude: [],

      listLocationExcluded: [],

      overlay: false,
      slider: [0, 1500],
      left_ranges_width:  10,
      total_ranges_width: 80,
      max_range: 0,
      timeContent: [],
      last_start_date: null,
      last_stop_date: null,
      num_sequences_target: [],
      num_sequences_background: [],
      wrong_last_start_date: false,
      wrong_last_stop_date: false,

      min_num_seq_target: 10,
      min_num_seq_background: 10,
      target_name: 'World',
      background_name: 'World',

      timeContentBackground: [],

      viewBackground: false,
      viewTarget: false,
      viewBothTargetBackground: true,

      graphOnNumSequences: true,
      graphOnPercSequences: false,

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
          data: ['Target', 'Background', 'AVG of previous 7 days in target', 'AVG of previous 7 days in background'],
          top: '20px',
          selectedMode: false,
          itemGap: 50,
        },
        series: [
            {
                type: 'bar',
                name: 'Background',
                radius: '50%',
                data: [],
                itemStyle: {color: '#9F3255'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: '#9F3255'
                    }
                },
            },
            {
                type: 'bar',
                name: 'Target',
                radius: '50%',
                data: [],
                itemStyle: {color: '#323F8B'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: '#323F8B'
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
                      }]
                      ]
                  }
            },
            {
                name: 'AVG of previous 7 days in target',
                type: 'line',
                data: [],
                color: '#323F8B',
            },
            {
                name: 'AVG of previous 7 days in background',
                type: 'line',
                data: [],
                color: '#9F3255',
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
    ...mapState(['queryGeo', 'startDateQueryGeo', 'stopDateQueryGeo', 'numLevelAboveBackground', 'toExcludeGeo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setTimeRangesTargetAndBackground', 'setStartDateQueryGeo', 'setStopDateQueryGeo',
     'setTrueErrorNumSeqQueryGeo', 'setFalseErrorNumSeqQueryGeo', 'setLocationToExcludeMulti']),
    ...mapActions(['setQueryGeo']),
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
    getDaysArray(start, end) {
      for (var arr = [], dt = new Date(start); dt <= end; dt.setDate(dt.getDate() + 1)) {
        let date = new Date(dt).toISOString().slice(0, 10);
        if(!arr.includes(date)) {
          arr.push(date);
        }
        if( date.indexOf('-10-24') !== -1){
          let date2 = new Date(date);
          date2.setDate(date2.getDate() + 1)
          let date3 = new Date(date2).toISOString().slice(0, 10);
          arr.push(date3);
        }
      }
      return arr;
    },
    renderGraphFilterDate(){
        let met =  JSON.parse(JSON.stringify(this.timeContent[this.targetIndex]));
        let met2 =  JSON.parse(JSON.stringify(this.timeContentBackground[this.targetIndex]));
        this.renderGraph(met, met2);
    },
    renderGraph(met, met2){

      let len = met.length;
      let i = 0;
      let arrX = [];
      let arrYBackground = [];
      let arrYTarget = [];
      let arrYLineTarget = [];
      let arrYLineBackground = [];
      let total_target = 0;
      let total_background = 0;
      while (i < len){
        let single_line = met[i];
        let single_line2 = met2[i];
        arrX.push(single_line['name']);
        if(this.viewTarget || this.viewBothTargetBackground) {
          let sum = 0;
          if (i - 7 > 0){
            for (let j = 8; j > 0; j = j - 1){
              sum = sum + parseInt(met[i-j]['value']);
            }
          }
          total_target = total_target + single_line['value'];
          arrYLineTarget.push((sum/7).toFixed(3));
          arrYTarget.push(single_line['value']);
        }
        if(this.viewBackground || this.viewBothTargetBackground) {
          let sum = 0;
          if (i - 7 > 0){
            for (let k = 8; k > 0; k = k - 1){
              sum = sum + parseInt(met2[i-k]['value']);
            }
          }
          total_background = total_background + single_line2['value'];
          arrYLineBackground.push(sum/7);
          arrYBackground.push(single_line2['value']);
        }
        i = i + 1;
      }

      if(this.graphOnPercSequences){
        for (let jj = 0; jj < arrYLineTarget.length; jj = jj + 1){
          arrYTarget[jj] = (arrYTarget[jj]/total_target)*100;
          arrYLineTarget[jj] = (arrYLineTarget[jj]/total_target)*100;
        }
        for (let ii = 0; ii < arrYLineBackground.length; ii = ii + 1){
          arrYBackground[ii] = (arrYBackground[ii]/total_background)*100;
          arrYLineBackground[ii] = (arrYLineBackground[ii]/total_background)*100;
        }
      }

      this.barChart.series[0].data = arrYBackground;
      this.barChart.series[1].data = arrYTarget;
      this.barChart.series[2].data = arrYLineTarget;
      this.barChart.series[3].data = arrYLineBackground;
      this.barChart.xAxis.data = arrX;

      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.timeName));
      }
      this.my_chart.setOption(this.barChart, true);
    },
    changeMarkerAndRender(min, max){
      this.barChart.series[1].markArea.data[0][0].xAxis = min;
      this.barChart.series[1].markArea.data[0][1].xAxis = max;

      // let lenXAxis = this.max_range;

      this.locationToExclude = [];
      this.setLocationToExcludeMulti(this.locationToExclude);
      this.num_sequences_target = [];
      this.num_sequences_background = [];
      this.setFalseErrorNumSeqQueryGeo();
      for(let k = 0; k < this.timeContent.length; k = k + 1) {
        let i = min;
        this.num_sequences_target[k] = 0;
        this.num_sequences_background[k] = 0;

        while (i < max) {

          this.num_sequences_target[k] = this.num_sequences_target[k] + this.timeContent[k][i].value;
          this.num_sequences_background[k] = this.num_sequences_background[k] + this.timeContentBackground[k][i].value;
          i = i + 1;
        }

        if (this.num_sequences_target[k] < this.min_num_seq_target || this.num_sequences_background[k] < this.min_num_seq_background){

          let query = JSON.parse(JSON.stringify(this.queryGeo));

          if(!query['geo_group']){
            console.log("");
          }
          else if(!query['country']){
            this.locationToExclude.push(query['geo_group'][k]);
          }
          else if(!query['region']){
            this.locationToExclude.push(query['country'][k]);
          }
          else if(!query['province']){
            this.locationToExclude.push(query['region'][k]);
          }
          else{
            this.locationToExclude.push(query['province'][k]);
          }
        }
      }

      if(this.locationToExclude.length === this.timeContent.length){
        this.setTrueErrorNumSeqQueryGeo();
      }
      this.setLocationToExcludeMulti(this.locationToExclude);

      this.renderGraphFilterDate();
    },
    translateIndexToDate(index){
      if(this.timeContent[this.targetIndex][index]) {
        return this.timeContent[this.targetIndex][index].name;
      }
    },
    translateDateToIndex(date){
      let index = this.timeContent[this.targetIndex].findIndex(function(item){
        return item.name === date;
      });
      return index;
    },
    loadData(){

      let query = JSON.parse(JSON.stringify(this.queryGeo));
      let target = [];
      let nameTarget = '';
      if(!query['geo_group']){
        target = [];
        nameTarget = '';
      }
      else if(!query['country']){
        target = query['geo_group'];
        nameTarget = 'geo_group';
      }
      else if(!query['region']){
        target = query['country'];
        nameTarget = 'country';
      }
      else if(!query['province']){
        target = query['region'];
        nameTarget = 'region';
      }
      else{
        target = query['province'];
        nameTarget = 'province';
      }

      if(target.length > 0) {
        this.possibleTarget = target;
        this.selectedTarget = target[0];
      }

      if(!(target.length > 1)) {

        let url = `/analyze/analyzeTimeDistributionCountryLineage`;
        this.overlay = true;
        if (query['geo_group']) {
          query['geo_group'] = query['geo_group'][0];
        }
        if (query['country']) {
          query['country'] = query['country'][0];
        }
        if (query['region']) {
          query['region'] = query['region'][0];
        }
        if (query['province']) {
          query['province'] = query['province'][0];
        }

        query['toExclude'] = [];
        let to_send = {'query': query};

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              // this.chosenApplied = true;
              // this.overlay = false;
              let arrOfDates = [];
              let dayList;
              let first_date;
              let last_date;
              if (res.length !== 0) {

                first_date = new Date(res[0]['name']);
                last_date = new Date();
                last_date.setDate(last_date.getDate() + 1)

                dayList = this.getDaysArray(first_date, last_date);
                dayList.forEach(day => {
                  let idx = res.findIndex(item => item['name'] === day);
                  if (idx === -1) {
                    let single_element = {'name': day, 'value': 0};
                    arrOfDates.push(single_element);
                  } else {
                    let single_element = {'name': day, 'value': res[idx]['value']};
                    arrOfDates.push(single_element);
                  }
                })
              }
              this.timeContent[0] = arrOfDates;
              this.max_range = this.timeContent[0].length - 1;

              let that = this;
              let index_start = this.timeContent[0].findIndex(function (item) {
                return item.name === that.last_start_date
              });
              if (index_start === -1) {
                index_start = 0;
              }

              let index_stop = this.timeContent[0].findIndex(function (item) {
                return item.name === that.last_stop_date
              });
              if (index_stop === -1) {
                index_stop = this.max_range;
              }

              let url = `/analyze/analyzeTimeDistributionBackgroundQueryGeo`;
              let query = JSON.parse(JSON.stringify(this.queryGeo));
              let query_false = '';
              query['minDate'] = first_date.toISOString().slice(0, 10);
              query['maxDate'] = last_date.toISOString().slice(0, 10);
              query['toExclude'] = this.toExcludeGeo;

              if (query['geo_group']) {
                query['geo_group'] = query['geo_group'][0];
              }
              if (query['country']) {
                query['country'] = query['country'][0];
              }
              if (query['region']) {
                query['region'] = query['region'][0];
              }
              if (query['province']) {
                query['province'] = query['province'][0];
              }

              if (!query['country']) {
                query_false = 'geo_group'
              } else if (!query['region']) {
                let arr_geo = ['geo_group'];
                let i = 0;
                let len = arr_geo.length;
                while (i < len && i < (this.numLevelAboveBackground - 1)) {
                  delete query[arr_geo[i]];
                  i = i + 1;
                }
                query_false = 'country'
              } else if (!query['province']) {
                let arr_geo = ['country', 'geo_group'];
                let i = 0;
                let len = arr_geo.length;
                while (i < len && i < (this.numLevelAboveBackground - 1)) {
                  delete query[arr_geo[i]];
                  i = i + 1;
                }
                query_false = 'region'
              } else {
                let arr_geo = ['region', 'country', 'geo_group'];
                let i = 0;
                let len = arr_geo.length;
                while (i < len && i < (this.numLevelAboveBackground - 1)) {
                  delete query[arr_geo[i]];
                  i = i + 1;
                }
                query_false = 'province'
              }

              let to_send = {'query': query, 'query_false': query_false};

              axios.post(url, to_send)
                  .then((res) => {
                    return res.data;
                  })
                  .then((res) => {
                    this.chosenApplied = true;
                    this.overlay = false;

                    let arrOfDatesBackground = [];
                    dayList.forEach(day => {
                      let idx = res.findIndex(item => item['name'] === day);
                      if (idx === -1) {
                        let single_element = {'name': day, 'value': 0};
                        arrOfDatesBackground.push(single_element);
                      } else {
                        let single_element = {'name': day, 'value': res[idx]['value']};
                        arrOfDatesBackground.push(single_element);
                      }
                    })

                    this.timeContentBackground[0] = arrOfDatesBackground;
                    this.targetIndex = 0;

                    this.slider = [index_start, index_stop];
                    this.last_start_date = this.translateIndexToDate(this.slider[0]);
                    this.last_stop_date = this.translateIndexToDate(this.slider[1]);
                    this.changeMarkerAndRender(this.slider[0], this.slider[0]);
                    this.setStartDateQueryGeo(this.last_start_date);
                    this.setStopDateQueryGeo(this.last_stop_date);

                  });
            });
      }
      else{
        let len = target.length;
        let i = 0;
        let startDate = null;
        let indexStart = null;
        let indexStop = null;
        this.startDateMultiMinor = null;
        this.targetIndex = 0;
        if(i < len) {
          this.loadDataMultipleTarget(i, len, nameTarget, startDate, indexStart, indexStop);
        }
      }
    },
    loadDataMultipleTarget(i, len, nameTarget, startDate, indexStart, indexStop){
      let url = `/analyze/analyzeTimeDistributionCountryLineage`;
      let query = JSON.parse(JSON.stringify(this.queryGeo));
      this.overlay = true;

      if (query['geo_group']) {
        if(nameTarget === 'geo_group'){
          query['geo_group'] = query['geo_group'][i];
        }
        else {
          query['geo_group'] = query['geo_group'][0];
        }
      }
      if (query['country']) {
        if(nameTarget === 'country'){
          query['country'] = query['country'][i];
        }
        else {
          query['country'] = query['country'][0];
        }
      }
      if (query['region']) {
        if(nameTarget === 'region'){
          query['region'] = query['region'][i];
        }
        else {
          query['region'] = query['region'][0];
        }
      }
      if (query['province']) {
        if(nameTarget === 'province'){
          query['province'] = query['province'][i];
        }
        else {
          query['province'] = query['province'][0];
        }
      }

      query['toExclude'] = [];
      let to_send = {'query': query};

      axios.post(url, to_send)
          .then((res) => {
            return res.data;
          })
          .then((res) => {
            let arrOfDates = [];
            let dayList;
            let first_date;
            let last_date;
            if (res.length !== 0) {

              first_date = new Date(res[0]['name']);
              if(this.startDateMultiMinor === null || (this.startDateMultiMinor > first_date)){
                this.startDateMultiMinor = first_date;
              }
              if(startDate !== null && first_date > startDate){
                first_date = startDate;
              }
              else{
                startDate = first_date;
              }

              last_date = new Date();
              last_date.setDate(last_date.getDate() + 1)

              dayList = this.getDaysArray(first_date, last_date);
              dayList.forEach(day => {
                let idx = res.findIndex(item => item['name'] === day);
                if (idx === -1) {
                  let single_element = {'name': day, 'value': 0};
                  arrOfDates.push(single_element);
                } else {
                  let single_element = {'name': day, 'value': res[idx]['value']};
                  arrOfDates.push(single_element);
                }
              })
            }
            this.timeContent[i] = arrOfDates;

            // if(this.max_range < this.timeContent[this.targetIndex].length - 1) {
            //   this.max_range = this.timeContent[this.targetIndex].length - 1;
            // }
            //
            // let that = this;
            // let index_start = this.timeContent[this.targetIndex].findIndex(function (item) {
            //   return item.name === that.last_start_date
            // });
            // if (index_start === -1) {
            //   index_start = 0;
            // }
            //
            // let index_stop = this.timeContent[this.targetIndex].findIndex(function (item) {
            //   return item.name === that.last_stop_date
            // });
            // if (index_stop === -1) {
            //   index_stop = this.max_range;
            // }

            let url = `/analyze/analyzeTimeDistributionBackgroundQueryGeo`;
            let query = JSON.parse(JSON.stringify(this.queryGeo));
            let query_false = '';
            query['minDate'] = first_date.toISOString().slice(0, 10);
            query['maxDate'] = last_date.toISOString().slice(0, 10);
            query['toExclude'] = this.toExcludeGeo;

            if (query['geo_group']) {
              if(nameTarget === 'geo_group'){
                query['geo_group'] = query['geo_group'][i];
              }
              else {
                query['geo_group'] = query['geo_group'][0];
              }
            }
            if (query['country']) {
              if(nameTarget === 'country'){
                query['country'] = query['country'][i];
              }
              else {
                query['country'] = query['country'][0];
              }
            }
            if (query['region']) {
              if(nameTarget === 'region'){
                query['region'] = query['region'][i];
              }
              else {
                query['region'] = query['region'][0];
              }
            }
            if (query['province']) {
              if(nameTarget === 'province'){
                query['province'] = query['province'][i];
              }
              else {
                query['province'] = query['province'][0];
              }
            }

            if (!query['country']) {
              query_false = 'geo_group'
            } else if (!query['region']) {
              let arr_geo = ['geo_group'];
              let i = 0;
              let len = arr_geo.length;
              while (i < len && i < (this.numLevelAboveBackground - 1)) {
                delete query[arr_geo[i]];
                i = i + 1;
              }
              query_false = 'country'
            } else if (!query['province']) {
              let arr_geo = ['country', 'geo_group'];
              let i = 0;
              let len = arr_geo.length;
              while (i < len && i < (this.numLevelAboveBackground - 1)) {
                delete query[arr_geo[i]];
                i = i + 1;
              }
              query_false = 'region'
            } else {
              let arr_geo = ['region', 'country', 'geo_group'];
              let i = 0;
              let len = arr_geo.length;
              while (i < len && i < (this.numLevelAboveBackground - 1)) {
                delete query[arr_geo[i]];
                i = i + 1;
              }
              query_false = 'province'
            }

            let to_send = {'query': query, 'query_false': query_false};

            axios.post(url, to_send)
                .then((res) => {
                  return res.data;
                })
                .then((res) => {

                  let arrOfDatesBackground = [];
                  dayList.forEach(day => {
                    let idx = res.findIndex(item => item['name'] === day);
                    if (idx === -1) {
                      let single_element = {'name': day, 'value': 0};
                      arrOfDatesBackground.push(single_element);
                    } else {
                      let single_element = {'name': day, 'value': res[idx]['value']};
                      arrOfDatesBackground.push(single_element);
                    }
                  })

                  this.timeContentBackground[i] = arrOfDatesBackground;

                  // this.targetIndex = 0;
                  //
                  // this.slider = [index_start, index_stop];
                  // this.last_start_date = this.translateIndexToDate(this.slider[0]);
                  // this.last_stop_date = this.translateIndexToDate(this.slider[1]);
                  // this.changeMarkerAndRender(this.slider[0], this.slider[0]);
                  // this.setStartDateQueryGeo(this.last_start_date);
                  // this.setStopDateQueryGeo(this.last_stop_date);

                  i = i + 1;
                  if (i < len) {
                    this.loadDataMultipleTarget(i, len, nameTarget, startDate, indexStart, indexStop);
                  } else {

                    for(let k = 0; k < this.timeContent.length; k = k + 1){
                      first_date = new Date(this.timeContent[k][0]['name']);
                      if(this.startDateMultiMinor < first_date){

                        last_date = new Date();
                        last_date.setDate(last_date.getDate() + 1)

                        let arrOfDates= [];
                        dayList = this.getDaysArray(this.startDateMultiMinor, last_date);
                        dayList.forEach(day => {
                          let idx = this.timeContent[k].findIndex(item => item['name'] === day);
                          if (idx === -1) {
                            let single_element = {'name': day, 'value': 0};
                            arrOfDates.push(single_element);
                          } else {
                            let single_element = {'name': day, 'value': this.timeContent[k][idx]['value']};
                            arrOfDates.push(single_element);
                          }
                        })
                        this.timeContent[k] = arrOfDates;

                         let arrOfDatesBackground = [];
                        dayList.forEach(day => {
                          let idx = this.timeContentBackground[k].findIndex(item => item['name'] === day);
                          if (idx === -1) {
                            let single_element = {'name': day, 'value': 0};
                            arrOfDatesBackground.push(single_element);
                          } else {
                            let single_element = {'name': day, 'value': this.timeContentBackground[k][idx]['value']};
                            arrOfDatesBackground.push(single_element);
                          }
                        })
                        this.timeContentBackground[k] = arrOfDatesBackground;
                      }
                    }

                    if(this.max_range < this.timeContent[this.targetIndex].length - 1) {
                      this.max_range = this.timeContent[this.targetIndex].length - 1;
                    }

                    let that = this;
                    let index_start = this.timeContent[this.targetIndex].findIndex(function (item) {
                      return item.name === that.last_start_date
                    });
                    if (index_start === -1) {
                      index_start = 0;
                    }

                    let index_stop = this.timeContent[this.targetIndex].findIndex(function (item) {
                      return item.name === that.last_stop_date
                    });
                    if (index_stop === -1) {
                      index_stop = this.max_range;
                    }

                    this.slider = [index_start, index_stop];
                    this.last_start_date = this.translateIndexToDate(this.slider[0]);
                    this.last_stop_date = this.translateIndexToDate(this.slider[1]);
                    this.changeMarkerAndRender(this.slider[0], this.slider[0]);
                    this.setStartDateQueryGeo(this.last_start_date);
                    this.setStopDateQueryGeo(this.last_stop_date);

                    this.chosenApplied = true;
                    this.overlay = false;
                  }

                });
          });
    },
    setTargetBackgroundName(){
      let query = JSON.parse(JSON.stringify(this.queryGeo));

      this.listLocationExcluded = [];

      let key = Object.keys(this.toExcludeGeo)[0];

      if(!query['geo_group']){
        this.target_name = 'World';
        this.background_name = 'World';
      }
      else if(!query['country']){
        this.target_name = query['geo_group'][this.targetIndex];
        if(this.toExcludeGeo['geo_group'] && this.toExcludeGeo['geo_group'].length > 0){
          this.background_name = 'World *';
          this.listLocationExcluded = this.toExcludeGeo['geo_group'];
        }
        else {
          this.background_name = 'World';
        }
      }
      else if(!query['region']){
        let arr_geo = ['geo_group'];
        this.target_name = query['country'][this.targetIndex];
        let len = arr_geo.length;
        if (this.numLevelAboveBackground > len){
          if(this.toExcludeGeo['geo_group'] && this.toExcludeGeo['geo_group'].length > 0){
            this.background_name = 'World *';
            this.listLocationExcluded = this.toExcludeGeo['geo_group'];
          }
          else {
            this.background_name = 'World';
          }
        }
        else{
          if(this.toExcludeGeo[key] && this.toExcludeGeo[key].length > 0){
            this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]] + ' *';
            this.listLocationExcluded = this.toExcludeGeo[key];
          }
          else {
            this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]];
          }
        }
      }
      else if(!query['province']){
        let arr_geo = ['country', 'geo_group'];
        this.target_name = query['region'][this.targetIndex];
        let len = arr_geo.length;
        if (this.numLevelAboveBackground > len){
          if(this.toExcludeGeo['geo_group'] && this.toExcludeGeo['geo_group'].length > 0){
            this.background_name = 'World *';
            this.listLocationExcluded = this.toExcludeGeo['geo_group'];
          }
          else {
            this.background_name = 'World';
          }
        }
        else{
          if(this.toExcludeGeo[key] && this.toExcludeGeo[key].length > 0){
            this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]] + ' *';
            this.listLocationExcluded = this.toExcludeGeo[key];
          }
          else {
            this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]];
          }
        }
      }
      else{
        let arr_geo = ['region', 'country', 'geo_group'];
        this.target_name = query['province'][this.targetIndex];
        let len = arr_geo.length;
        if (this.numLevelAboveBackground > len){
          if(this.toExcludeGeo['geo_group'] && this.toExcludeGeo['geo_group'].length > 0){
            this.background_name = 'World *';
            this.listLocationExcluded = this.toExcludeGeo['geo_group'];
          }
          else {
            this.background_name = 'World';
          }
        }
        else{
          if(this.toExcludeGeo[key] && this.toExcludeGeo[key].length > 0){
            this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]] + ' *';
            this.listLocationExcluded = this.toExcludeGeo[key];
          }
          else {
            this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]];
          }
        }
      }
    }
  },
  watch: {
    view_exclusive(){
      if(this.view_exclusive === 0){
        this.viewTarget = true;
        this.viewBackground = false;
        this.viewBothTargetBackground = false;
      }
      else if(this.view_exclusive === 1){
        this.viewTarget = false;
        this.viewBackground = true;
        this.viewBothTargetBackground = false;
      }
      else if(this.view_exclusive === 2){
        this.viewTarget = false;
        this.viewBackground = false;
        this.viewBothTargetBackground = true;
      }
    },
    perc_or_absolute_num_exclusive(){
      if(this.perc_or_absolute_num_exclusive === 0){
        this.graphOnNumSequences = true;
        this.graphOnPercSequences = false;
      }
      else if(this.perc_or_absolute_num_exclusive === 1){
        this.graphOnNumSequences = false;
        this.graphOnPercSequences = true;
      }
    },
    selectedTarget(){
      let that = this;
      let index = this.possibleTarget.findIndex(function (item) {
        return item === that.selectedTarget;
      });
      if (index !== -1) {
        this.targetIndex = index;
      }
      else{
        this.targetIndex = 0;
        this.selectedTarget = this.possibleTarget[0];
      }
    },
    targetIndex(){
      this.renderGraphFilterDate();
      this.setTargetBackgroundName();
      let min = this.slider[0];
      let max = this.slider[1];
      this.changeMarkerAndRender(min, max);
    },
    numLevelAboveBackground() {
      this.setTargetBackgroundName();
      this.loadData();
    },
    last_start_date(){
      this.wrong_last_start_date = false;
      let start = this.translateDateToIndex(this.last_start_date);
      if (start === -1 || start > this.slider[1]){
        this.wrong_last_start_date = true;
      }
      else {
        let stop = this.slider[1];
        this.slider = [start, stop];
      }
    },
    last_stop_date(){
      this.wrong_last_stop_date = false;
      let stop = this.translateDateToIndex(this.last_stop_date);
      if (stop === -1 || stop < this.slider[0]){
        this.wrong_last_stop_date = true;
      }
      else {
        let start = this.slider[0];
        this.slider = [start, stop];
      }
    },
    timeContent(){
      // this.renderGraphFilterDate();
    },
    filterDate(){
      this.renderGraphFilterDate();
    },
    queryGeo(){
      this.setTargetBackgroundName();
      this.loadData();
    },
    slider(){
      if(!this.overlay) {
        let min = this.slider[0];
        let max = this.slider[1];
        this.changeMarkerAndRender(min, max);

        this.last_start_date = this.translateIndexToDate(this.slider[0]);
        this.last_stop_date = this.translateIndexToDate(this.slider[1]);
        this.setStartDateQueryGeo(this.last_start_date);
        this.setStopDateQueryGeo(this.last_stop_date);
      }
    },
    viewBackground(){
      if(this.viewBackground=== true) {
        this.viewTarget = false;
        this.viewBothTargetBackground = false;
      }
      this.renderGraphFilterDate();
    },
    viewTarget(){
      if(this.viewTarget === true){
        this.viewBackground = false;
        this.viewBothTargetBackground = false;
      }
      this.renderGraphFilterDate();
    },
    viewBothTargetBackground(){
      if(this.viewBothTargetBackground === true){
        this.viewBackground = false;
        this.viewTarget = false;
      }
      this.renderGraphFilterDate();
    },
    graphOnNumSequences(){
      this.graphOnPercSequences = (this.graphOnNumSequences !== true);
      this.renderGraphFilterDate();
    },
    graphOnPercSequences(){
      this.graphOnNumSequences = (this.graphOnPercSequences !== true);
      this.renderGraphFilterDate();
    },
    toExcludeGeo(){
      this.setTargetBackgroundName();
      this.loadData();
    }
  },
  mounted() {
      this.loadData();
  },
}
</script>

<style scoped>

  /deep/ .centered-input input {
    text-align: center
  }

</style>