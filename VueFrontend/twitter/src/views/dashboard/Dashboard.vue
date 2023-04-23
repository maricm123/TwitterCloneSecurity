<template>
  <div class="container">
    <div class="columns is-multiline">
      <div v-if="$store.state.isAuthenticated" class="column is full">
        <button class="button is-gray">
          <router-link to="/dashboard/add-tweet">Add your tweet</router-link>
        </button>
      </div>
      <div class="column is-full">
        <!-- <h1>Hi {{user.username}}</h1> -->
        <h1 class="title">Tweets</h1>
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
    </div>
    <!-- <div class="column">
      <p class="bd-notification is-info">First column</p>
      <div class="columns is-mobile">
        <div class="column">
          <p class="bd-notification is-info">First nested column</p>
        </div>
        <div class="column">
          <p class="bd-notification is-info">Second nested column</p>
        </div>
      </div>
    </div>-->
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Dashboard",
  data() {
    return {
      tweets: []
    };
  },
  mounted() {
    this.getTweets();
  },
  methods: {
    async getTweets() {
      this.$store.commit("setIsLoading", true);

      axios
        .get("/api/tweet/")
        .then(response => {
          console.log(response);
          this.tweets = response.data;
        })
        .catch(error => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    }
  }
};
</script>
<style scoped>
* {
  position: ;
}
</style>