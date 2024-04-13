<template>
  <div id="SignupBox_">
    <h1 style="text-align: center; margin-bottom: 20px;">Signup</h1>
    <form @submit.prevent="createUser" enctype="multipart/form-data" >
      <div class="photo" style="margin: 10px auto;">
        <label for="IMG">
          <img v-if="previewPhoto" :src="previewPhoto" class="photo-img"/>
          <img v-else src="/src/assets/defaultProfile.png" class="photo-img"/>
          <div style="text-align: center; margin-top: 10px;">파일을 선택해주세요!</div>
        </label>
        <input id="IMG" type="file" ref="photo" hidden @change="changePhoto" />
      </div>
      
      <div class="SignupBox">
        <div class="col">
          <input type="text" class="form-control" :class="{'is-valid':check_idd, 'is-invalid':!check_idd}" placeholder="아이디" v-model="id" @input="check_id">
          <p v-if="check_idd === false" class="invalid-feedback"> 아이디: 영문자 또는 숫자 6~20자 입력해주세요(영문으로 시작해주세요) </p>
        </div>
        
        <div class="col">
          <input type="password" class="form-control" :class="{'is-valid':check_passs, 'is-invalid':!check_passs}" placeholder="비밀번호" v-model="password1" @input="check_pass">
          <p v-if="check_passs === false" class="invalid-feedback"> 비밀번호: 8~16자 영문, 숫자 조합으로 입력해주세요 </p>
        </div>

        <div class="col">
          <input type="password" class="form-control" :class="{'is-valid':check_pass22, 'is-invalid':!check_pass22}" placeholder="비밀번호 확인" v-model="password2" @input="check_pass2">
          <p v-if="check_pass22 === false" class="invalid-feedback"> 비밀번호가 일치하지 않습니다. </p>
        </div>
      </div>

      <div class="SignupBox">
        <div class="col">
          <input type="text" class="form-control" :class="{'is-valid':name!=='', 'is-invalid':name===''}" placeholder="이름" v-model="name">
        </div>

        <div class="col">
          <input type="text" class="form-control" :class="{'is-valid':check_birthh, 'is-invalid':!check_birthh}" placeholder="생년월일 8자리" v-model="birth" @input="check_birth">
          <p v-if="check_birthh === false" class="invalid-feedback"> YYYY-MM-DD 형식에 맞게 생년월일을 입력해주세요 </p>
        </div>

        <div class="col">
          <input type="text" class="form-control" :class="{'is-valid':check_phonee, 'is-invalid':!check_phonee}" placeholder="전화번호" v-model="phone" @input="check_phone">
          <p v-if="check_phonee === false" class="invalid-feedback"> 000-0000-0000 형식에 맞게 전화번호를 입력해주세요 </p>
        </div>
      </div>

      <div class="SignupBox">
        <h4 style="text-align: center; margin-top: 20px;">선호하는 장르</h4>
        <div id="genre-btns">
          <div v-for="genre in genres" :value="genre.id" >
            <button v-if="genre.name!=='다큐멘터리' && genre.name!=='서부' && genre.name!=='TV 영화'" @click.prevent="selectGenre" :value="genre.id">{{ genre.name }}</button>
          </div>
        </div>
        <p style="color: gray; font-size: small; margin-left: 10px;">*선택 사항입니다.</p>
      </div>

      <div id="SignupBox-button" style="padding-top: 0px;">
        <button class="btn btn-outline-light">회원가입</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "../stores/counter";
import { useRouter } from "vue-router";
import axios from "axios";
const router = useRouter();
const store = useCounterStore();
const genres = ref([]);

const photo = ref(null);
const previewPhoto = ref(null);
const id = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const name = ref(null);
const birth = ref(null);
const phone = ref(null);
const like_genres = [];

const check_idd = ref(true);
const check_passs = ref(true);
const check_pass22 = ref(true);
const check_birthh = ref(true);
const check_phonee = ref(true);

const check_id = () => {
  const trueForm = /^[a-z]+[a-z0-9]{5,19}$/g;
  check_idd.value = trueForm.test(id.value);
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

const createUser = function () {
  const User = {
    username: id.value,
    password1: password1.value,
    password2: password2.value,
    name: name.value,
    birth: birth.value,
    phoneNumber: phone.value,
    like_genres: like_genres,
  };
  if (photo.value.files.length > 0) {
    User["photo"] = photo.value.files[0];
  }
  store.Signup(User);
};

const selectGenre = (event) => {
  const target = event.target;
  const genre = Number(target.value);
  const index = like_genres.indexOf(genre);

  if (index == -1) {
    target.style.backgroundColor = "gray";
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
});
</script>

<style scoped>
#SignupBox_{
  margin-top: 80px;
  margin-bottom: 50px;
}
#SignupBox_ > form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 30px;
  box-shadow: 0px 0px 5px 0px rgb(131, 131, 131);
  background-color: rgba(0, 0, 0, 0.1);
  width: 80vw;
  max-width: 480px;
  padding: 40px 0px;
}
.SignupBox > *{
  margin: 20px;
}
.SignupBox{
  width: 100%;
  padding: 0 20px;
}
.photo-img{
  width: 100%;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}
#genre-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  border-top: 1px solid white;
  padding-top: 20px;
  margin: 10px;
}
#genre-btns >div> button {
  background-color: white;
  border: 1px solid rgb(119, 118, 118);
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 14px;
}
#SignupBox-button>button{
  width: 150px;
  height: 50px;
}
</style>
