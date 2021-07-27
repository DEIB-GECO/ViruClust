<template>
<div>
  <v-container fluid grid-list-xl style="justify-content: center;">
    <v-row justify="center" align="center">
      <v-card width="600px" style="margin-top:50px; padding: 50px" color="#F0E68C">
        <v-card-title class="justify-center"><h1>UPLOAD</h1></v-card-title>
        <v-card-text>
          <v-layout wrap justify-center style="padding: 30px; margin-top: 20px">
            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
              <input id="fileInputCSV" type="file" style="display:none"
                           v-on:change="loadCSV()" accept=".csv"
                           onclick="document.getElementById('fileInputCSV').value = ''"
                    />
              <v-btn
                     onclick="document.getElementById('fileInputCSV').click()"
                     class="white--text"
                     small
                     color="rgb(122, 139, 157)"
                     style="margin-top: 10px"
              >
                  Upload CSV
              </v-btn>
            </v-flex>

            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                <v-text-field
                  :value = this.nameLoadedFileCSV
                  solo
                  readonly
                  hide-details
                ></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center;">
              <input id="fileInputFASTA" type="file" style="display:none"
                           v-on:change="loadFASTA()" accept=".fasta"
                           onclick="document.getElementById('fileInputFASTA').value = ''"
                    />
              <v-btn
                     onclick="document.getElementById('fileInputFASTA').click()"
                     class="white--text"
                     small
                     color="rgb(122, 139, 157)"
                     style="margin-top: 10px"
              >
                  Upload FASTA
              </v-btn>
            </v-flex>

            <v-flex class="no-horizontal-padding xs6 d-flex" style="justify-content: center">
                <v-text-field
                  :value = this.nameLoadedFileFASTA
                  solo
                  readonly
                  hide-details
                ></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row wrap justify-center style="padding: 30px;">
            <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
              <v-btn
                     @click="apply()"
                     class="white--text"
                     color="red"
              >
                  PREPARE YOUR DATA
              </v-btn>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-row>

  </v-container>

  <v-dialog
      persistent
    v-model="missingFiles"
    width="300"
  >
    <v-card>
      <v-card-title class="headline" style="background-color: #FFBA08 ; color: white">
        Missing Files
        <v-spacer></v-spacer>
        <v-btn
            style="background-color: rgb(122, 139, 157)"
            slot="activator"
            icon
            small
          color="white"
          @click="missingFiles = !missingFiles"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="text-xs-center">
        <span>
          <br>
        Need both files!
        </span>
      </v-card-text>

    </v-card>
  </v-dialog>

  <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

</div>
</template>

<script>
import axios from "axios";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "LoadPage",
  data(){
    return{
      missingFiles: false,
      overlay: false,
    }
  },
  computed: {
    ...mapState(['nameLoadedFileFASTA', 'nameLoadedFileCSV', 'fileCSV', 'fileFASTA', 'sessionId']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations(['setLoadPage', 'setMetadataPage', 'setStatisticsPage', 'setFileCSV', 'setFileFASTA',
     'setNameFileCSV', 'setNameFileFASTA', 'setAllMetadata', 'setMutDict', 'setTrueDisableMetadata',
     'setFalseDisableMetadata', 'setSessionId']),
    ...mapActions([]),
    loadCSV(){
      this.setFileCSV(null);
      // this.fileCSV = null;
      let reader = new FileReader();
      let selectedFile = document.getElementById ('fileInputCSV'). files[0];

      this.setNameFileCSV(selectedFile.name);
      // this.nameLoadedFileCSV = selectedFile.name;

      let that = this;
      reader.onload = function() {
        that.setFileCSV(reader.result);
        // that.fileCSV = reader.result;
      }

      reader.readAsText(selectedFile);
    },
    loadFASTA(){
      this.setFileFASTA(null);
      // this.fileFASTA = null;
      let reader = new FileReader();
      let selectedFile = document.getElementById ('fileInputFASTA'). files[0];

      this.setNameFileFASTA(selectedFile.name);
      // this.nameLoadedFileFASTA = selectedFile.name;

      let that = this;
      reader.onload = function() {
        that.setFileFASTA(reader.result);
        // that.fileFASTA = reader.result;
      }
      reader.readAsText(selectedFile);
    },
    apply(){
      if(this.fileCSV === null || this.fileFASTA === null){
        this.missingFiles = true;
      }
      else {
        this.overlay = true;

        let url3 = '/private/upload_csv'
        let to_send3 = {'fileCSV': this.fileCSV}
        axios.post(url3, to_send3)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.setSessionId(res);
              this.uploadFASTA();
            });
      }
    },
    uploadFASTA(){
       let url2 = `/private/upload_fasta?session_id=${this.sessionId}`
        let to_send2 = {'fileFASTA': this.fileFASTA}
        axios.post(url2, to_send2)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.setMutDict(res);
              this.overlay = false;
            });
    },
  },
  watch: {
    overlay(){
      if(!this.overlay){
        this.setMetadataPage();
      }
    }
  },
  mounted() {
  }
}
</script>

<style scoped>


</style>