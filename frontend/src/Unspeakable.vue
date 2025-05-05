<template>
<div class="mt-8 unspeakable-text">
  <h1 class="opti text-center">UNSPEAKABLE</h1>
  <div class="flex flex-col lg:flex-row gap-6 max-w-5xl mx-auto mb-10 mt-8 px-4">
    <!-- Left panel: Game card -->
    <div class="flex-7">
      <div v-if="roundHasStarted" class="grid grid-cols-4 h-[315px]">
        <div class="col-span-3">
          <p class="text-xs">Describe:</p>
          <h2 class="text-3xl mt-1 mb-2 h-[36px]">{{ currentCard?.target }}</h2>
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

        <div class="h-[64px] w-[64px] col-span-1 card bg-base-100 text-center justify-self-end pr-12">
          <div class="flex justify-center gap-5">
            <div class="text-center text-green-500">
              <p class="text font-bold">{{ score.correct }}</p>
              <Check :size="18" />
            </div>
            <div class="text-center text-red-500">
              <p class="text font-bold">{{ score.passes }}</p>
              <X :size="18" />
            </div>
          </div>
        </div>

      </div>
      <div v-if="!selectedSetId && !roundHasStarted" class="flex justify-center h-[315px]">
        <img src="https://storage.googleapis.com/le-assets/images/ravenflip.jpg" width="200px" alt="raven">
      </div>
      <div v-if="selectedSetId && !roundHasStarted" class="h-[315px]">
        <p class="text-center pt-7">Score:</p>
        <p class="text-6xl text-center font-bold mt-1 mb-1">{{ gameScore.toLocaleString() }}</p>
        <div class="flex justify-center gap-8">
          <div class="text-center text-green-500">
            <p class="text font-bold">{{ score.correct }}</p>
            <Check :size="18" />
          </div>
          <div class="text-center text-red-500">
            <p class="text font-bold">{{ score.passes }}</p>
            <X :size="18" />
          </div>
          <div class="text-center">
            <p class="text font-bold">{{ score.max }}</p>
            <Zap :size="18" />
          </div>
        </div>
      </div>

      <!-- Bottom action buttons -->
      <!-- Show the "Start" button if round hasn't started, otherwise show Pass/Got it -->

      <div class="grid grid-cols-3 gap-4 mt-6">
        <div v-if="!roundHasStarted" class="col-span-2">
          <button
            @click="startRound"
            class="btn btn-outline w-full"
            :disabled="!selectedSetId || isLoadingCards || remainingCards.length === 0"
          >
            <span v-if="!isLoadingCards">Start</span>
            <span v-else class="loading loading-spinner loading-sm"></span>
          </button>
        </div>
        <div v-else class="col-span-2">
          <div class="grid grid-cols-2 gap-4">
            <button @click="answer(false)" class="btn btn-red btn-outline w-full">
              Pass
            </button>
            <button @click="answer(true)" class="btn btn-green btn-outline w-full">
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
          <option disabled :selected="!selectedSetId" :value="null">
            Choose a set of words...
          </option>
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
import { Check, Zap, X } from 'lucide-vue-next'


const props = defineProps({
  setId: {
    type: Number,
    required: true
  }
})

const availableSets = ref([{ id: 1, name: 'English' }])

const selectedSetId = ref(null)

const score = ref({correct: 0, passes: 0, streak: 0, max: 0})

// Cards data
const remainingCards = ref([])
const currentCard = ref(null)
const tabooWordCount = ref(3)

// Round timer state
const roundHasStarted = ref(false)
const timerMinutes = ref(1)
const timerSeconds = ref(30)
let countdownInterval = null

const isLoadingCards = ref(false)

const sounds = {
  gong: 'gong.mp3',
  whistle: 'whistle.m4a',
  right: 'gotit.mp3',
  wrong: 'quack.mp3',
  crow1: 'crow1.m4a',
  crow2: 'crow2.m4a',
  crow3: 'crow3.m4a',
  crow4: 'crow5.m4a',
  crow5: 'crow6.m4a'
}

const sfx = {}
const sfxLoaded = ref(false)

const loadSfx = () => {
  if (sfxLoaded.value) return
  for (const [key, path] of Object.entries(sounds)) {
    const audio = new Audio(`https://storage.googleapis.com/le-assets/sounds/${path}`)
    audio.load()
    sfx[key] = audio
  }
  sfxLoaded.value = true
}

// The array goes from 30s to 300s (5 mins), in 30s increments:
const timeOptions = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
// We'll use timeIndex (0..9) to pick from timeOptions:
const timeIndex = ref(2)

// Whenever timeIndex changes, reset timerMinutes and timerSeconds
watch(timeIndex, () => {
  resetTimer()
})

const resetTimer = () => {
  const totalSeconds = timeOptions[timeIndex.value]
  timerMinutes.value = Math.floor(totalSeconds / 60)
  timerSeconds.value = totalSeconds % 60
}

const resetScore = () => {
  score.value = {correct: 0, passes: 0, streak: 0, max: 0}
}

const gameScore = computed(() => {
  const { correct, passes, max } = score.value
  const maxMultiplier = 750
  const passPenalty = 750
  const total = correct * (10000 + (max * maxMultiplier)) - (passPenalty * passes)
  if (total < 0) return 0
  return total
})

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
  resetScore()
  playSfx('gong')
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
      playSfx('whistle')
    }
    timerMinutes.value = Math.floor(totalSeconds / 60)
    timerSeconds.value = totalSeconds % 60
  }, 1000)
}

const playSfx = (name) => {
  if (!sfx[name]) {
    console.warn(`Sound "${name}" not loaded`);
    return;
  }
  // Clone for overlapping playback
  const clone = sfx[name].cloneNode();
  clone.play().catch(err => {
    console.warn(`Could not play sound "${name}":`, err)
  })
}
// Get available sets
const fetchSets = async () => {
  const response = await publicApi.get('sets')
  availableSets.value = response.data
}

// Card fetching and shuffling
const fetchCards = async (setId = selectedSetId.value) => {
  remainingCards.value = []
  currentCard.value = null
  isLoadingCards.value = true
  try {
    const response = await publicApi.get(`sets/${setId}/cards/`)
    const cards = response.data
    remainingCards.value = shuffle(cards)
    nextCard()
  } catch (error) {
    console.error("Failed to fetch cards", error)
  } finally {
    isLoadingCards.value = false
  }
}

const shuffle = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[array[i], array[j]] = [array[j], array[i]]
  }
  return array
}

const answer = (isCorrect) => {
  if (isCorrect) {
    playSfx('right')
    score.value.correct ++
    score.value.streak ++
    score.value.max = Math.max(score.value.streak, score.value.max)
  }
  if (!isCorrect) {
    playSfx(`crow${Math.floor(Math.random() * 5) + 1}`)
    score.value.passes ++
    score.value.streak = 0
  }
  nextCard()
}

const nextCard = () => {
  if (remainingCards.value.length === 0) {
    currentCard.value = null
    return
  }
  currentCard.value = remainingCards.value.pop()
}

onMounted(() => {
  document.addEventListener('click', loadSfx, { once: true });
  fetchSets()
  fetchCards()
})

watch(selectedSetId, async (newSetId) => {
  await fetchCards(newSetId)
})
</script>
