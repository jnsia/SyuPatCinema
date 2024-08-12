<template>
  <div id="profile-img">
    <img
      :src="baseUrl + (userInfo.photo || '/media/profile/defaultProfile.png')"
      alt="Profile Image"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  userInfo: Object,
});

const baseUrl = ref(import.meta.env.VITE_APP_BASE_URL);
</script>

<style scoped>
#profile-img > img {
  border-radius: 50%;
}

@media (min-width: 500px) {
  #profile-img > img {
    width: 125px;
    height: 125px;
    margin-right: 40px;
  }
}

@media (max-width: 500px) {
  #profile-img > img {
    width: 100px;
    height: 100px;
    margin-right: 20px;
  }
}
</style>
