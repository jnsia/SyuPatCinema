<template>
  <div v-if="userInfo !== null" id="container-profile">
    <div id="profile">
      <ProfileImage :userInfo="userInfo" />
      <ProfileInfo
        :userInfo="userInfo"
        :isOwnProfile="isOwnProfile"
        @changeFollow="changeFollow"
      />
    </div>

    <ReviewSection
      :userInfo="userInfo"
      :isOwnProfile="isOwnProfile"
      @likeReview="likeReview"
    />
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
import { ref, onMounted } from "vue";
import { useAccountsStore } from "@/stores/accounts";
import { onBeforeRouteUpdate, useRoute, useRouter } from "vue-router";

import FollowProfile from "@/components/accounts/FollowProfile.vue";
import ProfileImage from "@/components/accounts/ProfileImage.vue";
import ProfileInfo from "@/components/accounts/ProfileInfo.vue";
import ReviewSection from "@/components/accounts/ReviewSection.vue";

import axios from "axios";
import accountsAPI from "@/apis/accountsAPI.js";

const route = useRoute();
const router = useRouter();
const store = useAccountsStore();

const userInfo = ref(null);
const isOwnProfile = ref(false);
const isFollowed = ref(null);

const getOtherUserInfo = async () => {
  await accountsAPI.getOtherUserInfo(
    route.params.id,
    (response) => {
      console.log(response.data);
      userInfo.value = response.data;
      isFollowed.value = userInfo.value.followers.includes(store.userId);
    },
    (error) => console.log(error)
  );

  if (userInfo.value && store.userId === userInfo.value.pk) {
    isOwnProfile.value = true;
  } else {
    isOwnProfile.value = false;
  }
};

onMounted(() => {
  getOtherUserInfo();
});

onBeforeRouteUpdate(() => {
  getOtherUserInfo();
});

const likeReview = () => {
  getOtherUserInfo();
};

const changeFollow = () => {
  axios({
    method: "POST",
    url: `${store.API_URL}/accounts/${userInfo.value.pk}/follow/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      isFollowed.value = response.data.is_followed;
      router.go();
    })
    .catch((err) => console.log(err));
};
</script>

<style scoped>
@media (min-width: 500px) {
  #container-profile {
    padding: 50px 30px;
  }
}
@media (max-width: 500px) {
  #container-profile {
    padding: 50px 10px;
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

#user-reviews {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal {
  color: black;
}
.modal-content {
  background-color: rgba(202, 202, 202, 0.95);
}
</style>
