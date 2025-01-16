import { defineStore } from 'pinia';

interface Hobby {
  id: number;
  name: string;
}

export const useHobbiesStore = defineStore('hobbies', {
  state: () => ({
    hobbies: [] as Hobby[],
  }),

  actions: {
    // Fetch all hobbies
    async fetchHobbies() {
      const response = await fetch('/api/hobbies/', {
        headers: { 'X-CSRFToken': (window as any).CSRF_TOKEN },
        credentials: 'include',
      });
      this.hobbies = await response.json();
      console.log('Fetched Hobbies from Backend:', this.hobbies); // Debug log
    },

    // Add a new hobby
    async addHobby(name: string) {
      const response = await fetch('/api/hobbies/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': (window as any).CSRF_TOKEN,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ name }),
      });
      const newHobby = await response.json();
      this.hobbies.push(newHobby);
      return newHobby;
    },
  },
});
