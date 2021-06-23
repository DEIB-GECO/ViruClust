<template>
  <div>
    <v-card width="100%" color="#F0E68C" style="margin-bottom: 50px; margin-top: 50px; padding: 50px">
      <v-row justify="center" align="center">
        <v-card width="600px" style="padding: 50px" color="#DAA520">
          <v-card-title class="justify-center">
            DISTRIBUTION LINEAGE IN GEO
          </v-card-title>
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
              <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                <v-select
                  v-model="selectedGeo"
                  :items="possibleGeo"
                  label="Geo"
                  solo
                  hide-details
                ></v-select>
              </v-flex>
              <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                <v-select
                  v-model="selectedSpecificGeo"
                  :items="possibleSpecificGeo"
                  label="Geo"
                  solo
                  hide-details
                ></v-select>
              </v-flex>
              <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                <v-text-field v-model="selectedGeoCount" solo type="number"></v-text-field>
              </v-flex>
             </v-layout>
             <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
               <v-btn
                       @click="applyTableLineageCountry()"
                       color="red"
                       class="white--text"
                       :disabled="selectedGeo === null || selectedSpecificGeo === null"
                >
                    APPLY
                </v-btn>
             </v-flex>
           </v-card-text>
        </v-card>
      </v-row>
      <v-row justify="center" align="center" v-if="headerTableLineageCountry.length !== 0">
        <v-card width="1600px" style="margin-bottom: 50px; margin-top:50px; padding: 50px" color="#DAA520">
           <v-card-text>
             <v-layout row wrap justify-center style="padding: 30px;">
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                  <v-data-table
                        :headers="headerTableLineageCountry"
                        :items="rowsTableLineageCountry"
                        class="data-table table_distribution_lineage_geo"
                        style="width: 90%; margin-bottom: 50px; border: grey solid 1px"
                        :sort-by.sync="sortByTableLineageCountry"
                        :sort-desc.sync="sortDescTableLineageCountry"
                  >
                      <template v-slot:item ="{ item }">
                        <tr>
                          <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerTableLineageCountry"
                              :key="header.value" v-show="header.show" :title="item['lineage']">
                                <span>{{item[header.value]}}</span>
                          </td>
                        </tr>
                      </template>
                  </v-data-table>
              </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                  <v-btn @click="downloadTable('table_geo')"
                         class="white--text"
                         small
                         color="rgb(122, 139, 157)">
                    Download Table</v-btn>
               </v-flex>
             </v-layout>
           </v-card-text>
        </v-card>
      </v-row>
    </v-card>

    <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";

