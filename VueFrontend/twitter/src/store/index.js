import { createStore } from "vuex";
import axios from 'axios';
export default createStore({
  state: {
    isLoading: false,
    isAuthenticated: false,
    token: '',
    refresh: '',
    currentUser: null,
  },
  getters: {},
  // Mutations are functions in Vuex that modify the state of the store.
  //  In this case, the 'initializeStore' mutation is responsible for updating the state of the store based on the data in local storage.
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    SET_CURRENT_USER(state, currentUser) {
      state.currentUser = currentUser;
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    // storovacemo posebno refresh da se ne salje svakim requestom
    // sa access tokenom
    setRefresh(state, refresh) {
      state.refresh = refresh
    },
    setRole(state, role) {
      state.role = role
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    }
  },
  actions: {
    async getCurrentUser({ commit, state }) {
      // Check if the user is already logged in
      if (state.currentUser) {
        return state.currentUser;
      } else {
        state.currentUser = null;
      }

      // Make the API request to get the current user
      const response = await axios.get("/api/current-user/", {
        headers: { Authorization: `Bearer ${state.token}` }
      });

      // Commit the SET_CURRENT_USER mutation with the response data
      const currentUser = response.data;
      commit("SET_CURRENT_USER", currentUser);

      // Return the current user data
      return currentUser;
    }
  },
  modules: {},
});
