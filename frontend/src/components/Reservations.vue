<template>
  <div v-if="props.reservation.ticket_set.length > 0" id="reservation">
    <div id="reservation-movie">
      <img :src="props.reservation.ticket_set[0].movie.poster_path" alt="" />
      <span>{{ props.reservation.ticket_set[0].movie.title }}</span>
    </div>
    <div id="reservation-detail">
      <p>
        극장 위치 : {{ region }}/{{
          props.reservation.ticket_set[0].theater.name
        }}
      </p>
      <p>상영 날짜 : {{ props.reservation.ticket_set[0].time.date }}</p>
      <p>상영 시간 : {{ props.reservation.ticket_set[0].time.time }}</p>

      <div
        id="reservation-detail-seats"
        v-for="ticket in props.reservation.ticket_set"
        :key="ticket.id"
      >
        <p>티켓 좌석 : {{ ticket.seat.row }}열 {{ ticket.seat.col }}행</p>
      </div>

      <div id="reservation-detail-people">
        <p>인원 수</p>
        <p>성인 : {{ adult }}</p>
        <p>청소년 : {{ teen }}</p>
      </div>

      <p id="reservation-detail-price">티켓 결제 금액 : {{ price }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAccountsStore } from "../stores/accounts";

const region = ref(null);
const adult = ref(0);
const teen = ref(0);
const price = ref(0);
const props = defineProps({
  reservation: Object,
  regions: Array,
});

const regions = ref(null)

const getRegions = async () => {
  axios({
    method: "GET",
    url: `${store.API_URL}/ticketing/regions/`,
  })
    .then((response) => {
      regions.value = response.data;
      console.log("regions ", regions.value);
    })
    .catch((err) => console.log(err));
};

onMounted(async () => {
  await getRegions()

  for (const obj in regions.value) {
    if (
      regions.value[obj].id === props.reservation.ticket_set[0]?.theater.regions
    ) {
      region.value = regions.value[obj].name;
      break;
    }
  }
  for (const ticket of props.reservation.ticket_set) {
    console.log(ticket.price);
    price.value += ticket.price;
    if (ticket.price === 15000) adult.value++;
    else teen.value++;
  }
});
</script>

<style scoped>
#reservation {
  display: flex;
  justify-content: space-around;
  align-items: center;

  border: 1px solid white;
  border-radius: 20px;
  margin: 10px 0;
  padding: 20px 20px;
}
#reservation-movie {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
#reservation-movie > img {
  width: 150px;
  margin-bottom: 5px;
}
#reservation-detail {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 12px;
}
</style>
