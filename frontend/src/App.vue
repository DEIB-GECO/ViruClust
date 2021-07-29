<template>
  <v-app>
      <v-toolbar dark color="#1D3557" style="width: 100%;">
        <v-img :src="require('./images/virusurf_logo.png')" contain max-width="39px" max-height="39px"></v-img>
        <v-toolbar-title class="headline" style="font-size: 32px !important; margin-left: 20px">
            <span>Viru</span>
            <span class="font-weight-light">Clust GISAID</span>
        </v-toolbar-title>

        <span style="font-size: 20px; white-space: nowrap; margin-left: 50px">enabled by data from
            <a href="https://www.gisaid.org" target="_blank">
                <img style="vertical-align: middle;" :src="require('./assets/gisaid.png')" alt="gisaid-logo"
                     height="24px"/>
            </a>
        </span>

        <v-spacer></v-spacer>

        <v-toolbar-items style="background-color: transparent" class="hidden-lg-and-down">
          <v-btn icon text href="http://geco.deib.polimi.it/virusurf/" target="_blank"
                style="background-color: transparent; width: 100px">
              <span>ViruSurf</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/virusurf_gisaid/" target="_blank"
                style="background-color: transparent; width: 200px">
              <span>ViruSurf GISAID</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/episurf/" target="_blank"
                 style="background-color: transparent; width: 100px">
              <span>EpiSurf</span>
          </v-btn>
          <v-btn icon text href="http://geco.deib.polimi.it/episurf_gisaid/" target="_blank"
                 style="background-color: transparent; width: 200px">
              <span>EpiSurf GISAID</span>
          </v-btn>
          <v-btn icon text href="https://github.com/DEIB-GECO/ViruClust/wiki" target="_blank"
                 style="background-color: transparent; width: 100px">
              <span>Wiki</span>
          </v-btn>
          <v-btn icon text href="/viruclust/repo_static/about_viruclust_.html" target="_blank"
            style="background-color: transparent; width: 100px">
              <span>ABOUT</span>
          </v-btn>
        </v-toolbar-items>

        <div class="hidden-xl-only">
        <v-menu>
          <template v-slot:activator="{ on, attrs }">
            <v-app-bar-nav-icon
              v-bind="attrs"
              v-on="on"
            >
            </v-app-bar-nav-icon>
          </template>
          <v-list-item style="background-color: white;">
              <v-list-item-content>
                <v-btn icon text href="http://geco.deib.polimi.it/virusurf/" target="_blank"
                      style="background-color: transparent; width: 200px">
                    <span>ViruSurf</span>
                </v-btn>
              </v-list-item-content>
          </v-list-item>
          <v-list-item style="background-color: white; border-top: grey solid 1px">
              <v-list-item-content>
                <v-btn icon text href="http://geco.deib.polimi.it/virusurf_gisaid/" target="_blank"
                      style="background-color: transparent; width: 200px">
                    <span>ViruSurf GISAID</span>
                </v-btn>
              </v-list-item-content>
          </v-list-item>
          <v-list-item style="background-color: white; border-top: grey solid 1px">
              <v-list-item-content>
                <v-btn icon text href="http://geco.deib.polimi.it/episurf/" target="_blank"
                       style="background-color: transparent; width: 200px">
                    <span>EpiSurf</span>
                </v-btn>
              </v-list-item-content>
          </v-list-item>
          <v-list-item style="background-color: white; border-top: grey solid 1px">
              <v-list-item-content>
                <v-btn icon text href="http://geco.deib.polimi.it/episurf_gisaid/" target="_blank"
                       style="background-color: transparent; width: 200px">
                    <span>EpiSurf GISAID</span>
                </v-btn>
              </v-list-item-content>
          </v-list-item>
          <v-list-item style="background-color: white; border-top: grey solid 1px">
              <v-list-item-content>
                <v-btn icon text href="https://github.com/DEIB-GECO/ViruClust/wiki" target="_blank"
                       style="background-color: transparent; width: 200px">
                    <span>Wiki</span>
                </v-btn>
              </v-list-item-content>
          </v-list-item>
          <v-list-item style="background-color: white; border-top: grey solid 1px">
              <v-list-item-content>
                <v-btn icon text href="/viruclust/repo_static/about_viruclust_.html" target="_blank"
                  style="background-color: transparent; width: 200px">
                    <span>ABOUT</span>
                </v-btn>
              </v-list-item-content>
          </v-list-item>
        </v-menu>
        </div>

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
