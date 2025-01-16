<template>
    <div class="container mt-5">
      <h1 class="text-center">Profile</h1>
  
      <!-- Logout Button -->
      <form action="/logout/" method="post" class="text-end">
        <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken" />
        <button type="submit" class="btn btn-danger">Logout</button>
      </form>
  
      <!-- Password Reset Link -->
      <div class="text-end mt-2">
        <a href="/password_change/" class="btn btn-link">Change Password</a>
      </div>
  
      <form @submit.prevent="saveChanges" class="card p-3">
        <!-- Name -->
        <div class="mb-3">
          <label>Name:</label>
          <input v-model="updatedProfile.name" class="form-control" type="text" />
        </div>
  
        <!-- Last Name -->
        <div class="mb-3">
          <label>Last Name:</label>
          <input v-model="updatedProfile.last_name" class="form-control" type="text" />
        </div>
  
        <!-- Username -->
        <div class="mb-3">
          <label>Username:</label>
          <input v-model="updatedProfile.username" class="form-control" type="text" />
        </div>
  
        <!-- Email -->
        <div class="mb-3">
          <label>Email:</label>
          <input v-model="updatedProfile.email" class="form-control" type="email" />
        </div>
  
        <!-- Date of Birth -->
        <div class="mb-3">
          <label>Date of Birth:</label>
          <input v-model="updatedProfile.date_of_birth" class="form-control" type="date" />
        </div>
  
        <!-- Hobbies -->
        <div class="mb-3">
          <label>Hobbies:</label>
          <ul>
            <li v-for="hobby in hobbiesStore.hobbies" :key="hobby.id">
              <input
                type="checkbox"
                :value="hobby.id"
                v-model="updatedProfile.hobbies"
              />
              {{ hobby.name }}
            </li>
          </ul>
  
          <!-- Add Existing Hobby -->
          <div class="mt-3">
            <label class="form-label" for="hobbyDropdown">Select an existing hobby to add:</label>
            <div class="d-flex flex-column">
                <select id="hobbyDropdown" v-model="selectedHobbyToAdd" class="form-control mb-2">
                     <option value="" disabled>Select a hobby</option>
                    <option v-for="hobby in availableHobbies" :key="hobby.id" :value="hobby.id">
                        {{ hobby.name }}
                    </option>
                </select>
                <button @click.prevent="addExistingHobby" class="btn btn-success">Add</button>
            </div>
          </div>
  
          <!-- Add New Hobby -->
          <div class="input-group mt-3">
            <input
              v-model="newHobby"
              placeholder="Add a new hobby"
              class="form-control"
              type="text"
            />
            <button @click.prevent="addNewHobby" class="btn btn-success mt-3">Add</button>
          </div>
        </div>
  
        <!-- Debug: Show selected hobby names -->
        <!-- <p>Selected Hobbies: {{ selectedHobbyNames }}</p> -->
  
        <!-- Save Button -->
        <button type="submit" class="btn btn-primary mt-3">Save Changes</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, ref, computed } from "vue";
  import { useUserStore } from "../stores/userStore";
  import { useHobbiesStore } from "../stores/hobbiesStore";
  
  export default defineComponent({
    setup() {
      const userStore = useUserStore();
      const hobbiesStore = useHobbiesStore();
  
      const updatedProfile = ref({
        name: "",
        last_name: "",
        username: "",
        email: "",
        date_of_birth: "",
        hobbies: [] as number[], // IDs of selected hobbies
      });
  
      const newHobby = ref("");
      const selectedHobbyToAdd = ref<number | null>(null);
      const csrfToken = ref((window as any).CSRF_TOKEN || "");
  
      onMounted(async () => {
        await Promise.all([userStore.fetchUserProfile(), hobbiesStore.fetchHobbies()]);
        updatedProfile.value = {
          name: userStore.user?.name || "",
          last_name: userStore.user?.last_name || "",
          username: userStore.user?.username || "",
          email: userStore.user?.email || "",
          date_of_birth: userStore.user?.date_of_birth || "",
          hobbies: userStore.user?.hobbies || [],
        };
      });
  
      const availableHobbies = computed(() =>
        hobbiesStore.hobbies.filter((h) => !updatedProfile.value.hobbies.includes(h.id))
      );
  
      const selectedHobbyNames = computed(() =>
        updatedProfile.value.hobbies
          .map((id) => hobbiesStore.hobbies.find((h) => h.id === id)?.name || "Unknown")
          .join(", ")
      );
  
      const saveChanges = async () => {
        await userStore.updateUserProfile({
          ...updatedProfile.value,
          hobbies: updatedProfile.value.hobbies,
        });
        alert("Profile updated successfully!");
      };
  
      const addExistingHobby = () => {
        if (selectedHobbyToAdd.value !== null && !updatedProfile.value.hobbies.includes(selectedHobbyToAdd.value)) {
          updatedProfile.value.hobbies.push(selectedHobbyToAdd.value);
        }
      };
  
      const addNewHobby = async () => {
        if (newHobby.value.trim()) {
          const existingHobby = hobbiesStore.hobbies.find(
            (h) => h.name.toLowerCase() === newHobby.value.toLowerCase().trim()
          );
          if (existingHobby) {
            alert(`Hobby "${newHobby.value}" already exists.`);
            return;
          }
  
          const response = await hobbiesStore.addHobby(newHobby.value.trim());
          if (response) {
            updatedProfile.value.hobbies.push(response.id);
          }
          newHobby.value = "";
        }
      };
  
      return {
        updatedProfile,
        hobbiesStore,
        newHobby,
        selectedHobbyToAdd,
        csrfToken,
        saveChanges,
        addExistingHobby,
        addNewHobby,
        availableHobbies,
        selectedHobbyNames,
      };
    },
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 0 auto;
  }
  
  .card {
    border-radius: 10px;
    padding: 20px;
  }
  
  button {
    width: 100%;
  }
  </style>
  