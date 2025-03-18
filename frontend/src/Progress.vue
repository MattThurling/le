<template>
  <div>

    <div class="flex flex-col sm:flex-row gap-4">
      <div class="w-full sm:w-1/2">
          <canvas ref="barChartCanvas"></canvas>
      </div>
      <div class="w-full sm:w-1/2">
          <canvas ref="doughnutChartCanvas"></canvas>
      </div>
    </div>

    <div class="divider"></div>

    <div>
      <input type="date" v-model="newTimeLog.date" class="input" required />
    </div>

    <div class="mt-4">
      <input type="text" v-model="newTimeLog.activity" placeholder="Activity" class="input" required />
    </div>

    <div class="mt-4">
      <input type="number" v-model="newTimeLog.duration" class="input validator" required placeholder="Minutes" min="1" max="1440" title="Must be between 1 and 1440" />
      <p class="validator-hint">Must be between 1 and 1440</p>
    </div>

    <div class="mt-4">
      <button @click="submitTimeLog" class="btn btn-wide btn-primary">Log study time</button>
    </div>  
    
    <div class="mt-4">
      <ul class="list bg-base-100 rounded-box shadow-md">
        <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">Time Logs</li>

        <li class="list-row" v-for="(log, index) in timelogs" :key="index">
            <div>
            {{ formatDate(log.date) }}
            </div>
            <div>
            {{ log.activity }}
            </div>
            <div>
            {{ log.duration }}
            </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from './api';
import Chart from 'chart.js/auto';

const timelogs = ref([]);  // Reactive state for storing fetched timelogs
const newTimeLog = ref({ date: '', activity: '', duration: '' });

// Chart.js references
const barChartCanvas = ref(null);
const doughnutChartCanvas = ref(null);
let barChartInstance = null;
let doughnutChartInstance = null;

const fetchTimeLogs = async () => {
  try {
    const response = await api.get('timelogs/');
    timelogs.value = response.data;  // Update the reactive state
  } catch (error) {
    console.error('Error fetching timelogs:', error);
  }
};

const submitTimeLog = async () => {
  if (!newTimeLog.value.date || !newTimeLog.value.activity || !newTimeLog.value.duration) {
    alert("Please fill out all fields.");
    return;
  }

  try {
    const response = await api.post('timelogs/', newTimeLog.value);
    timelogs.value.push(response.data); // Update the UI with the new log
    newTimeLog.value = { date: '', activity: '', duration: '' }; // Reset input fields
  } catch (error) {
    console.error('Error adding timelog:', error);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown';
  
  const date = new Date(dateString);
  if (isNaN(date)) return 'Invalid Date'; // Handle invalid dates

  return new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short' }).format(date);
};

// Function to create/update the bar chart
const updateBarChart = () => {
  if (!barChartCanvas.value || timelogs.value.length === 0) return;

  const labels = timelogs.value.map(log => log.date || 'Unknown'); // Extract dates
  const values = timelogs.value.map(log => log.duration || 0); // Extract logged hours

  // Destroy previous instance if it exists
  if (barChartInstance) {
    barChartInstance.destroy();
  }

  barChartInstance = new Chart(barChartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: '',
          data: values,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
            legend: {
                display: false // Hides the legend
            }
      },
      scales: {
            x: {
                display: false // Hides the x-axis labels
            }
          }
    }
  });
};

// Function to create/update the doughnut chart
const updateDoughnutChart = () => {
  if (!doughnutChartCanvas.value || timelogs.value.length === 0) return;

  // Aggregate total hours per activity
  const activityTotals = timelogs.value.reduce((acc, log) => {
    acc[log.activity] = (acc[log.activity] || 0) + log.duration;
    return acc;
  }, {});

  const labels = Object.keys(activityTotals); // Activity names
  const values = Object.values(activityTotals); // Total hours per activity

  // Destroy previous instance if it exists
  if (doughnutChartInstance) {
    doughnutChartInstance.destroy();
  }

  doughnutChartInstance = new Chart(doughnutChartCanvas.value, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [
        {
          label: 'Total Hours Per Activity',
          data: values,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ]
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
};

// Fetch data when the component is mounted
onMounted(async () => {

  await fetchTimeLogs();
  updateBarChart(); // Initialize bar chart after fetching data
  updateDoughnutChart(); // Initialize doughnut chart after fetching data
});

// Watch for changes in timelogs and update the charts dynamically
watch(timelogs, () => {
  updateBarChart();
  updateDoughnutChart();
}, { deep: true });

</script>
