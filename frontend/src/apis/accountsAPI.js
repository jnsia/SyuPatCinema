import axiosInstance from "@/utils/axios-instance";
import axiosTokenInstance from "@/utils/axios-token-instance";

const accountsAPI = {
  login: async (params, success, fail) => {
    await axiosInstance
      .post("/dj_rest_auth/login/", params)
      .then(success)
      .catch(fail);
  },
  signUp: async (params, success, fail) => {
    axiosInstance.defaults.headers["Content-Type"] = "multipart/form-data";
    await axiosInstance
      .post("/dj_rest_auth/signup/", params)
      .then(success)
      .catch(fail);
  },
  getUserInfo: async (success, fail) => {
    await axiosTokenInstance.get("/accounts/user/").then(success).catch(fail);
  },
  getOtherUserInfo: async (userId, success, fail) => {
    await axiosTokenInstance.get(`/accounts/user/${userId}/`).then(success).catch(fail);
  },
};

export default accountsAPI;
