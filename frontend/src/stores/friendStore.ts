import { defineStore } from 'pinia';

interface FriendRequest {
  sender: string;
  receiver: string;
  id?: number;
}

interface Friend {
  id: number;
  user1: string;
  user2: string;
}

export const useFriendStore = defineStore('friendStore', {
  state: () => ({
    outgoingRequests: [] as FriendRequest[],
    incomingRequests: [] as FriendRequest[],
    friends: [] as Friend[],
    isLoading: false,
  }),

  actions: {
    async fetchOutgoingRequests() {
      this.isLoading = true;
      const response = await fetch(`/api/outgoing-requests/`, {
        method: 'GET',
        headers: {
          'X-CSRFToken': (window as any).CSRF_TOKEN,
        },
        credentials: 'include',
      });
      const data = await response.json();
      this.outgoingRequests = data.outgoing_requests;
      this.isLoading = false;
    },

    async fetchIncomingRequests() {
      this.isLoading = true;
      const response = await fetch(`/api/incoming-requests/`, {
        method: 'GET',
        headers: {
          'X-CSRFToken': (window as any).CSRF_TOKEN,
        },
        credentials: 'include',
      });
      const data = await response.json();
      this.incomingRequests = data.incoming_requests;
      this.isLoading = false;
    },

    async acceptRequest(requestId: number) {
      const response = await fetch(`/api/accept-friend-request/`, {
        method: 'POST',
        body: JSON.stringify({ request_id: requestId }),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': (window as any).CSRF_TOKEN,
        },
        credentials: 'include',
      });

      if (response.ok) {
        this.incomingRequests = this.incomingRequests.filter(request => request.id !== requestId);
        const newFriendship = await response.json();
        this.friends.push(newFriendship.friendship); 
      }
    },

    async denyRequest(requestId: number) {
      const response = await fetch(`/api/reject-friend-request/`, {
        method: 'POST',
        body: JSON.stringify({ request_id: requestId }),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': (window as any).CSRF_TOKEN,
        },
        credentials: 'include',
      });

      if (response.ok) {
        this.incomingRequests = this.incomingRequests.filter(request => request.id !== requestId);
      }
    },

    async fetchFriends() {
      this.isLoading = true;
      const response = await fetch(`/api/friends/`, {
        method: 'GET',
        headers: {
          'X-CSRFToken': (window as any).CSRF_TOKEN,
        },
        credentials: 'include',
      });
      const data = await response.json();
      this.friends = data.friends;
      this.isLoading = false;
    },
  },
});
