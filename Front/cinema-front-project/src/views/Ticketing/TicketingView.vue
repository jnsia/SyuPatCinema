<template>
  <div v-if="regions" id="Ticketing-Box">
    <div id="box">
      <div class="select-box regions-box">
        <div class="select-title">
          <h3>지역</h3>
        </div>
        <div class="select-buttons" >
          <div class="selects" ref="region_list" :id="region.id" v-for="region in regions.slice(0,regions.length-1)" :key="region.id" role="button" @click="pickregion(region.id, region.name)">
            <span>{{ region.name }}</span>
          </div>
        </div>
      </div>

      <div class="select-box theaters-box" v-if="region_p">
        <div class="select-title">
          <h3>극장</h3>
        </div>
        <div class="select-buttons">
          <div
            class="selects"
            ref="theater_list"
            :id="theater.id" 
            :key="theater.id" 
            role="button" 
            v-for="theater in regions_theaters" 
            @click="picktheater(theater.id, theater.name)"
          >
            <span>{{ theater.name }}</span>
          </div>
        </div>
      </div>

      <div class="select-box movies-box">
        <div class="select-title">
          <h3>영화</h3>
        </div>
        <div v-if="theater_p" class="select-buttons">
          <div class="selects" ref="movie_list" :id="movie.id" v-for="movie in movies" :key="movie.id" role="button" @click="pickmovie(movie.id, movie.title, movie.poster_path)">
            <span>{{ movie.title }}</span>
          </div>
        </div>
        <div v-else class="select-buttons">
          <div>극장을 선택해주세요.</div>
        </div>
      </div>

      <div class="select-box dates-box">
        <div class="select-title">
          <h3>날짜</h3>
        </div>
        <div v-if="movie_p" class="select-buttons">
          <div class="selects" ref="date_list" :id="date.id" v-for="date in dates" :key="date.id" role="button" @click="pickdate(date.id, date.d)">
            <span>{{ date.d }}</span>
          </div>
        </div>
        <div v-else class="select-buttons">
          <div>영화를 선택해주세요.</div>
        </div>
      </div>

      <div class="select-box times-box">
        <div class="select-title">
          <h3>시간</h3>
        </div>
        <div v-if="date_p!==null" class="select-buttons">
          <div class="selects" ref="time_list" :id="time.id" v-for="time in times" :key="time.id" role="button" @click="picktime(time.id, time.t)">
            <span>{{ time.t }}</span>
          </div>
        </div>
        <div v-else class="select-buttons">
          <div style="text-align: center; margin-top: 15px;">날짜를</div>
          <div style="text-align: center; ">선택해주세요.</div>
        </div>
      </div>
    </div>
  </div>
  <div id="box2">
    <div id="ticketInfo" v-if="time_name!==null">
      <div id="ticketInfo-movieInfo">
        <img style="width: 100px;" :src="movie_src" alt="">
      </div>
      <div id="ticketInfo-detailInfo">
        <p > 영화 {{ movie_title }}</p>
        <p > 극장 {{ theater_name }}/{{ region_name }}</p>
        <p > 일시 {{ date_name }}/{{ time_name }}</p>
      </div>
    </div>
    <div id="goSeat">
      <button class="btn btn-danger btn-sm" @click="gotopickSeat">좌석 선택</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref,onMounted } from "vue";
import { useCounterStore } from "../../stores/counter";
import { reservationStore } from "../../stores/reservation";

import { useRouter,useRoute } from "vue-router";
const route = useRoute()
const router = useRouter()
const store = useCounterStore();
const store_ticketing = reservationStore()

// 선택된 지역/극장/영화
const region_p = ref(1)
const theater_p = ref(1)
const movie_p = ref(null)
const date_p = ref(null)
const time_p = ref(null)

const region_name = ref(null)
const theater_name = ref(null)
const movie_src = ref(null)
const movie_title = ref(null)
const date_name = ref(null)
const time_name = ref(null)

// 모든 지역/극장
const regions = ref(null);
const theaters = ref(null);
const movies = ref(null);
const regions_theaters = ref([]);
const dates = store_ticketing.dates
const times = store_ticketing.times
const region_list = ref(null)
const theater_list = ref(null)
const movie_list = ref(null)
const date_list = ref(null)
const time_list = ref(null)

onMounted(()=>{
  getRegions()
  getMovies()
})

const getRegions = () => {
  axios({
    method: "GET",
    url: `${store.API_URL}/ticketing/regions/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      regions.value = response.data
  })
    .then(()=>{
      pickregion(1, regions.value[0].name)
    })
    .catch((err)=>console.log(err))
};

const getTheater = () => {
  axios({
    method: "GET",
    url: `${store.API_URL}/ticketing/theaters/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      theaters.value = response.data
  })
    .then(()=>{
      regions_theaters.value = []
      for (const theater of theaters.value) {
        if(theater.regions === region_p.value){
          regions_theaters.value.push(theater)
        }
      }
    })
    .then(()=>{
      picktheater(1, theaters.value[0].name)
    })
    .catch((err)=>console.log(err))
}

