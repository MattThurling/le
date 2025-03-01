<template>
  <h1>Large English</h1>
  <p>Coming soon: a new resource site for English language learners, featuring serious exam preparation drills and daft videos!</p>
  <p>{{ message }}</p>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: "Loading..."
    };
  },
  async mounted() {
    try {
      const response = await axios.get("https://le-api.onrender.com/api/message/");
      console.log(response.data.message)
      this.message = response.data.message;
    } catch (error) {
      console.error("API call failed:", error);
      this.message = "Error fetching message";
    }
  }
};
</script>

