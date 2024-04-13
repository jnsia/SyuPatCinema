<template>
  <div id="main" v-if="userInfo">
    <h4 id="main-title1" style="text-align: center; margin-bottom: 20px;">회원 정보 조회 및 수정</h4>
    <form id="main-form1">

      <div class="photo">
        <label for="photo">
          <img id="img" :src="previewPhoto" />
          <div v-if="updating">파일을 선택해주세요!</div>
          <div v-else></div>
        </label>
        <input id="photo" type="file" ref="photo" hidden @change="changePhoto" :disabled="!updating"/>
      </div>

      <div class="input-group input-group-sm">
        <span class="input-group-text">ID</span>
        <input type="text" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" :placeholder="userInfo.username" v-model="username" @input="check_id" :disabled="!updating"><br>
        <span v-if="check_idd === false" style="color: rgb(214, 62, 62); font-size: small;">
          아이디: 영문자 또는 숫자 6~20자 입력해주세요(영문으로 시작해주세요)
        </span>
      </div>

      <div class="input-group input-group-sm">
        <span class="input-group-text">이름</span>
        <input type="text" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" :placeholder="userInfo.name" v-model="name" :disabled="!updating">
        <span></span>
      </div>

      <div class="input-group input-group-sm">
        <span class="input-group-text">생년월일</span>
        <input type="text" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" :placeholder="userInfo.birth" v-model="birth" @input="check_birth" :disabled="!updating"><br>
        <span v-if="check_birthh === false" style="color: rgb(214, 62, 62); font-size: small;">
          YYYY-MM-DD 형식에 맞게 생년월일을 입력해주세요
        </span>
      </div>

      <div class="input-group input-group-sm">
        <span class="input-group-text">전화번호</span>
        <input type="text" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" :placeholder="userInfo.phoneNumber" v-model="phone" @input="check_phone" :disabled="!updating"><br>
        <span v-if="check_phonee === false" style="color: rgb(214, 62, 62); font-size: small;">
          000-0000-0000 형식에 맞게 전화번호를 입력해주세요
        </span>
      </div>

      <div id="genre">
        <span style="font-size:large; margin-top: 5px;">선호하는 장르</span>
        <div id="genre-btns">
          <div v-for="genre in genres" :key="genre.id">
            <button  
              v-if="genre.name!=='다큐멘터리' && genre.name!=='서부' && genre.name!=='TV 영화'" 
              :style="{ backgroundColor: like_genres.includes(genre.id) ? 'grey' : 'white' }"
              :value="genre.id"
              :disabled="!updating"
              @click.prevent="selectGenre" 
               >
              {{ genre.name }}
            </button>
          </div>
        </div>
      </div>

      <div style="margin-bottom: 20px">
        <button v-if="updating === false" class="btn btn-primary btn-sm" @click="updating = true" >
          정보 수정하기
        </button>
        <template v-else>
          <button class="btn btn-danger btn-sm" @click=" () => { updating = false; updateUser();}">
            저장하기
          </button>
          <button class="btn btn-success btn-sm" style="margin-left: 10px ;" @click="returnProfile">취소하기</button>
        </template>
      </div>
    </form>


    <br>
    <br>
    <h4 id="main-title2" style="text-align: center;">비밀번호 변경</h4>
    <form id="main-form2" @submit.prevent="changePassword">
      <div class="input-group input-group-sm" style="margin-top: 20px;">
        <span class="input-group-text">현재 비밀번호</span>
        <input type="password" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" v-model="password" />
      </div>

      <div class="input-group input-group-sm" style="padding-bottom: 0px; text-align: start;">
        <span class="input-group-text">새 비밀번호</span>
        <input type="password" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" v-model="password1" @input="check_pass"/>
      </div>
      <span v-if="check_passs === false" style="color: rgb(214, 62, 62); font-size: small; padding-top: 0px;">
        비밀번호: 8~16자 영문, 숫자 조합으로 입력해주세요
      </span>
      

      <div class="input-group input-group-sm" style="padding-bottom: 0px;">
        <span class="input-group-text">새 비밀번호 확인</span>
        <input type="password" class="form-control" style="border-top-right-radius: 5px; border-bottom-right-radius: 5px;" v-model="password2" @input="check_pass2">
      </div>
      <span v-if="check_pass22 === false" style="color: rgb(214, 62, 62); font-size: small;padding-top: 0px;">
        비밀번호가 일치하지 않습니다.
      </span>

      

      <button class="btn btn-danger btn-sm" style="margin: 20px; padding-top: 3px; padding-bottom: 3px;">
        비밀번호 변경하기
      </button>
    </form>
    <br>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "../stores/counter";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter()
