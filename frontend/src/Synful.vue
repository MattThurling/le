<template>
  <div class="flex flex-col lg:flex-row gap-6 max-w-5xl mx-auto my-10 px-4">
    <!-- Left panel: Game card -->
    <div class="flex-2">
      <div class="card bg-base-200">
        <div class="card-body min-h-[400px]">
          <h2 class="card-title text-3xl mb-2">{{ currentCard?.target }}</h2>

          <div v-if="currentCard" class="mt-4 space-y-2">
            <ul class="list">
              <li v-for="(word, index) in visibleTabooWords" :key="index" class="text-xl">
                {{ word }}
              </li>
            </ul>
          </div>

          <p
            v-if="remainingCards.length === 0 && currentCard"
            class="mt-4 text-sm text-gray-500"
          >
            You've reached the end of the set!
          </p>
        </div>
      </div>

      <!-- Bottom action buttons -->
      <div class="grid grid-cols-2 gap-4 mt-6">
        <button @click="nextCard" class="btn btn-primary btn-outline w-full">Pass</button>
        <button @click="nextCard" class="btn btn-secondary btn-outline w-full">Got it!</button>
      </div>
    </div>

    <!-- Right panel: Settings -->
    <div class="flex-1">
       <!-- Timer (placeholder for now) -->
      <div class="my-6 text-center">
        <span class="countdown font-mono text-2xl">
          <span style="--value:00;" aria-live="polite" aria-label="00">00</span>
          :
          <span style="--value:59;" aria-live="polite" aria-label="59">59</span>
        </span>
      </div>

      <div class="card bg-base-400">
        <div class="card-body">

          <!-- Slider -->
          <div class="mb-4">
            <label class="label">
              <span class="label-text">
                Number of synful words: {{ tabooWordCount }}
              </span>
            </label>
            <input
              type="range"
              min="0"
              max="7"
              v-model="tabooWordCount"
              class="range range-xs range-neutral"
            />
          </div>

          <!-- Drop down -->
          <div class="mb-4">
            <select class="select select-bordered w-full" v-model="difficulty">
              <option value="easy">Business Words</option>
              <option value="medium">General</option>
              <option value="hard">Music</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { publicApi } from './api'

const props = defineProps({
  setId: {
    type: Number,
    required: true
  }
})

const remainingCards = ref([])
const currentCard = ref(null)
const tabooWordCount = ref(3)
const difficulty = ref('medium')

const visibleTabooWords = computed(() => {
  return currentCard.value?.taboo_words.slice(0, tabooWordCount.value) || []
})

const fetchCards = async () => {
  const response = await publicApi.get(`sets/${props.setId}/cards/`)
  const cards = response.data
  remainingCards.value = shuffle(cards)
  nextCard()
}

const shuffle = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[array[i], array[j]] = [array[j], array[i]]
  }
  return array
}

const nextCard = () => {
  if (remainingCards.value.length === 0) {
    currentCard.value = null
    return
  }
  currentCard.value = remainingCards.value.pop()
}
onMounted(fetchCards)
</script>
  