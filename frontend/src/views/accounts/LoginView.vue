<template>
  <div id="login-view">
    <h1>Login</h1>
    <div class="LoginBox">
      <div class="col">
        <input type="text" class="form-control" :class="{'is-valid':check_idd, 'is-invalid':!check_idd}" placeholder="아이디" v-model="id" @input="check_id">
        <p v-if="check_idd === false" class="invalid-feedback"> 아이디: 영문자 또는 숫자 6~20자 입력해주세요(영문으로 시작해주세요) </p>
      </div>
      <div class="col">
        <input type="password" class="form-control" :class="{'is-valid':check_passs, 'is-invalid':!check_passs}" placeholder="비밀번호" v-model="password" @input="check_pass">
        <p v-if="check_passs === false" class="invalid-feedback"> 비밀번호: 8~16자 영문, 숫자 조합으로 입력해주세요 </p>
      </div>
      <button class="btn btn-outline-light" @click.prevent="login">로그인</button>
      <p class="goSignup" @click="router.push({name: 'signup'})">회원가입 페이지로 이동하기 ></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountsStore } from "@/stores/accounts";
import { useRouter } from "vue-router";

const store = useAccountsStore();
const router = useRouter();

const login = function () {
  const user = {
    username: id.value,
    password: password.value,
  };

  store.login(user);
};

const id = ref(null);
const password = ref(null);

const check_idd = ref(true);
const check_passs = ref(true);

const check_id = () => {
  const trueForm = /^[a-z]+[a-z0-9]{5,19}$/g;
  check_idd.value = trueForm.test(id.value);
};

const check_pass = () => {
  const trueForm = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{8,16}$/;
  check_passs.value = trueForm.test(password.value);
};
</script>

<style scoped>
#login-view{
  margin-top: 80px;
  margin-bottom: 40px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 480px;
  width: 80vw;
}
.LoginBox {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 30px;
  box-shadow: 0px 0px 5px 0px rgb(131, 131, 131);
  background-color: rgba(0, 0, 0, 0.1);
  padding: 20px 40px;
  width: 100%;
  margin-top: 20px;
}

.LoginBox > * {
  width: 100%;
  margin: 10px;
}

.LoginBox > button{
  width: 150px;
  height: 50px;
}

.goSignup {
  text-align: center;
  color: gray;
  cursor: pointer;
}
</style>