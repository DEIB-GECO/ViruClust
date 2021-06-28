<template>
  <v-layout row wrap justify-center>
     <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
       <v-layout row wrap justify-center>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
            <SelectorsPieChart
                :nameField = "field + field"
                :fieldContent= "possibleValues2"
                :isLoading = "isLoading">
            </SelectorsPieChart>
          </v-flex>
         <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
          <v-select
            v-model="selected2"
            :items="possibleValues2"
            :label="field === 'geo_group' ? 'continent' : field"
            solo
            clearable
            hide-details
            :item-text="getFieldText"
            :loading="isLoading"
            :disabled="isLoading || possibleValues2.length === 0"
          >
            <template slot="item" slot-scope="data">
                <span class="item-value-span">{{getFieldText(data.item)}}</span>
                <span class="item-count-span">{{data.item.count}}</span>
            </template>
          </v-select>
         </v-flex>
       </v-layout>
     </v-flex>
  </v-layout>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import SelectorsPieChart from "./SelectorsPieChart";

export default {
  name: "SelectorsQueryGeo",
  components: {SelectorsPieChart},
  props: {
    field: {required: true,},
  },
  data() {
    return {
      possibleValues2: [],
      isLoading: false,
      selectorDisabled: false,
    }
  },
  computed: {
    ...mapState(['queryGeo']),
    ...mapGetters({}),
    selected2: {
      get() {
        return this.queryGeo[this.field]
      },
      set(value){
        this.setQueryGeo({field: this.field, list: value})
      }
    },
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
        to_send['field'] = this.field;
        to_send['query'] = query;

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.possibleValues2 = res;
              this.isLoading = false;
            });
      }
      else{
        this.possibleValues2 = [];
        this.isLoading = false;
      }
    }
  },
  mounted() {
    this.loadData();
  },
  watch: {
    queryGeo() {
      this.loadData();
    }
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