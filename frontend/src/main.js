import './styles.css'
import { createApp } from 'vue'
import Unspeakable from './Unspeakable.vue'
import Progress from './Progress.vue'

// Mount SynfulCard if target exists
const synfulTarget = document.getElementById('unspeakable-app')
if (synfulTarget) {
  const setId = parseInt(synfulTarget.dataset.setId)
  createApp(Unspeakable, { setId }).mount('#unspeakable-app')
}

// Mount Progress if target exists
const progressTarget = document.getElementById('progress-app')
if (progressTarget) {
  createApp(Progress).mount('#progress-app')
}
