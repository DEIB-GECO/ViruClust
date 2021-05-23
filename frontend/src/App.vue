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
          contain
          max-height="50"
          src="https://freepikpsd.com/wp-content/uploads/2019/10/lavori-in-corso-png-3.png"
          width="100"
        />
      </div>

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
