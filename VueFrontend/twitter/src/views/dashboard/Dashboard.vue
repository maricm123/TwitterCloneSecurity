<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <!-- <h1>Hi {{user.username}}</h1> -->
        <h1 class="title">Tweets</h1>
      </div>

      <!-- <div class="column is-12">
        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Company</th>
              <th>Contact person</th>
              <th>Assigned to</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="tweet in tweets" v-bind:key="tweet.id">
              <td>{{ tweet }}</td>
              <td>{{ lead.contact_person }}</td>
              <td>
                <template
                  v-if="lead.assigned_to"
                >{{ lead.assigned_to.first_name }} {{ lead.assigned_to.last_name }}</template>
              </td>
              <td>{{ lead.status }}</td>
              <td>
                <router-link :to="{ name: 'Lead', params: { id: lead.id }}">Details</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>-->
      <div class="card">
        <div class="card-image">
          <figure class="image is-4by3">
            <img src="https://bulma.io/images/placeholders/1280x960.png" alt="Placeholder image" />
          </figure>
        </div>
        <div class="card-content">
          <div class="media">
            <div class="media-left">
              <figure class="image is-48x48">
                <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image" />
              </figure>
            </div>
            <div class="media-content">
              <p class="title is-4">John Smith</p>
              <p class="subtitle is-6">@johnsmith</p>
            </div>
          </div>

          <div class="content">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Phasellus nec iaculis mauris.
            <a>@bulmaio</a>.
            <a href="#">#css</a>
            <a href="#">#responsive</a>
            <br />
            <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
          </div>
        </div>
      </div>
    </div>
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