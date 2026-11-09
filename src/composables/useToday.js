import { ref, onMounted, onBeforeUnmount } from 'vue'
import { isSameDay } from '../utils/date.js'

/**
 * Текущая дата, которая сама обновляется после полуночи
 * и когда пользователь возвращается на вкладку.
 */
export function useToday() {
  const today = ref(new Date())
  let timer = null

  function refresh() {
    const now = new Date()
    if (!isSameDay(now, today.value)) today.value = now
  }

  onMounted(() => {
    timer = setInterval(refresh, 60_000)
    document.addEventListener('visibilitychange', refresh)
  })

  onBeforeUnmount(() => {
    clearInterval(timer)
    document.removeEventListener('visibilitychange', refresh)
  })

  return today
}
