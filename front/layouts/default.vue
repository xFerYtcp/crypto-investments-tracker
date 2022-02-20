<template>
  <v-app dark>
    <v-navigation-drawer v-model="drawer" clipped fixed app>
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>

      <v-list>
        <v-list-item @click="$vuetify.theme.dark = !$vuetify.theme.dark">
          <v-list-item-action>
            <v-icon>mdi-brightness-6</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Dark mode</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar clipped-left fixed dark app class="purple darken-3">
      <!-- <v-app-bar-nav-icon @click.stop="drawer = !drawer" /> -->
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-btn icon>
        <v-img src="icon_inv.png" class="invertImg" contain max-height="24"></v-img>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <span v-if="$store.state.auth.loggedIn">
        Hi, {{$store.state.auth.user}}
        <v-btn icon @click.stop="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </span>
      <span v-else>
        Signin
        <v-btn icon @click.stop="$router.push('/login')">
          <v-icon>mdi-login</v-icon>
        </v-btn>
      </span>
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data() {
    return {
      drawer: true,
      items: [
        {
          icon: 'mdi-home',
          title: 'Welcome',
          to: '/',
        },
        {
          icon: 'mdi-chart-line',
          title: 'Investments',
          to: '/investments',
        },
                {
          icon: 'mdi-bitcoin',
          title: 'Currencies',
          to: '/currencies',
        },
                {
          icon: 'mdi-bank',
          title: 'Exchanges',
          to: '/exchanges',
        },
      ],
      title: 'InvestmentTracker',
    }
  },
  methods: {
    logout() {
      this.$auth.logout()
      this.$router.push('/login')
    },
    login() {
      this.$router.push('/login')
    },
  },
}
</script>

