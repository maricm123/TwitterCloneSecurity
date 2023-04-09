<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Sign up default user</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Username</label>
            <div class="control">
              <input type="text" name="username" class="input" v-model="username" />
            </div>
          </div>
          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="password" name="password" class="input" v-model="password" />
            </div>
          </div>

          <div class="field">
            <label>Repeat password</label>
            <div class="control">
              <input type="password" name="password2" class="input" v-model="password2" />
            </div>
          </div>

          <div class="field">
            <label>Email</label>
            <div class="control">
              <input type="text" name="email" class="input" v-model="email" />
            </div>
          </div>

          <div class="field">
            <label>First name</label>
            <div class="control">
              <input type="text" name="first_name" class="input" v-model="first_name" />
            </div>
          </div>

          <div class="field">
            <label>Last name</label>
            <div class="control">
              <input type="text" name="last_name" class="input" v-model="last_name" />
            </div>
          </div>

          <div class="field">
            <label>Age</label>
            <div class="control">
              <input type="number" name="age" class="input" v-model="age" />
            </div>
          </div>

          <div class="field">
            <label>Address</label>
            <div class="control">
              <input type="text" name="address" class="input" v-model="address" />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
export default {
  name: "DefaultSignUp",
  data() {
    return {
      username: "",
      password: "",
      email: "",
      password2: "",
      age: null,
      address: "",
      first_name: "",
      last_name: "",
      errors: []
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];

      if (this.username === "") {
        this.errors.push("The username is missing");
      }
      if (this.password === "") {
        this.errors.push("The password is too short");
      }
      if (this.password !== this.password2) {
        this.errors.push("The password are not matching");
      }
      if (!this.errors.length) {
        this.$store.commit("setIsLoading", true);
        const formData = {
          email: this.email,
          username: this.username,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
          age: this.age,
          address: this.address
        };
        await axios
          .post("http://127.0.0.1:8000/api/default-user/register/", formData)
          .then(response => {
            toast({
              message: "Account was created, please log in",
              type: "is-success",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
            this.$router.push("/login");
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(
                  `${property}: ${error.response.data[property]}`
                );
              }
            } else if (error.message) {
              this.errors.push("Something went wrong. Please try again!");
            }
          });

        this.$store.commit("setIsLoading", false);
      }
    }
  }
};
</script>