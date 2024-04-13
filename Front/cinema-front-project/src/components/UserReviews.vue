<template>
  <div id="review">
    <div id="review-box">
      <div id="review-movie">
        <img :src="movie.poster_path" alt="" style="width: 100px;">
        <p>{{ movie.title }}</p>
      </div>
      <div id="review-detail">
        <div id="review-box-content-score">
          <span v-for="star in starIcon">
            <span v-if="star === 2"><font-awesome-icon :icon="['fas', 'star']"/></span>
            <span v-else-if="star === 1"><font-awesome-icon :icon="['fas', 'star-half-stroke']"/></span>
            <span v-else><font-awesome-icon :icon="['far', 'star']" /></span>
          </span>
        </div>
        <p style="font-size: 14px;">{{ props.review.content }}</p>
        <p style="color: gray;">{{ ctl[0] + '년 ' + ctl[1] + '월 ' + ctl[2] + '일' }}</p>
      </div>
    </div>

    <div id="review-like">
      <button class="btn btn-outline-secondary btn-sm" id="like-review" @click="clickLike" >
        <div v-if="store.token!==null && props.review.like_users.includes(store.userInfo.pk)">
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
</template>


<script setup>
import { computed } from 'vue';
import { useCounterStore } from '@/stores/counter.js';

const store = useCounterStore()
const props = defineProps({
  review: Object,
  user: Object,
});

const movie = store.movies.find((m)=>m.id === props.review.movie)
store.movies[props.review.movie]
const ctl = props.review.updated_at.slice(0, 10).split('-')
const starIcon = computed(() => {
  if (props.review.score === 0) {
    return [0, 0, 0, 0, 0];
  } else if (props.review.score === 0.5) {
    return [1, 0, 0, 0, 0];
  } else if (props.review.score === 1) {
    return [2, 0, 0, 0, 0];
  } else if (props.review.score === 1.5) {
    return [2, 1, 0, 0, 0];
  } else if (props.review.score === 2) {
    return [2, 2, 0, 0, 0];
  } else if (props.review.score === 2.5) {
    return [2, 2, 1, 0, 0];
  } else if (props.review.score === 3) {
    return [2, 2, 2, 0, 0];
  } else if (props.review.score === 3.5) {
    return [2, 2, 2, 1, 0];
  } else if (props.review.score === 4) {
    return [2, 2, 2, 2, 0];
  } else if (props.review.score === 4.5) {
    return [2, 2, 2, 1, 0];
  } else if (props.review.score === 5) {
    return [2, 2, 2, 2, 2];
  }
});

const emit = defineEmits(["likeReview"]);
const clickLike = function () {
  console.log(props.review.id, props.review.movie)
  emit("likeReview", props.review.id, props.review.movie);
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  font-size: 10px;
}
#review{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
  
  border: 1px solid rgb(222, 222, 222);
  border-radius: 20px;
}
#review-detail {
  display: flex;
  flex-direction: column;
  justify-content: first baseline;
  flex-grow: 1;
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
#review-box-content-score {
  display: flex;
  flex-direction: row;
  align-items: center;
  color: gold;
}
#review-movie{
  display: flex;
  flex-direction: column;
  align-items: center;
}
#review-detail > div {
  margin-bottom: 10px;
}
#review-detail > p {
  margin-bottom: 5px;
}
#review-box{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
#review-box>*{
  margin: 5px;
}
#review>*{
  margin: 10px 5px;
}
#review-like{
  display: flex;
  align-items: center;
}
</style>
