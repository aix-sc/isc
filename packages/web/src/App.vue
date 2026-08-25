<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useExperiments } from '@/composables/useExperiments'
import { GITHUB_URL } from '@/data/experiments'
import AppHeader from '@/components/AppHeader.vue'
import HeroSection from '@/components/HeroSection.vue'
import OverviewSection from '@/components/OverviewSection.vue'
import ExperimentsSection from '@/components/ExperimentsSection.vue'
import PublicationsSection from '@/components/PublicationsSection.vue'
import RoadmapSection from '@/components/RoadmapSection.vue'
import FaqSection from '@/components/FaqSection.vue'
import ChatDock from '@/components/ChatDock.vue'

const { t } = useI18n()
const { experiments, summary, costRows } = useExperiments()
</script>

<template>
  <v-app>
    <AppHeader />
    <v-main class="shell">
      <HeroSection :summary="summary" />
      <v-container class="wrap">
        <OverviewSection />
        <ExperimentsSection :experiments="experiments" :summary="summary" :cost-rows="costRows" />
        <RoadmapSection />
        <PublicationsSection />
        <FaqSection />
      </v-container>
      <footer class="foot">
        <p class="foot-brand serif">{{ t('footer.title') }}</p>
        <div class="foot-team">
          <p class="foot-team-label">{{ t('footer.team') }}</p>
          <div class="foot-team-grid">
            <article class="foot-person">
              <img class="foot-avatar" src="/team/kyle.jpg" alt="Kyle Wild" width="76" height="76" loading="lazy" />
              <div class="foot-person-meta">
                <p class="foot-person-name serif">Kyle Wild</p>
                <p class="foot-person-role">{{ t('footer.kyleRole') }}</p>
                <p class="foot-person-bio">{{ t('footer.kyleBio') }}</p>
                <p class="foot-person-links">
                  <a class="foot-icon" href="https://www.linkedin.com/in/kylewild/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.78C.8 0 0 .78 0 1.74v20.52C0 23.22.8 24 1.78 24h20.44c.98 0 1.78-.78 1.78-1.74V1.74C24 .78 23.2 0 22.22 0z"/></svg></a>
                
                  <a class="foot-icon foot-icon--orcid" href="https://orcid.org/0009-0001-6918-3197" target="_blank" rel="noopener noreferrer" aria-label="ORCID"><svg viewBox="0 0 256 256" width="18" height="18" aria-hidden="true" focusable="false"><path fill="#A6CE39" d="M256,128c0,70.7-57.3,128-128,128S0,198.7,0,128S57.3,0,128,0S256,57.3,256,128z"/><path fill="#FFFFFF" d="M86.3,186.2H70.9V79.1h15.4v107.1z"/><path fill="#FFFFFF" d="M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z"/><path fill="#FFFFFF" d="M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1C84.2,46.7,88.7,51.3,88.7,56.8z"/></svg></a>
                  <span class="foot-orcid-id">ORCID: 0009-0001-6918-3197</span>
                </p>
              </div>
            </article>
            <article class="foot-person">
              <img class="foot-avatar" src="/team/yusuke.jpg" alt="Yusuke Takahashi" width="76" height="76" loading="lazy" />
              <div class="foot-person-meta">
                <p class="foot-person-name serif">Yusuke Takahashi, PhD</p>
                <p class="foot-person-role">{{ t('footer.yusukeRole') }}</p>
                <p class="foot-person-bio">{{ t('footer.yusukeBio') }}</p>
                <p class="foot-person-links">
                  <a class="foot-icon" href="https://www.linkedin.com/in/yusuketakahashiphd/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.78C.8 0 0 .78 0 1.74v20.52C0 23.22.8 24 1.78 24h20.44c.98 0 1.78-.78 1.78-1.74V1.74C24 .78 23.2 0 22.22 0z"/></svg></a>
                  <a class="foot-icon foot-icon--orcid" href="https://orcid.org/0009-0006-8351-2280" target="_blank" rel="noopener noreferrer" aria-label="ORCID"><svg viewBox="0 0 256 256" width="18" height="18" aria-hidden="true" focusable="false"><path fill="#A6CE39" d="M256,128c0,70.7-57.3,128-128,128S0,198.7,0,128S57.3,0,128,0S256,57.3,256,128z"/><path fill="#FFFFFF" d="M86.3,186.2H70.9V79.1h15.4v107.1z"/><path fill="#FFFFFF" d="M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z"/><path fill="#FFFFFF" d="M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1C84.2,46.7,88.7,51.3,88.7,56.8z"/></svg></a>
                </p>
              </div>
            </article>
          </div>
        </div>
        <div class="foot-inner">
          <div class="foot-links">
            <a href="https://muds.ac" target="_blank" rel="noopener">{{ t('footer.muds') }}</a>
            <a href="https://aix.sc/" target="_blank" rel="noopener">{{ t('footer.aixLab') }}</a>
            <a :href="GITHUB_URL" target="_blank" rel="noopener">{{ t('footer.github') }}</a>
            <a href="#top">{{ t('footer.backToTop') }}</a>
          </div>
        </div>
        <p class="foot-fine">{{ t('footer.fine') }}</p>
      </footer>
    </v-main>
    <ChatDock :experiments="experiments" :summary="summary" />
  </v-app>
