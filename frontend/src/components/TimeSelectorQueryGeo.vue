<template>
  <div style="position: relative;">
    <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; margin-top: 100px; z-index: 1">
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
                color="green"
                track-color="grey"
                height="2px"
              >
            </v-range-slider>
          </div>
        </v-flex>
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;
         padding-top: 0; padding-bottom: 0">
          <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: start;">
                <v-checkbox v-model="viewBackground"
                label="SHOW BACKGROUND"
                input-value="true">
                </v-checkbox>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-row>
    </v-container>
    <v-container fluid grid-list-xl style="justify-content: center;
  background-color: white; width: 100%">
      <v-row justify="center" align="center">
        <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
          <v-card style="width: 80%; margin: 20px" color="rgba(50, 255, 50, 0.5)">
            <v-card-title class="justify-center">
              TIME
            </v-card-title>
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 30px;">
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-bottom: 30px; margin-top: 10px">
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
                 padding: 0; position: relative; margin-bottom: 30px; margin-top: 10px">
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
              </v-layout>
              <v-layout row wrap justify-space-around style="padding-bottom: 30px;">
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-bottom: 30px; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <h3># SEQUENCES TARGET: </h3>
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
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative; margin-bottom: 30px; margin-top: 10px">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <h3># SEQUENCES BACKGROUND: </h3>
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
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative;">
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
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <h3>STOP: </h3>
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
      overlay: false,
      slider: [0, 1500],
      left_ranges_width:  10,
      total_ranges_width: 80,
      max_range: 0,
      timeContent: [],
      last_start_date: null,
      last_stop_date: null,
      num_sequences_target: 0,
      num_sequences_background: 0,
      wrong_last_start_date: false,
      wrong_last_stop_date: false,

      min_num_seq_target: 10,
      min_num_seq_background: 10,
      target_name: 'World',
      background_name: 'World',

      timeContentBackground: [],
      viewBackground: false,

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
                itemStyle: {color: 'rgba(255, 0, 0, 1)'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(255, 0, 0, 1)'
                    }
                },
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
            },
            {
                type: 'bar',
                radius: '50%',
                data: [],
                itemStyle: {color: 'rgba(0, 0, 255, 1)'},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 255, 1)'
                    }
                },
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
    ...mapState(['queryGeo', 'startDateQueryGeo', 'stopDateQueryGeo', 'numLevelAboveBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setTimeRangesTargetAndBackground', 'setStartDateQueryGeo', 'setStopDateQueryGeo',
     'setTrueErrorNumSeqQueryGeo', 'setFalseErrorNumSeqQueryGeo']),
    ...mapActions(['setQueryGeo']),
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
        let met =  JSON.parse(JSON.stringify(this.timeContent));
        let met2 =  JSON.parse(JSON.stringify(this.timeContentBackground));
        this.renderGraph(met, met2);
    },
    renderGraph(met, met2){

      let len = met.length;
      let i = 0;
      let arrX = [];
      let arrYBackground = [];
      let arrYTarget = [];
      while (i < len){
        let single_line = met[i];
        let single_line2 = met2[i];
        arrX.push(single_line['name']);
        arrYTarget.push(single_line['value']);
        if(this.viewBackground) {
          arrYBackground.push(single_line2['value']);
        }
        i = i + 1;
      }

      this.barChart.series[0].data = arrYBackground;
      this.barChart.series[1].data = arrYTarget;
      this.barChart.xAxis.data = arrX;

      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.timeName));
      }
      this.my_chart.setOption(this.barChart, true);
    },
    changeMarkerAndRender(min, max){
      this.barChart.series[0].markArea.data[0][0].xAxis = min;
      this.barChart.series[0].markArea.data[0][1].xAxis = max;

      let lenXAxis = this.timeContent.length;
      let i = 0;
      this.num_sequences_target = 0;
      this.num_sequences_background = 0;

      while(i < lenXAxis){
        if( i >= min && i <= max ){
          this.num_sequences_target = this.num_sequences_target + this.timeContent[i].value;
          this.num_sequences_background = this.num_sequences_background + this.timeContentBackground[i].value;
        }
        i = i + 1;
      }

      if (this.num_sequences_target < this.min_num_seq_target || this.num_sequences_background < this.min_num_seq_background){
        this.setTrueErrorNumSeqQueryGeo();
      }
      else{
        this.setFalseErrorNumSeqQueryGeo();
      }

      this.renderGraphFilterDate();
    },
    translateIndexToDate(index){
      if(this.timeContent[index]) {
        return this.timeContent[index].name;
      }
    },
    translateDateToIndex(date){
      let index = this.timeContent.findIndex(function(item){
        return item.name === date;
      });
      return index;
    },
    loadData(){
      let url = `/analyze/analyzeTimeDistributionCountryLineage`;
      this.overlay = true;

      let query = JSON.parse(JSON.stringify(this.queryGeo));

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
            if( res.length !== 0) {

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
            this.timeContent = arrOfDates;
            this.max_range = this.timeContent.length - 1;

            let that = this;
            let index_start = this.timeContent.findIndex(function(item){
              return item.name === that.last_start_date
            });
            if (index_start === -1){
              index_start = 0;
            }

            let index_stop = this.timeContent.findIndex(function(item){
              return item.name === that.last_stop_date
            });
            if (index_stop === -1){
              index_stop = this.max_range;
            }

            let url = `/analyze/analyzeTimeDistributionBackgroundQueryGeo`;
            let query = JSON.parse(JSON.stringify(this.queryGeo));
            let query_false = '';
            query['minDate'] = first_date.toISOString().slice(0, 10);
            query['maxDate'] = last_date.toISOString().slice(0, 10);

            if(!query['country']){
              query_false = 'geo_group'
            }
            else if(!query['region']){
              let arr_geo = ['geo_group'];
              let i = 0;
              let len = arr_geo.length;
              while (i<len && i<(this.numLevelAboveBackground-1)){
                delete query[arr_geo[i]];
                i = i + 1;
              }
              query_false = 'country'
            }
            else if(!query['province']){
              let arr_geo = ['country', 'geo_group'];
              let i = 0;
              let len = arr_geo.length;
              while (i<len && i<(this.numLevelAboveBackground-1)){
                delete query[arr_geo[i]];
                i = i + 1;
              }
              query_false = 'region'
            }
            else{
              let arr_geo = ['region', 'country', 'geo_group'];
              let i = 0;
              let len = arr_geo.length;
              while (i<len && i<(this.numLevelAboveBackground-1)){
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

                this.timeContentBackground = arrOfDatesBackground;

                this.slider = [index_start, index_stop];
                this.last_start_date = this.translateIndexToDate(this.slider[0]);
                this.last_stop_date = this.translateIndexToDate(this.slider[1]);
                this.changeMarkerAndRender(this.slider[0], this.slider[0]);
                this.setStartDateQueryGeo(this.last_start_date);
                this.setStopDateQueryGeo(this.last_stop_date);

              });
        });
    },
    setTargetBackgroundName(){
      let query = JSON.parse(JSON.stringify(this.queryGeo));

      if(!query['geo_group']){
        this.target_name = 'World';
        this.background_name = 'World';
      }
      else if(!query['country']){
        this.target_name = query['geo_group'];
        this.background_name = 'World';
      }
      else if(!query['region']){
        let arr_geo = ['geo_group'];
        this.target_name = query['country'];
        let len = arr_geo.length;
        if (this.numLevelAboveBackground > len){
          this.background_name = 'World';
        }
        else{
          this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]];
        }
      }
      else if(!query['province']){
        let arr_geo = ['country', 'geo_group'];
        this.target_name = query['region'];
        let len = arr_geo.length;
        if (this.numLevelAboveBackground > len){
          this.background_name = 'World';
        }
        else{
          this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]];
        }
      }
      else{
        let arr_geo = ['region', 'country', 'geo_group'];
        this.target_name = query['province'];
        let len = arr_geo.length;
        if (this.numLevelAboveBackground > len){
          this.background_name = 'World';
        }
        else{
          this.background_name = query[arr_geo[this.numLevelAboveBackground - 1]];
        }
      }
    }
  },
  watch: {
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
      let min = this.slider[0];
      let max = this.slider[1];
      this.changeMarkerAndRender(min, max);

      this.last_start_date = this.translateIndexToDate(this.slider[0]);
      this.last_stop_date = this.translateIndexToDate(this.slider[1]);
      this.setStartDateQueryGeo(this.last_start_date);
      this.setStopDateQueryGeo(this.last_stop_date);
    },
    viewBackground(){
      this.renderGraphFilterDate();
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