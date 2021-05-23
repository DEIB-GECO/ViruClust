import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
    page: null,
    nameLoadedFileCSV: '',
    fileCSV: null,
    nameLoadedFileFASTA: '',
    fileFASTA: null,
    allMetadata: null,
    allResultTable: [],
    allResultTableFixed: [],
    allResultTableHeaders: [],
    htmlAttached: null,
    xAxisBarSeqChart: [],
    yAxisBarSeqChart: [],
};

const getters = {

};

const mutations = {
    setLoadPage: (state) => {
        state.page = "loadPage";
    },
    setMetadataPage: (state) => {
        state.page = "metadataPage";
    },
    setStatisticsPage: (state) => {
        state.page = "statisticsPage";
    },
    setFileCSV: (state, value) => {
        state.fileCSV = value;
    },
    setNameFileCSV: (state, value) => {
        state.nameLoadedFileCSV = value;
    },
    setFileFASTA: (state, value) => {
        state.fileFASTA = value;
    },
    setNameFileFASTA: (state, value) => {
        state.nameLoadedFileFASTA = value;
    },
    setAllMetadata: (state, value) => {
        state.allMetadata = value;
    },
    setAllResultTable: (state, value) => {
        state.allResultTable = value;
    },
    setAllResultTableFixed: (state, value) => {
        state.allResultTableFixed = value;
    },
    setAllResultTableHeaders: (state, value) => {
        state.allResultTableHeaders = value;
    },
    setHtmlAttached: (state, value) => {
        state.htmlAttached = value;
    },
    setXAxisBarSeqChart: (state, value) => {
        state.xAxisBarSeqChart = value;
    },
    setYAxisBarSeqChart: (state, value) => {
        state.yAxisBarSeqChart = value;
    },
};

const actions = {

};

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})