</template>

<style scoped lang="scss">
/* Reserve room for the persistent chat rail (ChatDock) on desktop (>=960px). */
@media (min-width: 960px) {
  :global(html.chat-rail-open) .shell { padding-right: 360px; }
}
.wrap { max-width: 1080px; }
.foot { background: var(--navy); color: #fff; padding: 2.4rem clamp(1rem,4vw,3rem) 1.6rem; }
.foot-brand { max-width: 1080px; margin: 0 auto 1.8rem; font-size: 1.5rem; font-weight: 600; color: #fff;
  letter-spacing: -.01em; padding-bottom: 1.1rem; border-bottom: 1px solid #2C496E; }
.foot-inner { max-width: 1080px; margin: 0 auto; display: flex; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap; }
.foot-title { font-size: 1.3rem; font-weight: 600; }
.foot-links { display: flex; flex-direction: column; gap: .45rem; font-size: .88rem;
  a { color: #CFE0F2; text-decoration: none; } }
.foot-fine { max-width: 1080px; margin: 1.6rem auto 0; font-size: .74rem; color: #7E97B6; border-top: 1px solid #2C496E; padding-top: 1rem; }
.foot-team { max-width: 1080px; margin: 0 auto 1.9rem; }
.foot-team-label {
  font-family: var(--mono); font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
  color: #5BC2B5; display: flex; align-items: center; gap: .8rem; margin: 0 0 1.2rem;
}
.foot-team-label::after { content: ''; flex: 1; height: 1px; background: #2C496E; }
.foot-team-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem 2.4rem; }
.foot-person { display: flex; gap: .95rem; align-items: flex-start; }
.foot-avatar {
  flex: 0 0 auto; width: 76px; height: 76px; border-radius: 50%; object-fit: cover; background: #2C496E;
  box-shadow: 0 0 0 1px rgba(255,255,255,.16); transition: box-shadow .25s ease, transform .25s ease;
}
.foot-person:hover .foot-avatar { box-shadow: 0 0 0 2px #5BC2B5; transform: translateY(-2px); }
.foot-person-meta { min-width: 0; }
.foot-person-name { font-size: 1.05rem; font-weight: 600; color: #fff; line-height: 1.2; margin: 0; }
.foot-person-role {
  font-family: var(--mono); font-size: .68rem; letter-spacing: .04em; text-transform: uppercase;
  color: #5BC2B5; margin: .2rem 0 0;
}
.foot-person-bio { font-size: .8rem; line-height: 1.55; color: #B9CAE0; margin: .45rem 0 0; }
.foot-person-links { display: flex; align-items: center; gap: .65rem; margin: .55rem 0 0; }
.foot-icon { display: inline-flex; line-height: 0; color: #CFE0F2; transition: opacity .2s ease, color .2s ease; }
.foot-icon:hover { opacity: .82; color: #5BC2B5; }
.foot-orcid-id { font-family: var(--mono); font-size: .68rem; color: #7E97B6; }
@media (max-width: 640px) { .foot-team-grid { grid-template-columns: 1fr; } }
</style>
