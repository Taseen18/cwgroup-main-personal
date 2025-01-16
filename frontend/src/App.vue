<template>
    <div>
    <Navbar />
    <main class="container pt-4">
      <RouterView class="flex-shrink-0" />
    </main>
  </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { RouterView } from "vue-router";
  import Navbar from "../src/components/Navbar.vue";
  
  export default defineComponent({
    components: { RouterView,
      Navbar,
     },
  });
  </script>
  
  <style scoped>
  </style>
  
