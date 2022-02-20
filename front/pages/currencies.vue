<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex>
        <v-row>
          <v-col cols="12">
            <v-data-table
              :headers="headers"
              :items="coins"
              :items-per-page="10"
              class="elevation-1"
            >
              <template #[`item.price`]="{ item }">
                $ {{ currentValues[item.code] }}
              </template>
            </v-data-table>
            <currency-form></currency-form>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'ManageCoins',
  data() {
    return {
      headers: [
        { text: 'Code', value: 'code' },
        { text: 'Name', value: 'name' },
        { text: 'Price', value: 'price' },
      ],
      coins: [
        {
          code: '-',
          name: '-',
        },
      ],
      currentValues: {},
    }
  },
  mounted() {
    this.getCoins()
  },
  methods: {
    async getCoins() {
      await this.$axios.$get('currency/').then((data) => {
        this.coins = data
        this.coins.forEach((e) => {
          this.$axios
            .get(
              `https://min-api.cryptocompare.com/data/top/exchanges/full?fsym=${e.code}&tsym=USD`
            )
            .then((res) => {
              this.$set(
                this.currentValues,
                e.code,
                res.data.Data.AggregatedData?.PRICE
              )
            })
        })
      })
    },
  },
}
</script>

<style>
#lateral .new-invest-btn {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
</style>
