<template>
  <div>
    <v-layout row wrap justify-center>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
         <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"
            v-if="field !== 'lineage'">
              <SelectorsPieChart
                  :nameField = "field"
                  :field = "field"
                  nameQuery = 'time'
                  :fieldContent= "possibleValues"
                  :isLoading = "isLoading">
              </SelectorsPieChart>
            </v-flex>
           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"  v-if="field !== 'lineage'">
            <v-autocomplete
              v-model="selected"
              :items="possibleValues"
              :label="field === 'geo_group' ? 'continent' : field"
              solo
              clearable
              hide-details
              :item-text="getFieldText"
              :loading="isLoading"
              :disabled="isLoading || possibleValues.length === 0"
            >
              <template slot="item" slot-scope="data">
                  <span class="item-value-span">{{getFieldText(data.item)}}</span>
                  <span class="item-count-span">{{data.item.count}}</span>
              </template>
            </v-autocomplete>
           </v-flex>

           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="field === 'lineage'">
              <LineageTreeSelector
              :isLoading = "isLoading"
              :possibleValues = "possibleValues"
              :radio_select = "radio_select"
              type = "time" style="width: 100%">
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
  name: "SelectorsQueryTime",
  components: {LineageTreeSelector, SelectorsPieChart},
  props: {
    field: {required: true,},
    radio_select: {required: false,},
  },
  data() {
    return {
      possibleValues: [],
      isLoading: false,
      selectorDisabled: false,
    }
  },
  computed: {
    ...mapState(['queryTime', 'toExcludeTime']),
    ...mapGetters({}),
    selected: {
      get() {
        return this.queryTime[this.field]
      },
      set(value){
        this.setQueryTime({field: this.field, list: value})
      }
    },
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryTime']),
    getFieldText(item){
      let name = '';
      name = item['value'];
      return name;
    },
    loadData(){
      if(!((this.field === 'province' && !this.queryTime['region']) ||
        (this.field === 'region' && !this.queryTime['country']) ||
        (this.field === 'country' && !this.queryTime['geo_group']))){

        this.isLoading = true;
        let url = `/analyze/selectorQuery`;
        let query = JSON.parse(JSON.stringify(this.queryTime));
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
        query['toExclude'] = [];
        to_send['field'] = this.field;
        to_send['query'] = query;

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.possibleValues = res;
              if(this.possibleValues.length === 0){
                this.selected = null;
                 this.setQueryTime({field: this.field, list: null})
              }
              this.isLoading = false;
            });
      }
      else{
        this.possibleValues = [];
        this.isLoading = false;
      }
    }
  },
  mounted() {
    this.loadData();
  },
  watch: {
    queryTime() {
      this.loadData();
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

</style>