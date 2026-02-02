<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const scrollToTable = async () => {
  if (route.path !== '/') {
    await router.push('/')
  }
  
  // Aguarda a transição e a renderização
  setTimeout(() => {
    const element = document.getElementById('operadoras-table')
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }, 100)
}
</script>

<template>
  <div class="app-layout">
    <nav class="navbar glass-card">
      <div class="nav-content container">
        <router-link to="/" class="logo" style="text-decoration: none; color: inherit;">
          <div class="logo-icon">ANS</div>
          <span>Analytics Dashboard</span>
        </router-link>
        <div class="nav-links">
          <a href="/#operadoras-table" @click.prevent="scrollToTable" :class="{ active: $route.path === '/' }">Operadoras</a>
        </div>
      </div>
    </nav>

    <main class="container">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.navbar {
  margin: 1rem;
  border-radius: 1rem;
  position: sticky;
  top: 1rem;
  z-index: 100;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  font-size: 1.25rem;
}

.logo-icon {
  background: var(--primary);
  color: white;
  padding: 0.25rem 0.6rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
}

.nav-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.nav-links a.active {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

/* Page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
