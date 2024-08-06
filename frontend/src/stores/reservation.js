import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import { useAccountsStore } from "./accounts";
import axios from "axios";

export const reservationStore = defineStore(
  "reservation",
  () => {
    const store = useAccountsStore();
    const dates = [
      { id: 0, d: "11/24" },
      { id: 1, d: "11/25" },
      { id: 2, d: "11/26" },
      { id: 3, d: "11/27" },
      { id: 4, d: "11/28" },
    ];

    const times = [
      { id: 0, t: "9:30" },
      { id: 1, t: "12:00" },
      { id: 2, t: "14:30" },
      { id: 3, t: "17:00" },
      { id: 4, t: "20:30" },
    ];

    return {
      dates,
      times,
    };
  },
  { persist: true }
);
