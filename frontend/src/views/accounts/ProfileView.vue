<template>
  <div v-if="userInfo" id="container-profile">
    <div id="profile">
      <div id="profile-img">
        <img
          :src="
            baseUrl + (userInfo.photo || '/media/profile/defaultProfile.png')
          "
          alt=""
        />
      </div>
      <div id="profile-info">
        <div id="profile-info-main">
          <div>{{ userInfo.name }}</div>
          <div
            v-if="store.userId !== 0 && store.userId !== userInfo.pk"
            id="button-box01"
          >
            <button
              v-if="isFollowed"
              class="btn btn-outline-secondary btn-sm"
              @click="changeFollow"
            >
              팔로잉
            </button>
            <button v-else class="btn btn-primary btn-sm" @click="changeFollow">
              팔로우
            </button>
          </div>
          <div v-else-if="store.userId !== 0" id="button-box02">
            <button class="btn btn-outline-light btn-sm" @click="updateProfile">
              상세 정보 조회
            </button>
            <button class="btn btn-outline-danger btn-sm" @click="deleteUser">
              회원탈퇴
            </button>
          </div>
          <div v-else>
            <button class="btn btn-primary" @click="clickFollow_noLogin">
              팔로우
            </button>
          </div>
        </div>
        <div id="profile-info-detail">
          <div>
            <p style="font-size: 14px">작성한 평론</p>
            <p>{{ userInfo.user_write_reviews.length }}</p>
          </div>
          <div
            role="button"
            class="btn"
            data-bs-toggle="modal"
            data-bs-target="#Follower"
          >
            <p style="font-size: 14px">팔로워</p>
            <p>{{ userInfo.followers.length }}</p>
          </div>
          <div
            role="button"
            class="btn"
            data-bs-toggle="modal"
            data-bs-target="#Follow"
          >
            <p style="font-size: 14px">팔로잉</p>
            <p>{{ userInfo.followings.length }}</p>
          </div>
        </div>
      </div>
    </div>

    <div id="body">
      <div v-if="store.userId !== 0 && store.userId === userInfo.pk">
        <div id="body-title">
          <div
            id="body-title-review"
            role="button"
            @click="clickReview"
            :style="{ borderStyle: toggle ? 'solid' : 'none' }"
            style="font-size: large"
          >
            <span>작성한 평론</span>
          </div>
          <div
            id="body-title-reservation"
            role="button"
            @click="clickReservation"
            :style="{ borderStyle: !toggle ? 'solid' : 'none' }"
            style="font-size: large"
          >
            <span>예매 내역</span>
          </div>
        </div>

        <div v-if="toggle === true">
          <div v-if="userInfo.user_write_reviews.length === 0">
            <p style="text-align: center; margin: 50% 0">
              작성한 관람평이 없습니다.
            </p>
          </div>
          <div v-else>
            <UserReviews
              v-for="review in userInfo.user_write_reviews"
              :key="review.id"
              :review="review"
              :user="userInfo"
              @like-review="clickLike"
            />
          </div>
        </div>
        <div v-else>
          <div v-if="reservations.length === 0">
            <p style="text-align: center; margin: 50% 0">
              예매 내역이 없습니다.
            </p>
          </div>
          <div v-else>
            <Reservations
              v-for="reservation in reservations"
              :key="reservation.id"
              :reservation="reservation"
              :regions="regions"
            />
          </div>
        </div>
      </div>

      <div v-else>
        <div id="body-title">
          <div id="body-title-review" style="font-size: large">
            <span>작성한 평론</span>
          </div>
        </div>
        <UserReviews
          v-for="review in userInfo.user_write_reviews"
          :key="review.id"
          :review="review"
          :user="userInfo"
          @like-review="clickLike"
        />
      </div>
    </div>
  </div>

  <div
    class="modal fade"
    id="Follower"
    data-bs-backdrop="static"
    data-bs-keyboard="true"
    tabindex="-1"
    aria-labelledby="staticBackdropLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <p>팔로워</p>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
          ></button>
        </div>
        <div v-if="userInfo?.followers" class="modal-body">
          <div v-if="userInfo.followers.length === 0">
            <span>팔로워가 없습니다.</span>
          </div>
          <div v-else>
            <FollowProfile
              v-for="user in userInfo.followers"
              :key="user.pk"
              :user="user"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

  <div
    class="modal fade"
    id="Follow"
    data-bs-backdrop="static"
    data-bs-keyboard="true"
    tabindex="-1"
    aria-labelledby="staticBackdropLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <p>팔로잉</p>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
          ></button>
        </div>
        <div v-if="userInfo?.followings" class="modal-body">
          <div v-if="userInfo.followings.length === 0">
            <span>팔로우한 유저가 없습니다.</span>
          </div>
          <div v-else>
            <FollowProfile
              v-for="user in userInfo.followings"
              :key="user.pk"
              :user="user"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAccountsStore } from "@/stores/accounts";
