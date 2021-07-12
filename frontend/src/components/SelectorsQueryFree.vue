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
           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
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
         </v-layout>
       </v-flex>
    </v-layout>
    <v-layout>
      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding: 0; margin: 0;"
        v-if="this.selected === 'Europe'">
          <v-checkbox
            v-model="includeUK"
            hide-details
            input-value="true"
            label="Include UK"
            style="background-color: white; border: grey solid 1px; padding: 10px">
          </v-checkbox>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import SelectorsPieChart from "./SelectorsPieChart";

export default {
  name: "SelectorsQueryFree",
  components: {SelectorsPieChart},
  props: {
    field: {required: true,},
    type: {required: true,},
  },
  data() {
    return {
      possibleValues: [],
      isLoading: false,
      selectorDisabled: false,
      includeUK: true,
    }
  },
  computed: {
    ...mapState(['queryFreeTarget', 'queryFreeBackground', 'includeUKFreeTarget', 'includeUKFreeBackground']),
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
    ...mapMutations(['setIncludeUKFreeTarget', 'setIncludeUKFreeBackground']),
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
          query['includeUK'] = this.includeUKFreeTarget;
        }
        else if(this.type === 'background') {
          query['includeUK'] = this.includeUKFreeBackground;
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
    includeUK(){
      if(this.type === 'background') {
        this.setIncludeUKFreeBackground(this.includeUK);
      }
      else if(this.type === 'target') {
        this.setIncludeUKFreeTarget(this.includeUK);
      }
    },
    includeUKFreeTarget(){
      if(this.type === 'target') {
         this.loadData();
       }
    },
    includeUKFreeBackground(){
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