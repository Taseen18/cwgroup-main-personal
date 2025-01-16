<template>
    <div class="container mt-5">
      <h1 class="text-center">Friends Tab</h1>
  
      <!-- Loading State -->
      <div v-if="friendStore.isLoading" class="text-center py-4">
        <span>Loading...</span>
      </div>
  
      <div class="row">
        <!-- Outgoing Friend Requests -->
        <div class="col-md-4">
          <div class="card p-3 mb-4 list-box">
            <h2 class="h5 mb-3 text-center">Outgoing Requests</h2>
            <ul class="list-group">
              <li v-for="(request, index) in friendStore.outgoingRequests" :key="index" class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h3 class="h6 mb-1">{{ request.receiver }}</h3>
                  </div>
                </div>
              </li>
            </ul>
            <div v-if="friendStore.outgoingRequests.length === 0" class="text-center mt-3">
              <p>No outgoing requests</p>
            </div>
          </div>
        </div>
  
        <!-- Incoming Friend Requests -->
        <div class="col-md-4">
          <div class="card p-3 mb-4 list-box">
            <h2 class="h5 mb-3 text-center">Incoming Requests</h2>
            <ul class="list-group">
              <li v-for="(request, index) in friendStore.incomingRequests" :key="index"class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h3 class="h6 mb-1">{{ request.sender }}</h3>
                  </div>
                  <div>
                    <button v-if="request.id !== undefined"@click="acceptRequest(request.id)"class="btn btn-outline-success btn-sm me-2">
                      Accept
                    </button>
                    <button v-if="request.id !== undefined"@click="denyRequest(request.id)" class="btn btn-outline-danger btn-sm">
                      Deny
                    </button>
                  </div>
                </div>
              </li>
            </ul>
            <div v-if="friendStore.incomingRequests.length === 0" class="text-center mt-3">
              <p>No incoming requests</p>
            </div>
          </div>
        </div>
  
        <!-- Friends List -->
        <div class="col-md-4">
          <div class="card p-3 mb-4 list-box">
            <h2 class="h5 mb-3 text-center">Your Friends</h2>
            <ul class="list-group">
              <li v-for="(friend, index) in friendStore.friends" :key="index"class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <!-- Which user is the friend (not main)-->
                    <h3 class="h6 mb-1">
                      {{ friend.user1 === currentUser ? friend.user2 : friend.user1 }}
                    </h3>
                  </div>
                </div>
              </li>
            </ul>
            <div v-if="friendStore.friends.length === 0" class="text-center mt-3">
              <p>You have no friends yet</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, computed } from 'vue';
  import { useFriendStore } from '../stores/friendStore'; 
  import { useUserStore } from '../stores/userStore'; 
  
  export default defineComponent({
    name: 'FriendManagementPage',
    setup() {
      const friendStore = useFriendStore();
      const userStore = useUserStore();
  
      onMounted(async () => {
        await userStore.fetchUserProfile(); 
        await friendStore.fetchOutgoingRequests();
        await friendStore.fetchIncomingRequests();
        await friendStore.fetchFriends(); 
      });
  
      
      const currentUser = computed(() => userStore.user?.username || '');
  
      
      const acceptRequest = (requestId: number) => {
        if (requestId !== undefined) {
          friendStore.acceptRequest(requestId);
        }
      };
  
      const denyRequest = (requestId: number) => {
        if (requestId !== undefined) {
          friendStore.denyRequest(requestId);
        }
      };
  
      return {
        friendStore,
        currentUser,
        acceptRequest,
        denyRequest,
      };
    },
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .card {
    border-radius: 10px;
  }
  
  .list-group-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .list-box {
    min-height: 300px;
  }
  </style>
  