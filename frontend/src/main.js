import './styles.css'
import { createApp } from 'vue'
import Unspeakable from './Unspeakable.vue'
import Progress from './Progress.vue'
import * as lucide from 'lucide-vue-next';

// Mount SynfulCard if target exists
const unspeakableTarget = document.getElementById('unspeakable-app')
if (unspeakableTarget) {
  // TODO: revisit setId, not sure why / if this is needed
  const setId = parseInt(unspeakableTarget.dataset.setId)
  createApp(Unspeakable, { setId }).mount('#unspeakable-app')
}

// Mount Progress if target exists
const progressTarget = document.getElementById('progress-app')
if (progressTarget) {
  createApp(Progress).mount('#progress-app')
}
