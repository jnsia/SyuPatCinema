<template>
  <div id="all">

    <div id="navbar">
      <nav>
        <div id="navbar-box">
          <div id="navbar-box-box1"></div>
          <div id="navbar-box-box2">
            <RouterLink class="navbar-brand nav-link" :to="{ name: 'home' }">
              SYUPAT CINEMA
            </RouterLink >
          </div>
          <div id="navbar-box-box3">
            <ul v-if="!store.userInfo">
              <li class="nav-item">
                <div><RouterLink class="nav-link" :to="{ name: 'login' }">로그인</RouterLink></div>
              </li>
              <li class="nav-item">
                <div><RouterLink class="nav-link" :to="{ name: 'signup' }">회원가입</RouterLink></div>
              </li>
            </ul>
            <ul v-if="store.userInfo">
              <li class="nav-item">
                <div><RouterLink class="nav-link" :to="{ name: 'profile', params: { id: store.userInfo.pk } }" >프로필</RouterLink ></div>
              </li>
              <li class="nav-item">
                <div><RouterLink class="nav-link" :to="{ name: 'ticketing' }" >예매하기</RouterLink ></div>
              </li>
              <li class="nav-item">
                <div><a class="nav-link" @click="deleteUser">로그아웃</a></div>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>

    <div id="container">
      <RouterView />
    </div>

    <footer>
      <span style="margin-right: 20px;">© 2023 Cheosbung Patbung Shubung CINEMA</span>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useCounterStore } from "./stores/counter";

const store = useCounterStore();
const deleteUser = function () {
  if (!confirm('로그아웃 하시겠습니까?')) {
    return false
  }
  store.logoutUser();
};
</script>

<style scoped>
* {
  margin: 0 auto;
  padding: 0;
  list-style: none;
}

#all{
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #222222;
}

#navbar{
  color: white;
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
}

.nav-item>div{
  text-align: center;
  cursor: pointer;
}

.nav-item >div> a:active {
  color: gold;
  background-color: rgba(255, 255, 255, 0.5);
}

#navbar-box{
  display: flex;
  align-items: center;
  /* font-size: larger; */
  border-bottom: 1px solid white;
  height: 50px;
}

@media (max-width: 700px) {
  #navbar-box-box1 {
    display: none;
  }
  #navbar-box-box2{
    margin-left: 20px;
  }
}

@media (min-width: 420px) {
  .nav-link{
    padding: 10px 15px;
  }
  #navbar-box-box2 > a{
    font-size: 24px;
  }
}

@media (max-width: 420px) {
  .nav-link{
    padding: 10px 5px;
  }
  #navbar-box-box2 > a{
    font-size: 16px;
  }
}

#navbar-box-box3 > ul {
  display: flex;
  position: absolute;
  top: 5px;
  right: 5%;
}
.nav-link{
  /* padding: 10px 15px; */
  border-radius: 20px;
  font-size: 0.8rem;
}
#container{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
footer {
  width: 100%;
  height: 50px;
  opacity: 0.75;

  line-height: 50px;
  background-color: rgba(0, 0, 0, 0.1);
  font-size: small;
  text-align: center;
}
</style>
