<template>
  <div style="align-content: center; text-align: center">
    <div>
      <v-dialog width="1500" v-model="dialogMutations" persistent>
          <template v-slot:activator="{ on }">
            <v-btn
                v-on="on"
                slot="activator"
                class="white--text"
                 small
                 color="#1D3557"
                 style="margin-bottom: 10px"
                :disabled="(radio_group_lineage === 'only_lineage')"
            >
              ADD SET OF MUTATIONs ({{mutationToInsert.length}})
            </v-btn>
          </template>
          <v-card>
              <v-card-title
                      class="headline"
                      style="background-color: #A8DADC"
              >
                  ADD MUTATIONs:
                <v-spacer></v-spacer>
                <v-btn
                  color="black"
                  text
                  @click="deleteAllAccMutationsInserted();"
                >
                  DELETE ALL
                </v-btn>
              </v-card-title>
              <v-card-text style="text-align: center;">
                <v-container>
                  <v-layout row wrap justify-space-around style="border: black solid 1px; background-color: #F1FAEE; border-radius: 20px; margin: 10px; padding: 20px">
                    <v-flex class="no-horizontal-padding xs5 md2 d-flex" style="justify-content: center; margin-bottom: 10px">
                      <v-autocomplete
                        v-model="selectedProtein"
                        :items="possibleProteins"
                        label="Protein"
                        solo
                        clearable
                        hide-details>
                      </v-autocomplete>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs5 md2 d-flex" style="justify-content: center; margin-bottom: 10px">
                      <v-autocomplete
                        v-model="selectedOriginalAminoAcid"
                        :items="possibleAminoAcidsOriginal"
                        label="Original AminoAcid"
                        solo
                        clearable
                        hide-details>
                      </v-autocomplete>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs5 md2 d-flex" style="justify-content: center; margin-bottom: 10px">
                      <v-text-field
                          id="positionSelector"
                          v-model.number="selectedPosition"
                          solo
                          class="centered-input"
                          min="1"
                          :max="maxPositionProtein"
                          type="number"
                          label="Position"
                          hide-details>
                      </v-text-field>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs5 md2 d-flex" style="justify-content: center; margin-bottom: 10px">
                      <v-autocomplete
                        v-model="selectedAlternativeAminoAcid"
                        :items="possibleAminoAcidsAlternative"
                        label="Alternative AminoAcid"
                        solo
                        clearable
                        hide-details>
                      </v-autocomplete>
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;"></v-flex>
                    <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                      <v-btn
                          @click="addMutation()"
                           color="#E63946"
                           :disabled = "selectedPosition === null || selectedProtein === null
                           || selectedAlternativeAminoAcid === null
                           || selectedPosition > maxPositionProtein || selectedPosition < minPositionProtein
                           || selectedOriginalAminoAcid === selectedAlternativeAminoAcid"
                           class="white--text">ADD</v-btn> <!-- || selectedOriginalAminoAcid === null||  -->
                    </v-flex>
                    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;
                     margin-top: 30px; margin-bottom: 10px">
                     <v-layout row wrap justify-center>
                     <v-flex class="no-horizontal-padding xs12 md6 lg4 d-flex" style="justify-content: center;
                     border: black solid 1px; border-radius: 20px;">
                       <v-card width="400px" color="transparent" outlined >
                          <v-card-title class="justify-center">
                            <h5>UPLOAD MUTATIONS:</h5>
                            <v-dialog width="500">
                                <template v-slot:activator="{ on }">
                                  <v-btn
                                        v-on="on"
                                          slot="activator"
                                          class="info-button"
                                          x-small
                                          text icon color="grey"
                                          style="margin-bottom: 5px; margin-left: 20px">
                                      <v-icon class="info-icon">mdi-information</v-icon>
                                  </v-btn>
                                </template>
                                <v-card>
                                    <v-card-title
                                            class="headline grey lighten-2"
                                            primary-title
                                    >
                                        UPLOAD MUTATIONS:
                                    </v-card-title>
                                    <v-card-text style="text-align: center;">
                                     <span>
                                      <br><br>
                                     </span>
                                      <span><b>EXAMPLE OF FILE</b> <v-btn @click="downloadExampleMutations()" x-small icon
                                        style="margin-left: 20px;">
                                          <v-icon size="18">
                                            mdi-download-circle-outline
                                          </v-icon>
                                      </v-btn></span>
                                    </v-card-text>
                                </v-card>
                            </v-dialog>
                          </v-card-title>
                          <v-card-text>
                             <v-layout wrap justify-space-around>
                                <v-flex class="no-horizontal-padding xs3 d-flex" style="justify-content: center;">
                                  <input id="inputMutationsFile" type="file" style="display:none"
                                               v-on:change="loadMutationsFile()"
                                               onclick="document.getElementById('inputMutationsFile').value = ''"
                                        />
                                  <v-btn
                                         onclick="document.getElementById('inputMutationsFile').click()"
                                         class="white--text"
                                         small
                                         color="#E63946"
                                         style="margin-top: 10px"
                                  >
                                      Upload file
                                  </v-btn>
                                </v-flex>
                               <v-flex class="no-horizontal-padding xs8 d-flex" style="justify-content: center;">
                                 <v-text-field
                                  :value = this.nameFileMutations
                                  solo
                                  readonly
                                  hide-details
                                  style="margin-right: 10px"
                                ></v-text-field>
                                 <v-btn
                                    style="background-color: red; margin-top: 10px;"
                                    icon
                                    x-small
                                  color="white"
                                    @click="deleteMutationsFile()"
                                >
                                  <v-icon size="18">mdi-close</v-icon>
                                </v-btn>
                               </v-flex>
                             </v-layout>
                          </v-card-text>
                       </v-card>
                     </v-flex>
                   </v-layout>
                    </v-flex>
                  </v-layout>
                  <v-spacer></v-spacer>
                  <v-layout row wrap justify-center style="margin: 10px; padding: 10px">
                      <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; margin-bottom: 20px">
                        <h2>LIST OF MUTATIONs ({{mutationToInsert.length}})</h2>
                      </v-flex>
                      <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                        <div style="width: 80%">
                          <v-data-table
                                :headers="headerMutation"
                                :items="mutationToInsert"
                                class="data-table table_analyze_time"
                                style="width: 100%; border: grey solid 1px"
                          >
                              <template v-slot:item ="{ item }">
                                <tr>
                                  <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center; align-content: center" v-for="header in headerMutation"
                                      :key="header.value" v-show="header.show">
                                        <span v-if="header.value === 'index'">
                                          <v-btn
                                              style="background-color: #E63946"
                                              slot="activator"
                                              icon
                                              small
                                            color="white"
                                            @click="deleteSingleMutation(item[header.value])"
                                          >
                                            <v-icon>mdi-close</v-icon>
                                          </v-btn>
                                        </span>
                                        <span v-else>{{item[header.value]}}</span>
                                  </td>
                                </tr>
                              </template>
                          </v-data-table>
                        </div>
                      </v-flex>
                  </v-layout>
                  <v-spacer></v-spacer>
                  <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
                          <span>DOWNLOAD LIST OF MUTATIONS (.txt) <v-btn @click="downloadMutationsAsTxt()" x-small icon
                                  style="margin-left: 20px; margin-bottom: 5px">
                                    <v-icon size="23">
                                      mdi-download-circle-outline
                                    </v-icon>
                                </v-btn>
                          </span>
                      </v-flex>
                  <v-spacer></v-spacer>
                  <v-layout row wrap justify-center style="margin-top: 20px">
                      <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">
                        <v-btn
                            @click="confirmMutations()"
                             color="#E63946"
                             class="white--text">CONFIRM</v-btn>
                      </v-flex>
  <!--                    <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center;">-->
  <!--                      <v-btn-->
  <!--                          @click="exitMutationPanel()"-->
  <!--                           color="#E63946"-->
  <!--                           class="white&#45;&#45;text">CLEAR & EXIT</v-btn>-->
  <!--                    </v-flex>-->
                  </v-layout>
                </v-container>
              </v-card-text>
          </v-card>
      </v-dialog>
    </div>
    <div>
      <span v-for="(mutation, index) in listOfMutation" v-bind:key="index">
        <span v-if="index === 0"> [ </span>
        {{mutation}}
        <span v-if="index < listOfMutation.length - 1"> - </span>
        <span v-else> ] </span>
      </span>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";

