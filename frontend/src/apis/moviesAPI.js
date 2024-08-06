import axiosInstance from "@/utils/axios-instance";

const moviesAPI = {
  getGenres: async (success, fail) => {
    await axiosInstance.get("/movies/genres").then(success).catch(fail);
  },
  getMovies: async (success, fail) => {
    await axiosInstance.get("/movies").then(success).catch(fail);
  },
};

export default moviesAPI;
