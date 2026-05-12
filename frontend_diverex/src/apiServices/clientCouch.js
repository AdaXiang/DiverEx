import axios from "axios";

const apiC = axios.create({
    baseURL: process.env.REACT_APP_API_URL_COUCHDB,
});

export default apiC;