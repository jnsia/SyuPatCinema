<template>
  <div id="movie-line" v-for="movies in defaultGenresMovies">
    <div id="movie-moreView">
      <h4>{{ movies[0] }}</h4>
      <span id="movie-moreViewBtn" role="button" @click="goMovies(movies[0])"
        >더보기 ></span
      >
    </div>
    <div id="movie-card">
      <MovieCard v-for="movie in movies[1]" :key="movie.id" :movie="movie" />
    </div>
    <div class="end-line"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAccountsStore } from "@/stores/accounts";
import MovieCard from "@/components/MovieCard.vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useAccountsStore();
const genreMovies = ref([]);
const defaultGenres = ref([]);
const defaultGenresMovies = ref([]);

const goMovies = function (genre) {
  router.push({
    name: "movies",
    query: { genreName: genre },
  });
};

onMounted(() => {
  store.getMovies();
  console.log(store.moviesURLs);
  axios({
    method: "GET",
    url: `${store.API_URL}/movies/genres/`,
  })
    .then((response) => {
      for (const genre of response.data) {
        if (
          genre.name === "액션" ||
          genre.name === "로맨스" ||
          genre.name === "공포"
        ) {
          defaultGenres.value.push(genre);
        }
      }
    })
    .then(() => {
      for (const genre of defaultGenres.value) {
        store.getMoviesGenre(genre.id);
        defaultGenresMovies.value.push([genre.name, store.genre_movies]);
      }
    })
    .then(() => {
      if (store.userInfo !== null) {
        for (const genre of store.userInfo.like_genres) {
          store.getMoviesGenre(genre.id);
          genreMovies.value.push([genre.name, store.genre_movies]);
        }
      }
    })
    .catch((err) => console.log(err));
});
</script>

<style scoped>
.end-line {
  border: 0.5px solid gray;
}

@media (max-width: 1200px) {
  #movie-line {
    padding-left: 7.5%;
    padding-right: 7.5%;
  }
}

@media (min-width: 1200px) {
  #movie-line {
    padding-left: 16.75%;
    padding-right: 16.75%;
  }
}

#movie-line {
  padding-top: 20px;
  width: 100%;
}

#movie-moreView {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 0 5px;
}

#movie-moreViewBtn {
  font-size: small;
  opacity: 0.7;
}

#movie-card {
  display: flex;
  overflow-x: scroll;
  overflow-y: hidden;
  white-space: nowrap;
  flex-wrap: nowrap;
  width: 100%;
  gap: 10px;
  margin-bottom: 20px;
}

.scroll {
  /* 인터넷 익스플로러 */
  -ms-overflow-style: none;
  /* 파이어폭스 */
  scrollbar-width: none;
}

/* ( 크롬, 사파리, 오페라, 엣지 ) 동작 */
*::-webkit-scrollbar {
  width: 12px; /* 스크롤바 너비 */
  height: 8px; /* 가로 스크롤바 높이 */
}

*::-webkit-scrollbar-track {
  border-radius: 10px; /* 모서리 반경 */
}

*::-webkit-scrollbar-thumb {
  background-color: gray; /* 핸들 색상 */
  border-radius: 10px; /* 모서리 반경 */
}

*::-webkit-scrollbar-thumb:hover {
  background-color: black; /* 핸들 호버 색상 */
}
</style>
