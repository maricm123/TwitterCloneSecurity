<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">User Profile - {{user.email}}</h1>
        <!-- ovde ide v-if ako currentUser prati ovog usera onda ide button za unffollow -->
        <button class="button is-black" style="font-color: white" @click="followUser">Follow user</button>
        <!-- <button class="button is-black" style="font-color: white">Unfollow user</button> -->
      </div>
      <!-- ovde u if dodati jos ako currentUser prati usera kojem smo na profilu onda moze da vidi ovo -->
      <div v-if="user.account_status == 'OPEN'">
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
      tweets: [],
      user: {}
    };
  },
  created() {
    this.getUser();
  },
  methods: {
    async getUserTweets() {
      const userID = this.$route.params.id;
      await axios
        .get(`/api/tweets-by-user/${userID}`, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          this.tweets = response.data;
        });
    },
    async getUser() {
      this.$store.commit("setIsLoading", true);
      const userID = this.$route.params.id;
      axios
        .get(`/api/my-profile/${userID}/`)
        .then(response => {
          this.user = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
    async followUser() {
      this.$store.commit("setIsLoading", true);
      const userID = this.$route.params.id;
    }
  },

  mounted() {
    this.getUserTweets();
  }
};
</script>