import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
    page: 'entryPage',
    sessionId: '',
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
    disableMetadata: false,
    all_geo: [],
    all_lineages: [],
    all_protein: [],
    timeRangesTargetAndBackground: {},

    queryTime: {},
    queryGeo: {},
    startDateQueryGeo: null,
    stopDateQueryGeo: null,
};

const getters = {

};

const mutations = {
    setSessionId: (state, value) => {
        state.sessionId = value;
    },
    setLoadPage: (state) => {
        state.page = "loadPage";
    },
    setMetadataPage: (state) => {
        state.page = "metadataPage";
    },
    setStatisticsPage: (state) => {
        state.page = "statisticsPage";
    },
    setAnalyzePage: (state) => {
        state.page = "analyzePage";
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
    setTrueDisableMetadata: (state) => {
        state.disableMetadata = true;
    },
    setFalseDisableMetadata: (state) => {
        state.disableMetadata = false;
    },
    setAllGeo: (state, value) => {
        state.all_geo = value;
    },
    setAllLineages: (state, value) => {
        state.all_lineages = value;
    },
    setAllProtein: (state, value) => {
        state.all_protein = value;
    },
    setTimeRangesTargetAndBackground: (state, value) => {
        state.timeRangesTargetAndBackground = value;
    },
     setQueryTimeField: (state, payload) => {
        state.queryTime[payload.field] = payload.fieldQuery;
    },
    resetQueryTimeField: (state, field) => {
        delete state.queryTime[field];
    },
    reloadQueryTime: (state) => {
        state.queryTime = Object.assign({}, state.queryTime);
    },
    setQueryGeoField: (state, payload) => {
        state.queryGeo[payload.field] = payload.fieldQuery;
    },
    resetQueryGeoField: (state, field) => {
        delete state.queryGeo[field];
    },
    reloadQueryGeo: (state) => {
        state.queryGeo = Object.assign({}, state.queryGeo);
    },
    setStartDateQueryGeo: (state, value) => {
        state.startDateQueryGeo = value;
    },
    setStopDateQueryGeo: (state, value) => {
        state.stopDateQueryGeo = value;
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

    setQueryTime({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.queryTime[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setQueryTimeField', newPayload);
            } else {
                commit('resetQueryTimeField', field);
            }
            commit('reloadQueryTime');
        }
    },

    setQueryGeo({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.queryGeo[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setQueryGeoField', newPayload);
            } else {
                commit('resetQueryGeoField', field);
            }
            commit('reloadQueryGeo');
        }
    },

};

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})
