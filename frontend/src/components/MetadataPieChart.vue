<template>
    <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <div :id="nameMetadata" style="width: 1200px; height: 500px; user-select: none;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
         background-color: white; margin-top: 50px">
        </div>
      </v-row>
    </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "MetadataPieChart",
  props: {
    nameMetadata: {required: true,},
    metadataContent: {required: true,},
    filterDate: {required: false},
  },
  data(){
    return {
      pieChart: {
        title: {
        },
        tooltip: {
            trigger: 'item'
        },
        series: [
            {
                type: 'pie',
                radius: '50%',
                data: [],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
      },
      my_chart: null,
    }
  },
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    renderGraph(met){
      this.pieChart.series[0].data = met.sort(function(a, b){
        let num1 = a['value'];
        let num2 = b['value'];
        return num1 - num2;
      });
      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.nameMetadata));
      }
      this.my_chart.setOption(this.pieChart, true);
    }
  },
  mounted() {
      let met =  JSON.parse(JSON.stringify(this.metadataContent));
      this.renderGraph(met);
  },
  watch: {
    metadataContent(){
      let met =  JSON.parse(JSON.stringify(this.metadataContent));
      this.renderGraph(met);
    },
    filterDate(){
      if(this.filterDate === 'Month'){
        let met =  JSON.parse(JSON.stringify(this.metadataContent));
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
        let met =  JSON.parse(JSON.stringify(this.metadataContent));
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
        let met =  JSON.parse(JSON.stringify(this.metadataContent));
        this.renderGraph(met);
      }
    }
  }
}
</script>

<style scoped>

</style>