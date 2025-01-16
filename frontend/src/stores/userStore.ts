import { defineStore } from 'pinia';

//interface Hobby {
  //id: number;
  //name: string;
//}

interface User {
    id?: number;
    name?: string; 
    last_name?: string;
    username?: string;
    email?: string;
    date_of_birth?: string; 
    //hobbies?: Hobby[];
    hobbies?: number[]; 
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
  }),

  actions: {
    // Fetch user profile
    async fetchUserProfile() {
      const response = await fetch('/api/profile/', {
        headers: { 'X-CSRFToken': (window as any).CSRF_TOKEN },
        credentials: 'include',
      });
      const userData = await response.json();
      if (userData.hobbies) {
        userData.hobbies = userData.hobbies.map((hobby: { id: number }) => hobby.id); // Extract IDs
      }
      this.user = userData;
    },

    //async fetchUserProfile() {
      //const response = await fetch('/api/profile/', {
        //headers: { 'X-CSRFToken': (window as any).CSRF_TOKEN },
        //credentials: 'include',
      //});
      //this.user = await response.json();
    //},

    // Update user profile
    async updateUserProfile(updatedData: Partial<User>) {
      const response = await fetch('/api/profile/', {
        method: 'PUT',
        headers: {
          'X-CSRFToken': (window as any).CSRF_TOKEN,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(updatedData),
      });
      if (response.ok) {
        this.user = { ...this.user, ...updatedData };
      }
    },
  },
});
