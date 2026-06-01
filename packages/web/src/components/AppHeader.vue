<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { GITHUB_URL } from '@/data/experiments'
import { useLocale } from '@/composables/useLocale'

const { t } = useI18n()
const { current, change } = useLocale()

const links = computed(() => [
  { t: t('nav.overview'), h: '#overview' }, { t: t('nav.experiments'), h: '#experiments' },
  { t: t('nav.next'), h: '#next' }, { t: t('nav.faq'), h: '#faq' },
])

function toggleLocale() {
  change(current.value === 'ja' ? 'en' : 'ja')
}
</script>

<template>
  <v-app-bar flat height="58" class="nav" border>
    <a href="#top" class="brand">
      <img class="bmk" src="https://avatars.githubusercontent.com/u/289632491?s=400&u=99388cfe479cdadc79f93e0d846277f7eb18e490&v=4"
           alt="AIx" width="32" height="32" />
      <span class="bmt d-none d-sm-inline">{{ t('nav.brandTagline') }}</span>
    </a>
    <v-spacer />
    <a v-for="l in links" :key="l.h" :href="l.h" class="nl d-none d-md-inline">{{ l.t }}</a>
    <button class="lang" :aria-label="t('lang.label')" :title="t('lang.label')" @click="toggleLocale">
      <span :class="{ on: current === 'en' }">EN</span>
      <span class="sep">/</span>
      <span :class="{ on: current === 'ja' }">日本語</span>
    </button>
    <a :href="GITHUB_URL" target="_blank" rel="noopener" class="gh">{{ t('nav.github') }}</a>
  </v-app-bar>
</template>

<style scoped lang="scss">
.nav { background: rgba(251,250,247,.86) !important; backdrop-filter: blur(10px); padding: 0 clamp(1rem,4vw,3rem); }
.brand { display: flex; align-items: center; gap: .6rem; text-decoration: none; }
.bmk { width: 32px; height: 32px; border-radius: 8px; object-fit: cover; display: block; }
.bmt { font-size: .8rem; color: var(--soft); font-weight: 500; }
.nl { color: var(--soft); font-size: .82rem; text-decoration: none; margin: 0 .55rem; }
.nl:hover { color: var(--teal); }
.lang {
  display: inline-flex; align-items: center; gap: .25rem; background: none; border: none; cursor: pointer;
  font-family: var(--mono); font-size: .74rem; color: var(--mute); padding: .3rem .5rem; margin-left: .4rem;
  span.on { color: var(--navy); font-weight: 700; }
  .sep { color: var(--line); }
}
.lang:hover span:not(.sep) { color: var(--teal); }
.gh { font-family: var(--mono); font-size: .74rem; border: 1px solid var(--line); padding: .3rem .6rem; border-radius: 8px; color: var(--navy); text-decoration: none; margin-left: .4rem; }
</style>
