<template>
  <div id="seat" v-if="movie">
    <div id="movieInfo">
      <img :src="movie.poster_path" alt="" style="width: 100px;">
      
      <div id="movieInfo-detail">
        <h2>{{ movie.title }}</h2>
        <p>{{ date.split('/')[0] + '월 ' + date.split('/')[1] + '일' }} {{ time.split(':')[0] + '시 ' + time.split(':')[1] + '분' }}</p>
      </div>
    </div>

    <ul class="showcase">
      <li>
        <div class="availableSeat"></div>
        <small class="small">선택가능</small>
      </li>
      <li>
        <div class="selectedSeatIcon"></div>
        <small class="small">선택좌석</small>
      </li>
      <li>
        <div class="occupiedSeat"></div>
        <small class="small">선택불가</small>
      </li>
    </ul>

    <div @click="countSeatPrice" class="seatContainer">
      <div class="screen"></div>
      <div ref="seat_list" v-for="seat in seats" class="row">
        <span v-for="s in seat" :class="s == 0 ? 'seat' : 'occupiedSeat'" ></span>
      </div>
    </div>
    
    <div class="people">
      <p>성인</p>
      <div class="btn-group" role="group" aria-label="Basic example">
        <button type="button" class="btn btn-light" @click="(adults > 0 && button_condition) ? adults-- : console.log(false) ">-</button>
        <button type="button" class="btn btn-light">{{ adults }}</button>
        <button type="button" class="btn btn-light" @click="(adults + teenagers < 8 && button_condition) ? adults++ : console.log(false)">+</button>
      </div>
      <p>청소년</p>
      <div class="btn-group" role="group" aria-label="Basic example">
        <button type="button" class="btn btn-light" @click="(teenagers > 0 && button_condition) ? teenagers-- : console.log(false)">-</button>
        <button type="button" class="btn btn-light">{{ teenagers }}</button>
        <button type="button" class="btn btn-light" @click="(adults + teenagers < 8 && button_condition) ? teenagers++ : console.log(false)">+</button>
      </div>
      <p>가격 : {{ price }}</p>
      <button class="btn btn-danger" @click="reservation">결제하기</button>
    </div>
    
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAccountsStore } from '../../stores/accounts';

const store = useAccountsStore()
const route = useRoute()

const theater_pk = route.query.theater
const movie_pk = route.query.moviePk
const movie = ref(null)

const date = route.query.date_name
const time = route.query.time_name
const playDates = ref(null)
const playdate_pk = ref(null)

const adults = ref(0)
const teenagers = ref(0)
const price = ref(0)

const button_condition = computed(() => {
  if (totalPeople.value == 0) {
    return true
  }
  if (totalPeople.value == adults.value + teenagers.value) {
    return false
  } else {
    return true
  }
})

const seats = ref([
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
]);

// 해당되는 seat 정보를 불러오기
const getSeats = (playDatePk)=>{
  axios({
    method:"GET",
    url:`${store.API_URL}/ticketing/${0}/${theater_pk}/${movie_pk}/${playDatePk}/seat/`
  })
    .then((response)=>{
      for (const rowcol of response.data) {
        seats.value[rowcol.row][rowcol.col] = 1
      }
    })
    .catch((err)=>{
      console.log(err)
    })
}

// 해당 상영 날짜 시간 id 가져오기
const getPlayDate = ()=>{
  axios({
    method: "GET",
    url: `${store.API_URL}/ticketing/${0}/${theater_pk}/${movie_pk}/times/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      playDates.value = response.data
      for (const playdate of playDates.value) { 
        if(playdate.date===date && playdate.time===time){
          playdate_pk.value = playdate.id
          getSeats(playdate.id)
          break
        }
      }
  })
    .catch((err)=>console.log(err))
}

const getMovie = function() {
    axios({
    method: "GET",
    url: `${store.API_URL}/movies/${movie_pk}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      movie.value = response.data
  })
    .catch((err)=>console.log(err))
}

onMounted(()=>{
  getMovie()
  getPlayDate()
})

const seat_list = ref(null)
const totalPeople = ref(0)
function countSeatPrice(event) {
  if (adults.value + teenagers.value == 0) {
    alert('인원 수를 선택해주세요.')
    return false
  }
  if(totalPeople.value == adults.value + teenagers.value){
    price.value = 0
    totalPeople.value = 0
    for (let index = 0; index < seat_list.value.length; index++) {
      for (let j = 0; j < 8; j++) {
        seat_list.value[index].children[j].className=seats.value[index][j]==0?'seat':'occupiedSeat'
      }
    }
  }

  else if (event.target.className === "seat") {
    event.target.className = "selectedSeat";
    totalPeople.value++
  } else if (event.target.className === "selectedSeat") {
    event.target.className = "seat";
    totalPeople.value--
  }

  if(totalPeople.value == adults.value + teenagers.value){
    price.value = adults.value*15000+teenagers.value*10000

    for (let index = 0; index < seat_list.value.length; index++) {
      for (let j = 0; j < 8; j++) {
        // console.log(seat_list.value[index].children[j].className)
        if(seat_list.value[index].children[j].className==='selectedSeat'){
          seat_list.value[index].children[j].className='selectedSeatIcon'
        }
        else{
          seat_list.value[index].children[j].className='disavailableSeat'
        }
      }
    }
  }
}