export default {
  name: "SetMutationPanel",
  props: {
    radio_group_lineage: {required: true,},
    type:  {required: true,},
  },
  data() {
    return {
      listOfMutation: [],
      nameFileMutations: null,
      mutationToInsert: [],
      dialogMutations: false,
      possibleProteins: [],
      selectedProtein: null,
      selectedPosition: null,
      maxPositionProtein: 1000000,
      minPositionProtein: 1,
      possibleAminoAcidsOriginal: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'Y', 'W', 'Z'],
      possibleAminoAcidsAlternative: ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'Y', 'W', 'Z'],
      selectedOriginalAminoAcid: null,
      selectedAlternativeAminoAcid: null,
      headerMutation: [
        {'text': 'Protein', 'value': 'product', 'show': true, 'align': 'center'},
        {'text': 'Original AA', 'value': 'sequence_aa_original', 'show': true, 'align': 'center'},
        {'text': 'Position', 'value': 'start_aa_original', 'show': true, 'align': 'center'},
        {'text': 'Alternative AA', 'value': 'sequence_aa_alternative', 'show': true, 'align': 'center'},
        {'text': 'Delete', 'value': 'index', 'show': true, 'align': 'center'},
      ]
    }
  },
  computed: {
    ...mapState(['queryTime', 'all_protein', 'queryGeo', 'queryFreeTarget', 'queryFreeBackground']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryTime', 'setQueryGeo', 'setQueryFreeTarget', 'setQueryFreeBackground']),
    recalculateIndexAfterDeletion(){
      for(let i = 0; i < this.mutationToInsert.length; i = i + 1) {
        this.mutationToInsert[i]['index'] = i;
      }
    },
    downloadExampleMutations(){
      let text;
      text = 'Spike\tD614G\n' +
          'Spike\tL452R\n' +
          'NSP12\tP323L\n' +
          'NSP6\tS106-\n' +
          'NSP6\tG107-\n' +
          'NSP6\tF108-\n' +
          'E\tL21F\n' +
          'M\tI82T';
      let filename = 'exampleListMutations.txt';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    loadMutationsFile(){
      this.deleteMutationsFile();
      this.nameFileMutations = null;
      let reader = new FileReader();
      let selectedFile = document.getElementById ('inputMutationsFile'). files[0];
      this.nameFileMutations = selectedFile.name;
      let that = this;
      reader.onload = function() {
        let arrayIds = reader.result.split(/(?:;|\n)+/);
        for(let i = 0; i < arrayIds.length; i = i + 1) {
          if (arrayIds[i] !== null && arrayIds[i] !== undefined) {
            let obj = {}
            let single_mut = arrayIds[i].split(/(?:,|;|\t|\n| )+/);
            if(single_mut[0] && single_mut[0]!== null && single_mut[0]!==undefined) {
              obj['product'] = single_mut[0];
            }
            obj['file'] = true;
            if(single_mut[1] && single_mut[1]!== null && single_mut[1]!==undefined) {
              obj['start_aa_original'] = parseInt(single_mut[1].substring(1, single_mut[1].length - 1));
              obj['sequence_aa_original'] = single_mut[1][0];
              obj['sequence_aa_alternative'] = single_mut[1][single_mut[1].length - 1];
            }
            obj['index'] = that.mutationToInsert.length;
            if(single_mut[0] && single_mut[0]!== null && single_mut[0]!==undefined && single_mut[1] && single_mut[1]!== null && single_mut[1]!==undefined){
             that.checkIfMutationAlreadyExists(obj);
            }
          }
        }
        that.recalculateIndexAfterDeletion();
      }
      reader.readAsText(selectedFile);
    },
    deleteMutationsFile(){
      let array = [];
      this.nameFileMutations = null;
      for(let i = 0; i < this.mutationToInsert.length; i = i + 1) {
        if(this.mutationToInsert[i]['file'] === false){
          array.push(this.mutationToInsert[i]);
        }
      }
      this.mutationToInsert = array;
      this.recalculateIndexAfterDeletion();
    },
    downloadMutationsAsTxt(){
      let text = "";
      for(let i = 0; i < this.mutationToInsert.length; i = i + 1) {
        text += this.mutationToInsert[i]['product'] + '\t' + this.mutationToInsert[i]['sequence_aa_original'] +
            this.mutationToInsert[i]['start_aa_original'] + this.mutationToInsert[i]['sequence_aa_alternative'] + '\n';
      }
      let filename = 'mutationsList.txt';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    createListOfMutation(){
      this.listOfMutation = [];
      let len = this.mutationToInsert.length;
      let i = 0;
      while(i < len){
        let stringMutation;
        stringMutation = this.mutationToInsert[i]['product'] + '_' ;
        if(this.mutationToInsert[i]['sequence_aa_original'] !== null){
          stringMutation += this.mutationToInsert[i]['sequence_aa_original'] ;
        }
        else{
          stringMutation += '*';
        }
        stringMutation += this.mutationToInsert[i]['start_aa_original']
            + this.mutationToInsert[i]['sequence_aa_alternative'];
        this.listOfMutation.push(stringMutation);
        i = i + 1;
      }
    },
    deleteAllAccMutationsInserted(){
      this.mutationToInsert = [];
      this.nameFileMutations = null;
      this.recalculateIndexAfterDeletion();
    },
    checkIfMutationAlreadyExists(mutation){
      let bool = true;
      for(let i = 0; i < this.mutationToInsert.length; i = i + 1) {
        if(this.mutationToInsert[i]['product'] === mutation['product']
            && this.mutationToInsert[i]['start_aa_original'] === mutation['start_aa_original']
            && this.mutationToInsert[i]['sequence_aa_alternative'] === mutation['sequence_aa_alternative']
            && (this.mutationToInsert[i]['sequence_aa_original'] && mutation['sequence_aa_original']
            && this.mutationToInsert[i]['sequence_aa_original'] === mutation['sequence_aa_original']) ){
          bool = false;
          break;
        }
      }
      if(bool){
        this.mutationToInsert.push(mutation);
      }
    },
    changeColorPositionSelector(){
      if(this.selectedPosition > this.maxPositionProtein || this.selectedPosition < this.minPositionProtein){
        let delayInMilliseconds = 50;
        setTimeout(function() {
          let id1 = 'positionSelector';
          let elem1 = document.getElementById(id1);
          elem1.style['color'] = 'red';
        }, delayInMilliseconds);
      }
      else{
        let delayInMilliseconds = 50;
        setTimeout(function() {
          let id1 = 'positionSelector';
          let elem1 = document.getElementById(id1);
          elem1.style['color'] = 'black';
        }, delayInMilliseconds);
      }
    },
    confirmMutations(){
      if(this.type === 'time') {
        this.setQueryTime({field: "mutations", list: []});
        if(this.mutationToInsert.length === 0){
          this.setQueryTime({field: "mutations", list: null});
        }
        else {
          this.setQueryTime({field: "mutations", list: this.mutationToInsert});
        }
      }
      else if(this.type === 'geo') {
        this.setQueryGeo({field: "mutations", list: []});
        if(this.mutationToInsert.length === 0){
          this.setQueryGeo({field: "mutations", list: null});
        }
        else {
          this.setQueryGeo({field: "mutations", list: this.mutationToInsert});
        }
      }
      else if(this.type === 'target') {
        this.setQueryFreeTarget({field: "mutations", list: []});
        if(this.mutationToInsert.length === 0){
          this.setQueryFreeTarget({field: "mutations", list: null});
        }
        else {
          this.setQueryFreeTarget({field: "mutations", list: this.mutationToInsert});
        }
      }
      else if(this.type === 'background') {
        this.setQueryFreeBackground({field: "mutations", list: []});
        if(this.mutationToInsert.length === 0){
          this.setQueryFreeBackground({field: "mutations", list: null});
        }
        else {
          this.setQueryFreeBackground({field: "mutations", list: this.mutationToInsert});
        }
      }
      this.createListOfMutation();
      this.clearAll();
      this.dialogMutations = false;
    },
    exitMutationPanel(){
      this.mutationToInsert = [];
      if(this.type === 'time') {
        this.setQueryTime({field: "mutations", list: null});
      }
      else if(this.type === 'geo') {
        this.setQueryGeo({field: "mutations", list: null});
      }
      else if(this.type === 'target') {
        this.setQueryFreeTarget({field: "mutations", list: null});
      }
      else if(this.type === 'background') {
        this.setQueryFreeBackground({field: "mutations", list: null});
      }
      this.dialogMutations = false;
    },
    addMutation(){
      let obj = {}
      obj['product'] = this.selectedProtein;
      obj['start_aa_original'] = this.selectedPosition;
      obj['sequence_aa_original'] = this.selectedOriginalAminoAcid;
      obj['sequence_aa_alternative'] = this.selectedAlternativeAminoAcid;
      obj['index'] = this.mutationToInsert.length;
      obj['file'] = false;
      this.checkIfMutationAlreadyExists(obj);
      this.clearAll();
    },
    clearAll(){
      this.selectedProtein = null;
      this.selectedPosition = null;
      this.selectedOriginalAminoAcid = null;
      this.selectedAlternativeAminoAcid = null;
    },
    deleteSingleMutation(index){
      let array_copy = JSON.parse(JSON.stringify(this.mutationToInsert));
      array_copy.splice(index, 1);
      this.mutationToInsert = [];
      this.mutationToInsert = array_copy;
      this.recalculateIndexAfterDeletion();
    }
  },
  mounted() {
    if(this.type === 'time' && this.queryTime['mutations']) {
      this.mutationToInsert = this.queryTime['mutations'];
    }
    else {
      this.mutationToInsert = [];
    }
    this.possibleProteins = this.all_protein;
  },
  watch: {
    selectedProtein(){
      if(this.selectedProtein !== null) {
        let url = `/analyze/getProteinPosition`;

        let to_send = {'protein': this.selectedProtein};

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.maxPositionProtein = res['stop'];
              this.changeColorPositionSelector();
            });
      }
    },
    selectedPosition() {
      this.changeColorPositionSelector();
    },
    radio_group_lineage(){
      if(this.radio_group_lineage === 'only_lineage'){
        this.mutationToInsert = [];
        this.clearAll();
      }
    }
  }
}
</script>

<style scoped>

</style>