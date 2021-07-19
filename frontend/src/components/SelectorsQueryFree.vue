<template>
  <div>
    <v-layout row wrap justify-center>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
         <v-layout row wrap justify-center>
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"
            v-if="field !== 'lineage'">
              <SelectorsPieChart
                  :nameField = "type + field"
                  :field = "field"
                  :nameQuery = "'free' + type"
                  :fieldContent= "possibleValues"
                  :isLoading = "isLoading">
              </SelectorsPieChart>
            </v-flex>
           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="field !== 'lineage'">
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
                :type = "type" style="width: 100%">
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
  name: "SelectorsQueryFree",
  components: {LineageTreeSelector, SelectorsPieChart},
  props: {
    field: {required: true,},
    type: {required: true,},
  },
  data() {
    return {
      possibleValues: [],
      isLoading: false,
      selectorDisabled: false,
    }
  },
  computed: {
    ...mapState(['queryFreeTarget', 'queryFreeBackground', 'toExcludeFreeTarget', 'toExcludeFreeBackground']),
    ...mapGetters({}),
    selected: {
      get() {
        if(this.type === 'target'){
          return this.queryFreeTarget[this.field];
        }
        else if (this.type === 'background'){
          return this.queryFreeBackground[this.field];
        }
        else {
          return 0;
        }
      },
      set(value){
        if(this.type === 'target'){
          this.setQueryFreeTarget({field: this.field, list: value});
        }
        else if (this.type === 'background'){
          this.setQueryFreeBackground({field: this.field, list: value});
        }
      }
    },
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryFreeTarget', 'setQueryFreeBackground']),
    getFieldText(item){
      let name = '';
      name = item['value'];
      return name;
    },
    loadData(){
      let query ;
      if(this.type === 'target') {
        query = JSON.parse(JSON.stringify(this.queryFreeTarget));
      }
      else if(this.type === 'background') {
        query = JSON.parse(JSON.stringify(this.queryFreeBackground));
      }

      if(!((this.field === 'province' && !query['region']) ||
        (this.field === 'region' && !query['country']) ||
        (this.field === 'country' && !query['geo_group']))){

        this.isLoading = true;
        let url = `/analyze/selectorQuery`;
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

        if(this.type === 'target') {
          query['toExclude'] = [];
        }
        else if(this.type === 'background') {
          query['toExclude'] = [];
        }
        to_send['field'] = this.field;
        to_send['query'] = query;

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.possibleValues = res;
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
    queryFreeTarget() {
      if(this.type === 'target') {
        this.loadData();
      }
    },
    queryFreeBackground() {
      if(this.type === 'background') {
        this.loadData();
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

</style>