const reservation = (next_url) => {
  if (adults.value + teenagers.value == 0) {
    alert('인원 수를 선택해주세요.')
    return false
  }

  const ticketing = (seat_id, reservation_pk) => {
    axios({
      method: 'POST',
      url: `${store.API_URL}/ticketing/create_ticket/${reservation_pk}/${theater_pk}/${movie_pk}/${playdate_pk.value}/${seat_id}/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      data: {
        price: 15000,
      }
    }).then((response) => {
      console.log('ticketing', response.data)
    })
    .catch((err) => console.log(err.response.data))
  }

  const pushSeat = (row, col, reservation_pk) => {
    axios({
      method: 'POST',
      url: `${store.API_URL}/ticketing/${playdate_pk.value}/${row}/${col}/seat/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    }).then((response) => {
      console.log('seat id ', response.data['seat_id'])
      ticketing(response.data['seat_id'], reservation_pk)
    })
    .catch((err) => console.log(err.response.data))
  }
  
  const createReservation = (next_url) => {
    axios({
      method: 'POST',
      url: `${store.API_URL}/ticketing/reservation/${store.userInfo.pk}/detail/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    }).then((response) => {
      for (let i = 0; i < seat_list.value.length; i++) {
        for (let j = 0; j < 8; j++) {
          if(seat_list.value[i].children[j].className==='selectedSeatIcon'){
            console.log(j, seat_list.value[i].children[j].className)
            pushSeat(i, j, response.data.id)
          }
        }
      }
    })
    .then((url) => {
      // window.location.href = next_url
    })
    .catch((err) => console.log(err))
  }

  createReservation(next_url)
}

const kakaoPaymant = () => {
  const ready_URL = "https://kapi.kakao.com/v1/payment/ready";
  const admin_key = "d13c19a5b986900ad003f445a8de607b";

  if (adults.value + teenagers.value == 0) {
    alert('인원 수를 선택해주세요.')
    return false
  }

  if( totalPeople.value  !== adults.value + teenagers.value){
    alert('좌석을 선택해주세요.')
    return false
  }

  axios({
    method: "POST",
    headers: {
      Authorization: `KakaoAK ${admin_key}`,
      "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    },
    url: ready_URL,
    data: {
      cid: "TC0ONETIME",
      partner_order_id: "STRING5460",
      partner_user_id: "STRING5460",
      item_name: `${movie.value.title}`,
      quantity: totalPeople.value,
      total_amount: price.value,
      tax_free_amount: 1000,
      approval_url: `${store.SITE_URL}/profile/${store.userInfo.pk}`,
      cancel_url: `${store.SITE_URL}/profile/${store.userInfo.pk}`,
      fail_url: `${store.SITE_URL}/profile/${store.userInfo.pk}`,
    },
  })
    .then((response) => {
      const next_url = response.data['next_redirect_pc_url']
      reservation(next_url)
    })
    .catch((err) => console.log(err));
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

#seat {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin-top: 70px;
}

#movieInfo{
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
  margin-bottom: 40px;
}

#movieInfo-detail {
  display: flex;
  flex-direction: column;
}

#movieInfo-detail > h2 {
  margin-bottom: 10px;
}

#movieInfo-detail > p {
  color: gray;
  text-align: end;
}

@media (max-width: 500px) {
  .people {
    flex-direction: column;
  }
}

.people {
  margin-top: 40px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.showcase {
  background-color: #777;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  display: flex;
  justify-content: center;
  padding: 5px 10px;
}

li {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 10px;
}

.small {
  color: #777;
  margin-left: 2px;
}

.showcase .seat:hover {
  cursor: default;
  scale: 1;
}

.showcase .selectedSeat:hover {
  cursor: default;
  scale: 1;
}

.seatContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.screen {
  background-color: #fff;
  margin: 15px 0px;
  padding: 10px;
  width: 280px;
  height: 160px;
  transform: rotateX(-45deg);
  box-shadow: 0 3px 10px rgb(255 255 255 / 70%);
}

.availableSeat {
  background-color: #fff;
  width: 24px;
  height: 20px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: default;
}

.selectedSeatIcon {
  background-color: #ff3346;
  width: 24px;
  height: 20px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: default;
}

.occupiedSeat {
  background-color:#444451;
  width: 24px;
  height: 20px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: default;
}

.seat {
  background-color: #fff;
  width: 24px;
  height: 20px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: pointer;
}

.disavailableSeat {
  background-color: #444451;
  width: 24px;
  height: 20px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: default;
}

.selectedSeat {
  background-color: #ff3346;
  width: 24px;
  height: 20px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: pointer;
}

.seat:hover {
  scale: 1.2;
}

.selectedSeat:hover {
  scale: 1.2;
}

.seat:nth-of-type(2) {
  margin-right: 18px;
}

.seat:nth-of-type(7) {
  margin-left: 18px;
}

.selectedSeat:nth-of-type(2) {
  margin-right: 18px;
}

.selectedSeat:nth-of-type(7) {
  margin-left: 18px;
}

.occupiedSeat:nth-of-type(2) {
  margin-right: 18px;
}
.occupiedSeat:nth-of-type(7) {
  margin-left: 18px;
}

.row {
  display: flex;
}

#count {
  color: #6feaf6;
}

#costs {
  color: #6feaf6;
}
</style>