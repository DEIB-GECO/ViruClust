<template>
  <v-container fluid grid-list-xl style="justify-content: center;">
      <v-row justify="center" align="center">
        <v-card width="95%" style="margin-top:50px" color="#F0E68C">
          <v-card-text>
            <v-layout row wrap justify-center style="padding: 30px;">
              <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center"
              v-for="(item, index) in listRes" v-bind:key="item.cluster_name + item.mutation_name[0] + item.mutation_name[1] + item.mutation_name[2] + item.lineage_name">
                <v-card width="80%" color="#DAA520">
                  <v-card-title>
                    <h5>{{item.mutation_name[1]}}{{item.mutation_name[0]}}{{item.mutation_name[2]}}
                    in cluster {{item.cluster_name}} vs lineage {{item.lineage_name}}</h5>
                    <v-spacer></v-spacer>
                    <v-btn class="white--text" color="blue" @click="setSelectedIndex(index)">
                      <span v-if="selectedIndex === index">CLOSE </span>
                      <span v-else> MORE INFO </span>
                    </v-btn>
                  </v-card-title>
                  <v-card-text v-if="selectedIndex === index">
                    <ul>
                      <li>
                        Number of sequences in cluster {{item.cluster_name}} with mutation
                        {{item.mutation_name[1]}}{{item.mutation_name[0]}}{{item.mutation_name[2]}}: {{item.num_cluster}}
                      </li>
                      <li>
                        Percentage of sequences in cluster {{item.cluster_name}} with mutation
                        {{item.mutation_name[1]}}{{item.mutation_name[0]}}{{item.mutation_name[2]}}: {{item.perc_cluster.toPrecision(3) * 100}}%
                      </li>
                      <li>
                        Percentage of sequences in lineage {{item.lineage_name}} with mutation
                        {{item.mutation_name[1]}}{{item.mutation_name[0]}}{{item.mutation_name[2]}}: {{item.perc_lineage.toPrecision(3) * 100}}%
                      </li>
                      <li>
                        Fold change (%cluster / %lineage): {{item.fc.toPrecision(3)}}
                      </li>
                      <li>
                          Spike domain(s):
                        <ul>
                          <li v-for="domain in item.domains" v-bind:key="domain">{{domain}}</li>
                        </ul>
                      </li>
                      <li>
                        Epitope (linear, from IEDB): sequence {{item.epi_seq}} from position {{item.epi_start}} to {{item.epi_stop}}
                        in Spike (combination of {{item.epi_linear}} linear epitopes)
                      </li>
                      <li>
                        Publications linear epitopes:
                        <ul>
                          <li v-for="linear_epi in item.list_linear" v-bind:key="linear_epi">
                            <a :href="linear_epi" target="_blank">{{linear_epi}}</a>
                          </li>
                        </ul>
                      </li>
                      <li>
                        Epitope (non-linear, from IEDB): overlapping {{item.epi_nonlinear}} non-linear epitopes
                      </li>
                      <li>
                        Publications non-linear epitopes:
                        <ul>
                          <li v-for="nonlinear_epi in item.list_nonlinear" v-bind:key="nonlinear_epi">
                            <a :href="nonlinear_epi" target="_blank">{{nonlinear_epi}}</a>
                          </li>
                        </ul>
                      </li>
                      <li>
                        Sequences:
                        <ul>
                          <li v-for="(seq,key) in item.sequences" v-bind:key="key">
                            {{key}}
                            <ul>
                              <li v-for="(meta,key) in seq" v-bind:key="key + meta">
                                {{key}} : {{meta}}
                              </li>
                            </ul>
                          </li>
                        </ul>
                      </li>
                    </ul>
                  </v-card-text>
                </v-card>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-row>
  </v-container>

</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "ListResults",
  data(){
    return{
      selectedIndex: null,
    }
  },
  computed: {
    ...mapState(['listRes', 'listResFixed']),
    ...mapGetters({}),
  },
  methods: {
     ...mapMutations([]),
    ...mapActions([]),
    setSelectedIndex(value){
       if(this.selectedIndex === value){
         this.selectedIndex = null;
       }
       else{
         this.selectedIndex = value;
       }
    }
  },
  watch: {
  }
}
</script>

<style scoped>

</style>