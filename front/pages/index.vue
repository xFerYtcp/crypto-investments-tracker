<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex>
        <v-autocomplete
          v-model="exchange"
          :items="exchanges"
          item-text="name"
          item-value="id"
          label="Exchanges"
          hint="Select an exchange"
          chips
          clearable
          filled
          persistent-hint
          required
          single-line
          @change="getBalance()"
        ></v-autocomplete>
        <v-row dense>
          <v-col cols="12" sm="12" md="6" lg="4" class="d-flex center">
            <v-card
              v-if="balance"
              class="d-flex flex-column mx-auto"
              width="100%"
            >
              <v-list-item three-line class="light-blue darken-3 white--text">
                <v-list-item-title class="text-h4 mb-1 text-center white--text">
                  $ {{ round(totalCurrentBalance, 2) }}
                  <span class="caption">$ {{ round(totalBuy, 2) }}</span>
                </v-list-item-title>
              </v-list-item>
            </v-card>
          </v-col>
          <v-col cols="12" sm="12" md="6" lg="4" class="d-flex center">
            <v-card
              v-if="balance"
              class="d-flex flex-column mx-auto"
              width="100%"
            >
              <v-list-item
                three-line
                class="white--text"
                :class="[
                  totalCurrentBalance - totalBuy >= 0
                    ? 'green lighten-1'
                    : 'red lighten-1',
                ]"
              >
                <v-list-item-title class="text-h4 mb-1 text-center">
                  $ {{ round(totalCurrentBalance - totalBuy, 2) }}
                </v-list-item-title>
              </v-list-item>
            </v-card>
          </v-col>
          <v-col cols="12" sm="12" md="6" lg="4" class="d-flex center">
            <v-card
              v-if="balance"
              class="d-flex flex-column mx-auto"
              width="100%"
            >
              <v-list-item
                three-line
                class="white--text"
                :class="[
                  totalCurrentBalance - totalBuy >= 0
                    ? 'green lighten-1'
                    : 'red lighten-1',
                ]"
              >
                <v-list-item-title class="text-h4 mb-1 text-center">
                  {{
                    round(
                      ((totalCurrentBalance - totalBuy) / totalBuy) * 100,
                      2
                    )
                  }}%
                </v-list-item-title>
              </v-list-item>
            </v-card>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col
            v-for="b in balance"
            :key="b.currency__id"
            cols="12"
            sm="12"
            md="6"
            lg="4"
            class="d-flex center"
          >
            <home-currency-card
              :current-value="currentValues[b.currency__code]"
              :balance="b"
              :coin-data="coinData[b.currency__code]"
            />
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import HomeCurrencyCard from '~/components/HomeCurrencyCard.vue'
export default {
  name: 'IndexPage',
  components: { HomeCurrencyCard },
  data() {
    return {
      balance: [],
      currentValues: {},
      coinData: {},
      exchange: null,
      exchanges: [],
    }
  },
  computed: {
    totalBuy() {
      return this.balance.reduce((sumValue, curValue) => {
        return sumValue + (curValue.buy_cost - curValue.sell_cost)
      }, 0)
    },
    totalCurrentBalance() {
      return this.balance.reduce((sumValue, curValue) => {
        return sumValue + this.currentBalance(curValue)
      }, 0)
    },
  },
  mounted() {
    this.listUsedExchanges()
    this.getBalance()
  },
  methods: {
    round(value, decimals) {
      return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals)
    },
    listUsedExchanges() {
      this.$axios.$get('exchange?onlyused').then((data) => {
        this.exchanges = data
      })
    },
    currentBalance(item) {
      const curBal =
        (item.buy_quantity - item.sell_quantity) *
        this.currentValues[item.currency__code]
      return curBal
    },
    getBalance() {
      const url = this.exchange
        ? `balance?exchange=${this.exchange}`
        : 'balance'
      this.$axios.$get(url).then((data) => {
        this.balance = data
        this.balance.forEach((e) => {
          this.$axios
            .get(
              `https://min-api.cryptocompare.com/data/top/exchanges/full?fsym=${e.currency__code}&tsym=USD`
            )
            .then((res) => {
              this.$set(
                this.currentValues,
                e.currency__code,
                res.data.Data.AggregatedData?.PRICE
              )
              this.$set(this.coinData, e.currency__code, res.data.Data)
            })
          //
        })
      })
    },
  },
}
</script>
