<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <template #activator="{ on, attrs }">
        <v-fab-transition>
          <v-btn
            color="pink"
            dark
            bottom
            right
            fab
            class="v-btn-new"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-fab-transition>
      </template>

      <v-card>
        <v-toolbar dark color="purple darken-3">
          <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>New currency</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="postItem"> Save </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-container>
          <v-row>
            <v-col v-if="errors.length > 0" cols="12">
              <v-alert
                type="error"
                v-for="(e, i) in errors"
                :key="i"
                dismissible
              >
                <strong>{{ e[0] }}</strong
                ><br />
                {{ e[1][0] }}
              </v-alert>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="currency.code"
                type="text"
                label="Code*"
                filled
                persistent-hint
                required
                @input="
                  (v) => {
                    currency.code = v.toUpperCase()
                  }
                "
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="currency.name"
                type="text"
                label="Name*"
                filled
                persistent-hint
                required
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <!-- <pre><code>{{currency}}</code></pre> -->
      </v-card>
    </v-dialog>
  </v-row>
</template>


<script>
export default {
  name: 'InvestmentForm',
  data: () => ({
    currency: {
      code: null,
      name: null,
    },
    dialog: false,
    errors: [],
  }),

  mounted() {},
  methods: {
    postItem() {
      this.errors = []
      this.$axios
        .$post('/currency/', this.currency)
        .then(() => {
          this.dialog = false
          this.$parent.getCoins()
        })
        .catch((err) => {
          if (err.response) {
            const e = err.response.data
            const keys = Object.keys(e)
            for (let i = 0; i < keys.length; i++) {
              this.errors.push([keys[i], e[keys[i]]])
            }
          }
        })
    },
  },
}
</script>

<style scoped>
.v-btn-new {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
</style>
