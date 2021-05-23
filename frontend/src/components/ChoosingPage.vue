<template>
  <div>
    <LoadPage id="loadPage"></LoadPage>
    <MetadataPage id="metadataPage" class="notShow"></MetadataPage>
    <StatisticsPage id="statisticsPage" class="notShow"></StatisticsPage>
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
    page() {
      let page = this.page;
      const load = document.getElementById('loadPage');
      const metadata = document.getElementById('metadataPage')
      const statistics = document.getElementById('statisticsPage')
      load.classList.add("notShow");
      metadata.classList.add("notShow");
      statistics.classList.add("notShow");
      const page_now = document.getElementById(page);
      page_now.classList.remove("notShow");
    }
  }
}
</script>

<style scoped>

.notShow{
  display: none;
}

</style>