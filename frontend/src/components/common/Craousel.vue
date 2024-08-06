<template>
  <div
    v-if="moviesURLs.length > 0"
    id="carouselExampleAutoplaying"
    class="carousel slide"
    data-bs-ride="carousel"
  >
    <div class="carousel-inner">
      <template v-for="index in [0, 1, 2, 3, 4, 5]" :key="index">
        <div
          :class="index == 0 ? 'carousel-item active' : 'carousel-item'"
          data-bs-interval="2000"
        >
          <img
            :id="'movie_poster' + (index + 1)"
            :src="moviesURLs[index].movieThumbnail"
            role="button"
            data-bs-toggle="modal"
            data-bs-target="#get_modal_video"
            :data-video="moviesURLs[index].movieVideo"
            :data-title="moviesURLs[index].movieTitle"
            @click="clickScreen(`#movie_poster${index + 1}`)"
            class="d-block"
            style="margin: auto"
            alt=""
          />
        </div>
      </template>
    </div>

    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#carouselExampleAutoplaying"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>

    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#carouselExampleAutoplaying"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const movieThumbnailUrl = "https://i.ytimg.com/vi";
const moviesURLs = ref([
  {
    movieId: 9,
    movieTitle: "더 넌 2",
    movieVideo: "Aos7vzZukWQ",
    movieThumbnail: `${movieThumbnailUrl}/Aos7vzZukWQ/hqdefault.jpg`,
  },
  {
    movieId: 8,
    movieTitle: "레트리뷰션",
    movieVideo: "L8YiLp6Tq8g",
    movieThumbnail: `${movieThumbnailUrl}/L8YiLp6Tq8g/hqdefault.jpg`,
  },
  {
    movieId: 7,
    movieTitle: "쏘우 X",
    movieVideo: "wWOl_FLsxwM",
    movieThumbnail: `${movieThumbnailUrl}/Z1_ymjF0znY/maxresdefault.jpg`,
  },
  {
    movieId: 3,
    movieTitle: "프레디의 피자가게",
    movieVideo: "kAC7PGfGOfg",
    movieThumbnail: `${movieThumbnailUrl}/RaGNLFbVfLw/maxresdefault.jpg`,
  },
  {
    movieId: 4,
    movieTitle: "익스펜더블 4",
    movieVideo: "uvACT1gFCec",
    movieThumbnail: `${movieThumbnailUrl}/QrxQr5XoJcE/mqdefault.jpg`,
  },
  {
    movieId: 5,
    movieTitle: "더 마블스",
    movieVideo: "o2tUfTejJgA",
    movieThumbnail: `${movieThumbnailUrl}/UxrRXOPDkR4/maxresdefault.jpg`,
  },
]);

const clickScreen = function (idName) {
  const iframe_element = document.querySelector("#video_url");
  iframe_element.setAttribute(
    "src",
    `https://www.youtube.com/embed/${
      document.querySelector(idName).dataset.video
    }`
  );
  const title_element = document.querySelector("#modal-header-title");
  title_element.textContent = document.querySelector(idName).dataset.title;
};
</script>

<style scoped>
#carouselExampleAutoplaying {
  width: 100%;
}

.carousel-control-prev,
.carousel-control-next {
  margin: 40px 0;
}

.carousel-item > img {
  width: 70vw;
  height: 40vw;
  object-fit: cover;
}

@media (max-width: 1080px) {
  .carousel-item > img {
    width: 90vw;
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
</style>
