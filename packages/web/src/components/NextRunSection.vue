<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { ExperimentMeta } from '@/types/experiment'
import ExperimentMeta_ from './ExperimentMeta.vue'
defineProps<{ meta: ExperimentMeta }>()
const { t } = useI18n()
</script>

<template>
  <section id="next" class="block">
    <p class="kicker">{{ t('next.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-4">{{ t('next.title') }}</h2>
    <ExperimentMeta_ :meta="meta" />
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem,5vw,3.6rem) 0; border-top: 1px solid var(--line); }
</style>
