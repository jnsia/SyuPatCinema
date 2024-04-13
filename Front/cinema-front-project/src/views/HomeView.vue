<template>
  <div v-if="store.moviesURLs.length>0" id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel" >
    <div class="carousel-inner">
      <div class="carousel-item active" data-bs-interval="2000">
        <img id="movie_poster1" :src="store.moviesURLs[0].movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="store.moviesURLs[0].movieVideo" :data-title="store.moviesURLs[0].movieTitle" @click="clickScreen('#movie_poster1')" class="d-block" style="margin: auto;" alt=""/>
      </div>
      <!-- <div class="carousel-item" data-bs-interval="2000" v-for="url in store.moviesURLs.slice(1,store.moviesURLs.length)" :key="url.movieId" >
        <img :id="url.movieTitle" :src="url.movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="url.movieVideo" :data-title="url.movieTitle" @click="clickScreen_(url.movieTitle)"  class="d-block" style="margin: auto;"  alt=""/>
      </div> -->
      <div class="carousel-item " data-bs-interval="2000">
        <img id="movie_poster2" :src="store.moviesURLs[1].movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="store.moviesURLs[1].movieVideo" :data-title="store.moviesURLs[1].movieTitle" @click="clickScreen('#movie_poster2')" class="d-block" style="margin: auto;" alt=""/>
      </div>
      <div class="carousel-item " data-bs-interval="2000">
        <img id="movie_poster3" :src="store.moviesURLs[2].movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="store.moviesURLs[2].movieVideo" :data-title="store.moviesURLs[2].movieTitle" @click="clickScreen('#movie_poster3')" class="d-block" style="margin: auto;" alt=""/>
      </div>
      <div class="carousel-item " data-bs-interval="2000">
        <img id="movie_poster4" :src="store.moviesURLs[3].movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="store.moviesURLs[3].movieVideo" :data-title="store.moviesURLs[3].movieTitle" @click="clickScreen('#movie_poster4')" class="d-block" style="margin: auto;" alt=""/>
      </div>
      <div class="carousel-item " data-bs-interval="2000">
        <img id="movie_poster5" :src="store.moviesURLs[4].movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="store.moviesURLs[4].movieVideo" :data-title="store.moviesURLs[4].movieTitle" @click="clickScreen('#movie_poster5')" class="d-block" style="margin: auto;" alt=""/>
      </div>
      <div class="carousel-item " data-bs-interval="2000">
        <img id="movie_poster6" :src="store.moviesURLs[5].movieThumbnail" role="button" data-bs-toggle="modal" data-bs-target="#get_modal_video" :data-video="store.moviesURLs[5].movieVideo" :data-title="store.moviesURLs[5].movieTitle" @click="clickScreen('#movie_poster6')" class="d-block" style="margin: auto;" alt=""/>
      </div>
    </div>

    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev" >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>

    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next" >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
  
  <div id="movie-line">
    <div id="movie-moreView">
      <h4>전체 인기 순위</h4>
      <span id="movie-moreViewBtn" role="button" @click="goMovies('total')">더보기 ></span>
    </div>
    <div id="movie-card">
      <MovieCard
        v-for="movie in store.popular_movies"
        :key="movie.pk"
        :movie="movie"
      />
    </div>
    <div class="end-line"></div>
  </div>

  <template v-if="store.userInfo!==null && store.userInfo.like_genres.length > 0">
    <div id="movie-line" v-for="movies in genreMovies">
      <div id="movie-moreView">
        <h4>{{ movies[0] }}</h4>
        <span id="movie-moreViewBtn" role="button" @click="goMovies(movies[0])">더보기 ></span>
      </div>
      <div id="movie-card" >
        <MovieCard v-for="movie in movies[1]" :key="movie.id" :movie="movie" />
      </div>
      <div class="end-line"></div>
    </div>
  </template>

  <template v-else>
    <div id="movie-line" v-for="movies in defaultGenresMovies">
      <div id="movie-moreView">
        <h4>{{ movies[0] }}</h4>
        <span id="movie-moreViewBtn" role="button" @click="goMovies(movies[0])">더보기 ></span>
      </div>
      <div id="movie-card">
        <MovieCard v-for="movie in movies[1]" :key="movie.id" :movie="movie" />
      </div>
      <div class="end-line"></div>
    </div>
  </template>


  <div class="modal fade" id="get_modal_video" data-bs-keyboard="true" tabindex="-1" aria-hidden="false">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content" style="color: black;">
        <div class="modal-header">
          <div></div>
          <h4 id="modal-header-title"></h4>
          <button type="button" class="btn-close" data-bs-dismiss="modal" style="margin: 0px;"></button>
        </div>
        <div class="modal-body">
          <iframe id="video_url" src="" frameborder="0"></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUpdated, watch } from "vue";
import { useCounterStore } from "../stores/counter";
import MovieCard from "../components/MovieCard.vue";
import axios from "axios";
import { useRouter } from "vue-router";
const router = useRouter()
const store = useCounterStore();
const genreMovies = ref([]);
const defaultGenres = ref([]);
const defaultGenresMovies = ref([]);

const clickScreen = function(idName){
  console.log(document.querySelector(idName).dataset.video)
  console.log(document.querySelector(idName).dataset.title)
  const iframe_element = document.querySelector('#video_url')
  iframe_element.setAttribute('src', `https://www.youtube.com/embed/${document.querySelector(idName).dataset.video}`)
  const title_element = document.querySelector('#modal-header-title')
  title_element.textContent = document.querySelector(idName).dataset.title
}

const clickScreen_ = function(movieTitle){
  console.log(document.querySelector(`#${movieTitle}`).dataset.video)
  console.log(document.querySelector(`#${movieTitle}`).dataset.title)
  const iframe_element = document.querySelector('#video_url')
  iframe_element.setAttribute('src', `https://www.youtube.com/embed/${document.querySelector(`#${movieTitle}`).dataset.video}`)
  const title_element = document.querySelector('#modal-header-title')
  title_element.textContent = document.querySelector(`#${movieTitle}`).dataset.title
}

const goMovies = function(genre){
  router.push({
    name:"movies",
    query:{genreName:genre},
  })
}

onMounted(() => {
  store.getMovies();
  console.log(store.moviesURLs)
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
* {
  margin: 0;
  padding: 0;
}
.end-line {
  border: 0.5px solid gray;
}
#carouselExampleAutoplaying {
  width: 100%;
}
.carousel-control-prev,
.carousel-control-next {
  margin: 40px 0;
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
#movie-moreView{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 0 5px;
}
#movie-moreViewBtn{
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
  -ms-overflow-style: none; /* 인터넷 익스플로러 */
  scrollbar-width: none; /* 파이어폭스 */
}
/* ( 크롬, 사파리, 오페라, 엣지 ) 동작 */
*::-webkit-scrollbar {
  display: none;
}
.carousel-item > img{
  width: 60vw;
  object-fit: cover;
}
@media (min-width: 758px) {
  .carousel-item > img {
    width: 70vw;
  height: 40vw;
  }
}
@media (max-width: 758px) {
  #carouselExampleAutoplaying {
    margin-top: 50px;
  }
  .carousel-item > img {
    width: 100vw;
  height: 50vw;
  }
  .carousel-control-prev,
  .carousel-control-next {
    display: none;
  }
}
.modal-header{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.modal-body{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 500px;
  margin: auto;
}

#video_url {
  width: 100vw;
  height: 100%;
}

</style>
