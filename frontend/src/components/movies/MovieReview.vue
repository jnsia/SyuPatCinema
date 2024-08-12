<template>
  <div id="review">
    <div id="review-box">
      <div id="review-box-writer" @click="goProfile">
        <img :src="store.API_URL + (props.review.user.photo || '/media/profile/defaultProfile.jpeg')" alt="writer-img" />
        <p>{{ props.review.user.name }}</p>
      </div>
      <div v-if="!is_update" id="review-box-content">
        <div id="review-box-content-score">
          <span v-for="star in starIcon">
            <span v-if="star === 2" ><font-awesome-icon :icon="['fas', 'star']" /></span>
            <span v-else-if="star === 1" ><font-awesome-icon :icon="['fas', 'star-half-stroke']" /></span>
            <span v-else><font-awesome-icon :icon="['far', 'star']" /></span>
          </span>
        </div>
        <div class="review-content">
          <p style="font-size: 14px;">{{ props.review.content }}</p>
          <button
            v-if="store.token && store.userId === props.review.user.id"
            class="btn btn-outline-secondary btn-sm"
            style="padding: 0px 4px;"
            @click="is_update = !is_update">
            <font-awesome-icon :icon="['fa-solid', 'fa-pencil']" />
            <span> 수정</span>
          </button>
          <button
            v-if="store.token && store.userId === props.review.user.id"
            class="btn btn-outline-secondary btn-sm"
            style="padding: 0px 4px;"
            @click="deleteReview">
            <font-awesome-icon :icon="['fa-solid', 'fa-trash']" />
            <span> 삭제</span>
          </button>
        </div>
        <span style="font-size: 12px; color: gray;">{{ ctl[0] + '년 ' + ctl[1] + '월 ' + ctl[2] + '일' }}</span>
      </div>

      <div v-else id="review-box-content">
        <div class="score-box">
          <label for="score">평점</label>
          <select id="score" class="form-select" v-model="updateScore">
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
        <div class="review-content">
          <div class="form-floating">
            <textarea
              class="form-control"
              placeholder="평론를 작성해주세요!"
              id="floatingTextarea"
              v-model="updateContent"
              style="resize: none;">
            </textarea>
            <label for="floatingTextarea">평론</label>
          </div>
          <button
            class="btn btn-outline-secondary btn-sm"
            style="padding: 0px 4px;"
            @click="updateReview">
            <font-awesome-icon :icon="['fa-solid', 'fa-pencil']" />
            <span> 수정</span>
          </button>
        </div>
        <span style="font-size: 12px; color: gray;">{{ ctl[0] + '년 ' + ctl[1] + '월 ' + ctl[2] + '일' }}</span>
      </div>

      <div id="review-like">
        <button class="btn btn-outline-secondary btn-sm" id="like-review" @click="clickLike" >
          <div v-if="store.token!==null && props.review.like_users.includes(store.userId)">
            <font-awesome-icon :icon="['fas', 'heart']"  style="margin-right: 6px; color: red; font-size:small;" />
            <span style="font-size: small;">{{ props.review.like_users.length }}</span>
          </div>
          <div v-else>
            <font-awesome-icon :icon="['far', 'heart']"  style="margin-right: 6px; color: red; font-size:small;" />
            <span style="font-size: small;">{{ props.review.like_users.length }}</span>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAccountsStore } from "@/stores/accounts";
import { useRouter } from "vue-router";
import axios from "axios";
const router = useRouter();
const store = useAccountsStore();

const props = defineProps({
  review: Object,
  likeObj:Object,
});

const likeCount = computed(() => {
  return props.review.like_users.length;
});
const likes = computed(() => {
  return props.review.like_users.includes(store.userInfo.pk);
});

const ctl = props.review.updated_at.slice(0, 10).split('-')

const emit = defineEmits(["likeReview"]);
const clickLike = function () {
  if (store.token===null){
    alert('로그인이 필요합니다.')
  }
  else{
    emit("likeReview", props.review.id);
  }
  
};

const goProfile = function () {
  router.push({ name: "profile", params: { id: props.review.user.id } });
};

const is_update = ref(false)
const updateScore = ref(props.review.score)
const updateContent = ref(props.review.content)

const updateReview = () => {
  if (store.userInfo.pk !== props.review.user.id) {
    return false
  }

  if (updateContent.value === null) {
    alert('수정할 평론을 작성해주세요.')
    return false
  }

  axios({
    method: 'PUT',
    url: `${store.API_URL}/movies/${0}/reviews/${props.review.id}/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      content: updateContent.value,
      score: updateScore.value
    }
  }).then((response) => {
    alert('평론이 수정되었습니다!')
    router.go()
  }).catch((err) => console.log(err.response.data))
}

const deleteReview = () => {
  if (store.userInfo.pk !== props.review.user.id) {
    return false
  }

  axios({
    method: 'DELETE',
    url: `${store.API_URL}/movies/${0}/reviews/${props.review.id}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  }).then((response) => {
    alert('평론이 삭제되었습니다.')
    router.go()
  }).catch((err) => console.log(err.response.data))
}

const starIcon = computed(() => {
  const score = props.review.score;

  // 별 개수와 반별 개수를 정의
  const fullStars = Math.floor(score / 1);
  const halfStars = score % 1 >= 0.5 ? 1 : 0;

  // 총 5개의 별 아이콘 배열 생성
  return [0, 0, 0, 0, 0].map((_, index) => {
    if (index < fullStars) return 2; // 전체 별
    if (index === fullStars && halfStars) return 1; // 반 별
    return 0; // 빈 별
  });
});
</script>

<style scoped>
#review {
  border: 1px solid rgb(232, 232, 232);
  border-radius: 20px;
  padding: 20px 0;
}

#review-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

#review-box-writer {
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding-left: 5%;
  padding-right: 5%;
}

#review-box-writer > img {
  width: 75px;
  height: 75px;
  border-radius: 50%;
}

#review-box-content {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  flex-grow: 1;
  padding-right: 20px;
}

#review-box-content > div:nth-child(2n + 1) {
  margin-bottom: 10px;
}

.review-content {
  margin-bottom: 5px;
  /* display: flex; */
  justify-content: space-between;
  align-items: center;
}

.review-content > button {
  margin-top: 5px;
  margin-right: 10px;
}

#review-box-content-score {
  display: flex;
  flex-direction: row;
  align-items: center;
  color: gold;
}

#review-like {
  padding-left: 5%;
  padding-right: 5%;
}

#like-review {
  display: flex;
  align-items: center;
  border-radius: 30px;
}

#like-review > * {
  padding: 5px;
}

.scroll {
  -ms-overflow-style: none; /* 인터넷 익스플로러 */
  scrollbar-width: none; /* 파이어폭스 */
}

/* ( 크롬, 사파리, 오페라, 엣지 ) 동작 */
*::-webkit-scrollbar {
  display: none;
}
</style>
