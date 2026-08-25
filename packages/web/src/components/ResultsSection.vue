<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Chart, registerables, type ChartConfiguration } from 'chart.js'
import MetricChip from '@/components/MetricChip.vue'
import { MEASURED_VIEWS, HEADLINE, type MeasuredView } from '@/data/measured'
import { DATA_LINKS } from '@/data/publications'

Chart.register(...registerables)
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
      datasets: [
        {
          data: v.bars.map((b) => b.value),
          backgroundColor: v.bars.map((b) => (b.accent ? '#5BC2B5' : '#16263B')),
          borderRadius: 6,
          maxBarThickness: 42,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (c) => `${c.parsed.x} ${v.unit}`,
          },
        },
      },
      scales: {
        x: {
          type: v.log ? 'logarithmic' : 'linear',
          title: { display: true, text: v.unit },
          grid: { color: '#E8EDF3' },
        },
        y: { grid: { display: false } },
      },
    },
  }
}

onMounted(() => {
  if (canvas.value) chart = new Chart(canvas.value, buildConfig(view.value))
})
watch(view, (v) => {
  if (!chart) return
  chart.destroy()
  if (canvas.value) chart = new Chart(canvas.value, buildConfig(v))
})
onBeforeUnmount(() => chart?.destroy())
</script>

<template>
  <section id="results" class="block">
    <p class="kicker">{{ t('results.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-2">{{ t('results.title') }}</h2>
    <p class="lede">{{ t('results.lede') }}</p>

    <div class="chips mb-4">
      <MetricChip v-for="h in HEADLINE" :key="h.key" :value="h.value" :label="t('results.metric.' + h.key)" accent />
    </div>

    <v-btn-toggle v-model="active" mandatory divided density="comfortable" class="mb-3 toggle">
      <v-btn v-for="v in MEASURED_VIEWS" :key="v.id" :value="v.id" size="small">
        {{ t('results.view.' + v.id) }}
      </v-btn>
    </v-btn-toggle>

    <v-card class="pa-4">
      <div class="chart-holder" :style="{ height: 40 + view.bars.length * 52 + 'px' }">
        <canvas ref="canvas" />
      </div>
      <p class="note mt-2">{{ t('results.note.' + active) }}</p>
    </v-card>

    <p class="prov">
      {{ t('results.provenance') }}
      <a v-for="l in DATA_LINKS" :key="l.id" :href="l.href" target="_blank" rel="noopener noreferrer">{{ t('results.links.' + l.id) }}</a>
    </p>
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem, 5vw, 3.6rem) 0; border-top: 1px solid var(--line); }
.lede { max-width: 760px; color: var(--mute); margin-bottom: 1.1rem; }
.chips { display: flex; flex-wrap: wrap; gap: .7rem; }
.toggle { flex-wrap: wrap; }
.chart-holder { position: relative; width: 100%; }
.note { font-size: .8rem; color: var(--mute); }
.prov {
  margin-top: 1rem; font-size: .82rem; color: var(--mute);
  a { margin-left: .8rem; color: var(--teal); text-decoration: none; }
  a:hover { text-decoration: underline; }
}
</style>
