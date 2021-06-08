<template>
  <v-container fluid grid-list-xl style="justify-content: center; margin-top: 50px;">
    <v-row justify="center" align="center" v-if="nameMetadata !== 'date'">
      <v-container fluid grid-list-xl style="justify-content: center; width: 200px;">
        <v-select
          v-model="selectedMetadataFilter"
          :items="possibleMetadataFilter"
          label="Filter"
          multiple
          solo
          hide-details
          :disabled="disableMetadata"
        ></v-select>
      </v-container>
    </v-row>

    <v-row justify="center" align="center" v-else>
      <v-container fluid grid-list-xl style="justify-content: center; width: 350px; padding-bottom: 2px;">
        <v-text-field
            name="input-1"
            label="Filter"
            solo
            readonly
            v-model="shown_value"
            :append-icon="menuDate ? 'mdi-menu-down mdi-rotate-180' : 'mdi-menu-down'"
            @click="openMenu()"
            @click:append="openMenu()"
            hide-details
            :disabled="disableMetadata"
        >
        </v-text-field>
      </v-container>
    </v-row>
    <v-row justify="center" align="center" v-if="menuDate">
        <v-card>
          <v-card-text>
            <v-layout row wrap>
                <v-flex xs12 sm6>
                    <v-date-picker :type="dateType" v-model="min" :landscape="landscape" show-current no-title></v-date-picker>
                </v-flex>
                <v-flex xs12 sm6 class="hidden-xs-only">
                    <v-date-picker :type="dateType" v-model="max" :landscape="landscape" show-current no-title></v-date-picker>
                </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-actions class="justify-center">
              <v-btn
                      color="blue"
                      text
                      outlined
                      @click="setDate">
                  Apply
                  <v-icon dark right>mdi-checkbox-marked-circle</v-icon>
              </v-btn>
              <v-btn
                      color="red"
                      text
                      outlined
                      @click="deleteDate">
                  Clear
                  <v-icon dark right>mdi-cancel</v-icon>
              </v-btn>
          </v-card-actions>
        </v-card>
    </v-row>

    <v-row justify="center" align="center" style="margin-top: 40px">
      <v-container fluid grid-list-xl>
        <v-layout justify-center align-center>
          <v-btn
               @click="addFilter()"
               class="white--text"
               color="red"
               :disabled="disableMetadata"
          >
              APPLY
          </v-btn>
        </v-layout>
      </v-container>
    </v-row>

     <v-dialog
      persistent
    v-model="notProperDates"
    width="300"
  >
    <v-card>
      <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
        Select Proper Date
        <v-spacer></v-spacer>
        <v-btn
            style="background-color: rgb(122, 139, 157)"
            slot="activator"
            icon
            small
          color="white"
          @click="notProperDates = !notProperDates"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="text-xs-center">
        <span>
          <br>
          Select proper dates
        </span>
      </v-card-text>

    </v-card>
  </v-dialog>

  </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "SelectorFilter",
  props: {
    nameMetadata: {required: true,},
    metadataContent: {required: true,},
    filterDate: {required: false},
  },
  data(){
    return {
      possibleMetadataFilter: [],
      menuDate: false,
      landscape: false,
      shown_value: null,
      payload: null,
      min: null,
      max: null,
      dateType: "date",
      notProperDates: false,
      overlay: false,
    }
  },
  computed: {
    ...mapState(['selectedFilters', 'fileCSV', 'allMetadata', 'disableMetadata']),
    ...mapGetters({}),
    selectedMetadataFilter: {
      get() {
        return this.selectedFilters[this.nameMetadata];
      },
      set(value) {
        this.payload = {field: this.nameMetadata, list: value};
      }
    },
    textBoxValue() {
        let a = [];
        if (this.min != null)
            a.push('min: ' + this.min);
        if (this.max != null)
            a.push('max: ' + this.max);
        return a.join('; ');
    },
    selectedMin() {
        if (this.min) {
          return this.min
        }
        else{
          return null;
        }
    },
    selectedMax() {
        if (this.max) {
          return this.max
        }
        else{
          return null;
        }
    },
  },
  methods: {
    ...mapMutations(['setAllMetadata']),
    ...mapActions(['setSelectedFilter']),
    openMenu(){
      this.menuDate = !this.menuDate;
    },
    setDate() {
      if( this.min !== null && this.max !== null && this.min > this.max){
        this.notProperDates = true;
      }
      else {
        if(this.min !== null || this.max !== null) {
          let c = this.selectedMin;
          let b = this.selectedMax;

          let a = [{
            'min_val': c,
            'max_val': b,
          }];

          this.payload = {'field': this.nameMetadata, 'list': a};

          this.shown_value = this.textBoxValue;
        }

        this.menuDate = false;
      }
    },
    deleteDate() {
        this.payload = {'field': this.nameMetadata, 'list': []};
        this.min = null;
        this.max = null;
        this.shown_value = null;
        this.menuDate=false;
    },
    addFilter(){
      if(this.payload !== null) {
        this.setSelectedFilter(this.payload);
      }
    },
    chooseSelectableFilter(met){
      if (this.nameMetadata.includes('cluster')){
      met= met.sort(function(a, b) {
        let num1 = a['name'];
        let num2 = b['name'];
        return num1 - num2;
      });
    }
    else if (this.nameMetadata.includes('date')){
      met= met.sort(function(a, b) {
          let dt1 = a['name'];
          let p1 = dt1.split("-");
          let date1 = new Date(p1[0],p1[1],p1[2]);
          let dt2 = b['name'];
          let p2 = dt2.split("-");
          let date2 = new Date(p2[0],p2[1],p2[2]);
          return date1 > date2 ? 1 : -1;
      });
    }
    else {
      met = met.sort(function (a, b) {
        let num1 = a['name'];
        let num2 = b['name'];
        return num1 > num2 ? 1 : -1;
      })
    }

    let arr = [];
    let len = met.length;
    let i = 0;
    while (i < len){
      let val = met[i].name;
      arr.push(val)
      i = i + 1;
    }
    this.possibleMetadataFilter = arr;
    }
  },
  mounted() {
    //let met =  JSON.parse(JSON.stringify(this.metadataContent));
    //this.chooseSelectableFilter(met);
  },
  watch: {
    filterDate(){
      this.menuDate = false;
      this.min = null;
      this.max = null;

      if(this.filterDate === 'Month' || this.filterDate === 'Year'){
        this.dateType = "month";
      }
      else if(this.filterDate === 'Day') {
        this.dateType =  "date";
      }
    },
    selectedFilters(){
      if(this.nameMetadata === 'date'){
        if(!this.selectedFilters['date']){
          this.min = null;
          this.max = null;
          this.shown_value = this.textBoxValue;
        }
      }
    },
    metadataContent(){
      let met =  JSON.parse(JSON.stringify(this.metadataContent));
      this.chooseSelectableFilter(met);
    }
  }
}
</script>

<style scoped>

</style>