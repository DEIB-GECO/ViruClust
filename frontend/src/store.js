import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
    page: 'loadPage',
    nameLoadedFileCSV: '',
    fileCSV: null,
    nameLoadedFileFASTA: '',
    fileFASTA: null,
    allMetadata: null,
    mutDict: [],
    allResultTable: [],
    allResultTableFixed: [],
    proteinSelected: 'Spike (surface glycoprotein)',
    listRes: [],
    listResFixed: [],
    allResultTableHeaders: [],
    xAxisBarSeqChart: [],
    yAxisBarSeqChart: [],
    selectedFilters: {},
    statisticsInput: {},
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
    setMutDict: (state, value) => {
        state.mutDict = value;
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
    setProteinSelected: (state, value) => {
        state.proteinSelected = value;
    },
    setListRes: (state, value) => {
        state.listRes = value;
    },
    setListResFixed: (state, value) => {
        state.listResFixed = value;
    },
    setStatisticsInput: (state, value) => {
        state.statisticsInput = value;
    },
    setAllResultTableHeaders: (state, value) => {
        state.allResultTableHeaders = value;
    },
    setXAxisBarSeqChart: (state, value) => {
        state.xAxisBarSeqChart = value;
    },
    setYAxisBarSeqChart: (state, value) => {
        state.yAxisBarSeqChart = value;
    },
    setSelectedFilterField: (state, payload) => {
        state.selectedFilters[payload.field] = payload.fieldQuery;
    },
    resetSelectedFilterField: (state, field) => {
        delete state.selectedFilters[field];
    },
    reloadSelectedFilter: (state) => {
        state.selectedFilters = Object.assign({}, state.selectedFilters);
    },
};

const actions = {
    setSelectedFilter({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.selectedFilters[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setSelectedFilterField', newPayload);
            } else {
                commit('resetSelectedFilterField', field);
            }
            commit('reloadSelectedFilter');
        }
    },

};

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})
