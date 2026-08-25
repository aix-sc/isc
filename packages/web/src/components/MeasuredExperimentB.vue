<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Chart, registerables, type ChartConfiguration } from 'chart.js'
import type { ExperimentMeta } from '@/types/experiment'
import MetricChip from '@/components/MetricChip.vue'
import { MEASURED_VIEWS, HEADLINE, type MeasuredView } from '@/data/measured'
import { DATA_LINKS } from '@/data/publications'

Chart.register(...registerables)
defineProps<{ meta: ExperimentMeta }>()
const { t } = useI18n()

const active = ref<MeasuredView['id']>('exact')
const view = computed(() => MEASURED_VIEWS.find((v) => v.id === active.value)!)
const canvas = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

function buildConfig(v: MeasuredView): ChartConfiguration<'bar'> {
  return {
    type: 'bar',
    data: {
      labels: v.bars.map((b) => b.label),
      datasets: [{
        data: v.bars.map((b) => b.value),
        backgroundColor: v.bars.map((b) => (b.accent ? '#5BC2B5' : '#16263B')),
        borderRadius: 6,
        maxBarThickness: 42,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => `${c.parsed.x} ${v.unit}` } },
      },
      scales: {
        x: { type: v.log ? 'logarithmic' : 'linear', title: { display: true, text: v.unit }, grid: { color: '#E8EDF3' } },
        y: { grid: { display: false } },
      },
    },
  }
}
onMounted(() => { if (canvas.value) chart = new Chart(canvas.value, buildConfig(view.value)) })
watch(view, (v) => { chart?.destroy(); if (canvas.value) chart = new Chart(canvas.value, buildConfig(v)) })
onBeforeUnmount(() => chart?.destroy())
</script>

<template>
  <div>
    <h3 class="exp-name serif">{{ meta.name }}</h3>
    <v-alert type="success" variant="tonal" density="comfortable" class="mb-4">
      {{ t('experiments.publishedIcast') }}
    </v-alert>

    <div class="chips mb-4">
      <MetricChip v-for="h in HEADLINE" :key="h.key" :value="h.value" :label="t('results.metric.' + h.key)" accent />
    </div>

    <v-btn-toggle v-model="active" mandatory divided density="comfortable" class="mb-3 toggle">
      <v-btn v-for="v in MEASURED_VIEWS" :key="v.id" :value="v.id" size="small">{{ t('results.view.' + v.id) }}</v-btn>
    </v-btn-toggle>

    <v-card class="pa-4 mb-4">
      <div class="chart-holder" :style="{ height: 40 + view.bars.length * 52 + 'px' }">
        <canvas ref="canvas" />
      </div>
      <p class="note mt-2">{{ t('results.note.' + active) }}</p>
    </v-card>

    <v-card class="pa-5">
      <div class="field">
        <h4>{{ t('meta.purpose') }}</h4>
        <p>{{ meta.purpose }}</p>
      </div>
      <div class="field outcomes">
        <h4>{{ t('experiments.outcomes') }}</h4>
        <p>{{ meta.outcomes }}</p>
      </div>
    </v-card>

    <p class="prov">
      {{ t('results.provenance') }}
      <a v-for="l in DATA_LINKS" :key="l.id" :href="l.href" target="_blank" rel="noopener noreferrer">{{ t('results.links.' + l.id) }}</a>
    </p>
  </div>
</template>

<style scoped lang="scss">
.exp-name { font-weight: 600; font-size: 1.15rem; color: var(--navy); margin-bottom: .8rem; }
.chips { display: flex; flex-wrap: wrap; gap: .7rem; }
.toggle { flex-wrap: wrap; }
.chart-holder { position: relative; width: 100%; }
.note { font-size: .8rem; color: var(--mute); }
.field { padding: .2rem 0 .9rem; }
.field + .field { border-top: 1px dashed var(--line); padding-top: .9rem; }
.field h4 { font-family: var(--mono); font-size: .68rem; text-transform: uppercase; letter-spacing: .1em; color: var(--teal); margin-bottom: .35rem; }
.field p { font-size: .92rem; color: var(--soft); line-height: 1.6; max-width: 70ch; }
.outcomes { background: var(--ts); border: 1px solid #BFE0DA; border-radius: 11px; padding: .9rem 1.1rem;
  h4 { color: var(--teal); } p { color: var(--ink); } }
.prov { margin-top: 1rem; font-size: .82rem; color: var(--mute);
  a { margin-left: .8rem; color: var(--teal); text-decoration: none; font-family: var(--mono); }
  a:hover { text-decoration: underline; } }
</style>
