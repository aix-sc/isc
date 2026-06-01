<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { ExperimentMeta } from '@/types/experiment'

defineProps<{ meta: ExperimentMeta }>()
const { t } = useI18n()
</script>

<template>
  <div>
    <h3 class="exp-name serif">{{ meta.name }}</h3>
    <v-alert type="info" variant="tonal" density="comfortable" class="mb-4">
      {{ t('experiments.plannedNote') }}
    </v-alert>

    <v-card class="pa-5">
      <div class="field">
        <h4>{{ t('meta.purpose') }}</h4>
        <p>{{ meta.purpose }}</p>
      </div>
      <div class="field">
        <h4>{{ t('experiments.approach') }}</h4>
        <p>{{ meta.data }}</p>
      </div>
      <div class="field">
        <h4>{{ t('meta.evaluation') }}</h4>
        <p>{{ meta.evaluation }}</p>
      </div>
      <div v-if="meta.outcomes" class="field outcomes">
        <h4>{{ t('experiments.outcomes') }}</h4>
        <p>{{ meta.outcomes }}</p>
      </div>
    </v-card>
  </div>
</template>

<style scoped lang="scss">
.exp-name { font-weight: 600; font-size: 1.15rem; color: var(--navy); margin-bottom: .8rem; }
.field { padding: .2rem 0 .9rem; }
.field + .field { border-top: 1px dashed var(--line); padding-top: .9rem; }
.field h4 { font-family: var(--mono); font-size: .68rem; text-transform: uppercase; letter-spacing: .1em; color: var(--teal); margin-bottom: .35rem; }
.field p { font-size: .92rem; color: var(--soft); line-height: 1.6; max-width: 70ch; }
.outcomes {
  background: var(--ts); border: 1px solid #BFE0DA; border-radius: 11px; padding: .9rem 1.1rem; margin-top: .4rem;
  h4 { color: var(--teal); }
  p { color: var(--ink); }
}
.outcomes.field + .field, .field + .outcomes.field { border-top: none; }
</style>
