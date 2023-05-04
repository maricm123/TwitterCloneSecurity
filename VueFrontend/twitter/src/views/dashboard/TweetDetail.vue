<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12"></div>

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
          <button class="button is-submit" @click="userProfile">User profile</button>
        </div>
      </div>

      <hr />

      <!-- Only show update and delete buttons if the tweet belongs to the currently logged in user -->
      <div v-if="tweet.user && currentUser && tweet.user.id === currentUser.id">
        <button class="button is-info" @click="updateTweet">Update</button>
        <button class="button is-danger" @click="deleteTweet">Delete</button>
      </div>

      <div v-if="$store.state.isAuthenticated">
        <button
          class="button"
          :class="{ 'unlike': liked }"
          @click="likeTweet"
        >{{ liked ? 'Unlike' : 'Like' }}</button>
      </div>
      <div v-else>
        You need to
        <a href>login</a> to like this tweet
      </div>
      <!-- <div class="liked-by">Liked by: {{liked_by}}</div> -->
      <div>
        <p>Liked by:</p>
        <ul>
          <li v-for="username in liked_by" v-bind:key="username">{{ username }}</li>
        </ul>
      </div>
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
      currentUser: null,
      liked: false,
      liked_by: []
    };
  },
  async created() {
    this.$store.dispatch("getCurrentUser").then(currentUser => {
      // Do something with the current user data
      this.currentUser = currentUser;
    });
    // ako mi ne treba nista od ove fije osim da se storuje u state onda koristim samo ovo:
    //   mounted() {
    //   this.$store.dispatch("getCurrentUser");
    // }
    this.getTweet();
  },
  mounted() {},
  methods: {
    async likeTweet() {
      if (
        // this.tweet.liked_by.includes(this.$store.state.currentUser.username)
        Object.values(this.tweet.liked_by).includes(
          this.$store.state.currentUser.username
        )
      ) {
        // The current user has liked this tweet
        const tweetID = this.$route.params.id;
        await axios
          .delete(`/api/tweet/${tweetID}/like/`, {
            headers: { Authorization: `Bearer ${this.$store.state.token}` }
          })
          .then(response => {
            this.liked = false;
          })
          .catch(error => {
            console.log(error);
          });
      } else {
        const tweetID = this.$route.params.id;
        await axios
          .put(
            `/api/tweet/${tweetID}/like/`,
            {},
            {
              headers: { Authorization: `Bearer ${this.$store.state.token}` }
            }
          )
          .then(response => {
            this.liked = true;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
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
      await axios
        .get(`/api/tweet/${tweetID}/`)
        .then(response => {
          this.tweet = response.data;
          this.tweet.user = response.data.user;
          this.liked_by = response.data.liked_by;
          if (
            Object.values(response.data.liked_by).includes(
              this.$store.state.currentUser.username
            )
          ) {
            // The current user has liked this tweet
            this.liked = true;
          } else {
            this.liked = false;
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    // ova funkcionalnost i delete verovatno ne treba.
    async updateTweet() {
      // Navigate to the tweet update page
      this.$router.push(`/dashboard/tweets/${this.tweet.id}/update/`);
    },
    async userProfile() {
      // Navigate to the user profile page
      this.$router.push(`/dashboard/user-profile/${this.tweet.user.id}`);
    }
  }
};
</script>
<style lang="css" scoped>
.button {
  background-color: rgb(0, 0, 0);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.unlike {
  background-color: #ffcc00;
  color: rgb(187, 35, 35);
}

.liked-by {
  margin: auto;
}
</style>