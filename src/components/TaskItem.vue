<script setup>
import { ref, watch, nextTick } from 'vue'
import AppIcon from './AppIcon.vue'
import { UNDO_SECONDS } from '../composables/useTasks.js'

const props = defineProps({
  task: { type: Object, required: true },
  pending: { type: Boolean, default: false },
  secondsLeft: { type: Number, default: 0 },
})

const emit = defineEmits(['toggle', 'remove', 'undo'])

const removeButton = ref(null)
const undoButton = ref(null)

// Фокус не теряется: после нажатия на корзину — на «Вернуть», после возврата — снова на корзину.
watch(
  () => props.pending,
  async (isPending, wasPending) => {
    await nextTick()
    if (isPending) undoButton.value?.focus()
    else if (wasPending) removeButton.value?.focus()
  },
)
</script>

<template>
  <li class="item" :class="{ 'is-done': task.done, 'is-pending': pending }">
    <div class="item__row">
      <label class="check">
        <input
          class="check__input"
          type="checkbox"
          :checked="task.done"
          :disabled="pending"
          @change="emit('toggle')"
        />
        <span class="check__box" aria-hidden="true">
          <AppIcon name="check" :size="15" />
        </span>
        <span class="check__text"><span class="check__pill">{{ task.text }}</span></span>
      </label>

      <button
        ref="removeButton"
        type="button"
        class="item__remove"
        :class="{ 'is-hidden': pending }"
        :tabindex="pending ? -1 : 0"
        :aria-hidden="pending ? 'true' : undefined"
        :aria-label="`Удалить задачу «${task.text}»`"
        @click="emit('remove')"
      >
        <AppIcon name="trash" :size="19" />
      </button>
    </div>

    <div v-if="pending" class="undo">
      <span aria-hidden="true">Задача удалится через {{ secondsLeft }} с</span>
      <span class="sr-only" role="status">
        Задача удалена. Её можно вернуть в течение {{ UNDO_SECONDS }} секунд.
      </span>
      <button ref="undoButton" type="button" class="undo__button" @click="emit('undo')">
        <AppIcon name="arrow-back-up" :size="15" />
        Вернуть
      </button>
    </div>
  </li>
</template>

<style scoped>
.item {
  border-bottom: 0.5px dashed var(--c-line);
}

.item:last-child {
  border-bottom: 0;
}

.item__row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
}

.check {
  position: relative;
  display: flex;
  flex: 1;
  align-items: center;
  gap: 12px;
  min-width: 0;
  cursor: pointer;
}

.check__input {
  position: absolute;
  top: 50%;
  left: 0;
  width: 26px;
  height: 26px;
  margin: 0;
  opacity: 0;
  transform: translateY(-50%);
  cursor: pointer;
}

.check__box {
  display: flex;
  flex: 0 0 26px;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  color: transparent;
  background: #fff;
  border: 1.5px solid var(--c-accent);
  border-radius: 50%;
}

.check__input:checked + .check__box {
  color: #fff;
  background: var(--c-accent);
}

.check__input:focus-visible + .check__box {
  outline: 2px solid var(--c-accent);
  outline-offset: 2px;
}

/* Полупрозрачным делаем только нарисованный кружок.
   Настоящий чекбокс всегда остаётся невидимым (opacity: 0), иначе проступает квадратом. */
.check__input:disabled {
  cursor: default;
}

.check__input:disabled + .check__box {
  opacity: 0.4;
}

.is-pending .check {
  cursor: default;
}

.check__text {
  flex: 1;
  min-width: 0;
  font-size: 15px;
  line-height: 2;
  overflow-wrap: anywhere;
}

.check__pill {
  padding: 3px 8px;
  background: var(--c-accent-soft);
  border-radius: 6px;
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
}

.is-done .check__pill,
.is-pending .check__pill {
  background: transparent;
  color: var(--c-muted);
}

.is-done .check__pill {
  text-decoration: line-through;
}

.item__remove {
  display: flex;
  flex: 0 0 40px;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  color: var(--c-icon);
  background: transparent;
  border: 0;
  border-radius: 8px;
}

.item__remove:hover {
  color: var(--c-text);
}

.item__remove.is-hidden {
  visibility: hidden;
}

.undo {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin: 2px 0 10px 38px;
  padding: 6px 6px 6px 14px;
  font-size: 13px;
  color: var(--c-accent);
  background: var(--c-accent-soft);
  border-radius: 12px;
}

.undo::before {
  content: '';
  position: absolute;
  top: -5px;
  left: 18px;
  width: 10px;
  height: 10px;
  background: var(--c-accent-soft);
  transform: rotate(45deg);
}

.undo__button {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 14px;
  font-size: 13px;
  color: #fff;
  background: var(--c-accent);
  border: 0;
  border-radius: 999px;
}

.undo__button:hover {
  background: #66527c;
}
</style>
