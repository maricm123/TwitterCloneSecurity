import { createStore } from "vuex";

export default createStore({
  state: {
    isLoading: false,
    isAuthenticated: false,
    token: ''
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
    }
  },
  actions: {},
  modules: {},
});
