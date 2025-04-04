// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import CommonHobbiesPage from '../pages/CommonHobbiesPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import FriendsPage from '../pages/FriendsPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Profile Page', component: ProfilePage },
        { path: '/other/', name: 'Other Page', component: OtherPage },
        { path: '/common-hobbies/', name: 'Common Hobbies Page', component: CommonHobbiesPage },
        { path: '/friends-list/', name: 'Friends Page', component: FriendsPage}
    ]
})

export default router
