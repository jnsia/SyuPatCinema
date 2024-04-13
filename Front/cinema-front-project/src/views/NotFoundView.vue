<template>
    <div class="not-found-view">
        <h1>잘못된 url 주소로 오셨네요...!</h1>
        <img src="../assets/붕어빵 팥뿡_ 슈붕_.jpeg" alt="당연히 팥붕이지!">
        <div class="btns">
            <button @click="pat" class="btn btn-light btn-lg mx-2">팥붕</button>
            <span>VS</span>
            <button @click="syu" class="btn btn-light btn-lg mx-2">슈붕</button>
        </div>
        <h3>당신의 선택은...?</h3>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()
let cnt_try = 0

const pat = () => {
    alert('역시 붕어빵은 팥붕이죠!')
    router.replace({name: 'home'})
}

const syu = () => {
    const is_syu = confirm('슈붕을 선택하셨나요?')

    if (is_syu) {
        cnt_try++;

        if (cnt_try == 3) {
            alert('장난하세요?')
            return
        }

        if (cnt_try == 6) {
            alert('그만하시죠?')
            return
        }

        if (cnt_try == 9) {
            alert('이런 슈팥')
            router.replace({name: 'home'})
            return
        }

        for (let why = 0; why < cnt_try; why++) {
            alert('다시 생각해보세요.')
        }
    } else {
        alert('그래요. 다시 골라보세요...')
    }
}
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    color: white;
}
.not-found-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 100px;
    min-height: 100vh;
}
.not-found-view > img {
    width: 100%;
    margin: 40px;
}
.btns {
    display: flex;
    align-items: center;
    margin-bottom: 40px;
}
</style>