const getMovies = function () {
    axios({
    method: "GET",
    url: `${store.API_URL}/ticketing/movies/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      movies.value = response.data
  })
    .then(()=>{
      if (route.query.moviePk!==undefined){
        pickmovie(route.query.moviePk)
        console.log('영화 detail -> 예매하기', route.query.moviePk)
      }else{
        pickmovie(3, movies.value[0].title, movies.value[0].poster_path)
      }
    })
    .catch((err)=>console.log(err))
}

const pickregion = function(regionId, regionName){
  region_p.value = regionId
  region_name.value = regionName
  region_list.value.map((region) => {
    if (region.id == regionId) {
      region.style.border = '1px solid red'
      region.style.borderRadius = '10px'
      region.children[0].style.color = 'red'
    } else {
      region.style.border = ''
      region.style.borderRadius = ''
      region.children[0].style.color = 'black'
    }
  })
  getTheater()
}

const picktheater = function(theaterId, theaterName) {
  theater_p.value = theaterId
  theater_name.value = theaterName
  theater_list.value.map((theater) => {
    if (theater.id == theaterId) {
      theater.style.border = '1px solid red'
      theater.style.borderRadius = '10px'
      theater.children[0].style.color = 'red'
    } else {
      theater.style.border = ''
      theater.style.borderRadius = ''
      theater.children[0].style.color = 'black'
    }
  })
}

const pickmovie = function(movieId, movieTitle, movieSrc){
  movie_p.value = movieId
  movie_title.value = movieTitle
  movie_src.value = movieSrc
  movie_list.value.map((movie) => {
    if (movie.id == movieId) {
      movie.style.border = '1px solid red'
      movie.style.borderRadius = '10px'
      movie.children[0].style.color = 'red'
    } else {
      movie.style.border = ''
      movie.style.borderRadius = ''
      movie.children[0].style.color = 'black'
    }
  })
}

const pickdate = function(dateId, dateDate){
  if (movie_p.value===null) {
    alert('영화를 선택해주세요!')
    return false
  }

  date_p.value = dateId
  date_name.value = dateDate

  date_list.value.map((date) => {
    if (date.id == dateId) {
      date.style.border = '1px solid red'
      date.style.borderRadius = '10px'
      date.children[0].style.color = 'red'
    } else {
      date.style.border = ''
      date.style.borderRadius = ''
      date.children[0].style.color = 'black'
    }
  })
}

const picktime = function(timeId, timeTime){
  time_p.value = timeId
  time_name.value = timeTime
  time_list.value.map((time) => {
    if (time.id == timeId) {
      time.style.border = '1px solid red'
      time.style.borderRadius = '10px'
      time.children[0].style.color = 'red'
    } else {
      time.style.border = ''
      time.style.borderRadius = ''
      time.children[0].style.color = 'black'
    }
  })
}

const gotopickSeat = function(){
  console.log(movie_p.value)
  if(region_p.value!==null && theater_p.value!==null && movie_p.value!==null && date_p.value!==null && time_p.value!==null){
    router.push({
      name:'seat',
      query:{
        theater:theater_p.value,
        moviePk:movie_p.value,
        date_name:date_name.value,
        time_name:time_name.value,
      }})
  }
  else{
    alert('지역/지점/영화/시간을 선택해주세요')
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  font-size: 12px;
  color: black;
}
#Ticketing-Box{
  margin-top: 80px;
  margin-bottom: 30px;
}
#box{
  display: flex;
  min-height: 500px;
  box-shadow: 0 0 15px 5px gray;
  border-radius: 10px;
}
.select-box {
  background-color: white;
  border: 1px solid rgb(141, 141, 141);
}
.select-title{
  background-color: rgba(255, 245, 136, 0.4);
  height: 60px;
  /* padding: 20px 30px; */
  display: flex;
  align-items: center;
  justify-content: center;
}
.select-title
.select-title > h3 {
  font-size: 14px;
  font-weight: bold;
}
.select-buttons{
  display: flex;
  min-width: 15%;
  flex-direction: column;
  overflow-y: scroll;
  height: 70vh;
}
.selects {
  border: 1px solid rgb(230, 230, 230);
  padding: 20px 10px;
  text-align: center;
}
.scroll {
  -ms-overflow-style: none; /* 인터넷 익스플로러 */
  scrollbar-width: none; /* 파이어폭스 */
}
/* ( 크롬, 사파리, 오페라, 엣지 ) 동작 */
*::-webkit-scrollbar {
  display: none;
}

#box2{
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;

  background: rgba(255, 255, 255, 0.75);
  margin: 10px 0px;
  padding: 10px;
  width: 100%;
}
#ticketInfo{
  display: flex;
  flex-direction: row;
  justify-content:first baseline;
  padding: 10px;
}
#ticketInfo-detailInfo{
  margin-left: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
