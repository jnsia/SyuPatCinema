<template>
  <div id="navbar">
    <nav>
      <div id="navbar-box">
        <div id="navbar-box-box1"></div>
        <div id="navbar-box-box2">
          <RouterLink class="navbar-brand nav-link" :to="{ name: 'home' }">
            SYUPAT CINEMA
          </RouterLink>
        </div>
        <div id="navbar-box-box3">
          <ul v-if="!store.token">
            <li class="nav-item">
              <div>
                <RouterLink class="nav-link" :to="{ name: 'login' }"
                  >로그인</RouterLink
                >
              </div>
            </li>
            <li class="nav-item">
              <div>
                <RouterLink class="nav-link" :to="{ name: 'signup' }"
                  >회원가입</RouterLink
                >
              </div>
            </li>
          </ul>
          <ul v-else>
            <li class="nav-item">
              <div>
                <RouterLink
                  class="nav-link"
                  :to="{ name: 'profile', params: { id: store.userId } }"
                  >프로필</RouterLink
                >
              </div>
            </li>
            <li class="nav-item">
              <div>
                <RouterLink class="nav-link" :to="{ name: 'ticketing' }"
                  >예매하기</RouterLink
                >
              </div>
            </li>
            <li class="nav-item">
              <div><a class="nav-link" @click="logout">로그아웃</a></div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useAccountsStore } from "@/stores/accounts";

const store = useAccountsStore();

const logout = function () {
  if (!confirm("로그아웃 하시겠습니까?")) {
    return;
  }

  store.logoutUser();
};
</script>

<style scoped>
#navbar {
  color: white;
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.2);
}

.nav-item > div {
  text-align: center;
  cursor: pointer;
}

.nav-item > div > a:active {
  color: gold;
  background-color: rgba(255, 255, 255, 0.5);
}

#navbar-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
}

@media (max-width: 700px) {
  #navbar-box-box1 {
    display: none;
  }
  #navbar-box-box2 {
    margin-left: 20px;
  }
}

@media (min-width: 420px) {
  .nav-link {
    padding: 10px 15px;
  }
  #navbar-box-box2 > a {
    font-size: 24px;
  }
}

@media (max-width: 420px) {
  .nav-link {
    padding: 10px 5px;
  }
  #navbar-box-box2 > a {
    font-size: 16px;
  }
}

#navbar-box-box3 > ul {
  display: flex;
  position: absolute;
  top: 5px;
  right: 5%;
}

.nav-link {
  border-radius: 20px;
  font-size: 0.8rem;
}
</style>
