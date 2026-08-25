<script setup lang="ts">
import { computed, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { getPublications } from '@/data/publications'
import type { Locale } from '@/i18n'

const { t, locale } = useI18n()
const pubs = computed(() => getPublications(locale.value as Locale))
const imgFailed = reactive<Record<string, boolean>>({})
</script>

<template>
  <section id="publications" class="block">
    <p class="kicker">{{ t('pubs.kicker') }}</p>
    <h2 class="sec-title text-h5 mb-2">{{ t('pubs.title') }}</h2>
    <p class="lede">{{ t('pubs.lede') }}</p>

    <div class="pub-list">
      <article v-for="p in pubs" :key="p.id" class="pub-row">
        <div class="pub-top">
          <h3 class="pub-title serif">{{ p.title }}</h3>
          <span class="status">{{ p.status }}</span>
        </div>
        <p class="venue">
          {{ p.venue }}<template v-if="p.location"> · {{ p.location }}</template> · {{ p.date }}
        </p>
        <div class="authors">
          <span v-for="a in p.authors" :key="a.name" class="author">
            <img
              v-if="a.img && !imgFailed[a.name]"
              class="avatar"
              :src="a.img"
              :alt="a.name"
              width="28"
              height="28"
              loading="lazy"
              @error="imgFailed[a.name] = true"
            />
            <span v-else class="avatar avatar-init">{{ a.initials }}</span>
            <span class="aname">{{ a.name }}</span>
          </span>
        </div>
        <p class="summary">{{ p.summary }}</p>
        <p class="links">
          <a class="aix-link" :href="p.aixHref" target="_blank" rel="noopener noreferrer">{{ t('pubs.detail') }}</a>
          <a v-for="l in p.links" :key="l.href" :href="l.href" target="_blank" rel="noopener noreferrer">{{ l.label }}</a>
        </p>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss">
.block { padding: clamp(2.2rem, 5vw, 3.6rem) 0; border-top: 1px solid var(--line); }
.lede { max-width: 760px; color: var(--mute); margin-bottom: 1.4rem; }
.pub-list { display: flex; flex-direction: column; }
.pub-row { padding: 1.3rem 0; border-top: 1px solid var(--line); }
.pub-row:last-child { border-bottom: 1px solid var(--line); }
.pub-top { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.pub-title { font-size: 1.06rem; font-weight: 600; line-height: 1.4; color: var(--navy); margin: 0; max-width: 62rem; }
.status {
  flex: 0 0 auto; font-family: var(--mono); font-size: .66rem; letter-spacing: .05em; text-transform: uppercase;
  color: var(--teal); background: var(--ts); border: 1px solid #BFE0DA; border-radius: 999px; padding: .22rem .7rem;
  white-space: nowrap;
}
.venue { font-size: .8rem; color: var(--mute); margin: .35rem 0 .55rem; }
.authors { display: flex; flex-wrap: wrap; gap: .45rem 1.1rem; margin-bottom: .6rem; }
.author { display: inline-flex; align-items: center; gap: .45rem; }
.avatar {
  width: 28px; height: 28px; border-radius: 50%; object-fit: cover; background: var(--ts);
  box-shadow: 0 0 0 1px var(--line);
}
.avatar-init {
  display: inline-flex; align-items: center; justify-content: center;
  font-family: var(--mono); font-size: .62rem; font-weight: 700; color: var(--teal);
}
.aname { font-size: .82rem; color: var(--ink); }
.summary { font-size: .88rem; line-height: 1.65; color: var(--soft); max-width: 75ch; margin-bottom: .55rem; }
.links {
  a { margin-right: 1rem; font-size: .82rem; color: var(--teal); text-decoration: none; font-family: var(--mono); }
  a:hover { text-decoration: underline; }
  .aix-link { font-weight: 700; }
}
@media (max-width: 640px) { .pub-top { flex-direction: column; gap: .3rem; } }
</style>
