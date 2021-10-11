<template>
  <div>
    <v-layout row wrap justify-center>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
         <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"
            v-if="field !== 'lineage'">
              <SelectorsPieChart
                  :nameField = "field + field"
                  :field = "field"
                  nameQuery = 'geo'
                  :fieldContent= "possibleValues2"
                  :isLoading = "isLoading"
                  :pieChartBlocked = "pieChartBlocked">
              </SelectorsPieChart>
            </v-flex>
           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="field !== 'lineage'">
            <v-autocomplete
              v-model="selected2"
              :items="possibleValues2"
              :label="field === 'geo_group' ? 'continent' : field"
              solo
              clearable
              hide-details
              :item-text="getFieldText"
              :loading="isLoading"
              :disabled="isLoading || possibleValues2.length === 0 || pieChartBlocked"
              :multiple="checkMultiple()"
              style="position: relative"
            >
              <span slot="prepend-item" class="firstElement">
                Select multiple locations for separated analysis
              </span>
              <template slot="item" slot-scope="data">
                  <span class="item-value-span">{{getFieldText(data.item)}}</span>
                  <span class="item-count-span">{{data.item.count}}</span>
              </template>
            </v-autocomplete>
           </v-flex>

           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="field === 'lineage'">
              <LineageTreeSelector
                :isLoading = "isLoading"
                :possibleValues = "possibleValues2"
                :radio_select = "radio_select"
                type = "geo" style="width: 100%">
              </LineageTreeSelector>
           </v-flex>

         </v-layout>
       </v-flex>
    </v-layout>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import SelectorsPieChart from "./SelectorsPieChart";
import LineageTreeSelector from "./LineageTreeSelector";

export default {
  name: "SelectorsQueryGeo",
  components: {LineageTreeSelector, SelectorsPieChart},
  props: {
    field: {required: true,},
    radio_select: {required: false,},
  },
  data() {
    return {
      selected2: null,
      possibleValues2: [],
      isLoading: false,
      selectorDisabled: false,
      pieChartBlocked: false,
    }
  },
  computed: {
    ...mapState(['queryGeo', 'startDateQueryGeo', 'stopDateQueryGeo']),
    ...mapGetters({}),
    // selected2: {
    //   get() {
    //     return this.queryGeo[this.field]
    //   },
    //   set(value){
    //     this.setQueryGeo({field: this.field, list: value})
    //   }
    // },
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryGeo']),
    getFieldText(item){
      let name = '';
      name = item['value'];
      return name;
    },
    loadData(){
      if(!((this.field === 'province' && !this.queryGeo['region']) ||
        (this.field === 'region' && !this.queryGeo['country']) ||
        (this.field === 'country' && !this.queryGeo['geo_group']))){

        this.isLoading = true;
        let url = `/analyze/selectorQuery`;
        let query = JSON.parse(JSON.stringify(this.queryGeo));

        if(query['geo_group']){
          query['geo_group'] = query['geo_group'][0];
        }
        if(query['country']){
          query['country'] = query['country'][0];
        }
        if(query['region']){
          query['region'] = query['region'][0];
        }
        if(query['province']){
          query['province'] = query['province'][0];
        }

        let to_send = {};
        if (this.field === 'geo_group') {
          delete query['country'];
          delete query['region'];
          delete query['province'];
        } else if (this.field === 'country') {
          delete query['region'];
          delete query['province'];
        } else if (this.field === 'region') {
          delete query['province'];
        }
        // if(this.startDateQueryGeo){
        //   query['minDate'] = this.startDateQueryGeo;
        // }
        // if(this.stopDateQueryGeo){
        //   query['maxDate'] = this.stopDateQueryGeo;
        // }
        query['toExclude'] = [];
        to_send['field'] = this.field;
        to_send['query'] = query;

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.possibleValues2 = res;
              if(this.possibleValues2.length === 0){
                 this.selected2 = null;
                 this.setQueryGeo({field: this.field, list: null})
              }
              this.isLoading = false;
            });
      }
      else{
        this.possibleValues2 = [];
        this.isLoading = false;
      }
    },
    checkMultiple(){
      return !(this.field === 'lineage');
    },
    clearToExcludeField(){
      this.selected2 = [];
      this.setQueryGeo({field: this.field, list: []});
    }
  },
  mounted() {
    this.loadData();
  },
  watch: {
    queryGeo() {
      this.pieChartBlocked = false;
      if( ( this.field === 'country' && ( (this.queryGeo['geo_group'] && this.queryGeo['geo_group'].length > 1 ) ) ) ||
          ( this.field === 'region' && ( (this.queryGeo['country'] && this.queryGeo['country'].length > 1 ) || (this.queryGeo['geo_group'] && this.queryGeo['geo_group'].length > 1 ) ) ) ||
          ( this.field === 'province' && ( (this.queryGeo['region'] && this.queryGeo['region'].length > 1 ) || (this.queryGeo['country'] && this.queryGeo['country'].length > 1 ) || (this.queryGeo['geo_group'] && this.queryGeo['geo_group'].length > 1 ) ) )){
        this.pieChartBlocked = true;
      }

      this.loadData();
    },
    selected2() {
      if (this.selected2 !== null) {
        if(this.field === 'lineage'){
          this.setQueryGeo({field: this.field, list: null});
          this.setQueryGeo({field: this.field, list: this.selected2});
        }
        else {
          this.setQueryGeo({field: this.field, list: []});

          let copy = JSON.parse(JSON.stringify(this.selected2));

          // let that = this;
          // copy.sort((a, b) => {
          //   let index_a = that.possibleValues2.findIndex(function(item){
          //     return item['value'] === a;
          //   });
          //   let index_b = that.possibleValues2.findIndex(function(item){
          //     return item['value'] === b;
          //   });
          //
          //   let num_a = this.possibleValues2[index_a]['count'];
          //   let num_b = this.possibleValues2[index_b]['count'];
          //
          //   return num_a < num_b ? 1 : -1;
          // });

          this.setQueryGeo({field: this.field, list: copy});
        }
      } else {
        this.clearToExcludeField();
      }
    },
    'queryGeo.geo_group': function (){
        if(this.field === 'geo_group' && (!this.queryGeo['geo_group'] || this.queryGeo['geo_group'].length === 0)) {
          this.clearToExcludeField();
        }
    },
    'queryGeo.country': function (){
        if(this.field === 'country' && (!this.queryGeo['country'] || this.queryGeo['country'].length === 0)) {
          this.clearToExcludeField();
        }
    },
    'queryGeo.region': function (){
        if(this.field === 'region' && (!this.queryGeo['region'] || this.queryGeo['region'].length === 0)) {
          this.clearToExcludeField();
        }
    },
    'queryGeo.province': function (){
        if(this.field === 'province' && (!this.queryGeo['province'] || this.queryGeo['province'].length === 0 )) {
          this.clearToExcludeField();
        }
    },
  }
}
</script>

<style scoped>

  .item-value-span {
      padding-right: 3.5em;
  }

  .item-count-span {
      /*float:right;*/
      position: absolute;
      right: 0.5em;
  }

  .firstElement{
    padding: 5px;
    margin: 0;
    color: grey;
    text-align: center;
    border-bottom: grey solid 1px;
    position: sticky !important;
    position: -webkit-sticky !important;
    top: 0;
    z-index: 1;
    background: white;
  }

</style>