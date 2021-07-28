<template>
    <div>
      <v-btn @click="dialogModifyColumns = true"
           class="white--text"
           color="#E63946">
      MERGE COLUMNS</v-btn>

      <v-dialog
      persistent
      v-model="dialogModifyColumns"
      width="1000"
      >
        <v-card>
          <v-card-title class="headline" style="background-color: #A8DADC ;">
            MERGE COLUMNS
            <v-spacer></v-spacer>
            <v-btn
                style="background-color: rgb(122, 139, 157)"
                slot="activator"
                icon
                small
              color="white"
              @click="dialogModifyColumns = !dialogModifyColumns"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-card-text class="text-xs-center">
            <span>
              <v-layout row wrap justify-center style="padding: 30px;">
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; margin-top: 10px">
                <v-autocomplete
                  v-model="selectedHeader"
                  :items="possibleHeader"
                  label="Header"
                  solo
                  multiple
                  hide-details
                ></v-autocomplete>
               </v-flex>
                <v-flex class="no-horizontal-padding xs1 d-flex" style="justify-content: center; margin-top: 10px">
                </v-flex>
               <v-flex class="no-horizontal-padding xs4 d-flex" style="justify-content: center; margin-top: 10px">
                 <v-text-field
                  v-model = "newNameColumn"
                  solo
                  label= "Insert new name for column"
                  hide-details
                ></v-text-field>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                <v-btn @click="unionHeader()"
                     class="white--text"
                     small
                     color="#E63946"
                       :disabled="newNameColumn === null || selectedHeader.length === 0"
                      style="margin-top: 20px">
                UNION</v-btn>
               </v-flex>
               <v-flex class="no-horizontal-padding xs12 d-flex"
                       style="justify-content: center; margin-top: 40px; padding: 10px;"
                        v-if="arrayOfUnions.length > 0">
                 <v-layout row wrap justify-center align-center>
                   <v-flex class="no-horizontal-padding xs12 d-flex" style="margin: 20px" v-for="(singleUnion, idx) in arrayOfUnions" v-bind:key="idx">
                    <v-card color="#F1FAEE" style="width: 100%; padding: 10px">
                      <v-card-text>
                        <v-layout row wrap justify-center align-center>
                         <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                             <span style="text-align: center;"><b>NEW NAME COLUMN</b></span>
                         </v-flex>
                          <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                               <span style="text-align: center;"><b>COMBINED COLUMNS</b></span>
                         </v-flex>
                          <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center">
                            <span style="text-align: center;"><b>DELETE</b></span>
                         </v-flex>
                        </v-layout>
                        <v-layout row wrap justify-center align-center>
                         <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                           <span style="text-align: center;">
                              <span style="text-align: center;">{{singleUnion['nameUnion']}}</span>
                           </span>
                         </v-flex>
                          <v-flex class="no-horizontal-padding xs5 d-flex" style="justify-content: center">
                            <span style="text-align: center;">
                               <span style="text-align: center;" v-for="column in singleUnion['columns']" v-bind:key="column[0]">
                                 <span> {{column[0]}} </span><br>
                               </span>
                            </span>
                         </v-flex>
                          <v-flex class="no-horizontal-padding xs2 d-flex" style="justify-content: center">
                            <v-btn
                                style="background-color: rgba(255, 0, 0, 0.5)"
                                slot="activator"
                                icon
                                small
                              color="white"
                                :disabled="allCombinedColumns.includes(singleUnion['valueUnion'])"
                                @click="deleteNewColumn(singleUnion, idx)"
                            >
                              <v-icon>mdi-close</v-icon>
                            </v-btn>
                         </v-flex>
                        </v-layout>
                      </v-card-text>
                    </v-card>
                   </v-flex>
                 </v-layout>
               </v-flex>
              </v-layout>
            </span>
          </v-card-text>

        </v-card>
      </v-dialog>

    </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "ModifyColumnsHeatmap",
  props: {
    headerTable: {required: true,},
    rowTable: {required: true,},
    denominators: {required: true,},
  },
   data() {
      return {
        dialogModifyColumns: false,
        possibleHeader: [],
        selectedHeader: [],
        newNameColumn: null,
        arrayOfUnions: [],
        allCombinedColumns: [],
      }
   },
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    unionHeader(){
      let newName = "";
      if(this.denominators[this.newNameColumn]){
        newName = this.newNameColumn + 'new';
      }
      else{
        newName = this.newNameColumn;
      }

      let selectedColumnWithValue = [];

      for(let j= 0; j < this.rowTable.length; j=j+1){
        let total = 0;
        for(let k=0; k < this.selectedHeader.length; k=k+1){
          if(this.rowTable[j][this.selectedHeader[k]]){
            let that = this;
            let index = this.headerTable.findIndex(function(item){
              return item.text === that.selectedHeader[k];
            });
            if(index !== -1) {
              this.allCombinedColumns.push(this.headerTable[index]['value']);
              let singleSelectedWithValue = [this.selectedHeader[k], this.headerTable[index]['value']];
              selectedColumnWithValue.push(singleSelectedWithValue);
              this.headerTable.splice(index, 1);
            }
            total = total + parseInt(this.rowTable[j][this.selectedHeader[k]]);
            // delete this.rowTable[j][this.selectedHeader[k]];
          }
        }

        this.rowTable[j][newName] = total;
      }

      let total_denominator = 0;
      for(let k=0; k < this.selectedHeader.length; k=k+1){
            total_denominator = total_denominator +  parseInt(this.denominators[this.selectedHeader[k]]);
            // delete this.denominators[this.selectedHeader[k]];
      }
      this.denominators[newName] = total_denominator;

      let index2 = this.headerTable.findIndex(function(item){
        return item.text === 'lineage';
      });
      this.headerTable.splice(index2, 1);

      let index3 = this.headerTable.findIndex(function(item){
        return item.text === 'N/D';
      });
      if(index3 !== -1) {
        this.headerTable.splice(index3, 1);
      }

       let newHeader = {'text': this.newNameColumn, 'value': newName, 'show': true, 'align': 'center', 'width': '20vh'};
       this.headerTable.push(newHeader);
       this.headerTable.sort( function( a, b ) {
          a = a.value.toLowerCase();
          b = b.value.toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
      });

      let ND_header = {'text': 'N/D', 'value': 'N/D', 'show': true, 'align': 'center', 'width': '20vh'};
      let lineage_header = {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '20vh'};

      if(index3 !== -1){
        this.headerTable.unshift(ND_header);
      }
      this.headerTable.unshift(lineage_header);

      let single_union = {'nameUnion': this.newNameColumn, 'valueUnion': newName, 'columns': selectedColumnWithValue};
      this.arrayOfUnions.push(single_union);

      this.selectedHeader = [];
      this.newNameColumn = null;

    },
    calculatePossibleHeaders(){
      let arr_header = [];
      for (let i = 0; i < this.headerTable.length; i = i + 1){
        if(this.headerTable[i]['text'] !== 'lineage'){
          arr_header.push(this.headerTable[i]['text']);
        }
      }
      this.possibleHeader = arr_header;
    },
    deleteNewColumn(singleUnion, idx){
      let value = singleUnion['valueUnion'];
      let columns = singleUnion['columns'];

      for(let j= 0; j < this.rowTable.length; j=j+1){
        delete this.rowTable[j][value];
      }

      let index = this.headerTable.findIndex(function(item){
        return item.value === value;
      });
      if(index !== -1) {
        this.headerTable.splice(index, 1);
      }
      delete this.denominators[value];

      for(let k=0; k < columns.length; k=k+1){
        let newHeader = {'text': columns[k][0], 'value': columns[k][1], 'show': true, 'align': 'center', 'width': '20vh'};
        this.headerTable.push(newHeader);
        let indexCombinedColumns = this.allCombinedColumns.findIndex(function(item){
          return item === columns[k][1];
        });
        if(indexCombinedColumns) {
          this.allCombinedColumns.splice(indexCombinedColumns, 1);
        }
      }

      let index2 = this.headerTable.findIndex(function(item){
        return item.text === 'lineage';
      });
      this.headerTable.splice(index2, 1);

      let index3 = this.headerTable.findIndex(function(item){
        return item.text === 'N/D';
      });
      if(index3 !== -1) {
        this.headerTable.splice(index3, 1);
      }

      this.headerTable.sort( function( a, b ) {
          a = a.value.toLowerCase();
          b = b.value.toLowerCase();
          return a < b ? -1 : a > b ? 1 : 0;
      });

      let ND_header = {'text': 'N/D', 'value': 'N/D', 'show': true, 'align': 'center', 'width': '20vh'};
      let lineage_header = {'text': 'lineage', 'value': 'lineage', 'show': true, 'align': 'center', 'width': '20vh'};

      if(index3 !== -1){
        this.headerTable.unshift(ND_header);
      }
      this.headerTable.unshift(lineage_header);

      this.arrayOfUnions.splice(idx, 1);

      this.selectedHeader = [];
    }
  },
  watch: {
    headerTable(){
      this.calculatePossibleHeaders();
    }
  },
  mounted() {
    this.calculatePossibleHeaders();
  }
}
</script>

<style scoped>

</style>