const store = useCounterStore();
const genres = ref([]);
const userInfo = store.userInfo;
const updating = ref(false);

const name = ref(userInfo.name);
const username = ref(userInfo.username);
const birth = ref(userInfo.birth);
const phone = ref("0" + userInfo.phoneNumber.substr(3));
const photo = ref(null);
const previewPhoto = ref(store.API_URL + store.userInfo.photo);
const password = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const like_genres = userInfo.like_genres.map((genre) => genre.id);

const check_idd = ref(true);
const check_passs = ref(true);
const check_pass22 = ref(true);
const check_birthh = ref(true);
const check_phonee = ref(true);

const check_id = () => {
  const trueForm = /^[a-z]+[a-z0-9]{5,19}$/g;
  check_idd.value = trueForm.test(username.value);
};

const check_pass = () => {
  const trueForm = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{8,16}$/;
  check_passs.value = trueForm.test(password1.value);
};

const check_pass2 = () => {
  check_pass22.value = password1.value === password2.value;
};

const check_birth = () => {
  const trueForm = /^\d{4}-\d{2}-\d{2}$/;
  check_birthh.value = trueForm.test(birth.value);
};

const check_phone = () => {
  const trueForm = /^(?:\d{3}|\(\d{3}\))([-\/\.])\d{4}\1\d{4}$/;
  check_phonee.value = trueForm.test(phone.value);
};

const returnProfile = function(){
  router.go()
}

const updateUser = function () {
  const phoneNumber = "+82" + phone.value.substr(1);
  const User = {
    username: username.value,
    name: name.value,
    birth: birth.value,
    phoneNumber: phoneNumber,
    like_genres: like_genres,
  };
  if (photo.value.files.length > 0) {
    User["photo"] = photo.value.files[0];
  }

  if (window.confirm('수정하시겠습니까?')){
    axios({
    method: "PUT",
    url: `${store.API_URL}/accounts/${store.userInfo.pk}/user/update/`,
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "multipart/form-data",
    },
    data: User,
  })
    .then((response) => {
      store.getUserInfo();
    })
    .catch((err) => console.log(err.response.data));
  }
};

const changePassword = () => {
  if (window.confirm("비밀번호를 변경하시겠습니까?") === true) {
    axios({
      method: "PUT",
      url: `${store.API_URL}/accounts/${store.userInfo.pk}/user/changePasswoed/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: {
        password: password.value,
        password1: password1.value,
        password2: password2.value,
      },
    })
      .then((response) => {
        password.value = null;
        password1.value = null;
        password2.value = null;
        alert("비밀번호가 변경되었습니다!");
      })
      .catch((err) => alert(err.response.data["msg"]));
  }
};

const selectGenre = (event) => {
  const target = event.target;
  const genre = Number(target.value);
  const index = like_genres.indexOf(genre);
  if (index == -1) {
    target.style.backgroundColor = "rgb(119, 118, 118)";
    like_genres.push(genre);
  } else {
    target.style.backgroundColor = "white";
    like_genres.splice(index, 1);
  }
};

const getGenres = () => {
  axios({
    method: "GET",
    url: `${store.API_URL}/movies/genres/`,
  })
    .then((response) => {
      genres.value = response.data;
    })
    .catch((err) => console.log(err));
};

const changePhoto = (event) => {
  const files = event.target?.files;
  if (files.length > 0) {
    const file = files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      previewPhoto.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

onMounted(() => {
  getGenres();
  console.log(like_genres)
});
</script>



<style scoped>
input:disabled {
  background-color: rgb(148, 146, 146);
}
button:disabled{
  background: rgb(148, 146, 146);
}
#main{
  margin-top: 80px;
  max-width: 600px;
  width: 90%;
}
#main-form1 {
  border: 1px solid rgb(206, 206, 206);
  border-radius: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.1);
}
#main-form2{
  border: 1px solid rgb(206, 206, 206);
  border-radius: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.1);
}
#main-form1 > * {
  padding: 10px;
}
#main-form2 > * {
  padding: 10px;
}
.input-group{
  max-width: 400px;
}
#genre{
  display: flex; 
  flex-direction: column;
  align-items: center;
}
#genre>h4{
  margin: 0px;
}
#genre-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  border: 1px solid  rgb(119, 118, 118);;
  border-radius: 20px;
  margin: 15px;
  margin-top: 3px;
  padding: 20px;
}
#genre-btns > div>button {
  background-color: white;
  border: 1px solid rgb(119, 118, 118);
  padding: 5px 15px;
  border-radius: 20px;
}
.photo{
  margin-top: 15px;
}
.photo > label > div {
  text-align: center;
}
.photo > label > img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
}
</style>
