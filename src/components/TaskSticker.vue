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
  <!-- Стикер прикреплён скрепкой к правому краю рамки карточки.
       Слои снизу вверх: листок-подложка → задняя часть скрепки → бумага → передняя часть скрепки. -->
  <div class="sticker">
    <div class="sticker__under" aria-hidden="true"></div>

    <svg class="clip clip--back" viewBox="0 0 62 22" aria-hidden="true" focusable="false">
      <path d="M32 9 H53 a5 5 0 0 1 0 10 H12 a8.5 8.5 0 0 1 0 -17 H48" />
    </svg>

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

    <svg class="clip clip--front" viewBox="0 0 62 22" aria-hidden="true" focusable="false">
      <path class="clip__shadow" d="M39.4 20.5 H13.4 a8.5 8.5 0 0 1 0 -17 H39.4" />
      <path class="clip__wire" d="M38 19 H12 a8.5 8.5 0 0 1 0 -17 H38" />
      <path class="clip__shine" d="M38 19 H12 a8.5 8.5 0 0 1 0 -17 H38" />
      <path class="clip__wire" d="M38 9 H53 a5 5 0 0 1 0 10 H38" />
      <path class="clip__shine" d="M38 9 H53 a5 5 0 0 1 0 10 H38" />
    </svg>
  </div>
</template>

<style scoped>
.sticker {
  --torn: polygon(0 6%, 5% 2%, 10% 5%, 16% 1%, 22% 4%, 28% 0, 35% 4%, 42% 1%, 50% 5%, 57% 1%, 64% 4%, 71% 0, 78% 4%, 85% 1%, 92% 5%, 100% 2%, 100% 96%, 93% 99%, 86% 95%, 79% 100%, 71% 96%, 63% 99%, 55% 95%, 47% 100%, 39% 96%, 31% 99%, 23% 95%, 15% 100%, 8% 96%, 0 99%);
  --w: 180px;
  --h: 124px;
  --overhang: 8px; /* насколько стикер заходит за рамку карточки */
  --clip-scale: 1;
  --clip-x: 38; /* точка скрепки (в единицах её рисунка), которая ложится на рамку */
  --clip-top: 30px;

  position: absolute;
  top: 0;
  /* --card-pad-x задаётся карточкой: стикер выходит за её внутренний отступ и рамку */
  right: calc(-1 * (var(--card-pad-x, 32px) + var(--overhang)));
  z-index: 1;
  width: var(--w);
  height: var(--h);
}

.sticker__under,
.sticker__paper {
  position: absolute;
  clip-path: var(--torn);
}

/* Листок выглядывает снизу и узкой полоской слева, подальше от скрепки */
.sticker__under {
  inset: 12px 12px -9px -4px;
  background: var(--c-accent-mark);
  transform: rotate(-2.5deg);
}

.sticker__paper {
  inset: 0;
  z-index: 2;
  padding: 18px 20px 10px;
  background: var(--c-paper);
  transform: rotate(1.5deg);
}

.clip {
  position: absolute;
  top: var(--clip-top);
  left: calc(var(--w) - var(--overhang) - var(--clip-x) * var(--clip-scale) * 1px);
  width: calc(62px * var(--clip-scale));
  height: calc(22px * var(--clip-scale));
  overflow: visible;
  pointer-events: none;
  fill: none;
  stroke-linecap: round;
}

.clip--back {
  z-index: 1;
  stroke: #7c8288;
  stroke-width: 2.4;
}

.clip--front {
  z-index: 3;
}

.clip__shadow {
  stroke: rgba(80, 60, 30, 0.2);
  stroke-width: 2.4;
}

.clip__wire {
  stroke: #868c92;
  stroke-width: 2.4;
}

.clip__shine {
  stroke: #dadee1;
  stroke-width: 0.8;
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

/* Телефон: стикер и скрепка меньше, чтобы петли скрепки не выходили за экран */
@media (max-width: 600px) {
  .sticker {
    --w: 132px;
    --h: 96px;
    --overhang: 6px;
    --clip-scale: 0.7;
    --clip-x: 40;
    --clip-top: 22px;
  }

  .sticker__under {
    inset: 9px 9px -7px -3px;
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

/* Совсем узкие экраны: стикер чуть меньше, чтобы не заезжать на «что сделать сегодня?» */
@media (max-width: 359px) {
  .sticker {
    transform: scale(0.9);
    transform-origin: top right;
  }
}
</style>
