<template>
  <div>
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

export default {
  name: "ChoosingPage",
  components: {StatisticsPage, MetadataPage, LoadPage},
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