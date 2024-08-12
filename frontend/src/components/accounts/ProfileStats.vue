<template>
  <div id="profile-info-detail">
    <div>
      <p style="font-size: 14px">작성한 평론</p>
      <p>{{ userInfo?.user_write_reviews.length }}</p>
    </div>
    <div
      role="button"
      class="btn"
      data-bs-toggle="modal"
      data-bs-target="#Follower"
    >
      <p style="font-size: 14px">팔로워</p>
      <p>{{ userInfo?.followers.length }}</p>
    </div>
    <div
      role="button"
      class="btn"
      data-bs-toggle="modal"
      data-bs-target="#Follow"
    >
      <p style="font-size: 14px">팔로잉</p>
      <p>{{ userInfo?.followings.length }}</p>
    </div>
  </div>
</template>

<script setup>
const {userInfo} = defineProps({
  userInfo: Object,
});
</script>

<style scoped>
#profile-info-detail {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 20px;
  text-align: center;
}
#profile-info-detail > * {
  font-weight: bold;
  font-size: 14px;
  color: white;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
