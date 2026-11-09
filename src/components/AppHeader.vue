<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import AppIcon from './AppIcon.vue'
import { useToday } from '../composables/useToday.js'
import { monthGenitive, weekdayName, monthTitle, monthGrid, WEEKDAYS_SHORT } from '../utils/date.js'

const today = useToday()
const open = ref(false)
const root = ref(null)
const button = ref(null)

const day = computed(() => today.value.getDate())
const month = computed(() => monthGenitive(today.value))
const weekday = computed(() => weekdayName(today.value))
const title = computed(() => monthTitle(today.value))
const weeks = computed(() => monthGrid(today.value))

function toggle() {
  open.value = !open.value
}

function close({ returnFocus = false } = {}) {
  if (!open.value) return
  open.value = false
  if (returnFocus) button.value?.focus()
}

function onDocumentClick(event) {
  if (root.value && !root.value.contains(event.target)) close()
}

function onKeydown(event) {
  if (event.key === 'Escape') close({ returnFocus: true })
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <header class="header">
    <div ref="root" class="date">
      <button
        ref="button"
        type="button"
        class="date__button"
        :aria-expanded="open"
        aria-controls="calendar"
        @click="toggle"
      >
        <span class="date__day">{{ day }}</span>
        <span class="date__meta">
          <span class="date__month">{{ month }}</span>
          <span class="date__weekday">{{ weekday }}</span>
        </span>
        <AppIcon :name="open ? 'chevron-up' : 'chevron-down'" :size="14" class="date__chevron" />
        <span class="sr-only">, показать календарь</span>
      </button>

      <div v-show="open" id="calendar" class="calendar">
        <table class="calendar__table">
          <caption class="calendar__title">{{ title }}</caption>
          <thead>
            <tr>
              <th v-for="name in WEEKDAYS_SHORT" :key="name" scope="col">{{ name }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(week, w) in weeks" :key="w">
              <td
                v-for="(date, d) in week"
                :key="d"
                :class="{ 'is-today': date === day, 'is-weekend': d >= 5 }"
                :aria-current="date === day ? 'date' : undefined"
              >
                {{ date ?? '' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <p class="brand">Список дел</p>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 0.5px solid #dcdee4;
}

.date {
  position: relative;
}

.date__button {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  margin-left: -8px;
  padding: 4px 8px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  text-align: left;
}

.date__button:hover {
  background: rgba(23, 23, 26, 0.05);
}

.date__day {
  font-size: 42px;
  font-weight: 500;
  line-height: 0.85;
}

.date__meta {
  display: flex;
  flex-direction: column;
  padding-bottom: 1px;
}

.date__month {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.1;
}

.date__weekday {
  font-size: 12px;
  letter-spacing: 0.08em;
  color: var(--c-accent);
}

.date__chevron {
  margin-bottom: 3px;
  color: var(--c-text-2);
}

.calendar {
  position: absolute;
  top: calc(100% + 8px);
  left: -8px;
  z-index: 20;
  width: 232px;
  padding: 12px 12px 10px;
  background: #fff;
  border: 0.5px solid #ebf0f3;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(23, 23, 26, 0.08);
}

.calendar__table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  text-align: center;
  cursor: default;
  user-select: none;
}

.calendar__title {
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 500;
  text-align: left;
}

.calendar__table th {
  height: 24px;
  font-weight: 400;
  font-size: 11px;
  color: var(--c-text-2);
}

.calendar__table td {
  width: 30px;
  height: 28px;
  padding: 0;
}

.calendar__table td.is-weekend {
  color: var(--c-text-2);
}

.calendar__table td.is-today {
  font-weight: 500;
  color: #fff;
  background: radial-gradient(circle, var(--c-accent) 12px, transparent 12.5px);
}

.brand {
  font-size: 30px;
  font-weight: 500;
  line-height: 1;
}

@media (max-width: 600px) {
  .date__day {
    font-size: 34px;
  }

  .brand {
    font-size: 22px;
  }
}
</style>
