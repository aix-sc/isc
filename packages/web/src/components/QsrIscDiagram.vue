<script setup lang="ts">
import { useI18n } from 'vue-i18n'

// Same mechanism as OverviewSection: t() follows the global locale reactively,
// so the labels switch when the site language toggles.
const { t } = useI18n()
</script>

<template>
  <svg
    class="qsr-isc"
    viewBox="0 0 1000 500"
    role="img"
    :aria-label="t('overview.diagram.title')"
    xmlns="http://www.w3.org/2000/svg"
  >
    <title>{{ t('overview.diagram.title') }}</title>

    <!-- divider -->
    <line class="div" x1="500" y1="54" x2="500" y2="404" />

    <!-- ================= QSR (left) ================= -->
    <text class="hdr qsr" x="40" y="34">{{ t('overview.diagram.qsrHdr') }}</text>

    <rect class="card" x="40" y="62" width="420" height="50" rx="10" />
    <text class="bx ink" x="250" y="92" text-anchor="middle">{{ t('overview.diagram.q1') }}</text>
    <text class="arr mute" x="250" y="130" text-anchor="middle">↓</text>

    <rect class="card" x="40" y="138" width="420" height="62" rx="10" />
    <text class="bx ink" x="250" y="164" text-anchor="middle">{{ t('overview.diagram.q2a') }}</text>
    <text class="bx mute" x="250" y="186" text-anchor="middle">{{ t('overview.diagram.q2b') }}</text>
    <text class="arr mute" x="250" y="220" text-anchor="middle">↓</text>

    <rect class="card" x="40" y="226" width="420" height="50" rx="10" />
    <text class="bx ink" x="250" y="256" text-anchor="middle">{{ t('overview.diagram.q3') }}</text>
    <text class="arr mute" x="250" y="294" text-anchor="middle">↓</text>

    <rect class="card" x="40" y="300" width="420" height="62" rx="10" />
    <text class="bx ink" x="250" y="326" text-anchor="middle">{{ t('overview.diagram.q4a') }}</text>
    <text class="bx ink" x="250" y="348" text-anchor="middle">{{ t('overview.diagram.q4b') }}</text>

    <text class="badge qsr" x="250" y="392" text-anchor="middle">{{ t('overview.diagram.qBadge') }}</text>

    <!-- ================= ISC (right) ================= -->
    <text class="hdr isc" x="540" y="34">{{ t('overview.diagram.iscHdr') }}</text>

    <text class="tag isc" x="540" y="60">{{ t('overview.diagram.ingest') }}</text>
    <rect class="card" x="540" y="70" width="420" height="50" rx="10" />
    <text class="bx ink" x="750" y="100" text-anchor="middle">{{ t('overview.diagram.i1') }}</text>
    <text class="arr mute" x="750" y="138" text-anchor="middle">↓</text>

    <rect class="card" x="540" y="146" width="420" height="62" rx="10" />
    <text class="bx ink" x="750" y="172" text-anchor="middle">{{ t('overview.diagram.i2a') }}</text>
    <text class="bx mute" x="750" y="194" text-anchor="middle">{{ t('overview.diagram.i2b') }}</text>

    <text class="tag mute" x="540" y="246">{{ t('overview.diagram.query') }}</text>
    <rect class="card" x="540" y="256" width="420" height="50" rx="10" />
    <text class="bx ink" x="750" y="286" text-anchor="middle">{{ t('overview.diagram.i3') }}</text>

    <text class="badge isc" x="750" y="392" text-anchor="middle">{{ t('overview.diagram.iBadge') }}</text>

    <!-- ================= takeaway ================= -->
    <text class="cap mute" x="500" y="446" text-anchor="middle">{{ t('overview.diagram.cap') }}</text>
  </svg>
</template>

<style scoped>
.qsr-isc {
  display: block;
  width: 100%;
  height: auto;
  font-family: -apple-system, 'Helvetica Neue', 'Hiragino Sans', 'Noto Sans JP',
    'Yu Gothic', 'Meiryo', Arial, sans-serif;
}

.qsr-isc .card { fill: var(--isc-card, #f4f6f8); }
.qsr-isc .ink  { fill: var(--isc-ink, #1a1a1a); }
.qsr-isc .mute { fill: var(--isc-mute, #6b7280); }
.qsr-isc .qsr  { fill: var(--isc-qsr, #c0392b); }
.qsr-isc .isc  { fill: var(--isc-teal, #1b998b); }
.qsr-isc .div  { stroke: var(--isc-line, #d9dee3); stroke-width: 1; }

.qsr-isc .hdr   { font-size: 21px; font-weight: 700; }
.qsr-isc .bx    { font-size: 14.5px; }
.qsr-isc .tag   { font-size: 11px; font-weight: 700; letter-spacing: 0.04em; }
.qsr-isc .badge { font-size: 14.5px; font-weight: 700; }
.qsr-isc .arr   { font-size: 17px; }
.qsr-isc .cap   { font-size: 13px; }
</style>
