<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import { Chart, registerables, type ChartConfiguration } from 'chart.js'
import type { ExperimentMeta } from '@/types/experiment'

Chart.register(...registerables)
defineProps<{ meta: ExperimentMeta }>()
const { t } = useI18n()

const RULES = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'] as const
const canvas = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

const config = computed<ChartConfiguration<'bar'>>(() => ({
  type: 'bar',
  data: {
    labels: [t('expD.bars.iscCited'), t('expD.bars.wrongCite'), t('expD.bars.noValue')],
    datasets: [{
      data: [30, 0, 29],
      backgroundColor: ['#5BC2B5', '#B8860B', '#16263B'],
      borderRadius: 6,
      maxBarThickness: 46,
    }],
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { callbacks: { label: (c) => `${c.parsed.x} / 30` } } },
    scales: {
      x: { max: 30, title: { display: true, text: t('expD.unit') }, grid: { color: '#E8EDF3' } },
      y: { grid: { display: false } },
    },
  },
}))

onMounted(() => { if (canvas.value) chart = new Chart(canvas.value, config.value) })
onBeforeUnmount(() => chart?.destroy())
</script>

<template>
  <div>
    <h3 class="exp-name serif">{{ meta.name }}</h3>
    <v-alert type="success" variant="tonal" density="comfortable" class="mb-4">
      {{ t('experiments.publishedIcast') }}
    </v-alert>

    <v-card class="pa-4 mb-4">
      <h4 class="panel-h">{{ t('expD.decompTitle') }}</h4>
      <div class="chart-holder" style="height: 200px"><canvas ref="canvas" /></div>
      <p class="note mt-2">{{ t('expD.decompNote') }}</p>
    </v-card>

    <v-card class="pa-4 mb-4">
      <h4 class="panel-h">{{ t('expD.rulesTitle') }}</h4>
      <div class="rules">
        <div v-for="r in RULES" :key="r" class="rule">
          <span class="rid">{{ r }}</span>
          <span class="rtx">{{ t('expD.rules.' + r) }}</span>
        </div>
      </div>
      <p class="note mt-2">{{ t('expD.rulesNote') }}</p>
    </v-card>

    <v-card class="pa-5">
      <div class="field">
        <h4>{{ t('meta.purpose') }}</h4>
        <p>{{ meta.purpose }}</p>
      </div>
      <div class="field outcomes">
        <h4>{{ t('experiments.outcomes') }}</h4>
        <p>{{ t('expD.outcome') }}</p>
      </div>
    </v-card>
  </div>
</template>

<style scoped lang="scss">
.exp-name { font-weight: 600; font-size: 1.15rem; color: var(--navy); margin-bottom: .8rem; }
.panel-h { font-family: var(--mono); font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: var(--teal); margin-bottom: .6rem; }
.chart-holder { position: relative; width: 100%; }
.note { font-size: .8rem; color: var(--mute); }
.rules { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: .5rem .9rem; }
.rule { display: flex; gap: .55rem; align-items: baseline; font-size: .84rem; line-height: 1.5; }
.rid { font-family: var(--mono); font-weight: 700; color: var(--teal); flex: 0 0 auto; }
.rtx { color: var(--soft); }
.field { padding: .2rem 0 .9rem; }
.field + .field { border-top: 1px dashed var(--line); padding-top: .9rem; }
.field h4 { font-family: var(--mono); font-size: .68rem; text-transform: uppercase; letter-spacing: .1em; color: var(--teal); margin-bottom: .35rem; }
.field p { font-size: .92rem; color: var(--soft); line-height: 1.6; max-width: 70ch; }
.outcomes { background: var(--ts); border: 1px solid #BFE0DA; border-radius: 11px; padding: .9rem 1.1rem;
  h4 { color: var(--teal); } p { color: var(--ink); } }
</style>
