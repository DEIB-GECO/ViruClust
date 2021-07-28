<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <v-card width="95%" style="margin-top:50px" color="#F1FAEE">
          <v-card-text>
            <v-layout row wrap justify-center style="padding: 30px;">
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center"
              v-for="(item) in listRes" v-bind:key="item.cluster + item.mutation[0] + item.mutation[1] + item.mutation[2] + item.lineage">
                <div :id="item.cluster + item.mutation[0] + item.mutation[1] + item.mutation[2] + item.lineage" style="width: 100%; background-color: #A8DADC">
                  <v-card width="100%" color="transparent">
                    <v-card-title>
                      <h5>{{item.mutation[1]}}{{item.mutation[0]}}{{item.mutation[2]}}
                      in cluster {{item.cluster}} vs lineage {{item.lineage}}</h5>
                      <v-spacer></v-spacer>
                      <v-btn class="white--text" color="blue" @click="setSelectedIndex(item.cluster + item.mutation[0] + item.mutation[1] + item.mutation[2] + item.lineage)"
                             data-html2canvas-ignore="true"
                              style="margin-right: 20px">
                        <span v-if="selectedIndex === item.cluster + item.mutation[0] + item.mutation[1] + item.mutation[2] + item.lineage">CLOSE </span>
                        <span v-else> MORE INFO </span>
                      </v-btn>
                    </v-card-title>
                    <v-card-text v-if="selectedIndex === item.cluster + item.mutation[0] + item.mutation[1] + item.mutation[2] + item.lineage">
                      <v-layout row wrap justify-center style="padding: 30px;">
                        <v-flex class="no-horizontal-padding xs10 d-flex">
                          <ul>
                            <li>
                              Number of sequences in cluster {{item.cluster}} with mutation
                              {{item.mutation[1]}}{{item.mutation[0]}}{{item.mutation[2]}}: {{item['# cluster']}}
                            </li>
                            <li v-if="item['% cluster'] !== 'N/D' && item['% cluster'] !== null">
                              Percentage of sequences in cluster {{item.cluster}} with mutation
                              {{item.mutation[1]}}{{item.mutation[0]}}{{item.mutation[2]}}: {{item['% cluster'].toPrecision(3) * 100}}%
                            </li>
                            <li v-else>
                              Percentage of sequences in cluster {{item.cluster}} with mutation
                              {{item.mutation[1]}}{{item.mutation[0]}}{{item.mutation[2]}}: N/D
                            </li>
                            <li v-if="item['% lineage'] !== 'N/D' && item['% lineage'] !== null">
                              Percentage of sequences in lineage {{item.lineage}} with mutation
                              {{item.mutation[1]}}{{item.mutation[0]}}{{item.mutation[2]}}: {{item['% lineage'].toPrecision(3) * 100}}%
                            </li>
                            <li v-else>
                              Percentage of sequences in lineage {{item.lineage}} with mutation
                              {{item.mutation[1]}}{{item.mutation[0]}}{{item.mutation[2]}}: N/D
                            </li>
                            <li v-if="item.FC !== 'N/D' && item.FC !== null">
                              Fold change (%cluster / %lineage): {{item.FC.toPrecision(3)}}
                            </li>
                            <li v-else>
                              Fold change (%cluster / %lineage): N/D
                            </li>
                            <li>
                                Spike domain(s):
                              <span>
                                <br>&emsp;* <span v-for="domain in item.annotations" v-bind:key="domain">{{domain}}</span>
                              </span>
                            </li>
                            <li>
                              Epitope (linear, from IEDB): sequence {{item.epi_seq}} from position {{item.epi_start}} to {{item.epi_stop}}
                              in Spike (combination of {{item['#linear']}} linear epitopes)
                            </li>
                            <li>
                              Publications linear epitopes:
                              <span>
                                <span v-for="linear_epi in item['pubs linear']" v-bind:key="linear_epi">
                                  <br>&emsp;* <a :href="linear_epi" target="_blank">{{linear_epi}}</a>
                                </span>
                              </span>
                            </li>
                            <li>
                              Epitope (non-linear, from IEDB): overlapping {{item['#non-linear']}} non-linear epitopes
                            </li>
                            <li>
                              Publications non-linear epitopes:
                              <span>
                                <span v-for="nonlinear_epi in item['pubs non-linear']" v-bind:key="nonlinear_epi">
                                  <br>&emsp;* <a :href="nonlinear_epi" target="_blank">{{nonlinear_epi}}</a>
                                </span>
                              </span>
                            </li>
                            <li>
                              Sequences:
                              <span>
                                <span v-for="(seq,key) in item.sequences" v-bind:key="key">
                                  <br><span style="margin-right: 20px;">&emsp;* {{seq}}</span>
                                  <v-btn icon class="white--text" x-small @click="getSequenceMetadata(seq)"
                                         data-html2canvas-ignore="true"
                                         style="margin-bottom: 5px">
                                    <v-icon style=" background-color: rgb(122, 139, 157); border-radius: 100%">mdi-dots-horizontal</v-icon>
                                  </v-btn>
                                  <span>
                                    <span v-for="(all_metadata) in sequenceMetadataToShow" v-bind:key="all_metadata['id']">
                                      <span v-if="all_metadata['id'] === seq">
                                        <span v-for="(meta, key, index) in all_metadata" v-bind:key="key + meta">
                                          <span v-if="key !== 'id'">
                                            <br>&emsp;&emsp;- {{key}} : {{meta}}
                                          </span>
                                          <span v-if="index+1 === Object.keys(all_metadata).length"><br></span>
                                        </span>
                                      </span>
                                    </span>
                                  </span>
                                </span>
                              </span>
                            </li>
                          </ul>
                        </v-flex>
                        <v-flex class="no-horizontal-padding xs2 d-flex" data-html2canvas-ignore="true" style="padding: 0">
                          <v-spacer></v-spacer>
                          <v-btn class="white--text" small color="rgb(122, 139, 157)" @click="downloadCardAsPDF(item.cluster + item.mutation[0] + item.mutation[1] + item.mutation[2] + item.lineage)">
                            <span>DOWNLOAD PDF</span>
                          </v-btn>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                  </v-card>
                </div>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-row>

    <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

  </v-container>

