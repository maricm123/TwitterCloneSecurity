<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <!-- <h1 class="title">{{ client.name }}</h1> -->

        <!-- <div class="buttons">
          <router-link
            :to="{ name: 'EditClient', params: { id: client.id }}"
            class="button is-light"
          >Edit</router-link>
          <button class="button is-danger" @click="deleteClient">Delete</button>
        </div>-->
      </div>

      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">TweetDetail</h2>

          <p>
            <strong>Created at:</strong>
            {{ tweet.created_at }}
          </p>
          <br />
          <br />
          <text>
            <strong>Content:</strong>
            {{ tweet.text }}
          </text>
        </div>
      </div>

      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">Tweeted by</h2>

          <p>
            <strong>Username:</strong>
            {{ tweet.user.username }}
          </p>
          <p>
            <strong>Email:</strong>
            {{ tweet.user.email }}
          </p>
          <br />
          <button class="button is-submit">User profile</button>
        </div>
      </div>

      <hr />

      <!-- Only show update and delete buttons if the tweet belongs to the currently logged in user -->
      <div v-if="tweet.user && currentUser && tweet.user.id === currentUser.id">
        <button class="button is-info" @click="updateTweet">Update</button>
        <button class="button is-danger" @click="deleteTweet">Delete</button>
      </div>

      <!-- <div class="column is-12">
        <h2 class="subtitle">Notes</h2>

        <router-link
          :to="{ name: 'AddNote', params: { id: client.id }}"
          class="button is-success mb-6"
        >Add note</router-link>

        <div class="box" v-for="note in notes" v-bind:key="note.id">
          <h3 class="is-size-4">{{ note.name }}</h3>

          <p>{{ note.body }}</p>

          <router-link
            :to="{ name: 'EditNote', params: { id: client.id, note_id: note.id }}"
            class="button is-success mt-6"
          >Edit note</router-link>
        </div>
      </div>-->
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "TweetDetail",
  data() {
    return {
      tweet: {
        user: {}
      },
      currentUser: null
    };
  },
  created() {
    this.getCurrentUser();
  },
  mounted() {
    this.getTweet();
  },
  methods: {
    async deleteTweet() {
      this.$store.commit("setIsLoading", true);
      const tweetID = this.$route.params.id;
      await axios
        .delete(`/api/tweet/${tweetID}/`, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          console.log(response.data);
          this.$router.push("/dashboard");
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
    async getTweet() {
      this.$store.commit("setIsLoading", true);
      const tweetID = this.$route.params.id;
      console.log(tweetID);
      await axios
        .get(`/api/tweet/${tweetID}/`)
        .then(response => {
          this.tweet = response.data;
          this.tweet.user = response.data.user;
        })
        .catch(error => {
          console.log(error);
        });
    },
    async getCurrentUser() {
      axios
        .get("/api/current-user/", {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          this.currentUser = response.data;
        });
    },
    async updateTweet() {
      // Navigate to the tweet update page
      this.$router.push(`/dashboard/tweets/${this.tweet.id}/update/`);
    }
  }
};
</script>