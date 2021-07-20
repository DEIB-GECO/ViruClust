<template>
<div>
    <v-layout row wrap justify-center>
       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
         <v-layout row wrap justify-center>
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
              multiple
              :disabled="isLoading || possibleValues.length === 0 || field === null"
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
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";

export default {
  name: "SelectorQueryToExclude",
  props: {
    mode: {required: true,},
    field: {required: true,},
  },
  data() {
    return {
      possibleValues: [],
      isLoading: false,
      selectorDisabled: false,
      selected: [],
    }
  },
  computed: {
    ...mapState(['queryTime', 'toExcludeTime', 'queryGeo', 'toExcludeGeo',
                 'queryFreeTarget', 'toExcludeFreeTarget', 'queryFreeBackground', 'toExcludeFreeBackground']),
    ...mapGetters({}),
    // selected: {
    //   get() {
    //     if(this.mode === 'time') {
    //       return this.queryTime[this.field];
    //     }
    //     else if(this.mode === 'geo') {
    //       return this.queryGeo[this.field];
    //     }
    //     else if(this.mode === 'freetarget') {
    //       return this.queryFreeTarget[this.field];
    //     }
    //     else {
    //       return this.queryFreeBackground[this.field];
    //     }
    //   },
    //   set(value){
    //     if(this.mode === 'time') {
    //       this.setToExcludeTime({field: 'geo_group', list: []});
    //       this.setToExcludeTime({field: 'country', list: []});
    //       this.setToExcludeTime({field: 'region', list: []});
    //       this.setToExcludeTime({field: 'province', list: []});
    //       this.setToExcludeTime({field: this.field, list: value});
    //     }
    //     else if(this.mode === 'geo') {
    //       this.setToExcludeGeo({field: 'geo_group', list: []});
    //       this.setToExcludeGeo({field: 'country', list: []});
    //       this.setToExcludeGeo({field: 'region', list: []});
    //       this.setToExcludeGeo({field: 'province', list: []});
    //       this.setToExcludeGeo({field: this.field, list: value});
    //     }
    //     else if(this.mode === 'freetarget') {
    //       this.setToExcludeFreeTarget({field: 'geo_group', list: []});
    //       this.setToExcludeFreeTarget({field: 'country', list: []});
    //       this.setToExcludeFreeTarget({field: 'region', list: []});
    //       this.setToExcludeFreeTarget({field: 'province', list: []});
    //       this.setToExcludeFreeTarget({field: this.field, list: value});
    //     }
    //     else if(this.mode === 'freebackground') {
    //       this.setToExcludeFreeBackground({field: 'geo_group', list: []});
    //       this.setToExcludeFreeBackground({field: 'country', list: []});
    //       this.setToExcludeFreeBackground({field: 'region', list: []});
    //       this.setToExcludeFreeBackground({field: 'province', list: []});
    //       this.setToExcludeFreeBackground({field: this.field, list: value});
    //     }
    //   }
    // },
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setToExcludeTime', 'setToExcludeGeo', 'setToExcludeFreeTarget', 'setToExcludeFreeBackground']),
    getFieldText(item){
      let name = '';
      name = item['value'];
      return name;
    },
    loadData(){
      let query;
      if(this.mode === 'time') {
        query = JSON.parse(JSON.stringify(this.queryTime));
      }
      else if(this.mode === 'geo') {
        query = JSON.parse(JSON.stringify(this.queryGeo));
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
      }
      else if(this.mode === 'freetarget') {
        query = JSON.parse(JSON.stringify(this.queryFreeTarget));
      }
      else if(this.mode === 'freebackground') {
        query = JSON.parse(JSON.stringify(this.queryFreeBackground));
      }

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
      query['toExclude'] = [];
      to_send['field'] = this.field;
      to_send['query'] = query;

      axios.post(url, to_send)
          .then((res) => {
            return res.data;
          })
          .then((res) => {
            this.possibleValues = [];
            for(let i = 0; i < res.length; i = i +1){
              this.possibleValues.push(res[i]); // ['value']
            }
            this.isLoading = false;
          });
    },
    clearToExcludeField(){
      this.selected = [];
      if(this.mode === 'time') {
        this.setToExcludeTime({field: 'geo_group', list: []});
        this.setToExcludeTime({field: 'country', list: []});
        this.setToExcludeTime({field: 'region', list: []});
        this.setToExcludeTime({field: 'province', list: []});
      }
      else if(this.mode === 'geo') {
        this.setToExcludeGeo({field: 'geo_group', list: []});
        this.setToExcludeGeo({field: 'country', list: []});
        this.setToExcludeGeo({field: 'region', list: []});
        this.setToExcludeGeo({field: 'province', list: []});
      }
      else if(this.mode === 'freetarget') {
        this.setToExcludeFreeTarget({field: 'geo_group', list: []});
        this.setToExcludeFreeTarget({field: 'country', list: []});
        this.setToExcludeFreeTarget({field: 'region', list: []});
        this.setToExcludeFreeTarget({field: 'province', list: []});
      }
      else if(this.mode === 'freebackground') {
        this.setToExcludeFreeBackground({field: 'geo_group', list: []});
        this.setToExcludeFreeBackground({field: 'country', list: []});
        this.setToExcludeFreeBackground({field: 'region', list: []});
        this.setToExcludeFreeBackground({field: 'province', list: []});
      }
    }
  },
  mounted() {
    if(this.field !== null) {
      this.loadData();
    }
  },
  watch: {
    field(){
      if(this.field !== null) {
        this.clearToExcludeField();
        this.loadData();
      }
    },
    queryTime() {
      if(this.mode === 'time' && this.field !== null) {
        this.clearToExcludeField();
        this.loadData();
      }
    },
    queryGeo() {
      if(this.mode === 'geo' && this.field !== null) {
        this.clearToExcludeField();
        this.loadData();
      }
    },
    queryFreeTarget() {
      if(this.mode === 'freetarget' && this.field !== null) {
        this.clearToExcludeField();
        this.loadData();
      }
    },
    queryFreeBackground() {
      if(this.mode === 'freebackground' && this.field !== null) {
        this.clearToExcludeField();
        this.loadData();
      }
    },
    selected(){
      if(this.selected !== null) {
        if (this.mode === 'time') {
          this.setToExcludeTime({field: 'geo_group', list: []});
          this.setToExcludeTime({field: 'country', list: []});
          this.setToExcludeTime({field: 'region', list: []});
          this.setToExcludeTime({field: 'province', list: []});
          this.setToExcludeTime({field: this.field, list: this.selected});
        } else if (this.mode === 'geo') {
          this.setToExcludeGeo({field: 'geo_group', list: []});
          this.setToExcludeGeo({field: 'country', list: []});
          this.setToExcludeGeo({field: 'region', list: []});
          this.setToExcludeGeo({field: 'province', list: []});
          this.setToExcludeGeo({field: this.field, list: this.selected});
        } else if (this.mode === 'freetarget') {
          this.setToExcludeFreeTarget({field: 'geo_group', list: []});
          this.setToExcludeFreeTarget({field: 'country', list: []});
          this.setToExcludeFreeTarget({field: 'region', list: []});
          this.setToExcludeFreeTarget({field: 'province', list: []});
          this.setToExcludeFreeTarget({field: this.field, list: this.selected});
        } else if (this.mode === 'freebackground') {
          this.setToExcludeFreeBackground({field: 'geo_group', list: []});
          this.setToExcludeFreeBackground({field: 'country', list: []});
          this.setToExcludeFreeBackground({field: 'region', list: []});
          this.setToExcludeFreeBackground({field: 'province', list: []});
          this.setToExcludeFreeBackground({field: this.field, list: this.selected});
        }
      }
      else{
        this.clearToExcludeField();
      }
    }
  }
}
</script>

<style scoped>

  .item-value-span {
      padding-right: 3.5em;
  }

  .item-count-span {
      position: absolute;
      right: 0.5em;
  }

</style>