import UserReviews from "@/components/accounts/UserReviews.vue";
import FollowProfile from "@/components/accounts/FollowProfile.vue";
import Reservations from "@/components/Reservations.vue";
import { onBeforeRouteUpdate, useRoute, useRouter } from "vue-router";
import axios from "axios";
import accountsAPI from "@/apis/accountsAPI.js";

const route = useRoute();
const router = useRouter();
const store = useAccountsStore();

const toggle = ref(true);
const reviewBox = ref("black");
const reservationBox = ref("rgb(57, 57, 57)");

const baseUrl = ref(import.meta.env.VITE_APP_BASE_URL);
const userInfo = ref(null);

const isFollowed = ref(null);

const clickFollow_noLogin = function () {
  alert("로그인이 필요합니다.");
  return false;
};

const clickReview = function (event) {
  toggle.value = true;
  reviewBox.value = "black";
  reservationBox.value = "rgb(57, 57, 57)";
};

const clickReservation = function (event) {
  toggle.value = false;
  reviewBox.value = "rgb(57, 57, 57)";
  reservationBox.value = "black";
};

onMounted(async () => {
  await accountsAPI.getOtherUserInfo(
    route.params.id,
    (response) => {
      console.log(response.data);
      userInfo.value = response.data;
      // follow 여부
      isFollowed.value = userInfo.value.followers.includes(store.userId);
    },
    (err) => console.log(err)
  );

  if (userInfo.value && store.userId === userInfo.value.pk) {
    getReservations();
    getRegions();
  }
});

onBeforeRouteUpdate(() => {
  axios({
    method: "GET",
    url: `${store.API_URL}/accounts/${route.params.id}/user/`,
  })
    .then((response) => {
      userInfo.value = response.data;
      follow.value = userInfo.value.followers.includes(store.userId);
      router.go();
    })
    .catch((err) => console.log(err));
});

const changeFollow = function () {
  axios({
    method: "POST",
    url: `${store.API_URL}/accounts/${userInfo.value.pk}/follow/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      follow.value = response.data.is_followed;
      router.go();
    })
    .catch((err) => console.log(err));
};

const deleteUser = function () {
  if (window.confirm("회원 탈퇴 하시겠습니까?")) {
    axios({
      method: "DELETE",
      url: `${store.API_URL}/accounts/${store.userId}/delete/`,
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

const likeObj = ref(null);
const likeCount = ref();

const clickLike = function (reviewId, movieId) {
  if (user1.value === null) {
    alert("로그인이 필요합니다.");
    return false;
  }
  axios({
    method: "POST",
    url: `${store.API_URL}/movies/${movieId}/reviews/${reviewId}/likes/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      likeObj.value = response.data;
      router.go();
    })
    .catch((err) => console.log(err));
};

const reservations = ref(null);

const getReservations = function () {
  axios({
    method: "GET",
    url: `${store.API_URL}/ticketing/reservation/${store.userId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      reservations.value = response.data;
      console.log("예매내역", reservations.value);
    })
    .catch((err) => console.log(err));
};

const regions = ref(null);

const getRegions = function () {
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
</script>

<style scoped>
@media (min-width: 500px) {
  #container-profile {
    padding: 50px 30px;
  }
  #profile-img > img {
    width: 125px;
    height: 125px;
    margin-right: 40px;
  }
}
@media (max-width: 500px) {
  #container-profile {
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
#container-profile {
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
  font-size: x-large;
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
#body-title {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}
#body-title > * {
  width: 100%;
  text-align: center;
  padding-top: 10px;
  padding-bottom: 10px;
  border-width: 1px;
  border-color: white;
  border-radius: 10px;
}

.modal {
  color: black;
}
.modal-content {
  background-color: rgba(202, 202, 202, 0.95);
}
</style>
