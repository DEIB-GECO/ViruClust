<template>
  <v-app>
    <v-app-bar
      app
      color="#DAA520"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          class="shrink mt-1 hidden-sm-and-down"
          max-height="50"
          src="./images/work_in_progress.png"
          width="100"
          style="margin-left: 30px"
        />
      </div>
      <v-toolbar-title class="headline" style="font-size: 32px !important; margin-left: 20px">
          <span>Viru</span>
          <span class="font-weight-light">Clust</span>
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <ChoosingPage></ChoosingPage>
    </v-main>
  </v-app>
</template>

<script>
import ChoosingPage from "./components/ChoosingPage";

export default {
  name: 'App',

  components: {
    ChoosingPage,
  },

  data: () => ({
    //
  }),
};
</script>
