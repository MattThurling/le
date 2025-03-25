<template>
  <div>

    <div class="flex flex-row gap-4 mt-10">
      <div class="w-1/2 text-center">
        <p class="text text-xs">Current level:</p>
        <h2 class="text text-4xl font-bold text-neutral-content mt-3">B1</h2>
      </div>
      <div class="w-1/2 text-center">
        <p class="text text-xs">Goal:</p>
        <h2 class="text text-4xl font-bold text-secondary mt-3">B2</h2>
      </div>
    </div>

    <div class="text-center mt-8">
      <p class="text">
        This is going to take you <strong>300 hours</strong>. I don't care how smart you are.
      </p>
    </div>

    <div class="text-center mt-8">
      <p class="text text-xs">
        Progress
      </p>
    </div>

    <progress class="progress progress-secondary w-full mt-4" :value="totalDuration" max="18000"></progress>
  
    <div class="text-center mt-8">
      <p class="text">
        The good news is that some - or even all - of it should be fun. It all counts!
      </p>
    </div>



    <div class="divider"></div>

    <div class="text-center my-6">
      <p class="text text-xs">
        Record a study activity
      </p>
    </div>

    <div class="flex flex-col md:flex-row gap-4 w-full">
      <input type="date" v-model="newTimeLog.date" class="input w-full md:w-[20%]" required />

      <input type="text" v-model="newTimeLog.activity" placeholder="Activity" class="input w-full md:w-[40%]" required />

      <div class="w-full md:w-[15%]">
        <input type="number" v-model="newTimeLog.duration" class="input w-full" required placeholder="Minutes" />
      </div>

      <div class="w-full md:w-[25%]">
        <button @click="submitTimeLog" class="btn btn-primary w-full">Log study time</button>
      </div>
    </div>

    <div class="divider"></div>

    <div class="justify-center">
      <canvas ref="doughnutChartCanvas"></canvas>
    </div>

    <div class="divider"></div>
    
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
import { ref, onMounted, watch, computed } from 'vue';
import api from './api';
import Chart from 'chart.js/auto';

const timelogs = ref([]);  // Reactive state for storing fetched timelogs
const newTimeLog = ref({ date: '', activity: '', duration: '' });

// Chart.js references
const barChartCanvas = ref(null);
const doughnutChartCanvas = ref(null);
let barChartInstance = null;
let doughnutChartInstance = null;

const totalDuration = computed(() => {
  return timelogs.value.reduce((sum, log) => sum + (log.duration || 0), 0);
});

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
    await fetchTimeLogs();  // explicitly refresh from server
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
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',  
            'rgb(153, 102, 255)',  
            'rgb(255, 159, 64)',  
            'rgb(201, 203, 207)',  
            'rgb(0, 128, 128)',  
            'rgb(220, 20, 60)',  
            'rgb(34, 139, 34)',  
            'rgb(255, 140, 0)',  
            'rgb(123, 104, 238)',
          ],
          borderWidth: 0,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "left",
          labels: {
            usePointStyle: true, // Use small circles
            pointStyle: "circle",
          },
        },
      }
    }
  });
};

// Fetch data when the component is mounted
onMounted(async () => {
  await fetchTimeLogs();
  updateDoughnutChart(); // Initialize doughnut chart after fetching data
});

// Watch for changes in timelogs and update the charts dynamically
watch(timelogs, () => {
  updateDoughnutChart();
}, { deep: true });

</script>
