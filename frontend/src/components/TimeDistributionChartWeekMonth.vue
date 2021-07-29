<template>
  <div style="position: relative;">
    <v-container fluid grid-list-xl style="justify-content: center; text-align: center; z-index: 1; width: 1500px">
        <h2 style="margin-top: 50px;">TIME DISTRIBUTION <v-btn @click="download" x-small icon
            style="margin-left: 20px; margin-bottom: 5px">
              <v-icon size="23">
                mdi-download-circle-outline
              </v-icon>
         </v-btn></h2>
        <v-row justify="center" align="center" style="z-index: 1">
          <div :id="timeName" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; margin-top: 50px; z-index: 1">
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
          <v-card style="width: 100%; margin: 20px" color="#F48C0680">
            <v-card-text>
              <v-layout row wrap justify-space-around style="padding-bottom: 30px; padding-top: 30px">
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
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <span> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center;
                 padding: 0; position: relative">
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
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0;">
                      <span> (input date using the YYYY-MM-DD format) </span>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
        </v-flex>
        <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 20px">
          <v-card style="width: 80%; padding: 10px; background: linear-gradient(0deg, #F1FAEE 50%, #F1FAEE 50%)">
            <v-card-title class="justify-center"><h3>Select type of analysis</h3></v-card-title>
            <v-card-text>
              <v-layout row wrap justify-space-around>
                <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                  <v-select
                    v-model="selectedTypeOfAnalysis"
                    :items="possibleTypeOfAnalysis"
                    label="Protein"
                    solo
                    hide-details
                    ></v-select>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="selectedTypeOfAnalysis === 'Analysis per specific num of days'">
                  <h3>Select length of the period</h3>
                </v-flex>
                <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center; margin: 0; padding: 0" v-if="selectedTypeOfAnalysis === 'Analysis per specific num of days'">
                  <v-text-field
                    v-model="selectedNumDaysAnalysis"
                    label="Protein"
                    solo
                    min="0"
                    max="365"
                    hide-details
                    type="number"
                  ></v-text-field>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 20px" >
                  <span><b>(only bold squared periods are analyzed, as they contain enough sequences and can be compared with the adjacent periods)</b></span>
                </v-flex>
                <v-flex class="no-horizontal-padding xs12 md5 lg5 d-flex"
                        style="justify-content: center; margin-bottom: 5px"
                        v-for="(period, index) in timeDivision" v-bind:key="period[0]">
                       <v-row justify-center style="width:  100%; border: #1D3557 solid 7px;" v-if="timeDivisionAcceptable.includes(period)">
                          <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>PERIOD: </b><br> {{period[0]}} - {{period[1]}}</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>NUM SEQUENCES:</b><br> {{period[2]}}</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>ORDER:</b><br> {{index + 1}}</span>
                          </v-flex>
                       </v-row>
                       <v-row justify-center style="width:  100%; border: grey solid 1px;" v-else-if="timeDivisionNumSeqAcceptable.includes(period)">
                          <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>PERIOD: </b><br> {{period[0]}} - {{period[1]}}</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>NUM SEQUENCE:</b><br> {{period[2]}}</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>ORDER:</b><br> {{index + 1}}</span>
                          </v-flex>
                       </v-row>
                       <v-row justify-center style="width:  100%; border: grey solid 1px;" v-else>
                          <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>PERIOD: </b><br> {{period[0]}} - {{period[1]}}</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>NUM SEQUENCES:</b><br> {{period[2]}}</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center;">
                            <span style="text-align: center"><b>ORDER:</b><br> {{index + 1}}</span>
                          </v-flex>
                       </v-row>
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
  name: "TimeDistributionChartWeekMonth",
  props: {
    timeName: {required: true,},
    timeContent: {required: true,},
    filterDate: {required: true},
  },
  data(){
    return {
      overlay: false,
      slider: [0, 1500],
      max_range: 0,
      last_start_date: null,
      last_stop_date: null,
      num_sequences: 0,
      wrong_last_start_date: false,
      wrong_last_stop_date: false,

      selectedTypeOfAnalysis: 'Analysis per specific num of days',
      possibleTypeOfAnalysis: ['Analysis per specific num of days', 'Analysis per week', 'Analysis per month'],

      selectedNumDaysAnalysis: 30,
      timeDivision: [],
      timeDivisionNumSeqAcceptable: [],

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
                name: 'AVG of previous 7 days',
                type: 'line',
                data: [],
                color: '#323F8B',
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
    ...mapState(['timeDivisionAcceptable']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setTimeDivisionAcceptable', 'setTrueErrorNumSeqQueryTime', 'setFalseErrorNumSeqQueryTime']),
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
      return this.timeContent.findIndex(function(item){
        return item.name === date;
      });
    },
    computeTimeDivision(){
      this.timeDivision = [];
      let start ;
      let stop ;
      let num_days;
      let arr_acceptable_time_division = [];
      if(this.selectedTypeOfAnalysis === this.possibleTypeOfAnalysis[0]) {
        start = this.slider[0];
        stop = this.slider[1];
        num_days = parseInt(this.selectedNumDaysAnalysis);
        let while_condition = true;
        let i = start;
        while (while_condition) {
          let single_period = [];
          single_period[0] = this.translateIndexToDate(i);

          if (i + num_days > stop) {
            single_period[1] = this.translateIndexToDate(stop);
            while_condition = false;
          } else {
            single_period[1] = this.translateIndexToDate(i + num_days - 1);
          }

          let j = i;
          let num_seq = 0;
          while (j < i + num_days) {
            if (j <= stop) {
              num_seq = num_seq + this.timeContent[j].value;
            }
            j = j + 1;
          }
          single_period[2] = num_seq;

          if (num_seq > this.min_num_seq) {
            arr_acceptable_time_division.push(single_period);
          }

          this.timeDivision.push(single_period);
          i = i + num_days;
        }
      }
      else if(this.selectedTypeOfAnalysis === this.possibleTypeOfAnalysis[1]) { // WEEK
        let startDate = new Date(this.translateIndexToDate(this.slider[0]));
        let stopDate = new Date(this.translateIndexToDate(this.slider[1]));
        let distanceFromFirstMonday;
        let distanceFromLastSunday;
        num_days = 7;
        let firstMondayDate = startDate.getDay() || 7;
        if( firstMondayDate !== 1 ) {
          distanceFromFirstMonday = (firstMondayDate - 1);
          startDate.setHours(-24 * (firstMondayDate - 1));
        }
        else{
         distanceFromFirstMonday = (firstMondayDate - 1);
        }
        let lastSundayDate = stopDate.getDay() || 7;
        if( lastSundayDate !== 7 ) {
          distanceFromLastSunday = (7 - lastSundayDate);
          stopDate.setHours(24 * (7 - lastSundayDate));
        }
        else{
         distanceFromLastSunday = (7 - lastSundayDate);
        }
        if(this.slider[0] - distanceFromFirstMonday >= 0){
          start = this.slider[0] - distanceFromFirstMonday;
        }
        else{
          start = this.slider[0];
          num_days = (7 - distanceFromFirstMonday)
        }
        if(this.slider[1] + distanceFromLastSunday <= this.max_range){
          stop = this.slider[1] + distanceFromLastSunday;
        }
        else{
          stop = this.slider[1]; // - (7 - distanceFromLastSunday)
        }
        let while_condition = true;
        let i = start;
        while (while_condition) {
          let single_period = [];
          single_period[0] = this.translateIndexToDate(i);

          if (i + num_days > stop) {
            single_period[1] = this.translateIndexToDate(stop);
            while_condition = false;
          } else {
            single_period[1] = this.translateIndexToDate(i + num_days - 1);
          }

          let j = i;
          let num_seq = 0;
          while (j < i + num_days) {
            if (j <= stop) {
              num_seq = num_seq + this.timeContent[j].value;
            }
            j = j + 1;
          }
          single_period[2] = num_seq;

          if (num_seq > this.min_num_seq) {
            arr_acceptable_time_division.push(single_period);
          }

          this.timeDivision.push(single_period);
          i = i + num_days;
          num_days = 7;
        }
      }
      else if(this.selectedTypeOfAnalysis === this.possibleTypeOfAnalysis[2]) { // MONTH
        let startDate = new Date(this.translateIndexToDate(this.slider[0]));
        let stopDate = new Date(this.translateIndexToDate(this.slider[1]));
        // let firstDay = new Date(startDate.getFullYear(), startDate.getMonth(), 1);
        // let lastDay = new Date(stopDate.getFullYear(), stopDate.getMonth() + 1, 0);
        let firstDayDate = new Date(startDate).toISOString().slice(0, 10).split('-');
        let lastDayDate = new Date(stopDate).toISOString().slice(0, 10).split('-');
        let distanceFromFirstDay = (firstDayDate[2] - 1);
        let dayInMonthLastDay = this.dayInMoth(lastDayDate[1], lastDayDate[0]);
        let distanceFromLastDay = (dayInMonthLastDay - lastDayDate[2]);
        let daysFirstPeriod = 0;
        if(this.slider[0] - distanceFromFirstDay >= 0){
          start = this.slider[0] - distanceFromFirstDay;
        }
        else{
          let dayInMonth = this.dayInMoth(firstDayDate[1], firstDayDate[0]);
          start = this.slider[0];
          daysFirstPeriod = (dayInMonth - distanceFromFirstDay);
        }
        if(this.slider[1] + distanceFromLastDay <= this.max_range){
          stop = this.slider[1] + distanceFromLastDay;
        }
        else{
          // let dayInMonth = this.dayInMoth(lastDayDate[1], lastDayDate[0]);
          stop = this.slider[1]; // - (dayInMonth - distanceFromLastSunday)
        }
        let while_condition = true;
        let i = start;
        while (while_condition) {
          let single_period = [];
          single_period[0] = this.translateIndexToDate(i);
          let dayDate = new Date(single_period[0]).toISOString().slice(0, 10).split('-');
          let daysInMonth;
          if(daysFirstPeriod !== 0){
            daysInMonth = daysFirstPeriod;
          }
          else{
            daysInMonth = this.dayInMoth(dayDate[1], dayDate[0]);
          }

          if (i + daysInMonth > stop) {
            single_period[1] = this.translateIndexToDate(stop);
            while_condition = false;
          } else {
            single_period[1] = this.translateIndexToDate(i + daysInMonth - 1);
          }

          let j = i;
          let num_seq = 0;
          while (j < i + daysInMonth) {
            if (j <= stop) {
              num_seq = num_seq + this.timeContent[j].value;
            }
            j = j + 1;
          }
          single_period[2] = num_seq;

          if (num_seq > this.min_num_seq) {
            arr_acceptable_time_division.push(single_period);
          }

          this.timeDivision.push(single_period);
          i = i + daysInMonth;
          daysFirstPeriod = 0;
        }
      }
      this.timeDivisionNumSeqAcceptable = arr_acceptable_time_division;

      let arr_full_acceptable = [];
      for(let k = 0; k < this.timeDivisionNumSeqAcceptable.length; k = k + 1){
        if(k > 0){
          let date1 = new Date(this.timeDivisionNumSeqAcceptable[k][0]);
          let date2 = new Date(this.timeDivisionNumSeqAcceptable[k-1][1]);
          date1.setDate(date1.getDate() - 1);
          let date3 = new Date(date1).toISOString().slice(0, 10);
          let date4 = new Date(date2).toISOString().slice(0, 10);
          if(date3 === date4){
            arr_full_acceptable.push(this.timeDivisionNumSeqAcceptable[k]);
          }
        }
        if(k < this.timeDivisionNumSeqAcceptable.length - 1){
          let date1 = new Date(this.timeDivisionNumSeqAcceptable[k][1]);
          let date2 = new Date(this.timeDivisionNumSeqAcceptable[k+1][0]);
          date2.setDate(date2.getDate() - 1);
          let date3 = new Date(date1).toISOString().slice(0, 10);
          let date4 = new Date(date2).toISOString().slice(0, 10);
          if(date3 === date4){
            arr_full_acceptable.push(this.timeDivisionNumSeqAcceptable[k]);
          }
        }
        // if((k > 0 && this.timeDivisionNumSeqAcceptable[k][0] === this.timeDivisionNumSeqAcceptable[k-1][1]) ||
        // (k < this.timeDivisionNumSeqAcceptable.length && this.timeDivisionNumSeqAcceptable[k][1] === this.timeDivisionNumSeqAcceptable[k+1][0])){
        //   arr_full_acceptable.push(this.timeDivisionNumSeqAcceptable[k]);
        // }
      }

      if(arr_full_acceptable.length < 2){
        this.setTrueErrorNumSeqQueryTime();
      }
      else{
        this.setFalseErrorNumSeqQueryTime();
      }
      this.setTimeDivisionAcceptable(arr_full_acceptable);
    },
    dayInMoth(monthStr, yearStr){
      let numDays ;
      let month = parseInt(monthStr);
      let year = parseInt(yearStr);
      if(month === 4 || month === 6 || month === 9 || month === 11){
        numDays = 30;
      }
      else if (month === 2){
        if ((!(year%4) && (year%100)) || !year%400){
          numDays = 29;
        }
        else{
          numDays = 28;
        }
      }
      else{
        numDays = 31;
      }
      return numDays;
    }
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
      this.computeTimeDivision();
    },
    selectedNumDaysAnalysis(){
      if(this.selectedNumDaysAnalysis !== null
          && this.selectedNumDaysAnalysis !== undefined
          && this.selectedNumDaysAnalysis !== ''
          && this.selectedNumDaysAnalysis !== ' '
          && this.selectedNumDaysAnalysis > 0) {
        this.computeTimeDivision();
      }
    },
    selectedTypeOfAnalysis(){
      if(this.selectedTypeOfAnalysis !== this.possibleTypeOfAnalysis[0]
        || (this.selectedNumDaysAnalysis !== null
          && this.selectedNumDaysAnalysis !== undefined
          && this.selectedNumDaysAnalysis !== ''
          && this.selectedNumDaysAnalysis !== ' '
          && this.selectedNumDaysAnalysis > 0)) {
        this.computeTimeDivision();
      }
    }
  },
  mounted() {
      this.setFalseErrorNumSeqQueryTime();
      this.max_range = this.timeContent.length - 1;
      this.slider = [0, this.max_range];
      this.changeMarkerAndRender(0, this.max_range);
      this.computeTimeDivision();
  },
}
</script>

<style scoped>

  /deep/ .centered-input input {
    text-align: center
  }

</style>