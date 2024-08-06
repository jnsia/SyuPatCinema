import { ref, computed, watch } from "vue";
import { defineStore, storeToRefs } from "pinia";
import { useRouter } from "vue-router";

import accountsAPI from "@/apis/accountsAPI";

export const useAccountsStore = defineStore(
  "accounts",
  () => {
    const router = useRouter();
    const userId = ref(0);
    const token = ref(null);
    const likeGenres = ref();
    const API_URL = "http://127.0.0.1:8000";

    const getUserInfo = async () => {
      await accountsAPI.getUserInfo(
        (response) => {
          const { pk, user_like_genres } = response.data;
          userId.value = pk;

          if (user_like_genres && user_like_genres.length > 0) {
            likeGenres.value = user_like_genres;
          } else {
            likeGenres.value = ["액션", "로맨스", "공포"]
          }
        },
        (error) => console.log(error.response)
      );
    };

    const login = async (payload) => {
      await accountsAPI.login(
        payload,
        async (response) => {
          token.value = await response.data.key;
          router.replace({ name: "home" });
        },
        (err) => console.log(confirm("아이디/비밀번호가 틀렸습니다."))
      );

      getUserInfo();
    };

    const logoutUser = () => {
      localStorage.clear();
      token.value = null;
      router.replace({ name: "home" });
    };

    return {
      login,
      logoutUser,
      getUserInfo,
      userId,
      token,
      API_URL,
      likeGenres,
    };
  },
  { persist: true }
);
