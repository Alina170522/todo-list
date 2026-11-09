import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

export const STORAGE_KEY = 'todo-list:v1'
export const UNDO_SECONDS = 5
export const MAX_LENGTH = 200

/** Читает задачи из localStorage. Повреждённые или чужие данные не ломают страницу. */
function loadTasks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const data = JSON.parse(raw)
    if (!Array.isArray(data)) return []
    return data
      .filter((t) => t && typeof t.id === 'string' && typeof t.text === 'string' && t.text.trim())
      .map((t) => ({ id: t.id, text: t.text.slice(0, MAX_LENGTH), done: Boolean(t.done) }))
  } catch {
    return []
  }
}

function saveTasks(tasks) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks))
  } catch {
    // Хранилище недоступно (приватный режим, переполнение) — список работает до закрытия вкладки.
  }
}

function makeId() {
  if (globalThis.crypto?.randomUUID) return crypto.randomUUID()
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`
}

/**
 * Состояние списка дел.
 *
 * Удаление в два шага: задача сначала помечается «удаляется» на UNDO_SECONDS секунд
 * и остаётся в localStorage. Только по окончании отсчёта она удаляется окончательно.
 * Поэтому, если обновить страницу во время отсчёта, задача вернётся.
 */
export function useTasks() {
  const tasks = ref(loadTasks())
  const deadlines = ref(new Map()) // id → время окончательного удаления, мс
  const now = ref(Date.now())
  const timers = new Map()
  let ticker = null

  watch(tasks, saveTasks, { deep: true })

  function startTicker() {
    if (!ticker) ticker = setInterval(() => (now.value = Date.now()), 250)
  }

  function stopTickerIfIdle() {
    if (deadlines.value.size === 0 && ticker) {
      clearInterval(ticker)
      ticker = null
    }
  }

  function isPending(id) {
    return deadlines.value.has(id)
  }

  function add(text) {
    const value = text.trim().slice(0, MAX_LENGTH)
    if (!value) return false
    tasks.value.push({ id: makeId(), text: value, done: false })
    return true
  }

  function toggle(id) {
    if (isPending(id)) return
    const task = tasks.value.find((t) => t.id === id)
    if (task) task.done = !task.done
  }

  function remove(id) {
    if (isPending(id)) return // защита от двойного нажатия
    deadlines.value.set(id, Date.now() + UNDO_SECONDS * 1000)
    now.value = Date.now()
    startTicker()
    timers.set(id, setTimeout(() => finalizeRemove(id), UNDO_SECONDS * 1000))
  }

  function finalizeRemove(id) {
    timers.delete(id)
    deadlines.value.delete(id)
    tasks.value = tasks.value.filter((t) => t.id !== id)
    stopTickerIfIdle()
  }

  function undo(id) {
    clearTimeout(timers.get(id))
    timers.delete(id)
    deadlines.value.delete(id)
    stopTickerIfIdle()
  }

  function secondsLeft(id) {
    const deadline = deadlines.value.get(id)
    if (!deadline) return 0
    return Math.max(1, Math.ceil((deadline - now.value) / 1000))
  }

  // Задачи без учёта тех, что сейчас удаляются, — по ним считается стикер.
  const activeTasks = computed(() => tasks.value.filter((t) => !deadlines.value.has(t.id)))
  const doneCount = computed(() => activeTasks.value.filter((t) => t.done).length)

  // Если список открыт в двух вкладках, подтягиваем изменения из другой вкладки.
  function onStorage(event) {
    if (event.key === STORAGE_KEY) tasks.value = loadTasks()
  }

  onMounted(() => window.addEventListener('storage', onStorage))

  onBeforeUnmount(() => {
    window.removeEventListener('storage', onStorage)
    timers.forEach(clearTimeout)
    clearInterval(ticker)
  })

  return { tasks, activeTasks, doneCount, add, toggle, remove, undo, isPending, secondsLeft }
}
