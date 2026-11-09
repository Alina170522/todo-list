<script setup>
import AppIcon from './AppIcon.vue'
import { REPO_URL, AUTHOR } from '../config.js'

const year = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="footer__row">
      <p>© {{ year }} {{ AUTHOR }} · тестовое задание</p>
      <p>Задачи сохраняются в этом браузере</p>
    </div>
    <a class="footer__link" :href="REPO_URL" target="_blank" rel="noopener noreferrer">
      <AppIcon name="brand-github" :size="15" />
      Код на GitHub
    </a>
  </footer>
</template>

<style scoped>
.footer {
  width: min(704px, 100% - 24px);
  margin: auto auto 0;
  padding: 14px 0 20px;
  font-size: 12px;
  line-height: 1.6;
  color: var(--c-text-2);
  border-top: 1px solid #e3e5ea;
}

.footer__row {
  display: flex;
  justify-content: space-between;
  gap: 4px 16px;
  flex-wrap: wrap;
}

.footer__link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-top: 4px;
  color: var(--c-text);
  text-decoration: underline;
  text-decoration-color: #b0b2ba;
  text-underline-offset: 3px;
}

.footer__link:hover {
  text-decoration-color: currentColor;
}

@media (max-width: 600px) {
  .footer__row {
    flex-direction: column;
  }
}
</style>
