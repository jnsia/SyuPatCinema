<template>
  <div id="movie-detail-view">
    <div v-if="movie" id="movie-detail-main">
      <div id="movie-detail-title">
        <img :src="movie.poster_path" alt="" style="width: 250px" />
      </div>
      <div id="description">
        <div>
          <h2>
            <font-awesome-icon
              :icon="['fas', 'angle-left']"
              style="margin-right: 10px; cursor: pointer; color: gray;"
              @click="router.go(-1)"
            />
            {{ movie.title }}
          </h2>
          <p>
            <span>{{ genres.join(", ") }} | {{ movie.runtime }} 분</span>
          </p>
        </div>
        <div class="description-02-description">
          <p style="font-size: 13px;">{{ movie.description }}</p>
        </div>
        <div id="description-buttons">
          <button id="kakaotalk-sharing-btn" class="btn btn-warning" @click="kakaoShare">공유</button>
          <button class="btn btn-danger" @click="goTicketing(movie.id)">예매하기</button>
        </div>
        <div id="description-02-score">
          <span>관람객 평점</span>
          <span style="font-weight: bolder; font-size: x-large">
            {{ scoreAvg }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="movie" id="movie-detail-body">
      <ReviewCreate :moviePk="movie.id" />
      <template v-if="movie.review_set.length > 0">
        <MovieReview
          v-for="review in movie.review_set"
          :key="review.id"
          :review="review"
          @like-review="likeReview"
        />
      </template>
      <template v-else>
        <p style="text-align: center; margin: 60px">작성된 관람평이 없습니다.</p>
      </template>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAccountsStore } from "@/stores/accounts";
import ReviewCreate from "@/components/movies/ReviewCreate.vue";
import MovieReview from "@/components/movies/MovieReview.vue";

const store = useAccountsStore();
const route = useRoute();
const router = useRouter();
const movie = ref(null);
const genres = ref([]);
const scoreAvg = ref(0);
const likeObj = ref(null)

// 영화 정보 불러오기
const getMovie = () => {
  axios({
    method: "GET",
    url: `${store.API_URL}/movies/${route.params.id}/`,
  })
    .then((response) => {
      movie.value = response.data;
      getGenres();
      // 관람객 평점
      if (movie.value.review_set.length > 0) {
        let totalScore = 0;
        for (const review of movie.value.review_set) {
          totalScore += review.score;
        }
        scoreAvg.value = (totalScore / movie.value.review_set.length).toFixed(
          2
        );
      }
    })
    .catch((err) => console.log(err));
};

// 영화 장르 불러오기
const getGenres = () => {
  axios({
    method: "GET",
    url: `${store.API_URL}/movies/genres/`,
  })
    .then((response) => {
      for (const genre of response.data) {
        if (movie.value.genres.includes(genre.id) === true) {
          genres.value.push(genre.name);
        }
      }
    })
    .catch((err) => console.log(err));
};

let shareCnt = 1;

const kakaoShare = () => {
  if (!window.Kakao.isInitialized()) {
    Kakao.init("bc54b4605a72209f83571de67f59c3f9"); // 사용하려는 앱의 JavaScript 키 입력
  }

  Kakao.Share.createDefaultButton({
    container: "#kakaotalk-sharing-btn",
    objectType: "feed",
    content: {
      title: `${movie.value.title}`,
      description: `${movie.value.description}`,
      imageUrl: `${movie.value.backdrop_path}`,
      link: {
        // [내 애플리케이션] > [플랫폼] 에서 등록한 사이트 도메인과 일치해야 함
        mobileWebUrl: `${store.SITE_URL}`,
        webUrl: `${store.SITE_URL}`,
      },
    },
    social: {
      // likeCount: scoreAvg.value || 5,
      // commentCount: movie.value.review_set.length,
      commentCount: movie.value.review_set.length || 1,
      sharedCount: shareCnt++,
    },
    buttons: [
      {
        title: "웹으로 보기",
        link: {
          mobileWebUrl: `${store.SITE_URL}/detail/${movie.id}`,
          webUrl: `${store.SITE_URL}/detail/${movie.id}`,
        },
      },
    ],
    installTalk: true,
  });
};

// 페이지 mounted 될때 영화정보 불러오는 함수 호출
onMounted(() => {
  getMovie();
});


const likeReview = function (reviewId) {
  axios({
    method: "POST",
    url: `${store.API_URL}/movies/${movie.value.id}/reviews/${reviewId}/likes/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      // likeObj.value = response.data
      router.go()
    })
    .catch((err) => console.log(err));
};

const goTicketing = function(movieId,movieTitle, movieSrc){
  if(store.token===null){
    alert('로그인이 필요합니다.')
    router.getRoutes()
    return false
  }
  router.push({
    name:'ticketing',
    query:{
      movieId,
      movieTitle,
      movieSrc,
    }})
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

#movie-detail-view {
  padding: 0 15%;
  width: 100%;
  min-height: 100vh;
}

@media (max-width: 1200px) {
  #movie-detail-view {
    padding-left: 7.5%;
    padding-right: 7.5%;
  }
}

@media (min-width: 1200px) {
  #movie-detail-view {
    padding-left: 25%;
    padding-right: 25%;
  }
}

@media (max-width: 600px) {
  #movie-detail-main {
      flex-direction: column;
  }

  #movie-detail-view {
    padding: 0 5%;
  }
}

#movie-detail-main {
  display: flex;
  margin-top: 50px;
  align-items: center;
  padding: 1%;
}

#description-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

#movie-detail-main > * {
  margin: 0.5%;
  padding: 10px;
}

#movie-detail-body{
  display: flex;
  flex-direction: column;
  gap: 20px;
}

#description {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

#description > div > h2 {
  font-weight: bold;
  margin-bottom: 20px;
  font-size: 28px;
}

#description-02-button > button {
  border-radius: 40px;
}

#description-02-score {
  border: 1px solid rgb(255, 185, 185);
  border-radius: 10px;
  padding: 10px;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
