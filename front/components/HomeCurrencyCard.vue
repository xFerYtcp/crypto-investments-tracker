<template>
  <v-card v-if="balance" class="d-flex flex-column mx-auto" width="100%">
    <v-list-item three-line class="deep-purple darken-1 white--text">
      <v-list-item-content>
        <div class="text-overline">
          {{ balance.currency__name }}
        </div>
        <v-list-item-title class="text-h4 mb-1">
          {{ balance.currency__code }}
        </v-list-item-title>
        <v-list-item-subtitle class="text-h5 white--text"
          >$ {{ coinData ? coinData.AggregatedData.PRICE : '-' }}
          <span class="caption"
            >{{
              coinData
                ? $parent.round(coinData.AggregatedData.CHANGEPCT24HOUR, 2)
                : '-'
            }}% in 24Hr</span
          ></v-list-item-subtitle
        >
      </v-list-item-content>

      <v-list-item-avatar v-if="coinData" tile size="80"
        ><img
          :src="`https://www.cryptocompare.com/${[
            coinData.CoinInfo.ImageUrl,
          ]}`"
      /></v-list-item-avatar>
    </v-list-item>

    <v-card-text>
      <v-row align="center">
        <v-col cols="6">
          <p class="text-h5">
            {{ balance.currency__code }}
            {{ $parent.round(balance.buy_quantity - balance.sell_quantity, 5) }}
          </p>
          <p class="text--primary">
            $
            {{ $parent.round($parent.currentBalance(balance), 2) }}
            <span class="caption text--disabled"
              >$
              {{ $parent.round(balance.buy_cost - balance.sell_cost, 2) }}</span
            >
          </p>
        </v-col>
        <v-col
          class="text-h4 text-right"
          :class="[
            ($parent.currentBalance(balance)-(balance.buy_cost - balance.sell_cost)) >= 0 ? 'green--text' : 'red--text',
          ]"
          cols="6"
        >
          {{
            $parent.round(
              (((balance.buy_quantity - balance.sell_quantity) * currentValue -
                (balance.buy_cost - balance.sell_cost)) /
                (balance.buy_cost - balance.sell_cost)) *
                100,
              2
            )
          }}%
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>


<script>
export default {
  name: 'HomeCurrencyCard',
  props: {
    balance: { type: Object, default: null },
    currentValue: { type: Number, default: null },
    coinData: { type: Object, default: null },
  },
  computed: {},
}
</script>
