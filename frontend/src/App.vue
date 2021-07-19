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

      <span style="font-size: 20px; white-space: nowrap; margin-left: 50px">enabled by data from
          <a href="https://www.gisaid.org" target="_blank">
              <img style="vertical-align: middle;" :src="require('./assets/gisaid.png')" alt="gisaid-logo"
                   height="24px"/>
          </a>
      </span>

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
