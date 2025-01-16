<template>
    <div>
      <h1>Test Stores</h1>
  
      <!-- User Profile Section -->
      <h2>User Profile</h2>
      <div v-if="userStore.user">
        <pre>{{ userStore.user }}</pre>
      </div>
      <div v-else>
        <p>Loading user profile...</p>
      </div>
  
      <!-- Hobbies Section -->
      <h2>Hobbies</h2>
      <div v-if="hobbiesStore.hobbies.length">
        <pre>{{ hobbiesStore.hobbies }}</pre>
      </div>
      <div v-else>
        <p>Loading hobbies...</p>
      </div>
  
      <!-- Button to Load Data -->
      <button @click="loadStores">Reload Data</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useUserStore } from '../stores/userStore';
  import { useHobbiesStore } from '../stores/hobbiesStore';
  
  export default defineComponent({
    setup() {
      const userStore = useUserStore();
      const hobbiesStore = useHobbiesStore();
  
      const loadStores = async () => {
        await Promise.all([
          userStore.fetchUserProfile(),
          hobbiesStore.fetchHobbies(),
        ]);
      };
  
      // Load data when the component mounts
      loadStores();
  
      return { userStore, hobbiesStore, loadStores };
    },
  });
  </script>
  