<template>
<div style="position: relative;">
    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 50px">
     <h2>SELECTION OF COLLECTION-DATES TIME FRAME
        <v-btn @click="download" x-small icon
            style="margin-left: 20px; margin-bottom: 5px">
              <v-icon size="23">
                mdi-download-circle-outline
              </v-icon>
        </v-btn>
     </h2>
    </v-flex>
    <v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; z-index: 1">
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
                color="#F48C0680"
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
          <v-card style="width: 80%; margin: 20px" color="#F48C0680">
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 5px; padding-top: 5px">
                <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                    <h3>NUM SEQUENCES: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0;">
                      <v-text-field
                        :value = "num_sequences"
                        solo
                        readonly
                        hide-details
                        class = "centered-input"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; position: relative;">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <h3>START: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0">
                      <v-text-field
                        v-model = "last_start_date"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                         <template v-slot:append>
                            <v-icon v-if="wrong_last_start_date"
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
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; position: relative">
                  <v-layout row wrap justify-space-around>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0">
                      <h3>END: </h3>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs10 d-flex" style="justify-content: center; padding: 0">
                      <v-text-field
                        v-model = "last_stop_date"
                        solo
                        hide-details
                        class = "centered-input"
                      >
                        <template v-slot:append>
                            <v-icon v-if="wrong_last_stop_date"
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
name: "TimeSelectorDistributionLineageInGeo",
  props: {
    timeName: {required: true,},
    geoGranularity: {required: true},
    geoSpecific: {required: true},
  },
  data(){
    return {
      overlay: false,
      slider: [0, 1500],
      max_range: 0,
      timeContent: [],
      last_start_date: null,
      last_stop_date: null,
      num_sequences: 0,
      wrong_last_start_date: false,
      wrong_last_stop_date: false,

      min_num_seq: 10,

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
          data: ['Collected sequences, per date', 'AVG of previous 7 days'],
          top: '20px',
          selectedMode: false,
          itemGap: 50,
        },
        series: [
            {
                name: 'Collected sequences, per date',
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
                    }]
                    ]
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
    ...mapState(['startDateDistributionLineageInGeo', 'stopDateDistributionLineageInGeo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setStartDateDistributionLineageInGeo', 'setStopDateDistributionLineageInGeo']),
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
        this.renderGraph(met);
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
      this.my_chart.setOption(this.barChart, true);
    },
    changeMarkerAndRender(min, max){
      if(min === max){
        if(max < this.max_range) {
          this.barChart.series[0].markArea.data[0][0].xAxis = min;
          this.barChart.series[0].markArea.data[0][1].xAxis = max + 1;
        }
        else{
          this.barChart.series[0].markArea.data[0][0].xAxis = min - 1;
          this.barChart.series[0].markArea.data[0][1].xAxis = max;
        }
      }
      else{
        this.barChart.series[0].markArea.data[0][0].xAxis = min;
        this.barChart.series[0].markArea.data[0][1].xAxis = max;
      }

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

      let query = {};
      if(this.geoGranularity !== 'world') {
        query[this.geoGranularity] = this.geoSpecific;
      }
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

            this.slider = [index_start, index_stop];
            this.last_start_date = this.translateIndexToDate(this.slider[0]);
            this.last_stop_date = this.translateIndexToDate(this.slider[1]);
            this.changeMarkerAndRender(this.slider[0], this.slider[0]);

            this.setStartDateDistributionLineageInGeo(this.last_start_date);
            this.setStopDateDistributionLineageInGeo(this.last_stop_date);

            this.chosenApplied = true;
            this.overlay = false;

        });
    },
  },
  watch: {
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
    slider(){
      let min = this.slider[0];
      let max = this.slider[1];
      this.changeMarkerAndRender(min, max);

      this.last_start_date = this.translateIndexToDate(this.slider[0]);
      this.last_stop_date = this.translateIndexToDate(this.slider[1]);

      this.setStartDateDistributionLineageInGeo(this.last_start_date);
      this.setStopDateDistributionLineageInGeo(this.last_stop_date);
    },
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