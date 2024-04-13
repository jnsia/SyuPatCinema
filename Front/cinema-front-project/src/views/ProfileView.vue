<template>
  <div v-if="user2" id="container-profile">
    <div id="profile">
      <div id="profile-img">
        <img :src=" store.API_URL + (user2.photo || '/media/profile/defaultProfile.png') " alt="" />
      </div>
      <div id="profile-info">
        <div id="profile-info-main">
          <div>{{ user2.name }}</div>
          <div v-if="user1!==null && user1.pk !== user2.pk" id="button-box01">
            <button v-if="follow" class="btn btn-outline-secondary btn-sm" @click="changeFollow" > 팔로잉 </button>
            <button v-else class="btn btn-primary btn-sm" @click="changeFollow"> 팔로우 </button>
          </div>
          <div v-else-if="user1!==null" id="button-box02">
            <button class="btn btn-outline-light btn-sm" @click="updateProfile">
              상세 정보 조회
            </button>
            <button class="btn btn-outline-danger btn-sm" @click="deleteUser">
              회원탈퇴
            </button>
          </div>
          <div v-else>
            <button class="btn btn-primary" @click="clickFollow_noLogin"> 팔로우 </button>
          </div>
        </div>
        <p id="profile-info-detail">
          <div>
            <p style="font-size: 14px;">작성한 평론</p>
            <p>{{ user2.user_write_reviews.length }}</p>
          </div>
          <div role="button" class="btn" data-bs-toggle="modal" data-bs-target="#Follower">
            <p style="font-size: 14px;">팔로워</p>
            <p>{{ user2.followers.length }}</p>
          </div>
          <div role="button" class="btn" data-bs-toggle="modal" data-bs-target="#Follow">
            <p style="font-size: 14px;">팔로잉</p>
            <p>{{ user2.followings.length }}</p>
          </div>
        </p>
      </div>
    </div>

    <div id="body">
      <div v-if="user1!==null &&  user1.pk===user2.pk">
        <div id="body-title">
          <div id="body-title-review" role="button" @click="clickReview" :style="{'borderStyle': toggle ? 'solid' : 'none'}" style="font-size: large;">
            <span>작성한 평론</span>
          </div>
          <div id="body-title-reservation" role="button" @click="clickReservation" :style="{'borderStyle': !toggle ? 'solid' : 'none'}" style="font-size: large;">
            <span>예매 내역</span>
          </div>
        </div>

        <div v-if="toggle===true">
          <div v-if="user2.user_write_reviews.length===0"><p style="text-align: center; margin: 50% 0;">작성한 관람평이 없습니다.</p></div>
          <div v-else><UserReviews v-for="review in user2.user_write_reviews" :key="review.id" :review="review" :user="user2" @like-review="clickLike"/></div>
        </div>
        <div v-else>
          <div v-if="reservations.length===0"><p style="text-align: center; margin: 50% 0;">예매 내역이 없습니다.</p></div>
          <div v-else><Reservations v-for="reservation in reservations" :key="reservation.id" :reservation="reservation" :regions="regions"/></div>
        </div>
      </div>

      <div v-else>
        <div id="body-title">
          <div id="body-title-review" style="font-size: large;">
            <span>작성한 평론</span>
          </div>
        </div>
        <UserReviews v-for="review in user2.user_write_reviews" :key="review.id" :review="review" :user="user2" @like-review="clickLike"/>
      </div>
    </div>
  </div>

  <div class="modal fade" id="Follower" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <p>팔로워</p>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div v-if="followers.length===0"><span>팔로워가 없습니다.</span></div>
          <div v-else><FollowProfile v-for="user in followers" :key="user.pk" :user="user"/></div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="Follow" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <p>팔로잉</p>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div v-if="followings.length===0"><span>팔로우한 유저가 없습니다.</span></div>
          <div v-else><FollowProfile v-for="user in followings" :key="user.pk" :user="user"/></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useCounterStore } from "../stores/counter";
import UserReviews from "@/components/UserReviews.vue";
import Reservations from "@/components/Reservations.vue";
import FollowProfile from "@/components/FollowProfile.vue";
import {
  onBeforeRouteUpdate,
  useRoute,
  useRouter,
} from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const store = useCounterStore();

const toggle = ref(true)
const reviewBox = ref('black')
const reservationBox = ref('rgb(57, 57, 57)')

const user1 = ref(null)
const user2 = ref(null);
const follow = ref(null);

const clickFollow_noLogin = function(){
  alert('로그인이 필요합니다.')
  return false
}

const clickReview = function(event){
  toggle.value = true
  reviewBox.value = 'black'
  reservationBox.value = 'rgb(57, 57, 57)'
}

const clickReservation = function(event){
  toggle.value = false
  reviewBox.value = 'rgb(57, 57, 57)'
  reservationBox.value = 'black'
}

