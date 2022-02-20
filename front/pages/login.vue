<template>
  <v-app>
    <v-row>
      <v-alert v-if="loginError" dismissible type="error">{{
        loginError
      }}</v-alert>
      <v-alert v-if="loginSuccess" dismissible type="success">{{
        loginSuccess
      }}</v-alert>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md6>
            <!-- <v-card class="elevation-12"> -->
            <v-card-title><v-icon large class="mx-3">mdi-account-circle</v-icon> SignIn</v-card-title>
            <v-card-text>
              <form ref="form" @submit.prevent="userLogin()">
                <v-text-field
                  v-model="login.username"
                  name="username"
                  label="Username"
                  type="text"
                  placeholder="username"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="login.password"
                  name="password"
                  label="Password"
                  type="password"
                  placeholder="password"
                  required
                ></v-text-field>
                <v-btn type="submit" class="mt-4" color="primary" value="log in"
                  >Login</v-btn
                >
              </form>
            </v-card-text>
            <!-- </v-card> -->
          </v-flex>
        </v-layout>
      </v-container>
    </v-row>
  </v-app>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      login: {
        username: '',
        password: '',
      },
      loginError: null,
      loginSuccess: null,
    }
  },
  methods: {
    async userLogin() {
      // try {
      //   const response = await this.$auth.loginWith('local', {
      //     data: this.login,
      //   })
      //   console.log(response)
      //   this.$router.push('/')
      // } catch (err) {
      //   this.loginError = err
      //   console.log(err)
      // }
      try {
        await this.$auth
          .loginWith('local', {
            data: this.login,
          })
          .catch((e) => {
            this.loginError = e
          })
        if (this.$auth.loggedIn) {
          this.loginSuccess = 'Successfully Logged In'
          this.$router.push('/')
        }
      } catch (e) {
        this.loginError = e
      }
    },
  },
}
</script>
