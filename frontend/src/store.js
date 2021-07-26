import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
    page: 'homePage',
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
    numLevelAboveBackground: 1,

    errorNumSeqQueryTime: false,
    errorNumSeqQueryGeo: false,

    queryFreeTarget: {},
    queryFreeBackground: {},
    startDateQueryFreeTarget: null,
    stopDateQueryFreeTarget: null,
    startDateQueryFreeBackground: null,
    stopDateQueryFreeBackground: null,
    numSequencesQueryFreeTarget: 0,
    numSequencesQueryFreeBackground: 0,

    startDateDistributionLineageInGeo: null,
    stopDateDistributionLineageInGeo: null,

    toExcludeTime: {},
    toExcludeGeo: {},
    toExcludeFreeTarget: {},
    toExcludeFreeBackground: {},

    locationToExcludeMulti: [],

    timeDivisionAcceptable: [],

    colorPValueChart: ['rgba(50, 255, 50, 0.5)', 'rgba(255, 0, 0, 0.5)',
                       'rgba(0, 0, 255, 0.5)', 'rgba(230, 15, 250, 0.5)', 'rgba(9,192,217, 0.5)'],
    colorPValueInfoBox: ['rgba(50, 255, 50, 1)', 'rgba(255, 0, 0, 1)',
                         'rgba(0, 0, 255, 1)', 'rgba(230, 15, 250, 1)', 'rgba(9,192,217, 1)'],

    startValuePValueBarChartTime: 0,
    endValuePValueBarChartTime: 0,
    startValuePValueBarChartGeo: 0,
    endValuePValueBarChartGeo: 0,
    startValuePValueBarChartFree: 0,
    endValuePValueBarChartFree: 0,

    selectedTabAnalyzeFromHome: 1,

    color_1: [],
    color_2: [],
    color_3: [],
};

const getters = {

};

