<template>
  <h1>Large English</h1>
  <p>Coming soon: a new resource site for English language learners, featuring serious exam preparation drills and daft videos!</p>

  <ul v-if="prompts.length">
    <li v-for="prompt in prompts" :key="prompt.id">
      {{ prompt.title }}
    </li>
  </ul>
  <p v-else>Loading prompts...</p>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";
import type { Prompt } from "./types"; // ✅ Import the Prompt type

export default defineComponent({
  setup() {
    const prompts = ref<Prompt[]>([]); // ✅ Type-safe ref

    const fetchPrompts = async () => {
      try {
        const response = await axios.get<Prompt[]>("https://le-api.onrender.com/api/prompts/");
        prompts.value = response.data;
      } catch (error) {
        console.error("API call failed:", error);
      }
    };

    onMounted(fetchPrompts);

    return { prompts };
  },
});
</script>