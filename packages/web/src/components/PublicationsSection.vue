<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { getPublications } from '@/data/publications'
import type { Locale } from '@/i18n'

const { t, locale } = useI18n()
const pubs = computed(() => getPublications(locale.value as Locale))
</script>

<template>
  <section id="publications" class="block">
    <p class="kicker">{{ t('pubs.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-2">{{ t('pubs.title') }}</h2>
    <p class="lede">{{ t('pubs.lede') }}</p>

    <v-row dense>
      <v-col v-for="p in pubs" :key="p.id" cols="12" md="4">
        <v-card class="pa-4 pub" height="100%">
          <p class="badge">{{ p.badge }}</p>
          <p v-if="p.award" class="award">&#127942; {{ p.award }}</p>
          <h3 class="pub-title serif">{{ p.title }}</h3>
          <p class="authors">{{ p.authors }}</p>
          <p class="venue">{{ p.venueLine }}</p>
          <p class="summary">{{ p.summary }}</p>
          <p class="links">
            <a v-for="l in p.links" :key="l.href" :href="l.href" target="_blank" rel="noopener noreferrer">{{ l.label }}</a>
          </p>
        </v-card>
      </v-col>
    </v-row>
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem, 5vw, 3.6rem) 0; border-top: 1px solid var(--line); }
.lede { max-width: 760px; color: var(--mute); margin-bottom: 1.1rem; }
.pub { border-top: 3px solid var(--teal); display: flex; flex-direction: column; }
.badge {
  font-family: var(--mono); font-size: .68rem; letter-spacing: .06em; text-transform: uppercase;
  color: var(--teal); margin-bottom: .4rem;
}
.award { font-size: .78rem; font-weight: 700; color: #B8860B; margin-bottom: .3rem; }
.pub-title { font-size: 1.02rem; font-weight: 600; line-height: 1.35; margin-bottom: .45rem; }
.authors { font-size: .8rem; color: var(--navy); margin-bottom: .15rem; }
.venue { font-size: .74rem; color: var(--mute); margin-bottom: .6rem; }
.summary { font-size: .84rem; line-height: 1.6; color: var(--ink); flex: 1; }
.links {
  margin-top: .7rem;
  a { margin-right: .9rem; font-size: .82rem; color: var(--teal); text-decoration: none; font-family: var(--mono); }
  a:hover { text-decoration: underline; }
}
</style>
