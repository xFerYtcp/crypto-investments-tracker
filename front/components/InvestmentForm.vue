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
            class="v-btn-investment"
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
          <v-toolbar-title
            >New investment action {{ currency }}</v-toolbar-title
          >
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="postItem"> Save </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-container>
          <v-row>
            <v-col v-if="errors.length > 0" cols="12">
              <v-alert
                v-for="(e, i) in errors"
                :key="i"
                type="error"
                dismissible
              >
                <strong>{{ e[0] }}</strong
                ><br />
                {{ e[1][0] }}
              </v-alert>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="investment.date"
                type="datetime-local"
                label="Date*"
                hint="Trade date and time"
                filled
                persistent-hint
                required
                :max="now"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="investment.exchange_id"
                :items="exchanges"
                item-text="name"
                item-value="id"
                label="Exchange"
                hint="Which exchange"
                filled
                persistent-hint
                required
                single-line
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <!-- <v-btn-toggle
                v-model="investment.order_type"
                elevation="2"
                dark
                required
                label="Currency"
                hint="Which currency"
              >
                <v-btn value="buy" block color="green">Buy</v-btn>
                <v-btn value="sell" block color="red">Sell</v-btn>
              </v-btn-toggle> -->
              <v-autocomplete
                v-model="investment.order_type_id"
                :items="order_types"
                item-text="name"
                item-value="id"
                label="Order type"
                hint="Wich order type"
                filled
                persistent-hint
                required
                single-line
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6">
              <v-autocomplete
                v-model="investment.currency_id"
                :items="currencies"
                item-text="code"
                item-value="id"
                label="Currency"
                hint="Which currency"
                filled
                persistent-hint
                required
                single-line
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="investment.price"
                label="Price"
                type="number"
                :prefix="currency"
                min="0"
                step="0.0000001"
                filled
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="investment.quantity"
                label="Quantity"
                type="number"
                :prefix="currency"
                min="0"
                step="0.0000001"
                filled
                required
                @input="updateCost"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="6">
              <v-text-field
                v-model="investment.cost"
                label="Cost"
                type="number"
                prefix="$"
                min="0"
                step="0.01"
                filled
                required
                @input="updateQuantity"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="investment.reference"
                type="text"
                label="Reference"
                filled
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="investment.comment"
                type="text"
                label="Comment"
                filled
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
        <!-- <pre><code>{{investment}}</code></pre> -->
      </v-card>
    </v-dialog>
  </v-row>
</template>


<script>
export default {
  name: 'InvestmentForm',
  data: () => ({
    investment: {
      date: null,
      exchange_id: null,
      currency_id: null,
      order_type_id: null,
      price: null,
      quantity: null,
      cost: null,
    },
    currencyForm: false,
    dialog: false,
    now: null,
    currencies: [],
    exchanges: [],
    order_types: [],
    errors: [],
  }),
  computed: {
    currency() {
      if (this.investment?.currency_id) {
        return this.currencies.find((i) => i.id === this.investment.currency_id)
          ?.code
      }
      return ''
    },
  },
  watch: {
    'investment.currency_id': {
      handler() {
        this.$axios
          .get(
            `https://min-api.cryptocompare.com/data/top/exchanges/full?fsym=${this.currency}&tsym=USD`
          )
          .then((res) => {
            this.investment.price = res.data.Data.AggregatedData.PRICE
          })
      },
    },
  },
  mounted() {
    this.setNow()
    this.loadFormData()
  },
  methods: {
    updateCost() {
      if (this.investment.price) {
        this.investment.cost = this.investment.quantity * this.investment.price
      }
    },
    updateQuantity() {
      if (this.investment.price) {
        this.investment.quantity = this.investment.cost / this.investment.price
      }
    },
    postItem() {
      this.errors = []
      this.$axios
        .$post('/investments/', this.investment)
        .then(() => {
          this.dialog = false
          this.$parent.getInvestments()
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
    setNow() {
      const now = new Date()
      let dd = now.getDate()
      let mm = now.getMonth() + 1
      const yyyy = now.getFullYear()
      if (dd < 10) {
        dd = '0' + dd
      }
      if (mm < 10) {
        mm = '0' + mm
      }
      this.now = `${yyyy}-${mm}-${dd}T${now.getHours()}:${now.getMinutes()}`
      this.investment.date = this.now
    },
    async loadFormData() {
      this.currencies = await this.$axios.$get('/currency/')
      this.exchanges = await this.$axios.$get('/exchange/')
      this.order_types = await this.$axios.$get('/order_type/')
    },
  },
}
</script>

<style scoped>
.v-btn-investment {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
</style>
