<script setup>
import { ref, watch } from 'vue'
import AppIcon from './AppIcon.vue'
import { MAX_LENGTH } from '../composables/useTasks.js'

const props = defineProps({
  inputId: { type: String, required: true },
})

const emit = defineEmits(['add'])

const text = ref('')
const error = ref('')
const input = ref(null)
const errorId = `${props.inputId}-error`

function submit() {
  if (!text.value.trim()) {
    error.value = 'Введите текст задачи'
    input.value?.focus()
    return
  }
  emit('add', text.value)
  text.value = ''
  error.value = ''
  input.value?.focus()
}

watch(text, () => {
  if (error.value) error.value = ''
})

defineExpose({ focus: () => input.value?.focus() })
</script>

<template>
  <form class="form" novalidate @submit.prevent="submit">
    <div class="form__row">
      <input
        :id="inputId"
        ref="input"
        v-model="text"
        class="form__input"
        :class="{ 'is-invalid': error }"
        type="text"
        :maxlength="MAX_LENGTH"
        autocomplete="off"
        enterkeyhint="done"
        placeholder="Купить хлеб"
        :aria-invalid="error ? 'true' : 'false'"
        :aria-describedby="errorId"
      />
      <button type="submit" class="form__button">
        <AppIcon name="plus" :size="16" />
        <span>Добавить</span>
      </button>
    </div>
    <p :id="errorId" class="form__error" aria-live="polite">{{ error }}</p>
  </form>
</template>

<style scoped>
.form {
  margin-top: 22px;
}

.form__row {
  display: flex;
  gap: 10px;
}

.form__input {
  flex: 1;
  min-width: 0;
  height: 44px;
  padding: 0 18px;
  font-size: 14px;
  background: #fff;
  border: 1px solid var(--c-border);
  border-radius: 999px;
  transition: box-shadow 0.15s, border-color 0.15s;
}

.form__input::placeholder {
  color: var(--c-muted);
}

.form__input:focus {
  outline: none;
  border-color: var(--c-accent);
  box-shadow: 0 0 0 3px var(--c-accent-mark);
}

.form__input.is-invalid {
  border-color: #e24b4a;
  background: #fdf3f3;
  box-shadow: 0 0 0 3px rgba(226, 75, 74, 0.18);
}

.form__button {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 44px;
  padding: 0 20px;
  font-size: 14px;
  color: #fff;
  background: var(--c-btn);
  border: 0;
  border-radius: 999px;
}

.form__button:hover {
  background: #2c2c31;
}

.form__error {
  min-height: 20px;
  margin: 6px 0 0 18px;
  font-size: 13px;
  color: var(--c-error);
}

/* На телефоне шрифт поля 16px — иначе Safari на iPhone приближает страницу при фокусе */
@media (max-width: 600px) {
  .form__input {
    font-size: 16px;
    padding: 0 14px;
  }

  .form__button {
    padding: 0 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .form__input {
    transition: none;
  }
}
</style>
