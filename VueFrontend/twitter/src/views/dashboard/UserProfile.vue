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

      <div class="card" v-for="tweet in tweets" v-bind:key="tweet.id">
        <div class="card-content">
          <div class="media">
            <div class="media-left">
              <figure class="image is-48x48">
                <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image" />
              </figure>
            </div>
            <div class="media-content">
              <p class="title is-4">{{tweet.user.username}}</p>
              <p class="subtitle is-6">{{tweet.user.email}}</p>
            </div>
          </div>

          <div class="content">
            {{tweet.text}}
            <br />
            <time>{{tweet.created_at}}</time>
          </div>
        </div>
        <button class="button is-black" style="font-color: white">
          <router-link :to="{ name: 'TweetDetail', params: { id: tweet.id }}">Details</router-link>
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
  data() {
    return {
      tweets: []
    };
  },
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
    },
    async getUserTweets() {
      await axios
        .get("/api/tweets-by-me/", {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          console.log(response);
          this.tweets = response.data;
        });
    }
  },
  mounted() {
    this.getUserTweets();
  }
};
</script>