<template>
  <v-app>
      <v-toolbar dark color="#DAA520" style="width: 100%">
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

        <v-spacer></v-spacer>

        <v-toolbar-items style="background-color: transparent">
          <v-btn icon text href="http://geco.deib.polimi.it/episurf/" target="_blank"
                 style="background-color: transparent; width: 100px">
              <span>EpiSurf</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/episurf_gisaid/" target="_blank"
                 style="background-color: transparent; width: 200px">
              <span>EpiSurf GISAID</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/virusurf/" target="_blank"
                style="background-color: transparent; width: 100px">
              <span>ViruSurf</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/virusurf_gisaid/" target="_blank"
                style="background-color: transparent; width: 200px">
              <span>ViruSurf GISAID</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/genosurf/" target="_blank"
              style="background-color: transparent; width: 100px">
              <span>GenoSurf</span>
          </v-btn>
          <v-btn icon text href="" target="_blank"
                 style="background-color: transparent; width: 100px">
              <span>Wiki</span>
          </v-btn>
          <v-btn icon text href="" target="_blank"
                style="background-color: transparent; width: 100px">
                  <span>About</span>
              </v-btn>
        </v-toolbar-items>

      </v-toolbar>

    <v-main>
      <ChoosingPage></ChoosingPage>
    </v-main>

    <v-footer app>
        <v-flex
                lighten-2
                xs6
                class="bottom-info"
                style="font-size:12px;">
            <div>Data used in this web application remain subject to GISAID’s <a
                href="http://gisaid.org/DAA/" target="_blank">Terms
              and Conditions</a>.
            </div>
        </v-flex>
    </v-footer>

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
