<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { getRoadmap } from '@/data/roadmap'
import type { Locale } from '@/i18n'

const { t, locale } = useI18n()
const items = computed(() => getRoadmap(locale.value as Locale))
</script>

<template>
  <section id="roadmap" class="block">
    <p class="kicker">{{ t('roadmap.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-2">{{ t('roadmap.title') }}</h2>
    <p class="lede">{{ t('roadmap.lede') }}</p>

    <div class="grid">
      <v-card v-for="it in items" :key="it.id" class="pa-4 item">
        <h3 class="name">{{ it.name }}</h3>
        <p class="note">{{ it.note }}</p>
      </v-card>
    </div>

    <p class="policy">{{ t('roadmap.policy') }}</p>
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem, 5vw, 3.6rem) 0; border-top: 1px solid var(--line); }
.lede { max-width: 760px; color: var(--mute); margin-bottom: 1.1rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 1rem; }
.item { border-left: 3px solid var(--line); }
.name { font-size: .92rem; font-weight: 600; color: var(--navy); margin-bottom: .4rem; }
.note { font-size: .82rem; line-height: 1.6; color: var(--mute); }
.policy {
  margin-top: 1.1rem; font-size: .78rem; color: var(--mute);
  border-left: 3px solid var(--teal); padding-left: .8rem;
}
</style>
