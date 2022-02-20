<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex>
        <v-row>
          <v-col cols="12">
            <v-data-table
              :headers="headers"
              :items="exchanges"
              :items-per-page="10"
              class="elevation-1"
            >
            <template #[`item.url`]="{ item }">
                <a
                  v-if="item.url"
                  :href="item.url"
                  target="_blank"
                >
                  {{ item.url }}
                </a>
              </template>
            </v-data-table>
            <exchange-form></exchange-form>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'ManageExchanges',
  data() {
    return {
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Url', value: 'url' },
      ],
      exchanges: [
        {
          name: '-',
          url: '-'
        },
      ],
    }
  },
  mounted() {
    this.getExchanges()
  },
  methods: {
    async getExchanges() {
      const exchanges = await this.$axios.$get('exchange/')
      this.exchanges = exchanges
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
