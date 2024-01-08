import axios from "axios";

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  headers: {
    "content-type": "application/json",
  },
});

export default service;



