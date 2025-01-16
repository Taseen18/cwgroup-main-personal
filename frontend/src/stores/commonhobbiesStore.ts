import { defineStore } from 'pinia';
import { useUserStore } from './userStore';

interface CommonHobby {
  username: string;
  common_hobbies_count: number;
}

interface PaginatedResponse {
  userId: string;
  results: CommonHobby[];
  current_page: number;
  total_pages: number;
}

export const useCommonHobbiesStore = defineStore('commonHobbies', {
  state: () => ({
    commonHobbies: [] as CommonHobby[],
    currentPage: 1,
    totalPages: 1,
    minAge: 0,
    maxAge: 100,
    isLoading: false,
  }),

  actions: {
    async fetchCommonHobbies(pageNum: number = 1) {
      const userStore = useUserStore();
      this.isLoading = true;

      const response = await fetch(
        `/api/common-hobbies/?userId=${userStore.user?.id}&page=${pageNum}&min_age=${this.minAge}&max_age=${this.maxAge}`,
        {
          headers: { 'X-CSRFToken': (window as any).CSRF_TOKEN },
          credentials: 'include',
        }
      );

      const data: PaginatedResponse = await response.json();

      this.commonHobbies = data.results;
      this.currentPage = data.current_page;
      this.totalPages = data.total_pages;
      this.isLoading = false;
    },

    setAgeFilter(minAge: number, maxAge: number) {
      this.minAge = minAge;
      this.maxAge = maxAge;
      this.fetchCommonHobbies(1);
    },

    async nextPage() {
      if (this.currentPage < this.totalPages) {
        await this.fetchCommonHobbies(this.currentPage + 1);
      }
    },

    async previousPage() {
      if (this.currentPage > 1) {
        await this.fetchCommonHobbies(this.currentPage - 1);
      }
    },

    async sendFriendRequest(receiverUsername: string) {
      this.isLoading = true;

      const response = await fetch('/api/send-friend-request/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': (window as any).CSRF_TOKEN,
        },
        body: JSON.stringify({ receiver_username: receiverUsername }),
        credentials: 'include',
      });

      const data = await response.json();

      if (response.ok) {
        alert('Friend request sent successfully');
      } else {
        alert(data.error || 'Failed to send friend request');
      }

      this.isLoading = false;
    },
  },
});
