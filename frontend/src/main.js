import './styles.css'
import { createApp } from 'vue'
import SynfulCard from './Synful.vue'
import Progress from './Progress.vue'

// Mount SynfulCard if target exists
const synfulTarget = document.getElementById('synful-app')
if (synfulTarget) {
  const setId = parseInt(synfulTarget.dataset.setId)
  createApp(SynfulCard, { setId }).mount('#synful-app')
}

// Mount Progress if target exists
const progressTarget = document.getElementById('progress-app')
if (progressTarget) {
  createApp(Progress).mount('#progress-app')
}
