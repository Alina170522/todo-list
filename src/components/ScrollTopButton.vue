<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import AppIcon from './AppIcon.vue'

const emit = defineEmits(['activate'])

const visible = ref(false)
let frame = 0

// Кнопка нужна, только когда страница длинная и прокручена дальше первого экрана.
function update() {
  frame = 0
  const pageIsLong = document.documentElement.scrollHeight > window.innerHeight * 1.3
  visible.value = pageIsLong && window.scrollY > window.innerHeight * 0.6
}

function onScroll() {
  if (!frame) frame = requestAnimationFrame(update)
}

function goTop() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' })
  emit('activate')
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll)
  update()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
  cancelAnimationFrame(frame)
})
</script>

<template>
  <Transition name="to-top">
    <button
      v-show="visible"
      type="button"
      class="to-top"
      aria-label="Наверх, к добавлению задачи"
      @click="goTop"
    >
      <AppIcon name="arrow-up" :size="22" />
    </button>
  </Transition>
</template>

<style scoped>
.to-top {
  position: fixed;
  right: max(24px, env(safe-area-inset-right));
  bottom: calc(24px + env(safe-area-inset-bottom));
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  padding: 0;
  color: #fff;
  background: var(--c-accent);
  border: 0;
  border-radius: 50%;
  box-shadow: 0 4px 14px rgba(70, 50, 95, 0.28);
}

.to-top:hover {
  background: #66527c;
}

.to-top:focus-visible {
  outline-offset: 3px;
}

.to-top-enter-active,
.to-top-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.to-top-enter-from,
.to-top-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 600px) {
  .to-top {
    right: max(16px, env(safe-area-inset-right));
    bottom: calc(20px + env(safe-area-inset-bottom));
  }
}

@media (prefers-reduced-motion: reduce) {
  .to-top-enter-active,
  .to-top-leave-active {
    transition: none;
  }
}
</style>
