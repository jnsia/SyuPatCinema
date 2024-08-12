import axiosInstance from "@/utils/axios-instance";
import axiosTokenInstance from "@/utils/axios-token-instance";

const moviesAPI = {
  getGenres: async (success, fail) => {
    await axiosInstance.get("/movies/genres/").then(success).catch(fail);
  },
  getMovies: async (success, fail) => {
    await axiosInstance.get("/movies/").then(success).catch(fail);
  },
  likeReview: async (reviewId, success, fail) => {
    await axiosTokenInstance
      .post(`/movies/review/like/${reviewId}/`)
      .then(success)
      .catch(fail);
  },
};

export default moviesAPI;