export default {
  name: "AnalyzeDistributionLineageInGeo",
  data() {
    return {
      overlay: false,
      selectedGeo: null,
      possibleGeo: ['geo_group', 'country', 'region'],
      selectedSpecificGeo: null,
      possibleSpecificGeo: [],
      selectedGeoCount: 1000,
      headerTableLineageCountry: [],
      rowsTableLineageCountry: [],
      sortByTableLineageCountry: [],
      sortDescTableLineageCountry: [],
    }
  },
  computed: {
    ...mapState(['all_geo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllGeo']),
    ...mapActions([]),
    downloadTable(table){
      let text = "";
      let result_sorted = this.sortResults(table);
      if(table === 'table_geo'){
        text = this.json2csv(result_sorted, this.headerTableLineageCountry);
      }
      let filename = 'result.csv';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    json2csv(input, selected_headers) {
        var json = input;
        var fields = [];
        var fields2 = [];
        selected_headers.forEach(function (el) {
            fields.push(el.text);
        });
        selected_headers.forEach(function (el) {
            fields2.push(el.value);
        });
        var csv = json.map(function (row) {
            return fields2.map(function (fieldName) {
                let string_val ;
                string_val = String(row[fieldName]);
                string_val = string_val.replaceAll("\n", " ");
                return JSON.stringify(string_val);
            }).join(',')
        });
        csv.unshift(fields.join(','));
        return csv.join('\r\n')
    },
    sortResults(table){
      let len;
      let sortBy;
      let sortDesc;
      let results;
      if(table === 'table_geo'){
        len = this.sortByTableLineageCountry.length;
        sortBy = this.sortByTableLineageCountry;
        sortDesc = this.sortDescTableLineageCountry;
        results = JSON.parse(JSON.stringify(this.rowsTableLineageCountry));
      }
      if(len > 0) {
         return results.sort(function(a1, b1) {
            let i = 0;
            let a = a1[sortBy[i]];
            let b = b1[sortBy[i]];
            if(sortDesc[i] === false) {
                return a > b ? 1 : -1;
            }
            else{
                return a < b ? 1 : -1;
            }
         });
       }
       else{
         return results;
       }
    },
    applyTableLineageCountry(){
      this.headerTableLineageCountry = [];
      this.rowsTableLineageCountry = [];
      this.overlay = true;
      let url = `/analyze/tableLineageCountry`;
      let to_send = {'type': this.selectedGeo, 'value': this.selectedSpecificGeo, 'minCountSeq': this.selectedGeoCount};
      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          let seq_mut_arr = JSON.parse(JSON.stringify(res));
          this.headerTableLineageCountry = [];

          let ii = 0;
          let len_arr = seq_mut_arr.length;
          let headers = [];
          let arr_name_headers = [];
          while (ii < len_arr) {
            let single_line = seq_mut_arr[ii];
            Object.keys(single_line).forEach(key => {
              if(!arr_name_headers.includes(key) && key !== 'lineage') {
                let single_header = {};
                arr_name_headers.push(key);
                if (key === null || key === ''){
                  single_header['text'] = 'N/D';
                }
                else {
                  single_header['text'] = key;
                }

                single_header['value'] = key;
                single_header['show'] = true;
                single_header['align'] = 'center';
                single_header['width'] = '20vh';

                headers.push(single_header);
              }
              else if (key !== 'lineage'){
                if (single_line['lineage'] === null || key === ''){
                  single_line['lineage'] = 'N/D';
                }
              }
            })
            ii = ii + 1;
          }

          headers.sort( function( a, b ) {
              a = a.value.toLowerCase();
              b = b.value.toLowerCase();

              return a < b ? -1 : a > b ? 1 : 0;
          });

          let lineage_header = {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '20vh'};

          headers.unshift(lineage_header);

          this.headerTableLineageCountry = headers;

          this.rowsTableLineageCountry = seq_mut_arr;

          this.overlay = false;

        });
    },
  },
  watch: {
    selectedGeo(){
      this.headerTableLineageCountry = [];
      this.rowsTableLineageCountry = [];
      if(this.selectedGeo !== null){
        let array_specific_geo = [];
        this.all_geo.forEach(elem => {
          if(elem[this.selectedGeo] !== null) {
            if (!array_specific_geo.includes(elem[this.selectedGeo])) {
              array_specific_geo.push(elem[this.selectedGeo]);
            }
          }
        })
        array_specific_geo.sort( function( a, b ) {
          a = a.toLowerCase();
          b = b.toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
        });
        this.possibleSpecificGeo = array_specific_geo;
      }
    },
    selectedSpecificGeo() {
      this.headerTableLineageCountry = [];
      this.rowsTableLineageCountry = [];
    },
  },
  mounted() {
    let url = `/analyze/allGeo`;
    axios.get(url)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.setAllGeo(res);

    });
  }
}
</script>

<style scoped>

  .table_distribution_lineage_geo table > tbody > tr > td:nth-child(1){
    box-shadow: inset -0.5px 0 0 0 grey;
  }
  /*position: sticky !important;*/
  /*  position: -webkit-sticky !important;*/
  /*  left: 0px;*/
  /*  z-index: 9998;*/
  /*  background: white;*/

</style>