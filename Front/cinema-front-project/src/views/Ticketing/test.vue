<template>
  <div id="app">
    <div class="movieContainer">
      <label for="movie"> Pick a Movie : </label>
      <select v-model="movie">
        <option disabled value="0">Please select one</option>
        <option class="price" value="10">Avengers:Endgame ($10)</option>
        <option class="price" value="12">Joker ($12)</option>
        <option class="price" value="8">Toy Story 4 ($8)</option>
        <option class="price" value="9">The Lion King ($9)</option>
      </select>
    </div>

    <ul class="showcase">
      <li>
        <div class="availableSeat"></div>
        <small class="small">Available Seat</small>
      </li>
      <li>
        <div class="selectedSeatIcon"></div>
        <small class="small">Selected Seat</small>
      </li>
      <li>
        <div class="occupiedSeat"></div>
        <small class="small">Occupied Seat</small>
      </li>
    </ul>

    <div @click="countSeatPrice" class="seatContainer">
      <div class="screen"></div>
      <div v-for="seat in seats" class="row">
        <span v-for="s in seat" :class="s == 0 ? 'seat' : 'occupiedSeat'" ></span>
      </div>
    </div>

    <p class="text">
      You have selected <span id="count">{{ numberPeople }}</span> seats for a
      price of $ <span id="costs">{{ numberPeople * movie }}</span>
    </p>
  </div>
</template>

<script setup>
const { createApp, ref } = "vue";

const numberPeople = ref(0);
const movie = ref(0);
const seats = ref([
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
]);

function countSeatPrice(event) {
  if (movie.value == "") {
    alert("choose the movie");
    return;
  }

  if (event.target.className === "seat") {
    event.target.className = "selectedSeat";
  } else if (event.target.className === "selectedSeat") {
    event.target.className = "seat";
  }

  const selectedSeatCount = document.querySelectorAll(".selectedSeat").length;

  numberPeople.value = selectedSeatCount;
}
</script>

<style>
#app {
    font-family: "Lato", sans-serif;
  background-color: #242333;
  color: #fff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 800px;
}

.movieContainer {
  margin: 20px 0px;
}

.showcase {
  background-color: #777;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  display: flex;
  justify-content: center;
  margin: 16px 0;
  padding: 5px 10px;
}

.movieContainer select {
  margin: 10px;
  padding: 5px 15px 5px 15px;
  border-radius: 7px;
  appearance: none;
  border: 0;
}

.movieContainer select option {
  text-align: left;
}

li {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 10px;
}

.small {
  color: #777;
  margin-left: 2px;
}

.showcase .seat:hover {
  cursor: default;
  scale: 1;
}

.showcase .selectedSeat:hover {
  cursor: default;
  scale: 1;
}

.seatContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.screen {
  background-color: #fff;
  margin: 15px 0px;
  padding: 10px;
  width: 280px;
  height: 160px;
  transform: rotateX(-45deg);
  box-shadow: 0 3px 10px rgb(255 255 255 / 70%);
}

.seat {
  background-color: #444451;
  width: 30px;
  height: 24px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: pointer;
}

.availableSeat {
  background-color: #444451;
  width: 30px;
  height: 24px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: default;
}

.selectedSeatIcon {
  background-color: #ff3346;
  width: 30px;
  height: 24px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: default;
}

.seat:hover {
  scale: 1.2;
}

.selectedSeat:hover {
  scale: 1.2;
}

.seat:nth-of-type(2) {
  margin-right: 18px;
}

.seat:nth-of-type(7) {
  margin-left: 18px;
}

.selectedSeat:nth-of-type(2) {
  margin-right: 18px;
}

.selectedSeat:nth-of-type(7) {
  margin-left: 18px;
}

.occupiedSeat:nth-of-type(2) {
  margin-right: 18px;
}
.occupiedSeat:nth-of-type(7) {
  margin-left: 18px;
}

.selectedSeat {
  background-color: #ff3346;
  width: 30px;
  height: 24px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  cursor: pointer;
}

.occupiedSeat {
  background-color: #fff;
  width: 30px;
  height: 24px;
  margin: 6px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.row {
  display: flex;
}

.text {
  margin-top: 30px;
  padding: 20px;
}

#count {
  color: #6feaf6;
}

#costs {
  color: #6feaf6;
}
</style>