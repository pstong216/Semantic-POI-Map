import { createStore } from 'vuex';

export default createStore({
  state: {
    geoJsonData: null,
    center_lon: null,
    center_lat: null,
    radius: 300,
    head_class: 'all'
  },
  mutations: {
    setGeoJsonData(state, data) {
      state.geoJsonData = data;
    },
    setCenterLon(state, lon) {
      state.center_lon = lon;
    },
    setCenterLat(state, lat) {
      state.center_lat = lat;
    },
    setRadius(state, radius) {
      state.radius = radius;
    },
    setHeadclass(state, head_class) {
      state.head_class = head_class;
    },
  },
  actions: {
    async fetchGeoJsonData({commit, state }, { center_lon, center_lat, radius, head_class }) {
      // Update the state with the new values
      commit('setCenterLon', center_lon);
      commit('setCenterLat', center_lat);
      commit('setRadius', radius);
      commit('setHeadclass', head_class);

      const requestUrl = `http://localhost:5000/poi/${center_lon}/${center_lat}/${radius}/${head_class}`;
      try {
        const response = await fetch(requestUrl);

        const data = await response.json();
        if (data) {
          // 如果data不为空，那么commit这个mutation
          commit('setGeoJsonData', data);
        } else {
          // 如果data为空，那么执行其他操作，例如打印一条消息
          console.log('Empty response from API.');
        }
      } catch (error) {
        console.error('Failed to fetch GeoJSON data:', error);
      }
    }
  },
  getters: {
    geoJsonData: (state) => state.geoJsonData,
    center_lon: (state) => state.center_lon,
    center_lat: (state) => state.center_lat,
    radius: (state) => state.radius,
    head_class:(state) => state.head_class,
  },
});