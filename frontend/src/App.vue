<template>
  <div id="all">
    <Nav />
    
    <div id="container">
      <RouterView />
    </div>

    <footer>
      <span>© 2023 Cheosbung Patbung Shubung CINEMA</span>
    </footer>
  </div>
</template>

<script setup>
import Nav from "./components/common/Nav.vue"
import { RouterView } from "vue-router";
</script>

<style>
@import url('./App.css');

#all{
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #222222;
}

#container{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
</style>
