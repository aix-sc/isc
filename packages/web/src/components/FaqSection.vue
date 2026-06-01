<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { getFaq } from '@/data/faq'
import { useLocale } from '@/composables/useLocale'

const { t } = useI18n()
const { current } = useLocale()
const items = computed(() => getFaq(current.value))
</script>

<template>
  <section id="faq" class="block">
    <p class="kicker">{{ t('faq.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-3">{{ t('faq.title') }}</h2>
    <p class="lede mb-4">{{ t('faq.lede') }}</p>

    <v-expansion-panels variant="accordion" multiple class="faq">
      <v-expansion-panel v-for="(item, i) in items" :key="i">
        <v-expansion-panel-title>
          <span class="q"><span class="qmark">Q.</span>{{ item.q }}</span>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <p class="a">{{ item.a }}</p>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem,5vw,3.6rem) 0; border-top: 1px solid var(--line); }
.lede { max-width: 62ch; color: var(--soft); }
.faq { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
.q { display: flex; gap: .55rem; align-items: baseline; font-weight: 600; color: var(--navy); font-size: .95rem; line-height: 1.45; }
.qmark { font-family: var(--mono); color: var(--teal); font-weight: 700; flex: none; }
.a { color: var(--soft); font-size: .92rem; line-height: 1.65; max-width: 72ch; }
:deep(.v-expansion-panel-title) { min-height: 56px; }
</style>
