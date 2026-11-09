<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import AppHeader from './components/AppHeader.vue'
import TaskSticker from './components/TaskSticker.vue'
import TaskForm from './components/TaskForm.vue'
import TaskItem from './components/TaskItem.vue'
import AppFooter from './components/AppFooter.vue'
import { useTasks } from './composables/useTasks.js'

const INPUT_ID = 'new-task'

const { tasks, activeTasks, doneCount, add, toggle, remove, undo, isPending, secondsLeft } = useTasks()

const form = ref(null)

const allDone = computed(
  () => activeTasks.value.length > 0 && doneCount.value === activeTasks.value.length,
)

// Когда задача удалилась окончательно и фокус «потерялся», возвращаем его в поле ввода.
watch(
  () => tasks.value.length,
  async (length, oldLength) => {
    if (length >= oldLength) return
    await nextTick()
    if (document.activeElement === document.body) form.value?.focus()
  },
)
</script>

<template>
  <div class="page">
    <main class="card">
      <AppHeader />

      <section class="intro" aria-labelledby="page-title">
        <div class="intro__text">
          <label :for="INPUT_ID" class="bubble">что сделать сегодня?</label>
          <h1 id="page-title" class="title">Мои <span class="title__mark">дела</span></h1>
        </div>
        <TaskSticker :total="activeTasks.length" :done="doneCount" />
      </section>

      <TaskForm ref="form" :input-id="INPUT_ID" @add="add" />

      <p v-if="tasks.length === 0" class="quote">
        Постановка целей — это первый шаг к превращению невидимого в видимое.
      </p>

      <ul v-else class="list" aria-label="Задачи">
        <TaskItem
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          :pending="isPending(task.id)"
          :seconds-left="secondsLeft(task.id)"
          @toggle="toggle(task.id)"
          @remove="remove(task.id)"
          @undo="undo(task.id)"
        />
      </ul>

      <p v-if="allDone" class="quote">Успех — это награда за упорный труд.</p>
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  min-height: inherit;
}

.card {
  width: min(640px, 100% - 24px);
  margin: 32px auto 24px;
  padding: 28px 32px 20px;
  background: rgba(255, 255, 255, 0.3);
  -webkit-backdrop-filter: blur(1.5px);
  backdrop-filter: blur(1.5px);
  border: 1px solid rgba(220, 222, 228, 0.95);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(23, 23, 26, 0.05);
}

.intro {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px 20px;
  margin-top: 18px;
}

.bubble {
  display: inline-block;
  padding: 7px 14px;
  font-size: 13px;
  color: var(--c-accent);
  background: var(--c-accent-soft);
  border-radius: 999px 999px 999px 4px;
  cursor: pointer;
}

.bubble:hover {
  color: #5e4a75; /* темнее акцента, чтобы на тёмном фоне контраст оставался ≥ 4,5:1 */
  background: var(--c-accent-mark);
}

.title {
  margin-top: 12px;
  font-size: clamp(26px, 6vw, 34px);
  font-weight: 500;
  line-height: 1.2;
}

.title__mark {
  position: relative;
  padding: 0 4px;
  background: var(--c-accent-mark);
}

.title__mark::before,
.title__mark::after {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--c-accent);
  border-radius: 50%;
}

.title__mark::before {
  top: -6px;
  left: -5px;
}

.title__mark::after {
  right: -5px;
  bottom: -6px;
}

.list {
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
}

@media (max-width: 600px) {
  .card {
    margin: 12px auto 20px;
    padding: 18px 16px 14px;
    border-radius: 16px;
  }

  .bubble {
    padding: 6px 12px;
    font-size: 12px;
  }

  .intro {
    gap: 12px;
  }
}
</style>
