import axios from "axios";

// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_URL, // 기본 URL
  timeout: 10000, // 요청 타임아웃 (밀리초)
  headers: {
    "Content-Type": "application/json", // 기본 헤더
  },
});

// 요청 인터셉터 설정
axiosInstance.interceptors.request.use(
  function (config) {
    // 요청 전 로직 (예: 로딩 스피너 표시)
    console.log("Request was sent");
    return config;
  },
  function (error) {
    // 요청 에러 처리
    return Promise.reject(error);
  }
);

// 응답 인터셉터 설정
axiosInstance.interceptors.response.use(
  function (response) {
    // 응답 데이터 가공 (필요 시)
    return response;
  },
  function (error) {
    // 응답 에러 처리
    if (error.response) {
      // 서버 응답이 있는 경우
      console.error("Error response", error.response);
    } else if (error.request) {
      // 요청이 이루어졌으나 응답이 없는 경우
      console.error("No response", error.request);
    } else {
      // 요청 설정 중 에러 발생
      console.error("Error", error.message);
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
