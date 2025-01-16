<template>
  <div class="h1">
    <h1>{{ title }}</h1>

    <!-- The LOGOUT function uses regular HTML POST -->
    <form action="/api/logout/" method="post">
      <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken" />
      <button type="submit">Logout</button>
    </form>

    <!-- User Profile Section -->
    <div>
      <h2>User Profile</h2>
      <pre v-if="userStore.user">{{ userStore.user }}</pre>
      <p v-else>Loading user profile...</p>
    </div>

    <!-- Hobbies Section -->
    <div>
      <h2>Hobbies (independent of user)</h2>
      <ul v-if="hobbiesStore.hobbies.length">
        <li v-for="hobby in hobbiesStore.hobbies" :key="hobby.id">{{ hobby.name }}</li>
      </ul>
      <p v-else>Loading hobbies...</p>
    </div>

    <!-- Button to Load Data -->
    <button @click="loadStores">Reload Data</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/userStore";
import { useHobbiesStore } from "../stores/hobbiesStore";

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

    // Automatically load stores on component mount
    loadStores();

    return {
      userStore,
      hobbiesStore,
      loadStores,
      csrfToken: (window as any).CSRF_TOKEN || "",
    };
  },
  data() {
    return {
      title: "Main Page: edited by taseen and isa",
    };
  },
});
</script>

<style scoped>
.h1 {
  font-size: 2rem;
  font-weight: bold;
}
</style>

