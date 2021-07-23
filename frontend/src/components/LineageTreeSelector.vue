<template>
  <div v-click-outside="onClickOutside">
      <div>
        <v-text-field
              v-model="search"
              :label="labelLineage"
              solo
              hide-details
              @click="clickOnTextField"
              :loading="isLoading || isLoadingLineage"
              :disabled="isLoading || isLoadingLineage"
              style="position: relative; width: 350px; padding: 0"
            >
          <template v-slot:label>
            <div v-if="labelLineage.toLowerCase() === 'lineage'" :id="'label1' + type" style="color: grey">{{labelLineage}}</div>
            <div v-else :id="'label2' + type" style="color: black">{{labelLineage}}</div>
          </template>
          <template v-slot:append>
            <v-icon v-if="showLineages && search !== null" @click="clearSearch()" dark color= rgb(105,105,105)>
              mdi-close
            </v-icon>
            <v-icon v-else-if="!showLineages && selectedLineage !== null" @click="clearSelectedLineage" dark color= rgb(105,105,105)>
              mdi-close
            </v-icon>
            <v-icon v-if="!showLineages" @click="clickOnTextField" dark style="background: radial-gradient(rgb(105,105,105), rgb(105,105,105), white, white, white);">
              mdi-arrow-down-drop-circle
            </v-icon>
            <v-icon v-else @click="onClickOutside"  dark style="background: radial-gradient(rgb(105,105,105), rgb(105,105,105), white, white, white);">
              mdi-arrow-up-drop-circle
            </v-icon>
          </template>
        </v-text-field>
      </div>
      <v-card
          :id = "'dropDownLineages' + type"
        class="mx-auto scroll"
        max-height="400px"
        min-width="350px"
        style="position: absolute; margin-top: 1px; z-index: 1; border-radius: 0; box-shadow: 2px 2px 4px darkgrey;"
      >
        <v-card-text>
          <v-treeview
            ref="tree"
            :items="items"
            :search="search"
            :filter="filter"
            :active.sync="activeLineage"
            activatable
            :open.sync="open"
            dense
          > <!-- open-all -->
            <template slot="label" slot-scope="{ item }">
              <div style="width: 100%; height: 100%;">
                <span class="item-value-span">{{item.name}}</span>
                <span class="item-count-span">{{item['count']}}</span>
              </div>
            </template>
          </v-treeview>
        </v-card-text>
      </v-card>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";

export default {
  name: "LineageTreeSelector",
  props: {
    isLoading: {required: true,},
    possibleValues: {required: true,},
    type: {required: true,},
  },
  data() {
    return {
      showLineages: false,
      selectedLineage: null,
      labelLineage: 'lineage',
      caseSensitive: false,

      isLoadingLineage: false,

      deactivate: false,
      activeLineage: [],
      items: [],

      open: [],
      allOpened: false,
      lastOpen: [],

      search: null,
    }
  },
  computed: {
    ...mapState([]),
    ...mapGetters({}),
    filter () {
      return this.caseSensitive
        ? (item, search, textKey) => item[textKey].indexOf(search) > -1
        : undefined
    },
  },
  methods: {
    ...mapMutations([]),
    ...mapActions(['setQueryTime', 'setQueryGeo', 'setQueryFreeTarget', 'setQueryFreeBackground']),
    saveItem(item){
      if(item.count === 0){
        this.activeLineage = [];
        this.deactivate = true;
      }
      else {
        this.deactivate = false;
        this.showLineages = false;
        if (document.getElementById('dropDownLineages' + this.type)) {
          document.getElementById('dropDownLineages' + this.type).style.display = 'none';
        }
        this.search = null;
        this.labelLineage = item.name;
        this.selectedLineage = item.name.split(" ")[0];
        this.open = [];
      }
    },
    computeLineageTree(){
      if(this.possibleValues && this.possibleValues.length > 0){
        this.isLoadingLineage = true;
        let url = `/analyze/getLineageTree`;
        let to_send = {'possibleLineages': this.possibleValues}
        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.isLoadingLineage = false;
              this.items = res;
            });
      }
    },
    clickOnTextField(){
      this.showLineages = true;
      if(document.getElementById('dropDownLineages' + this.type)) {
        document.getElementById('dropDownLineages' + this.type).style.display = 'block';
      }
    },
    onClickOutside(){
      this.showLineages = false;
      this.search = null;
      this.open = [];
      if(document.getElementById('dropDownLineages' + this.type)) {
        document.getElementById('dropDownLineages' + this.type).style.display = 'none';
      }
    },
    clearSearch(){
      this.search = null;
    },
    clearSelectedLineage(){
      this.isLoadingLineage = true;
      this.search = null;
      this.activeLineage = [];
      this.labelLineage = 'lineage';
      this.selectedLineage = null;

      let delayInMilliseconds = 0;
      let that = this;
      setTimeout(function() {
        that.onClickOutside();
        that.isLoadingLineage = false;
      }, delayInMilliseconds);
    },
    chechChildrenForId(active, children){
        for(let i = 0; i < children.length; i = i + 1){
            if(children[i]['id'] === active){
              this.saveItem(children[i]);
            }
            else{
              if(children[i]['children'].length > 0){
                this.chechChildrenForId(active, children[i]['children']);
              }
            }
          }
    },
  },
  watch: {
    possibleValues(){
      this.computeLineageTree();
    },
    search(){
      if (this.search) {
        if (!this.allOpened) {
          this.lastOpen = this.open;
          this.allOpened = true;
          this.$refs.tree.updateAll(true);
        }
      } else {
        this.$refs.tree.updateAll(false);
        this.allOpened = false;
        this.open = this.lastOpen;
      }
    },
    selectedLineage(){
      if(this.type === 'time') {
        this.setQueryTime({field: 'lineage', list: this.selectedLineage});
      }
      else if(this.type === 'geo') {
        this.setQueryGeo({field: 'lineage', list: this.selectedLineage});
      }
      else if(this.type === 'target') {
        this.setQueryFreeTarget({field: 'lineage', list: this.selectedLineage});
      }
      else if(this.type === 'background') {
        this.setQueryFreeBackground({field: 'lineage', list: this.selectedLineage});
      }
    },
    activeLineage: {
        handler(newVal, oldVal) {
          if(newVal.length === 0 && this.selectedLineage !== null && !this.deactivate){
            this.activeLineage[0] = oldVal[0];
          }
          else {
            for (let k = 0; k < this.activeLineage.length; k = k + 1) {
              for (let i = 0; i < this.items.length; i = i + 1) {
                if (this.items[i]['id'] === this.activeLineage[k]) {
                  this.saveItem(this.items[i]);
                } else {
                  if (this.items[i]['children'].length > 0) {
                    this.chechChildrenForId(this.activeLineage[k], this.items[i]['children']);
                  }
                }
              }
            }
          }
        },
        deep: true
    },
  },
  mounted() {
    this.computeLineageTree();
    document.getElementById('dropDownLineages' + this.type).style.display = 'none';
  }
}

</script>

<style scoped>

  .scroll {
     overflow-y: scroll
  }

  .item-value-span {
      padding-right: 3.5em;
  }

  .item-count-span {
      /*float:right;*/
      position: absolute;
      right: 0.5em;
  }

</style>