onMounted(() => {
  // 현재 로그인한 User 정보 조희 user1(로그인 안하면 null)
  if(store.token!==null){
    store.getUserInfo();
    user1.value = store.userInfo
  }
  // 방문한 User 정보 조희 user2
  axios({
    method: "GET",
    url: `${store.API_URL}/accounts/${route.params.id}/user/`,
  })
    .then((response) => {
      user2.value = response.data;
      // follow 여부
      if(user1.value!==null){
        follow.value = user2.value.followers.includes(user1.value.pk);
      }
      // user2의 Follow 정보 조회
      getFollowUsersInfo()
    })
    .then(()=>{
      console.log(user1.value)
      console.log(user2.value)
      // 예매내역 조회
      if (user1.value!==null && user1.value.pk === user2.value.pk)
        getReservations()
        getRegions()
    })
    .catch((err) => console.log(err));
});

onBeforeRouteUpdate(() => {
  axios({
    method: "GET",
    url: `${store.API_URL}/accounts/${route.params.id}/user/`,
  })
    .then((response) => {
      user2.value = response.data;
      follow.value = user2.value.followers.includes(user1.value.pk);
      router.go();
    })
    .catch((err) => console.log(err));
});

const changeFollow = function () {
  axios({
    method: "POST",
    url: `${store.API_URL}/accounts/${user2.value.pk}/follow/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      follow.value = response.data.is_followed;
      router.go()
    })
    .catch((err) => console.log(err));
};

const deleteUser = function () {
  if (window.confirm("회원 탈퇴 하시겠습니까?")) {
    axios({
      method: "DELETE",
      url: `${store.API_URL}/accounts/${user1.value.pk}/delete/`,
    })
      .then(() => {
        store.logoutUser();
      })
      .then(() => {
        confirm("회원탈퇴 되었습니다.");
      })
      .catch((err) => console.log(err));
  }
};

const updateProfile = () => {
  router.push({ name: "profileUpdate", params: { id: store.userInfo.pk } });
};

const likeObj = ref(null)
const likeCount = ref()
const clickLike = function (reviewId, movieId) {
  if(user1.value===null){
    alert('로그인이 필요합니다.')
    return false
  }
  axios({
    method: "POST",
    url: `${store.API_URL}/movies/${movieId}/reviews/${reviewId}/likes/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      likeObj.value = response.data
      console.log(likeObj.value)
      router.go()
    })
    .catch((err) => console.log(err));
};

const reservations = ref(null)
const getReservations = function(){
  axios({
    method:'GET',
    url:`${store.API_URL}/ticketing/reservation/${user1.value.pk}/`,
    headers:{
      Authorization:`Token ${store.token}`
    }
  })
    .then((response)=>{
      reservations.value = response.data
      console.log('예매내역', reservations.value)
    })
    .catch(err=>console.log(err))
}

const regions = ref(null)
const getRegions = function(){
  axios({
        method:'GET',
        url:`${store.API_URL}/ticketing/regions/`,
    })
      .then((response)=>{
          regions.value = response.data
          console.log('regions ', regions.value)
      })
      .catch(err=>console.log(err))
}

const followers = ref([])
const followings = ref([])
const getFollowUsersInfo = function(){
  for (const userPk of user2.value.followers) {
    axios({
      method:'GET',
      url:`${store.API_URL}/accounts/${userPk}/user/`,
    })
      .then((response)=>{
        followers.value.push(response.data)
      })
      .catch(err=>console.log(err))
  }
  
  for (const userPk of user2.value.followings) {
    axios({
      method:'GET',
      url:`${store.API_URL}/accounts/${userPk}/user/`,
    })
      .then((response)=>{
        followings.value.push(response.data)
      })
      .catch(err=>console.log(err))
  }
}
</script>

<style scoped>
* {
  margin: 0 auto;
  padding: 0;
}
@media (min-width: 500px) {
  #container-profile{
    padding: 50px 30px;
  }
  #profile-img > img {
    width: 125px;
    height: 125px;
    margin-right: 40px;
  }
}
@media (max-width: 500px) {
  #container-profile{
    padding: 50px 10px;
  }
  #profile-img > img {
    width: 100px;
    height: 100px;
    margin-right: 20px;
  }
  * {
    font-size: 14px;
  }
}
#container-profile{
  margin-top: 80px;
  min-height: 100vh;
  border-radius: 20px;
  border: 1px solid white;
  /* padding: 50px 30px; */
  padding-bottom: 20px;
  background-color: rgba(0, 0, 0, 0.1);
}
#profile {
  display: flex;
  flex-direction: row;
  /* justify-content: space-around; */
  align-items: center;
  margin-bottom: 30px;
}
#profile-img > img {
  border-radius: 50%;
}
#profile-info {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
#profile-info-main {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  font-size:x-large;
  font-weight: bolder;
  margin-bottom: 20px;
  gap: 10px;
}
#profile-info-main > * {
  display: flex;
  align-items: center;
  gap: 10px;
}
#profile-info-detail {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 20px;
  text-align: center;
}
#profile-info-detail > * {
  /* font-size: larger; */
  font-weight: bold;
  font-size: 14px;
  color: white;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
#user-reviews {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
#body-title{
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}
#body-title>*{
  width: 100%;
  text-align: center;
  padding-top: 10px;
  padding-bottom: 10px;
  border-width: 1px;
  border-color: white;
  border-radius: 10px;
}

.modal{
  color: black;
}
.modal-content{
  background-color: rgba(202, 202, 202, 0.95);
}
</style>
