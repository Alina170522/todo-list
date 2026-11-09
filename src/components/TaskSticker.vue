<script setup>
import { computed } from 'vue'
import { plural, TASK_FORMS } from '../utils/text.js'

const props = defineProps({
  total: { type: Number, required: true },
  done: { type: Number, required: true },
})

const word = computed(() => plural(props.total, TASK_FORMS))
</script>

<template>
  <div class="sticker">
    <div class="sticker__under" aria-hidden="true"></div>
    <div class="sticker__paper">
      <p class="sticker__label">на сегодня</p>
      <p class="sticker__count">
        {{ total }} <span class="sticker__word">{{ word }}</span>
      </p>
      <p v-if="total > 0" class="sticker__done">
        <span aria-hidden="true">сделано {{ done }}/{{ total }}</span>
        <span class="sr-only">сделано {{ done }} из {{ total }}</span>
      </p>
    </div>
  </div>
</template>

<style scoped>
.sticker {
  --torn: polygon(0 6%, 5% 2%, 10% 5%, 16% 1%, 22% 4%, 28% 0, 35% 4%, 42% 1%, 50% 5%, 57% 1%, 64% 4%, 71% 0, 78% 4%, 85% 1%, 92% 5%, 100% 2%, 100% 96%, 93% 99%, 86% 95%, 79% 100%, 71% 96%, 63% 99%, 55% 95%, 47% 100%, 39% 96%, 31% 99%, 23% 95%, 15% 100%, 8% 96%, 0 99%);
  position: relative;
  flex: 0 0 auto;
  width: 180px;
  height: 124px;
  margin: 8px 8px 0 0;
}

.sticker__under,
.sticker__paper {
  position: absolute;
  clip-path: var(--torn);
}

.sticker__under {
  inset: 8px -8px -6px 10px;
  background: var(--c-accent-mark);
  transform: rotate(-4deg);
}

.sticker__paper {
  inset: 0;
  padding: 18px 20px 10px;
  background: var(--c-paper);
  transform: rotate(1.5deg);
}

.sticker__label {
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--c-text-2);
}

.sticker__count {
  margin-top: 2px;
  font-size: 32px;
  font-weight: 500;
  line-height: 1.15;
}

.sticker__word {
  font-size: 17px;
}

.sticker__done {
  margin-top: 2px;
  font-family: var(--font-hand);
  font-size: 24px;
  line-height: 1.2;
  color: var(--c-accent);
  transform: rotate(-3deg);
  transform-origin: left center;
}

@media (max-width: 480px) {
  .sticker {
    width: 134px;
    height: 98px;
    margin: 4px 6px 0 0;
  }

  .sticker__paper {
    padding: 14px 14px 8px;
  }

  .sticker__label {
    font-size: 11px;
  }

  .sticker__count {
    font-size: 24px;
  }

  .sticker__word {
    font-size: 14px;
  }

  .sticker__done {
    font-size: 19px;
  }
}
</style>
