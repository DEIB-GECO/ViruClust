<template>
  <div>
    <v-layout wrap align-center justify-center style="margin-top: 50px">
      <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
        <v-layout wrap align-center justify-center style="margin-bottom: 50px">
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 20px">
            <h3>CLUSTER</h3>
          </v-flex>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
            <v-data-table
                    :headers="headerCluster"
                    :items="rowsCluster"
                    class="data-table"
                    style="width: 90%; margin-bottom: 50px; border: grey solid 1px"
                    :sort-by.sync="sortByCluster"
                    :sort-desc.sync="sortDescCluster"
            >
                <template v-slot:item ="{ item }">
                  <tr>
                    <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerCluster"
                        :key="header.value" v-show="header.show">
                      <span>
                        <span v-if="item[header.value] !== '' && item[header.value] !== null && item[header.value] !== undefined">
                          <span v-if="header.value === 'count_seq' || header.value === 'count_mutation'">
                            <v-btn class="white--text" color="blue" small @click="analyzeSeqOrMut(item, header.value, 'cluster')">
                              {{item[header.value]}}
                            </v-btn>
                          </span>
                          <span v-else>{{item[header.value]}}</span>
                        </span>
                        <span v-else>
                          <span>N/D</span>
                        </span>
                      </span>

                    </td>
                  </tr>
                </template>
                <template slot="body.append" style="text-align: center;">
                    <tr style="text-align: center; background-color: darkgrey">
                      <td><b>Tot: {{totNumCluster}}</b></td>
                      <td><b>Tot: {{totNumSeqCluster}}</b></td>
                      <td><b></b></td>
                    </tr>
                </template>
            </v-data-table>
          </v-flex>

          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
            <v-btn @click="downloadTable('cluster')"
                   class="white--text"
                       small
                   color="rgb(122, 139, 157)">
              Download Cluster Table</v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
        <v-layout wrap align-center justify-center style="margin-bottom: 50px">
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 20px">
            <h3>LINEAGE</h3>
          </v-flex>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
            <v-data-table
                    :headers="headerLineage"
                    :items="rowsLineage"
                    class="data-table"
                    style="width: 90%; margin-bottom: 50px; border: grey solid 1px"
                    :sort-by.sync="sortByLineage"
                    :sort-desc.sync="sortDescLineage"
            >
                <template v-slot:item ="{ item }">
                  <tr>
                    <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerLineage"
                        :key="header.value" v-show="header.show">
                      <span>
                        <span v-if="item[header.value] !== '' && item[header.value] !== null && item[header.value] !== undefined">
                          <span v-if="header.value === 'count_seq' || header.value === 'count_mutation'">
                            <v-btn class="white--text" color="blue" small @click="analyzeSeqOrMut(item, header.value, 'lineage')">
                              {{item[header.value]}}
                            </v-btn>
                          </span>
                          <span v-else>{{item[header.value]}}</span>
                        </span>
                        <span v-else>
                          <span>N/D</span>
                        </span>
                      </span>

                    </td>
                  </tr>
                </template>
                <template slot="body.append" style="text-align: center;">
                    <tr style="text-align: center; background-color: darkgrey">
                      <td><b>Tot: {{totNumLineage}}</b></td>
                      <td><b>Tot: {{totNumSeqLineage}}</b></td>
                      <td><b></b></td>
                    </tr>
                </template>
            </v-data-table>
          </v-flex>

          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
            <v-btn @click="downloadTable('lineage')"
                 class="white--text"
                     small
                 color="rgb(122, 139, 157)">
            Download Lineage Table</v-btn>
          </v-flex>
        </v-layout>
      </v-flex>

      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
        <v-layout wrap align-center justify-center style="margin-bottom: 50px">
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-bottom: 20px">
            <h3>GROUP CLUSTER - LINEAGE</h3>
          </v-flex>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
            <v-data-table
                    :headers="headerGroup"
                    :items="rowsGroup"
                    class="data-table"
                    style="width: 90%; margin-bottom: 50px; border: grey solid 1px"
                    :sort-by.sync="sortByGroup"
                    :sort-desc.sync="sortDescGroup"
            >
                <template v-slot:item ="{ item }">
                  <tr>
                    <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerGroup"
                        :key="header.value" v-show="header.show">
                      <span>
                        <span v-if="item[header.value] !== '' && item[header.value] !== null && item[header.value] !== undefined">
                          <span v-if="header.value === 'count_mutation_per_sequence'" style="white-space: nowrap; display: inline-block;">
                            <span v-for="(singMut, index) in item[header.value]" v-bind:key="index">
                              <span v-if="index !== 0"> , </span>
                              <span>{{singMut}}</span>
                            </span>
                          </span>
                          <span v-else-if="header.value === 'count_seq' || header.value === 'count_mutation'">
                            <v-btn class="white--text" color="blue" small @click="analyzeSeqOrMut(item, header.value, 'group')">
                              {{item[header.value]}}
                            </v-btn>
                          </span>
                          <span v-else>{{item[header.value]}}</span>
                        </span>
                        <span v-else>
                          <span v-if="header.value === 'analyze_mutation_per_sequence'">
                            <v-btn class="white--text" color="blue" small @click="analyzeMutPerSeq(item)">
                              ANALYZE MUT PER SEQ
                            </v-btn>
                          </span>
                          <span v-else>N/D</span>
                        </span>
                      </span>

                    </td>
                  </tr>
                </template>
                <template slot="body.append" style="text-align: center;">
                    <tr style="text-align: center; background-color: darkgrey">
                      <td colspan="2"><b>Tot: {{totNumGroup}}</b></td>
                      <td><b>Tot: {{totNumSeqGroup}}</b></td>
                      <td><b></b></td>
                      <td><b></b></td>
                      <td><b></b></td>
                    </tr>
                </template>

            </v-data-table>
          </v-flex>
          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
            <v-btn @click="downloadTable('group')"
                 class="white--text"
                     small
                 color="rgb(122, 139, 157)">
            Download Group Table</v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
  </v-layout>

  <v-dialog
      persistent
    v-model="dialogAnalyzeMutPerSeq"
    width="1200"
  >
    <v-card>
      <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
        ANALYSE MUTATION PER SEQUENCE
        <v-spacer></v-spacer>
        <v-btn
            style="background-color: rgb(122, 139, 157)"
            slot="activator"
            icon
            small
          color="white"
          @click="dialogAnalyzeMutPerSeq = !dialogAnalyzeMutPerSeq"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="text-xs-center">
        <span>
          <span v-for="(v,k) in analyzedMutPerSeqInstance" v-bind:key="k">
            <span v-if="k === 'infos'">
              <v-layout row wrap justify-center style="padding: 30px;">
                <v-card color="#F0E68C" width="500px" class="justify-center">
                  <v-card-title class="justify-center">
                      INFOS:
                  </v-card-title>
                  <v-card-text style="text-align: center;">
                    <span v-for="(value_info, key_info) in v" v-bind:key="key_info">
                      <b> - {{key_info}} : </b> {{value_info}} <br>
                    </span>
                  </v-card-text>
                </v-card>
              </v-layout>
            </span>
            <span v-else-if="k === 'sequences'">
              <v-layout row wrap justify-center style="padding: 30px;">
                <v-card color="#F0E68C" width="1000px" class="justify-center">
                  <v-card-title class="justify-center">
                      SEQUENCES:
                  </v-card-title>
                  <v-card-text>
                    <span v-for="(value_seq, index) in v" v-bind:key="index">
                      <b> - {{value_seq['seq']}} : </b><br>
                      <span v-for="(val_seq, key_seq) in value_seq['count']" v-bind:key="key_seq">
                          {{val_seq}}&nbsp;&nbsp;&nbsp;&nbsp;
                      </span>
                      <br><br>
                    </span>
                  </v-card-text>
                </v-card>
              </v-layout>
            </span>
          </span>
        </span>
      </v-card-text>
    </v-card>
  </v-dialog>

  <v-dialog
      persistent
    v-model="dialogShowSeqOrMut"
    width="1200"
  >
    <v-card>
      <v-card-title class="headline" style="background-color: #DAA520 ; color: white">
        ANALYSIS SEQUENCES / MUTATION
        <v-spacer></v-spacer>
        <v-btn
            style="background-color: rgb(122, 139, 157)"
            slot="activator"
            icon
            small
          color="white"
          @click="dialogShowSeqOrMut = !dialogShowSeqOrMut"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="text-xs-center">
        <span>
          <span v-for="(v,k) in selectedSequencesOrMutation" v-bind:key="k">
            <span v-if="k === 'infos'">
              <v-layout row wrap justify-center style="padding: 30px;">
                <v-card color="#F0E68C" width="500px" class="justify-center">
                  <v-card-title class="justify-center">
                      INFOS:
                  </v-card-title>
                  <v-card-text style="text-align: center;">
                    <span v-for="(value_info, key_info) in v" v-bind:key="key_info">
                      <b> - {{key_info}} : </b> {{value_info}} <br>
                    </span>
                  </v-card-text>
                </v-card>
              </v-layout>
            </span>
            <span v-else-if="k === 'sequences' || k === 'mutations'" >
              <v-layout row wrap justify-center style="padding: 30px;">
                <v-card color="#F0E68C" width="1000px" class="justify-center">
                  <v-card-title class="justify-center">
                      {{k.toUpperCase()}}:
                  </v-card-title>
                  <v-card-text>
                    <span v-for="(value_seq, index) in v" v-bind:key="index">
                      <span> - {{value_seq}} </span><br><br>
                    </span>
                  </v-card-text>
                </v-card>
              </v-layout>
            </span>
          </span>
        </span>
      </v-card-text>
    </v-card>
  </v-dialog>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "InputStats",
  data(){
    return{
      headerCluster: [],
      rowsCluster: [],
      headerLineage: [],
      rowsLineage: [],
      headerGroup: [],
      rowsGroup: [],
      totNumCluster: 0,
      totNumLineage: 0,
      totNumSeqCluster: 0,
      totNumSeqLineage: 0,
      totNumGroup: 0,
      totNumSeqGroup: 0,
      dialogAnalyzeMutPerSeq: false,
      dialogShowSeqOrMut: false,
      analyzedMutPerSeqInstance: {},
      selectedSequencesOrMutation: {},
      sortByCluster: [],
      sortDescCluster: [],
      sortByLineage: [],
      sortDescLineage: [],
      sortByGroup: [],
      sortDescGroup: [],
    }
  },
  computed: {
    ...mapState(['statisticsInput']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    downloadTable(table){
      let text = "";
      let result_sorted = this.sortResults(table);
      if(table === 'group') {
        text = this.json2csv(result_sorted, this.headerGroup);
      }
      if(table === 'lineage') {
        text = this.json2csv(result_sorted, this.headerLineage);
      }
      if(table === 'cluster') {
        text = this.json2csv(result_sorted, this.headerCluster);
      }
      let filename = table + '_table.csv';
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
          if(el.value !== 'analyze_mutation_per_sequence') {
            fields.push(el.text);
          }
        });
        selected_headers.forEach(function (el) {
          if(el.value !== 'analyze_mutation_per_sequence') {
            fields2.push(el.value);
          }
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
       let len
       let results
       let sortBy
       let sortDesc
       if(table === 'group') {
         len = this.sortByGroup.length;
         sortBy = this.sortByGroup;
         sortDesc = this.sortDescGroup;
         results = JSON.parse(JSON.stringify(this.rowsGroup));
       }
       if(table === 'lineage') {
         len = this.sortByLineage.length;
         sortBy = this.sortByLineage;
         sortDesc = this.sortDescLineage;
         results = JSON.parse(JSON.stringify(this.rowsLineage));
       }
       if(table === 'cluster') {
         len = this.sortByCluster.length;
         sortBy = this.sortByCluster;
         sortDesc = this.sortDescCluster;
         results = JSON.parse(JSON.stringify(this.rowsCluster));
       }
      if(len > 0) {
         return results.sort(function(a1, b1) {
            let i = 0;
            let a = a1[sortBy[i]];
            let b = b1[sortBy[i]];
            if(sortDesc[i] === false) {
              if (sortBy[i] === 'cluster_name'){
                let num1 = a.match(/\d+/g);
                let num2 = b.match(/\d+/g);
                return num1[0] - num2[0];
              }
              else {
                return a > b ? 1 : -1;
              }
            }
            else{
              if (sortBy[i] === 'cluster_name'){
                let num1 = a.match(/\d+/g);
                let num2 = b.match(/\d+/g);
                return num2[0] - num1[0];
              }
              else {
                return a < b ? 1 : -1;
              }
            }
         });
       }
       else{
         return results;
       }
    },
    analyzeMutPerSeq(item){
      this.dialogAnalyzeMutPerSeq = true;
      let all_stats_gr_c_mut_seq = JSON.parse(JSON.stringify(this.statisticsInput['stat_gr_c_mut_seq']));
      let id_seq = item['cluster_name'] + '-' + item['lineage_name'];
      let json_mut_per_seq = all_stats_gr_c_mut_seq[id_seq];

      json_mut_per_seq  = json_mut_per_seq.sort(function(a, b) {
          return a['count'].length - b['count'].length;
        });

      this.analyzedMutPerSeqInstance['infos'] = JSON.parse(JSON.stringify(item));
      this.analyzedMutPerSeqInstance['sequences'] = json_mut_per_seq;
    },
    analyzeSeqOrMut(item, header, table){
      this.selectedSequencesOrMutation = {};
      if(header === 'count_seq'){
        let all_stats = {};
        let id_seq = "";
        if(table === 'group'){
          all_stats = JSON.parse(JSON.stringify(this.statisticsInput['stat_group']));
          id_seq = item['cluster_name'] + '-' + item['lineage_name'];
        }
        else if(table === 'lineage'){
          all_stats = JSON.parse(JSON.stringify(this.statisticsInput['stat_lin']));
          id_seq = item['lineage_name'];
        }
        else if(table === 'cluster'){
          all_stats = JSON.parse(JSON.stringify(this.statisticsInput['stat_clu']));
          id_seq = item['cluster_name'];
        }
        let json_seq = all_stats[id_seq];

        json_seq  = json_seq.sort(function(a, b) {
          return a - b;
        });

        this.selectedSequencesOrMutation['infos'] = JSON.parse(JSON.stringify(item));
        this.selectedSequencesOrMutation['sequences'] = json_seq ;

      }
      else if (header === 'count_mutation'){
        let all_stats = {};
        let id_seq = "";
        if(table === 'group'){
          all_stats= JSON.parse(JSON.stringify(this.statisticsInput['stat_group_mut']));
          id_seq = item['cluster_name'] + '-' + item['lineage_name'];
        }
        else if(table === 'lineage'){
          all_stats = JSON.parse(JSON.stringify(this.statisticsInput['stat_lin_mut']));
          id_seq = item['lineage_name'];
        }
        else if(table === 'cluster'){
          all_stats = JSON.parse(JSON.stringify(this.statisticsInput['stat_clu_mut']));
          id_seq = item['cluster_name'];
        }
        let json_mut = all_stats[id_seq];

        json_mut  = json_mut.sort(function(a, b) {
          let spl1 = a.split("|");
          let spl2 = b.split("|");
          let a1 = parseInt(spl1[0]);
          let b1 = parseInt(spl2[0]);
          return a1 - b1;
        });

        this.selectedSequencesOrMutation['infos'] = JSON.parse(JSON.stringify(item));
        this.selectedSequencesOrMutation['mutations'] = json_mut;
      }
      this.dialogShowSeqOrMut = true;
    },
  },
  watch: {
  },
  mounted() {

    this.headerCluster = [
      {text: 'Cluster name', value: 'cluster_name', sortable: true, show: true, align: 'center', width: '15hv', sort: (a, b) => {
        let num1 = a.match(/\d+/g);
        let num2 = b.match(/\d+/g);
        return num1[0] - num2[0];
      }},
      {text: '# Sequences', value: 'count_seq', sortable: true, show: true, align: 'center', width: '15hv'},
      {text: '# Mutation', value: 'count_mutation', sortable: true, show: true, align: 'center', width: '15hv'},
    ];

    this.headerLineage = [
      {text: 'Lineage name', value: 'lineage_name', sortable: true, show: true, align: 'center', width: '15hv'},
      {text: '# Sequences', value: 'count_seq', sortable: true, show: true, align: 'center', width: '15hv'},
      {text: '# Mutation', value: 'count_mutation', sortable: true, show: true, align: 'center', width: '15hv'},
    ]

    this.headerGroup = [
      {text: 'Cluster name', value: 'cluster_name', sortable: true, show: true, align: 'center', width: '150px', sort: (a, b) => {
        let num1 = a.match(/\d+/g);
        let num2 = b.match(/\d+/g);
        return num1[0] - num2[0];
      }},
      {text: 'Lineage name', value: 'lineage_name', sortable: true, show: true, align: 'center', width: '150px'},
      {text: '# Sequences', value: 'count_seq', sortable: true, show: true, align: 'center', width: '150px'},
      {text: '# Mutation', value: 'count_mutation', sortable: true, show: true, align: 'center', width: '150px'},
      {text: '# Mutation per sequence', value: 'count_mutation_per_sequence', sortable: false, show: true, align: 'center', width: '15hv'},
      {text: 'Analyze mutation per sequence', value: 'analyze_mutation_per_sequence', sortable: false, show: true, align: 'center', width: '15hv'},
    ]

    let all_stats_cluster = JSON.parse(JSON.stringify(this.statisticsInput['stat_clu']));
    let all_stats_cluster_mut = JSON.parse(JSON.stringify(this.statisticsInput['stat_clu_mut']));
    let all_stats_lineage = JSON.parse(JSON.stringify(this.statisticsInput['stat_lin']));
    let all_stats_lineage_mut = JSON.parse(JSON.stringify(this.statisticsInput['stat_lin_mut']));
    let all_stats_group = JSON.parse(JSON.stringify(this.statisticsInput['stat_group']));
    let all_stats_group_mut = JSON.parse(JSON.stringify(this.statisticsInput['stat_group_mut']));
    let all_stats_gr_c_mut_seq = JSON.parse(JSON.stringify(this.statisticsInput['stat_gr_c_mut_seq']));

    this.rowsCluster = [];
    this.rowsLineage = [];
    this.rowsGroup = [];

    this.totNumSeqCluster = 0;
    this.totNumSeqLineage = 0;
    this.totNumSeqGroup = 0;

    Object.keys(all_stats_cluster).forEach(key => {
        let len = all_stats_cluster[key].length;
        let num_mut = all_stats_cluster_mut[key].length;
        let line = {'cluster_name': key, 'count_seq': len, 'count_mutation': num_mut};
        this.totNumSeqCluster = this.totNumSeqCluster + len;
        this.rowsCluster.push(line);
    });

    this.totNumCluster = this.rowsCluster.length;

    this.rowsCluster = this.rowsCluster.sort(function(a, b){
      let num1 = a['cluster_name'].match(/\d+/g);
      let num2 = b['cluster_name'].match(/\d+/g);
      return num1 - num2;
    });

    Object.keys(all_stats_lineage).forEach(key => {
        let len = all_stats_lineage[key].length;
        let num_mut = all_stats_lineage_mut[key].length;
        let line = {'lineage_name': key, 'count_seq': len, 'count_mutation': num_mut};
        this.totNumSeqLineage = this.totNumSeqLineage + len;
        this.rowsLineage.push(line);
    });

    this.totNumLineage = this.rowsLineage.length;

    this.rowsLineage = this.rowsLineage.sort(function(a, b){
      let num1 = a['lineage_name'];
      let num2 = b['lineage_name'];
      return num1 > num2 ? 1 : -1;
    });


    Object.keys(all_stats_group).forEach(key => {
        let strings = key.split("-");
        let arrMutSeq = []
        let single_stats_mut_seq = all_stats_gr_c_mut_seq[key];
        let len2 = single_stats_mut_seq.length;
        let i = 0;
        while (i<len2){
          arrMutSeq.push(single_stats_mut_seq[i]['count'].length);
          i = i + 1;
        }

        arrMutSeq = arrMutSeq.sort(function(a, b) {
          let a1 = parseInt(a);
          let b1 = parseInt(b);
          return a1 - b1;
        });

        let len = all_stats_group[key].length;
        let num_mut = all_stats_group_mut[key].length;
        let line = {'cluster_name': strings[0], 'lineage_name': strings[1], 'count_seq': len, 'count_mutation': num_mut, 'count_mutation_per_sequence': arrMutSeq};
        this.totNumSeqGroup = this.totNumSeqGroup + len;
        this.rowsGroup.push(line);
    });

    this.totNumGroup = this.rowsGroup.length;

    this.rowsGroup = this.rowsGroup.sort(function(a, b){
      let num1 = a['cluster_name'].match(/\d+/g);
      let num2 = b['cluster_name'].match(/\d+/g);
      return num1 - num2;
    });


    //// PER TABELLA ANALISI SEQ MUT ARRAY

    // let seq_mut_arr = JSON.parse(JSON.stringify(this.statisticsInput['sequence_mutation_arr']));
    //
    // this.headerLineage = [];
    //
    // let single_line = seq_mut_arr[0];
    //       let headers = [];
    //       Object.keys(single_line).forEach(key => {
    //           let single_header = {};
    //           single_header['text'] = key;
    //           single_header['value'] = key;
    //
    //           single_header['show'] = true;
    //           single_header['align'] = 'center';
    //           single_header['width'] = '18vh';
    //
    //           headers.push(single_header);
    //       })
    // this.headerLineage = headers;
    //
    // this.rowsLineage = seq_mut_arr;


    //// PER TABELLA LINEAGE COUNTRY

    // let seq_mut_arr = JSON.parse(JSON.stringify(this.statisticsInput['lineage_country_arr']));
    //
    // this.headerLineage = [];
    //
    // let ii = 0;
    // let len_arr = seq_mut_arr.length;
    // let headers = [];
    // let arr_name_headers = [];
    // while (ii < len_arr) {
    //   let single_line = seq_mut_arr[ii];
    //   Object.keys(single_line).forEach(key => {
    //     if(!arr_name_headers.includes(key) && key !== 'lineage') {
    //       let single_header = {};
    //       arr_name_headers.push(key);
    //       single_header['text'] = key;
    //       single_header['value'] = key;
    //
    //       single_header['show'] = true;
    //       single_header['align'] = 'center';
    //       single_header['width'] = '18vh';
    //
    //       headers.push(single_header);
    //     }
    //   })
    //   ii = ii + 1;
    // }
    //
    // headers.sort( function( a, b ) {
    //     a = a.value.toLowerCase();
    //     b = b.value.toLowerCase();
    //
    //     return a < b ? -1 : a > b ? 1 : 0;
    // });
    //
    // let lineage_header = {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '18vh'};
    //
    // headers.unshift(lineage_header);
    //
    // this.headerLineage = headers;
    //
    // this.rowsLineage = seq_mut_arr;

  }
}
</script>

<style scoped>

</style>