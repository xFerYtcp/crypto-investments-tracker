<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
              class="py-5"
            ></v-text-field>
            <v-data-table
              :headers="headers"
              :items="investments"
              :items-per-page="10"
              :search="search"
              class="elevation-1"
            >
              <template #[`item.id`]="{ item }">
                <v-btn rounded icon @click="deleteInvestment(item.id)">
                  <v-icon color="red">mdi-trash-can-outline</v-icon>
                </v-btn>
              </template>
              <template #[`item.date`]="{ item }">
                {{ new Date(item.date).toLocaleString() }}
              </template>
              <template #[`item.order_type`]="{ item }">
                <v-chip :color="getColor(item.order_type.category)" dark>
                  {{ item.order_type.name }}
                </v-chip>
              </template>
              <template #[`item.price`]="{ item }">
                $ {{ item.price }}
              </template>
              <template #[`item.cost`]="{ item }">
                $ {{ round(item.cost, 5) }}
              </template>
              <template #[`item.quantity`]="{ item }">
                {{ item.currency.code }} {{ round(item.quantity, 5) }}
              </template>
              <template #[`item.exchange`]="{ item }">
                <a
                  v-if="item.exchange"
                  :href="item.exchange.url"
                  target="_blank"
                >
                  {{ item.exchange.name }}
                </a>
              </template>
            </v-data-table>
            <investment-form></investment-form>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'InvestmentsPage',
  data() {
    return {
      search: '',
      headers: [
        { text: 'Action', value: 'id' },
        { text: 'Date', value: 'date' },
        { text: 'Exchange', value: 'exchange' },
        { text: 'Order type', value: 'order_type' },
        { text: 'Currency', value: 'currency.code' },
        { text: 'Price', value: 'price' },
        { text: 'Quantity', value: 'quantity' },
        { text: 'Cost', value: 'cost' },
        { text: 'Reference', value: 'reference' },
      ],
      investments: [
        {
          date: '-',
          currency: {
            code: '-',
            name: '-',
          },
          order_type: '-',
          price: '-',
          quantity: '-',
          cost: '-',
          exchange: {
            name: '-',
            url: '-',
          },
        },
      ],
    }
  },
  mounted() {
    this.getInvestments()
  },
  methods: {
    round(value, decimals) {
      return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals)
    },
    getitemOrderType() {
      return `item.order_type`
    },
    getColor(orderType) {
      if (orderType === 'buy') return 'green'
      else if (orderType === 'sell') return 'red'
      else return 'grey'
    },
    deleteInvestment(id) {
      this.$axios
        .$delete(`investments/${id}/`)
        .then(this.getInvestments())
        .catch((err) => console.debug(err))
    },
    async getInvestments() {
      const investments = await this.$axios.$get('investments/')
      this.investments = investments
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
