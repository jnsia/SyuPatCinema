<template>
  <div id="profile-info">
    <div id="profile-info-main">
      <div>{{ userInfo?.name }}</div>
      <div v-if="isOwnProfile">
        <div id="button-box02">
          <button class="btn btn-outline-light btn-sm" @click="updateProfile">
            상세 정보 조회
          </button>
          <button class="btn btn-outline-danger btn-sm" @click="deleteUser">
            회원탈퇴
          </button>
        </div>
      </div>
      <div v-else>
        <div v-if="isLoggedIn" id="button-box01">
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
        <div v-else>
          <button class="btn btn-primary" @click="clickFollow_noLogin">
            팔로우
          </button>
        </div>
      </div>
    </div>
    <ProfileStats :userInfo="userInfo" />
  </div>
</template>

<script setup>
import ProfileStats from "./ProfileStats.vue";
import { useRouter } from "vue-router";
import { useAccountsStore } from "@/stores/accounts";

const router = useRouter();
const store = useAccountsStore();

const { userInfo, isFollowed, isLoggedIn, isOwnProfile } = defineProps({
  userInfo: Object,
  isFollowed: Boolean,
  isLoggedIn: Boolean,
  isOwnProfile: Boolean,
});

const emit = defineEmits(["changeFollow"]);

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
  router.push({ name: "profileUpdate", params: { id: store.userId } });
};

const clickFollow_noLogin = function () {
  alert("로그인이 필요합니다.");
  return false;
};
</script>

<style scoped>
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
</style>
