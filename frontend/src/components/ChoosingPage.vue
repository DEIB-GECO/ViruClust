<template>
  <div>
    <HomePage id="homePage" v-if="this.page === 'homePage'"></HomePage>
    <EntryPage id="entryPage" v-if="this.page === 'entryPage'"></EntryPage>
    <AnalyzePage id="analyzePage" v-if="this.page === 'analyzePage'"></AnalyzePage>
    <LoadPage id="loadPage" v-if="this.page === 'loadPage'"></LoadPage>
    <MetadataPage id="metadataPage" v-if="this.page === 'metadataPage'"></MetadataPage>
    <StatisticsPage id="statisticsPage" v-if="this.page === 'statisticsPage'"></StatisticsPage>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import LoadPage from "./LoadPage";
import MetadataPage from "./MetadataPage";
import StatisticsPage from "./StatisticsPage";
import EntryPage from "./EntryPage";
import AnalyzePage from "./AnalyzePage";
import HomePage from "./HomePage";

export default {
  name: "ChoosingPage",
  components: {HomePage, AnalyzePage, EntryPage, StatisticsPage, MetadataPage, LoadPage},
  computed: {
    ...mapState(['page']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
  },
  watch: {
  }
}
</script>

<style scoped>

</style>