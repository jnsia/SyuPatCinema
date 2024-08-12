<template>
  <div>
    <div v-if="isOwnProfile">
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

      <div v-if="toggle">
        <div v-if="userInfo.user_write_reviews.length === 0">
          <p style="text-align: center; margin: 50% 0">
            작성한 관람평이 없습니다.
          </p>
        </div>
        <div v-else>
          <UserReviews
            v-for="review in userInfo.user_write_reviews"
            :key="review.like_users.length"
            :review="review"
            :user="userInfo"
            @likeReview="likeReview"
          />
        </div>
      </div>
      <div v-else>
        <div v-if="reservations.length === 0">
          <p style="text-align: center; margin: 50% 0">예매 내역이 없습니다.</p>
        </div>
        <div v-else>
          <Reservations
            v-for="reservation in reservations"
            :key="reservation.id"
            :reservation="reservation"
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
        @likeReview="likeReview"
      />
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import UserReviews from "@/components/accounts/UserReviews.vue";
import Reservations from "@/components/Reservations.vue";
import { useAccountsStore } from "@/stores/accounts";

const store = useAccountsStore();
const { userInfo, isOwnProfile } = defineProps({
  userInfo: Object,
  isOwnProfile: Boolean,
});

const emit = defineEmits(["likeReview"]);

const likeReview = () => emit("likeReview");

const toggle = ref(true);
const reservations = ref(null);

const clickReview = () => {
  toggle.value = true;
};

const clickReservation = () => {
  toggle.value = false;
};

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

onMounted(() => {
  getReservations();
});
</script>

<style scoped>
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
</style>
