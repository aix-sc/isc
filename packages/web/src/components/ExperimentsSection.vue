<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { ExperimentMeta, ExpCSummary, CostRow } from '@/types/experiment'
import CostModelSection from './CostModelSection.vue'
import MaintenanceSection from './MaintenanceSection.vue'
import PlannedExperiment from './PlannedExperiment.vue'

const props = defineProps<{
  experiments: ExperimentMeta[]
  summary: ExpCSummary | null
  costRows: CostRow[]
}>()

const { t } = useI18n()
const tab = ref<'A' | 'B' | 'C' | 'D'>('A')

const byId = (id: string): ExperimentMeta =>
  props.experiments.find((e) => e.id === id) ?? props.experiments[0]
const metaA = computed(() => byId('A'))
const metaB = computed(() => byId('B'))
const metaC = computed(() => byId('C'))
const metaD = computed(() => byId('D'))

const tabs = computed(() => [
  { id: 'A' as const, label: t('experiments.tabs.A'), kind: t('experiments.status.interactive') },
  { id: 'B' as const, label: t('experiments.tabs.B'), kind: t('experiments.status.planned') },
  { id: 'C' as const, label: t('experiments.tabs.C'), kind: t('experiments.status.completed') },
  { id: 'D' as const, label: t('experiments.tabs.D'), kind: t('experiments.status.planned') },
])
</script>

<template>
  <section id="experiments" class="block">
    <p class="kicker">{{ t('experiments.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-4">{{ t('experiments.title') }}</h2>

    <v-tabs v-model="tab" class="exp-tabs mb-5" color="primary" density="comfortable" show-arrows>
      <v-tab v-for="x in tabs" :key="x.id" :value="x.id" class="exp-tab">
        <span class="lbl">{{ x.label }}</span>
        <span class="kind">{{ x.kind }}</span>
      </v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="A">
        <CostModelSection :meta="metaA" />
      </v-window-item>
      <v-window-item value="B">
        <PlannedExperiment :meta="metaB" />
      </v-window-item>
      <v-window-item value="C">
        <MaintenanceSection :meta="metaC" :summary="summary" :cost-rows="costRows" />
      </v-window-item>
      <v-window-item value="D">
        <PlannedExperiment :meta="metaD" />
      </v-window-item>
    </v-window>
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem,5vw,3.6rem) 0; border-top: 1px solid var(--line); }
.exp-tabs { border-bottom: 1px solid var(--line); }
.exp-tab {
  text-transform: none; letter-spacing: 0; min-height: 56px;
  display: flex; flex-direction: column; align-items: flex-start; justify-content: center;
  .lbl { font-family: var(--serif); font-weight: 600; font-size: .98rem; line-height: 1.1; }
  .kind { font-family: var(--mono); font-size: .6rem; text-transform: uppercase; letter-spacing: .08em; color: var(--mute); }
}
/* The inner experiment sections already have their own top border/padding;
   neutralize it inside the tab window so the tab strip owns the separation. */
.exp-tabs + .v-window :deep(.block) { border-top: none; padding-top: 1rem; }
</style>