const mutations = {
    setSessionId: (state, value) => {
        state.sessionId = value;
    },
    setHomePage: (state) => {
        state.page = "homePage";
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
    setTrueErrorNumSeqQueryTime: (state) => {
        state.errorNumSeqQueryTime = true;
    },
    setFalseErrorNumSeqQueryTime: (state) => {
        state.errorNumSeqQueryTime = false;
    },
    setTrueErrorNumSeqQueryGeo: (state) => {
        state.errorNumSeqQueryGeo = true;
    },
    setFalseErrorNumSeqQueryGeo: (state) => {
        state.errorNumSeqQueryGeo = false;
    },
    setNumLevelAboveBackground: (state, value) => {
        state.numLevelAboveBackground = value;
    },
    setStartDateQueryFreeTarget: (state, value) => {
        state.startDateQueryFreeTarget = value;
    },
    setStopDateQueryFreeTarget: (state, value) => {
        state.stopDateQueryFreeTarget= value;
    },
    setStartDateQueryFreeBackground: (state, value) => {
        state.startDateQueryFreeBackground = value;
    },
    setStopDateQueryFreeBackground: (state, value) => {
        state.stopDateQueryFreeBackground = value;
    },
    setQueryFreeTargetField: (state, payload) => {
        state.queryFreeTarget[payload.field] = payload.fieldQuery;
    },
    resetQueryFreeTargetField: (state, field) => {
        delete state.queryFreeTarget[field];
    },
    reloadQueryFreeTarget: (state) => {
        state.queryFreeTarget = Object.assign({}, state.queryFreeTarget);
    },
    setQueryFreeBackgroundField: (state, payload) => {
        state.queryFreeBackground[payload.field] = payload.fieldQuery;
    },
    resetQueryFreeBackgroundField: (state, field) => {
        delete state.queryFreeBackground[field];
    },
    reloadQueryFreeBackground: (state) => {
        state.queryFreeBackground = Object.assign({}, state.queryFreeBackground);
    },
    setNumSequencesQueryFreeTarget: (state, value) => {
        state.numSequencesQueryFreeTarget = value;
    },
    setNumSequencesQueryFreeBackground: (state, value) => {
        state.numSequencesQueryFreeBackground = value;
    },
    setStartDateDistributionLineageInGeo: (state, value) => {
        state.startDateDistributionLineageInGeo = value;
    },
    setStopDateDistributionLineageInGeo: (state, value) => {
        state.stopDateDistributionLineageInGeo= value;
    },
     setLocationToExcludeMulti: (state, value) => {
        state.locationToExcludeMulti= value;
    },

    setToExcludeTimeField: (state, payload) => {
        state.toExcludeTime[payload.field] = payload.fieldQuery;
    },
    resetToExcludeTimeField: (state, field) => {
        delete state.toExcludeTime[field];
    },
    reloadToExcludeTime: (state) => {
        state.toExcludeTime = Object.assign({}, state.toExcludeTime);
    },

    setToExcludeGeoField: (state, payload) => {
        state.toExcludeGeo[payload.field] = payload.fieldQuery;
    },
    resetToExcludeGeoField: (state, field) => {
        delete state.toExcludeGeo[field];
    },
    reloadToExcludeGeo: (state) => {
        state.toExcludeGeo = Object.assign({}, state.toExcludeGeo);
    },

    setToExcludeFreeTargetField: (state, payload) => {
        state.toExcludeFreeTarget[payload.field] = payload.fieldQuery;
    },
    resetToExcludeFreeTargetField: (state, field) => {
        delete state.toExcludeFreeTarget[field];
    },
    reloadToExcludeFreeTarget: (state) => {
        state.toExcludeFreeTarget = Object.assign({}, state.toExcludeFreeTarget);
    },

    setToExcludeFreeBackgroundField: (state, payload) => {
        state.toExcludeFreeBackground[payload.field] = payload.fieldQuery;
    },
    resetToExcludeFreeBackgroundField: (state, field) => {
        delete state.toExcludeFreeBackground[field];
    },
    reloadToExcludeFreeBackground: (state) => {
        state.toExcludeFreeBackground = Object.assign({}, state.toExcludeFreeBackground);
    },

    setTimeDivisionAcceptable: (state, value) => {
        state.timeDivisionAcceptable = value;
    },

    setStartValuePValueBarChartTime: (state, value) => {
        state.startValuePValueBarChartTime = value;
    },
    setEndValuePValueBarChartTime: (state, value) => {
        state.endValuePValueBarChartTime = value;
    },
    setStartValuePValueBarChartGeo: (state, value) => {
        state.startValuePValueBarChartGeo = value;
    },
    setEndValuePValueBarChartGeo: (state, value) => {
        state.endValuePValueBarChartGeo = value;
    },
    setStartValuePValueBarChartFree: (state, value) => {
        state.startValuePValueBarChartFree = value;
    },
    setEndValuePValueBarChartFree: (state, value) => {
        state.endValuePValueBarChartFree = value;
    },

    setSelectedTabAnalyzeFromHome: (state, value) => {
        state.selectedTabAnalyzeFromHome = value;
    },

    setColor1: (state, value) => {
        state.color_1 = value;
    },
    setColor2: (state, value) => {
        state.color_2 = value;
    },
    setColor3: (state, value) => {
        state.color_3 = value;
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

    setQueryFreeTarget({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.queryFreeTarget[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setQueryFreeTargetField', newPayload);
            } else {
                commit('resetQueryFreeTargetField', field);
            }
            commit('reloadQueryFreeTarget');
        }
    },

    setQueryFreeBackground({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.queryFreeBackground[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setQueryFreeBackgroundField', newPayload);
            } else {
                commit('resetQueryFreeBackgroundField', field);
            }
            commit('reloadQueryFreeBackground');
        }
    },

    setToExcludeTime({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.toExcludeTime[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setToExcludeTimeField', newPayload);
            } else {
                commit('resetToExcludeTimeField', field);
            }
            commit('reloadToExcludeTime');
        }
    },

    setToExcludeGeo({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.toExcludeGeo[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setToExcludeGeoField', newPayload);
            } else {
                commit('resetToExcludeGeoField', field);
            }
            commit('reloadToExcludeGeo');
        }
    },

    setToExcludeFreeTarget({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.toExcludeFreeTarget[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setToExcludeFreeTargetField', newPayload);
            } else {
                commit('resetToExcludeFreeTargetField', field);
            }
            commit('reloadToExcludeFreeTarget');
        }
    },

    setToExcludeFreeBackground({commit, state}, payload) {
        const field = payload.field;

        let newList = payload.list;
        if (!newList)
            newList = [];

        let previousList = state.toExcludeFreeBackground[field];
        if (!previousList)
            previousList = [];

        if (!(JSON.stringify(previousList) === JSON.stringify(newList))) { //  || newList.length === 0
            if (newList.length > 0) {
                const newPayload = {field: field, fieldQuery: newList};
                commit('setToExcludeFreeBackgroundField', newPayload);
            } else {
                commit('resetToExcludeFreeBackgroundField', field);
            }
            commit('reloadToExcludeFreeBackground');
        }
    },

};

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})
