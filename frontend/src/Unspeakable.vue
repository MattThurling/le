<template>
<div class="mt-8 unspeakable-text">
  <h1 class="opti text-center">UNSPEAKABLE</h1>
  <div class="flex flex-col lg:flex-row gap-6 max-w-5xl mx-auto mb-10 mt-8 px-4">
    <!-- Left panel: Game card -->
    <div class="flex-7">
      <div class="grid grid-cols-4 h-[315px]">
        <div class="col-span-3">
          <p class="text-xs">Describe:</p>
          <h2 class="text-3xl mb-2 h-[36px]">{{ currentCard?.target }}</h2>
          <p class="text-xs mt-6">without saying:</p>
          <ul v-if="currentCard" class="list mt-1">
            <li
              v-for="(word, index) in visibleTabooWords"
              :key="index"
              class="text-xl unspeakable-text"
            >
              {{ word }}
            </li>
          </ul>
          <p
            v-if="remainingCards.length === 0 && currentCard"
            class="mt-4 text-sm text-gray-500"
          >
            You've reached the end of the set!
          </p>
        </div>

        <div class="h-[64px] w-[64px] col-span-1 card bg-base-100 text-center justify-self-end">
          <p class="text-xs mt-1">Score:</p>
          <p class="text-4xl text-accent font-bold mb-1">{{ score }}</p>
        </div>

      </div>

      <!-- Bottom action buttons -->
      <!-- Show the "Start" button if round hasn't started, otherwise show Pass/Got it -->

      <div class="grid grid-cols-3 gap-4 mt-6">
        <div v-if="!roundHasStarted" class="col-span-2">
          <button @click="startRound" class="btn btn-outline btn-accent w-full">
            Start
          </button>
        </div>
        <div v-else class="col-span-2">
          <div class="grid grid-cols-2 gap-4">
            <button @click="nextCard(-1)" class="btn btn-primary btn-outline w-full">
              Pass
            </button>
            <button @click="nextCard(1)" class="btn btn-secondary btn-outline w-full">
              Got it!
            </button>
          </div>
        </div>
        
        <div class="font-mono text-xl flex items-center justify-center">
            {{ formattedMinutes }}:{{ formattedSeconds }} 
        </div>
      </div>

     
    </div>

    <!-- Right panel: Settings -->
    <div class="flex-3">
      <!-- Set Selector Dropdown -->
      <div class="mt-8 mb-8">
        <select class="select select-bordered w-full" v-model="selectedSetId">
          <option
            v-for="set in availableSets"
            :key="set.id"
            :value="set.id"
          >
            {{ set.name }}
          </option>
        </select>
      </div>

       <!-- Unspeakable words slider -->
       <div class="mb-4">
        <label class="label">
          <span class="label-text">
            Unspeakable words: {{ tabooWordCount }}
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

      <!-- Time slider (in 30s intervals from 30s to 5min) -->
      <div class="mb-4">
        <label class="label">
          <span class="label-text">
            Time per round:
          </span>
        </label>
        <input
          :disabled="roundHasStarted"
          type="range"
          min="0"
          max="9"
          step="1"
          v-model="timeIndex"
          class="range range-xs range-neutral"
        />
      </div>
    </div>
  </div>
</div>
  
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { publicApi } from './api'


const props = defineProps({
  setId: {
    type: Number,
    required: true
  }
})

const availableSets = ref([{ id: 1, name: 'English' }])

const selectedSetId = ref(1)

const score = ref(0)

// Cards data
const remainingCards = ref([])
const currentCard = ref(null)
const tabooWordCount = ref(3)

// Round timer state
const roundHasStarted = ref(false)
const timerMinutes = ref(1)
const timerSeconds = ref(30)
let countdownInterval = null


// The array goes from 30s to 300s (5 mins), in 30s increments:
const timeOptions = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
// We'll use timeIndex (0..9) to pick from timeOptions:
const timeIndex = ref(2)

// A nicely formatted display of the currently selected time (e.g., "2:00")
const selectedTimeDisplay = computed(() => {
  const totalSeconds = timeOptions[timeIndex.value]
  const mins = Math.floor(totalSeconds / 60)
  const secs = totalSeconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
})


// Whenever timeIndex changes, reset timerMinutes and timerSeconds
watch(timeIndex, () => {
  resetTimer()
})

const resetTimer = () => {
  const totalSeconds = timeOptions[timeIndex.value]
  timerMinutes.value = Math.floor(totalSeconds / 60)
  timerSeconds.value = totalSeconds % 60
}

// Show only 'tabooWordCount' words
const visibleTabooWords = computed(() => {
  return currentCard.value?.taboo_words.slice(0, tabooWordCount.value) || []
})

// Formatting helpers for display
const formattedMinutes = computed(() => String(timerMinutes.value).padStart(2, '0'))
const formattedSeconds = computed(() => String(timerSeconds.value).padStart(2, '0'))

// Starts the round and the countdown
const startRound = () => {
  roundHasStarted.value = true
  resetTimer()
  score.value = 0
  playSound('gong.mp3')
  startCountdown()
}

const startCountdown = () => {
  let totalSeconds = timerMinutes.value * 60 + timerSeconds.value

  clearInterval(countdownInterval)

  countdownInterval = setInterval(() => {
    totalSeconds--
    if (totalSeconds <= 0) {
      clearInterval(countdownInterval)
      roundHasStarted.value = false
      playSound('whistle.m4a')
    }
    timerMinutes.value = Math.floor(totalSeconds / 60)
    timerSeconds.value = totalSeconds % 60
  }, 1000)
}

const playSound = (file) => {
  const sfx = new Audio(`https://storage.googleapis.com/le-assets/sounds/${file}`)
  sfx.play()
}
// Get available sets
const fetchSets = async () => {
  const response = await publicApi.get('sets')
  availableSets.value = response.data
}

// Card fetching and shuffling
const fetchCards = async (setId = selectedSetId.value) => {
  const response = await publicApi.get(`sets/${setId}/cards/`)
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


const nextCard = (points = 0) => {
  if (points === 1) playSound('gotit.mp3')
  if (points === -1) playSound('quack.mp3')
  score.value += points
  if (remainingCards.value.length === 0) {
    currentCard.value = null
    return
  }
  currentCard.value = remainingCards.value.pop()
}

onMounted(() => {
  fetchSets()
  fetchCards()
})

watch(selectedSetId, async (newSetId) => {
  await fetchCards(newSetId)
})
</script>
