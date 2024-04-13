<template>
  <div>
    <form @submit.prevent="createReview" id="create-review">
      <div class="score-box">
        <label for="score">평점</label>
        <select id="score" class="form-select" v-model="score">
          <option>0.5</option>
          <option>1</option>
          <option>1.5</option>
          <option>2</option>
          <option>2.5</option>
          <option>3</option>
          <option>3.5</option>
          <option>4</option>
          <option>4.5</option>
          <option>5</option>
        </select>
      </div>
      <div class="form-floating">
        <textarea
          class="form-control"
          placeholder="평론를 작성해주세요!"
          id="floatingTextarea"
          v-model="content"
          style="resize: none;">
        </textarea>
        <label for="floatingTextarea">평론</label>
      </div>
      <button class="btn btn-success btn-sm">관람평 작성</button>
    </form>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "../stores/counter";

const router = useRouter();
const props = defineProps({
  moviePk: Number,
});

const store = useCounterStore();

const score = ref(0);
const content = ref(null);

const createReview = function () {
  if (store.token===null){
    alert('로그인이 필요합니다.')
    return false
  }
  if (score.value === 0) {
    alert('해당 영화의 평점을 선택해주세요!')
    return false
  }

  if (content.value === null) {
    alert('평론을 남겨주세요!')
    return false
  }

  axios({
    method: "POST",
    url: `${store.API_URL}/movies/${props.moviePk}/reviews/create/`,
    data: {
      score: score.value,
      content: content.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      console.log("create review 성공");
      router.go();
    })
    .catch((err) => console.log(err.response.data));
};
</script>

<style scoped>
#create-review {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-around;
  gap: 20px;

  border: 1px solid rgb(255, 191, 191);
  border-radius: 10px;
  padding: 20px;
}

.score-box {
  display: flex;
  align-items: center;
  height: max-content;
}

.score-box > label {
  width: 100%;
  margin-right: 5px;
}

.form-floating {
  width: 40%;
}

.scroll {
  -ms-overflow-style: none; /* 인터넷 익스플로러 */
  scrollbar-width: none; /* 파이어폭스 */
}

/* ( 크롬, 사파리, 오페라, 엣지 ) 동작 */
*::-webkit-scrollbar {
  display: none;
}

.content-box {
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>
