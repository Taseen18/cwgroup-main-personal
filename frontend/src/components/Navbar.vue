<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <!-- Logo or brand -->
        <router-link class="navbar-brand" to="/">Group 19 CWK</router-link>
  
        <!-- Toggler for mobile view -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
  
        <!-- Navbar links -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <!-- Link to ProfilePage -->
              <router-link class="nav-link" to="/">Profile Page</router-link>
            </li>
            <li class="nav-item">
              <!-- Link to CommonHobbyPage -->
              <router-link class="nav-link" to="/common-hobbies/">Common Hobbies Page</router-link>
            </li>
            <li class="nav-item">
              <!-- Link to FriendsPage -->
              <router-link class="nav-link" to="/friends-list/">Friends Page</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "Navbar",
  });
  </script>
  
  <style scoped>
  /* Optional styling overrides here. currently just using defualt*/
  </style>
  
