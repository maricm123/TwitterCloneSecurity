<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">User Profile</h1>
      </div>
      <div class="column is full">
        <button class="button is-light">
          <router-link to="/dashboard/add-tweet">Add your tweet</router-link>
        </button>
      </div>

      <div class="column is-12">
        <div class="buttons">
          <!-- <router-link
            :to="{ name: 'EditMember', params: { id: $store.state.user.id }}"
            class="button is-light"
          >Edit</router-link>-->

          <button @click="logout()" class="button is-danger">Log out</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UserProfile",
  methods: {
    async logout() {
      const refresh = localStorage.getItem("refresh");
      await axios
        .post(
          "/api/logout/",
          { refresh },
          {
            headers: { Authorization: `Bearer ${this.$store.state.token}` }
          }
        )
        .then(response => {
          console.log("Logged out");
        })
        .catch(error => {
          console.log(JSON.stringify(error));
        });
      this.$store.commit("removeToken");
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
      localStorage.removeItem("role");

      this.$router.push("/login");
    }
  }
};
</script>