<template>
  <div class="container mt-5">
    <h1 class="text-center">Find Users with Common Hobbies</h1>

    <!-- Age Filter Form -->
    <div class="card p-3 mb-4">
      <h2 class="h4 mb-3">Age Filter</h2>
      <form @submit.prevent="applyFilter" class="row">
        <div class="col-md-5 mb-3">
          <label class="form-label">Minimum Age:</label>
          <input
            v-model.number="minAge"
            type="number"
            class="form-control"
            min="0"
            max="100"
            :disabled="store.isLoading"
          />
        </div>
        <div class="col-md-5 mb-3">
          <label class="form-label">Maximum Age:</label>
          <input
            v-model.number="maxAge"
            type="number"
            class="form-control"
            min="0"
            max="100"
            :disabled="store.isLoading"
          />
        </div>
        <div class="col-md-2 mb-3 d-flex align-items-end">
          <button type="submit" class="btn btn-primary w-100" :disabled="store.isLoading">
            Search
          </button>
        </div>
      </form>
    </div>

    <!-- Loading State -->
    <div v-if="store.isLoading" class="text-center py-4">
      <span class="visually-hidden">Loading...</span>
    </div>

    <!-- Results -->
    <div v-else-if="store.commonHobbies?.length" class="card">
      <ul class="list-group list-group-flush">
        <li v-for="hobby in store.commonHobbies" :key="hobby.username" class="list-group-item">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h3 class="h5 mb-1">{{ hobby.username }}</h3>
              <p class="text-muted mb-0">
                {{ hobby.common_hobbies_count }} common 
                {{ hobby.common_hobbies_count === 1 ? 'hobby' : 'hobbies' }}
              </p>
            </div>
            <button @click="sendFriendRequest(hobby.username)" class="btn btn-outline-primary":disabled="store.isLoading">
              Add Friend
            </button>
          </div>
        </li>
      </ul>

      <!-- Pagination -->
      <div class="card-footer">
        <div class="d-flex justify-content-between">
          <button @click="store.previousPage()" class="btn btn-outline-primary" :disabled="store.currentPage <= 1">
            Previous
          </button>
          <span class="align-self-center">
            Page {{ store.currentPage }} of {{ store.totalPages }}
          </span>
          <button @click="store.nextPage()" class="btn btn-outline-primary" :disabled="store.currentPage >= store.totalPages">
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useCommonHobbiesStore } from '../stores/commonhobbiesStore';

export default defineComponent({
  name: 'CommonHobbiesPage',

  setup() {
    const store = useCommonHobbiesStore();
    const minAge = ref<number>(0);
    const maxAge = ref<number>(100);

    const applyFilter = () => {
      store.setAgeFilter(minAge.value, maxAge.value);
    };

    const sendFriendRequest = (receiverUsername: string) => {
      store.sendFriendRequest(receiverUsername);
    };

    onMounted(() => {
      store.fetchCommonHobbies();
    });

    return {
      store,
      minAge,
      maxAge,
      applyFilter,
      sendFriendRequest,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  border-radius: 10px;
}

.pagination button {
  width: auto;
}
</style>
