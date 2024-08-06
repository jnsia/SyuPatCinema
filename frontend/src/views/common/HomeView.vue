<template>
  <Craousel />

  <div id="movie-line">
    <div id="movie-moreView">
      <h4>전체 인기 순위</h4>
      <span id="movie-moreViewBtn" role="button" @click="goMovies('total')"
        >더보기 ></span
      >
    </div>
    <div id="movie-card">
      <MovieCard
        v-for="movie in popularMovies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
    <div class="end-line"></div>
  </div>

  <div id="movie-line" v-for="(movies, genre) in genreMovies" :key="genre">
    <div id="movie-moreView">
      <h4>{{ genre }}</h4>
      <span id="movie-moreViewBtn" role="button" @click="goMovies(genre)"
        >더보기 ></span
      >
    </div>
    <div id="movie-card">
      <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
    </div>
    <div class="end-line"></div>
  </div>

  <div
    class="modal fade"
    id="get_modal_video"
    data-bs-keyboard="true"
    tabindex="-1"
    aria-hidden="false"
  >
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content" style="color: black">
        <div class="modal-header">
          <div></div>
          <h4 id="modal-header-title"></h4>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            style="margin: 0px"
          ></button>
        </div>
        <div class="modal-body">
          <iframe id="video_url" src="" frameborder="0"></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Craousel from "@/components/common/Craousel.vue";
import MovieCard from "@/components/movies/MovieCard.vue";

import { ref, onMounted, onUpdated, watch } from "vue";
import { useAccountsStore } from "@/stores/accounts";
import { useRouter } from "vue-router";
import moviesAPI from "@/apis/moviesAPI.js";

const router = useRouter();
const store = useAccountsStore();

const movies = ref([]);
const popularMovies = ref([]);
const genreMovies = ref({});

const goMovies = function (genre) {
  router.push({
    name: "movies",
    query: { genreName: genre },
  });
};

const getMovies = async () => {
  await moviesAPI.getMovies(
    (response) => {
      movies.value = response.data;
      movies.value.sort(
        (movie1, movie2) => movie2["popularity"] - movie1["popularity"]
      );
    },
    (err) => console.log(err)
  );
};

onMounted(async () => {
  await store.getUserInfo();
  await getMovies();

  popularMovies.value = movies.value.splice(0, 8);

  store.likeGenres.forEach((genre) => {
    genreMovies.value[genre] = [];
  });

  movies.value.forEach((movie) => {
    movie.genres.forEach((genre) => {
      if (store.likeGenres.includes(genre.name)) {
        genreMovies.value[genre.name].push(movie);
      }
    });
  });

  console.log(genreMovies.value);
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

.modal-body {
  width: 100%;
  height: 320px;
}

#video_url {
  width: 100%;
  height: 100%;
}
</style>
