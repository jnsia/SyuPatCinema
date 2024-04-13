<template>
    <div id="profile" style="height: 100px;">
        <div id="userInfo-img">
            <img :src="store.API_URL+props.user.photo" alt="" >
        </div>
        <div id="userInfo-username">
            <p style="font-weight: bold;">{{ props.user.username }}</p>
            <p style="font-size: small; opacity: 0.7;">{{ props.user.name }}</p>
        </div>
    </div>
</template>

<script setup>
import { useCounterStore } from '../stores/counter';

const store = useCounterStore()
const props = defineProps({
    user:Object
})
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
}
#profile{
    width: 80vw;
    max-width: 320px;
    height: 100px;

    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0px 20px;
    margin: 5px 0px;

    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
}
#userInfo-img > img{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    margin-right: 10px;

    border: 1px solid rgb(216, 216, 216);
}
#userInfo-username{
    display: flex;
    flex-direction: column;
}
</style>
