import axios from "axios";

const YouTube_API_KEY = import.meta.YouTube_API_KEY;

const youtubeAxiosInstance = axios.create({
  baseURL: "https://www.googleapis.com/youtube/v3/search", // 기본 URL
  timeout: 10000, // 요청 타임아웃 (밀리초)
  headers: {
    "Content-Type": "application/json", // 기본 헤더
  },
});

const youtubeAPI = ({
    getVideos: async (params, success, fail) =>
        await youtubeAxiosInstance
          .get("", {
            params: {
              key: YouTube_API_KEY,
              part: "snippet",
              q: params,
              chart: "mostPopular",
              type: "video",
              maxResults: 1,
            },
          })
          .then(success)
          .catch(fail)
})

export default youtubeAPI
