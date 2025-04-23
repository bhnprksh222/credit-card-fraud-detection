import axios from "axios"

const API = axios.create({
    baseURL: "http://localhost:8000",
    withCredentials: true,
    headers: {
        "Context-Type": "application/json"
    }
})

export default API;
