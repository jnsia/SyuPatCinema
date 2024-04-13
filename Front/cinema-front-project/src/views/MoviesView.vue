<template>
    <div id="box">
        <div class="genre-name">
            <h1 v-if="genreName==='total'" id="movie-genre" style="text-align: center;"><font-awesome-icon
              :icon="['fas', 'angle-left']"
              style="margin-right: 10px; cursor: pointer;"
              @click="router.push({name: 'home'})"
            />영화 전체 보기</h1>
            <h1 v-else id="movie-genre" style="text-align: center;"><font-awesome-icon
              :icon="['fas', 'angle-left']"
              style="margin-right: 10px; cursor: pointer;"
              @click="router.push({name: 'home'})"
            />{{ genreName }}</h1>
        </div>
        <div id="movie-box">
            <MovieCard v-for="movie in movies_genre" :key="movie.id" :movie="movie"/>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref,onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '../stores/counter';
import MovieCard from "../components/MovieCard.vue";

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const genreName = route.query.genreName
const genrePk = ref(null)
const movies_genre = ref([])

onMounted(()=>{
    getGenres()
})
const getGenres = function(){
    axios({
        method: "GET",
        url: `${store.API_URL}/movies/genres/`,
    })
        .then((response) => {
            if(genreName!=='total'){
                for (const genre of response.data) {
                    if(genre.name===genreName){
                        genrePk.value = genre.id
                        break
                    }
                }    
            }
            console.log(genreName, genrePk.value)
            getMovies()
        })
        .catch((err)=>console.log(err))
}

const getMovies = function(){
    axios({
        method: "GET",
        url: `${store.API_URL}/movies/`,
    })
        .then((response) => {
            console.log(response.data)
            if(genreName==='total'){
                movies_genre.value = response.data
            }
            else{
                for (const movie of response.data) {
                    if(movie.genres.includes(genrePk.value)===true){
                        movies_genre.value.push(movie)
                    }
                }
                console.log(movies_genre.value)
            }
        })
        .catch((err)=>console.log(err))
}

</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
@media (min-width: 758px) {
    #box{
        margin: 0 10%;
    }
}
@media (max-width: 758px) {
}
#box{
    min-height: 100vh;
    margin-top: 80px;
}
.genre-name > h1 {
    font-size: 24px;
    margin-bottom: 20px;
    text-align: left;
}
#movie-box{
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}
#movie-box > div {
    margin: 5px;
}
</style>