</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import { jsPDF } from 'jspdf'
import axios from "axios";

export default {
  name: "ListResults",
  props: {
    sortBy: {required: true,},
    sortDesc: {required: true,},
  },
  data(){
    return{
      selectedIndex: null,
      overlay: false,
      sequenceMetadataToShow: [],
    }
  },
  computed: {
    ...mapState(['listRes', 'listResFixed', 'sessionId']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations(['setListRes']),
    ...mapActions([]),
    setSelectedIndex(value){
       this.sequenceMetadataToShow = [];
       if(this.selectedIndex === value){
         this.selectedIndex = null;
       }
       else{
         this.selectedIndex = value;
       }
    },
    sortListRes(){
       if(this.sortBy.length > 0) {
         let len = this.sortBy.length;
         let results = JSON.parse(JSON.stringify(this.listRes));
         let that = this;
         return results.sort(function(a1, b1) {
              let i = 0;
              while(i < len) {
                let a = a1[that.sortBy[i]];
                let b = b1[that.sortBy[i]];
                let is_same = false;
                if (Array.isArray(a)){
                  is_same = (a.length === b.length) && a.every(function(element, index) {
                      return element === b[index];
                  });
                }
                else{
                  if(a === b){
                    is_same = true;
                  }
                }
                if(is_same && (i+1) < len){
                  i = i + 1;
                }
                else if (is_same && (i+1) >= len){
                  let a2 = a1['cluster'];
                  let b2 = b1['cluster'];
                  if (a2 === b2){
                    let a = a1['mutation'];
                    let b = b1['mutation'];
                    if (a[0] === b[0]) {
                      if (a[1] === b[1]) {
                        if(a[2] === "-"){
                          return 1;
                        }
                        else if(b[2] === "-"){
                          return -1;
                        }
                        else {
                          return a[2] > b[2] ? 1 : -1;
                        }
                      }
                      else{
                        if(a[1] === "-"){
                          return 1;
                        }
                        else if(b[1] === "-"){
                          return -1;
                        }
                        else {
                          return a[1] > b[1] ? 1 : -1;
                        }
                      }
                    }
                    else {
                      return parseInt(a[0],10) > parseInt(b[0], 10) ? 1 : -1;
                    }
                  }
                  else {
                    let num11 = a2.match(/\d+/g);
                    let num22 = b2.match(/\d+/g);
                    return num11[0] - num22[0];
                  }
                }
                else{
                  if(that.sortDesc[i] === false) {
                    if (that.sortBy[i] === 'cluster'){
                      let num1 = a.match(/\d+/g);
                      let num2 = b.match(/\d+/g);
                      return num1[0] - num2[0];
                    }
                    else if (that.sortBy[i] === 'mutation'){
                      if (a[0] === b[0]) {
                        if (a[1] === b[1]) {
                          if(a[2] === "-"){
                            return 1;
                          }
                          else if(b[2] === "-"){
                            return -1;
                          }
                          else {
                            return a[2] > b[2] ? 1 : -1;
                          }
                        }
                        else{
                          if(a[1] === "-"){
                            return 1;
                          }
                          else if(b[1] === "-"){
                            return -1;
                          }
                          else {
                            return a[1] > b[1] ? 1 : -1;
                          }
                        }
                      }
                      else {
                        return parseInt(a[0],10) > parseInt(b[0], 10) ? 1 : -1;
                      }
                    }
                    else {
                      return a > b ? 1 : -1;
                    }
                  }
                  else{
                    if (that.sortBy[i] === 'cluster'){
                      let num1 = a.match(/\d+/g);
                      let num2 = b.match(/\d+/g);
                      return num2[0] - num1[0];
                    }
                    else if (that.sortBy[i] === 'mutation'){
                      if (a[0] === b[0]) {
                        if (a[1] === b[1]) {
                          if(a[2] === "-"){
                            return -1;
                          }
                          else if(b[2] === "-"){
                            return 1;
                          }
                          else {
                            return a[2] < b[2] ? 1 : -1;
                          }
                        }
                        else{
                          if(a[1] === "-"){
                            return -1;
                          }
                          else if(b[1] === "-"){
                            return 1;
                          }
                          else {
                            return a[1] < b[1] ? 1 : -1;
                          }
                        }
                      }
                      else {
                        return parseInt(a[0],10) < parseInt(b[0], 10) ? 1 : -1;
                      }
                    }
                    else {
                      return a < b ? 1 : -1;
                    }
                  }
                }
              }
         });
       }
       else{
         let results = JSON.parse(JSON.stringify(this.listRes));
         return results.sort(function(a1, b1) {
           let a = a1['cluster'];
           let b = b1['cluster'];
           let num1 = a.match(/\d+/g);
           let num2 = b.match(/\d+/g);
           return num1[0] - num2[0];
         });
       }
    },
    downloadCardAsPDF(id){
      this.overlay = true;
      var pdf = new jsPDF('p', 'pt', 'a4');
      var element = (document.getElementById(id));
      let that = this;
      pdf.html(element, {
        html2canvas: {
            scale: 0.5,
        },
        callback: function (pdf) {
            pdf.save('card.pdf');
            that.overlay = false;
        }
      })
    },
    getSequenceMetadata(id){
      if(!this.sequenceMetadataToShow.some(item => item.id === id)) {
        let url = `/private/sequence?session_id=${this.sessionId}`
        let to_send = {'sequence_id': id};
        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              res['id'] = id;
              this.sequenceMetadataToShow.push(res);
            });
      }
      else{
        this.sequenceMetadataToShow.forEach(elem => {
          if (elem.id === id){
            this.sequenceMetadataToShow.splice(this.sequenceMetadataToShow.indexOf(elem), 1);
          }
        })
      }
    }
  },
  watch: {
    sortBy(){
      let list_sorted = this.sortListRes();
      this.setListRes(list_sorted);
    },
    sortDesc(){
      let list_sorted = this.sortListRes();
      this.setListRes(list_sorted);
    },
  },
}
</script>

<style scoped>

 ul li{
   margin-bottom: 10px;
 }

</style>