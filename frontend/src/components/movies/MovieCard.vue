<template>
  <div id="movie" role="button"  @click="goDetail">
    <div id="movie-imgbox">
      <img :src="props.movie.poster_path" alt="img"/>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
  movie: Object,
});

const router = useRouter();
const goDetail = function () {
  router.push({
    name: "detail",
    params: { id: props.movie.id },
  });
};

</script>

<style scoped>
#movie-imgbox > img{
  display: inline-block;
  height: 200px;
  border-radius: 10px;
  object-fit: cover;
  flex: 0 0 auto;
}
</style>
