<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; margin-top: 100px; z-index: 1">
          </div>
        </v-row>
    </v-container>

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
                color="red"
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
              TIME
            </v-card-title>
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 30px;">
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                  <h3># SEQUENCES: </h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center; padding: 0;">
                  <v-text-field
                    :value = "num_sequences"
                    solo
                    readonly
                    hide-details
                    class = "centered-input"
                  ></v-text-field>
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
                        readonly
                        class = "centered-input"
                      >
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
                        readonly
                        class = "centered-input"
                      >
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
      slider: [0, 1500],
      left_ranges_width:  10,
      total_ranges_width: 80,
      max_range: 0,
      timeContent: [],
      last_start_date: null,
      last_stop_date: null,
      num_sequences: 0,

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
                    }]
                    ]
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
    ...mapState(['queryGeo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setTimeRangesTargetAndBackground', 'setStartDateQueryGeo', 'setStopDateQueryGeo']),
    ...mapActions(['setQueryGeo']),
    getDaysArray(start, end) {
      for (var arr = [], dt = new Date(start); dt <= end; dt.setDate(dt.getDate() + 1)) {
        arr.push(new Date(dt).toISOString().slice(0, 10));
      }
      return arr;
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
    changeMarkerAndRender(min, max){
      this.barChart.series[0].markArea.data[0][0].xAxis = min;
      this.barChart.series[0].markArea.data[0][1].xAxis = max;

      let lenXAxis = this.timeContent.length;
      let i = 0;
      this.num_sequences = 0;

      while(i < lenXAxis){
        if( i >= min && i <= max ){
          this.num_sequences = this.num_sequences + this.timeContent[i].value;
        }
        i = i + 1;
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
            this.chosenApplied = true;
            this.overlay = false;
            let arrOfDates = [];
            if( res.length !== 0) {

              let first_date = new Date(res[0]['name']);
              let last_date = new Date();
              last_date.setDate(last_date.getDate() + 1)

              let dayList = this.getDaysArray(first_date, last_date);
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

            this.slider = [index_start, index_stop];

            this.last_start_date = this.translateIndexToDate(this.slider[0]);
            this.last_stop_date = this.translateIndexToDate(this.slider[1]);
            this.setStartDateQueryGeo(this.last_start_date);
            this.setStopDateQueryGeo(this.last_stop_date);

            this.changeMarkerAndRender(this.slider[0], this.slider[0]);
        });
    }
  },
  watch: {
    timeContent(){
      this.renderGraphFilterDate();
    },
    filterDate(){
      this.renderGraphFilterDate();
    },
    queryGeo(){
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