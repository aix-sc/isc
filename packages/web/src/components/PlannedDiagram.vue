<script setup lang="ts">
import { useI18n } from 'vue-i18n'
defineProps<{ id: string }>()
const { t } = useI18n()
const HAS = ['Aprime', 'E', 'F', 'G', 'H', 'I']
</script>

<template>
  <v-card v-if="HAS.includes(id)" class="pa-4 mb-4 fig-card">
    <!-- A' : measured cost curves crossing at R* -->
    <svg v-if="id === 'Aprime'" viewBox="0 0 720 230" class="fig" role="img">
      <line x1="60" y1="190" x2="690" y2="190" class="ax" />
      <line x1="60" y1="190" x2="60" y2="20" class="ax" />
      <text x="675" y="212" class="lab">reads →</text>
      <text x="18" y="30" class="lab">cost ↑</text>
      <line x1="60" y1="170" x2="660" y2="40" class="qsr" />
      <path d="M 60 95 L 660 118" class="isc" />
      <circle cx="392" cy="105" r="6" class="star" />
      <line x1="392" y1="105" x2="392" y2="190" class="dash" />
      <text x="384" y="215" class="mono">R*</text>
      <text x="600" y="35" class="mono qsr-t">QSR</text>
      <text x="600" y="135" class="mono isc-t">ISC</text>
      <text x="70" y="88" class="small">compile once (ingest)</text>
      <text x="470" y="80" class="small">pay per read</text>
    </svg>

    <!-- E : corpus-driven incremental axis adaptation -->
    <svg v-else-if="id === 'E'" viewBox="0 0 720 230" class="fig" role="img">
      <rect x="30" y="80" width="150" height="70" rx="10" class="box" />
      <text x="105" y="110" class="mid">corpus</text>
      <text x="105" y="130" class="mid small">+ new docs</text>
      <line x1="180" y1="115" x2="270" y2="115" class="arrow" marker-end="url(#ah)" />
      <line x1="330" y1="185" x2="330" y2="45" class="axis2" />
      <line x1="270" y1="160" x2="470" y2="90" class="axis2" />
      <line x1="280" y1="60" x2="480" y2="160" class="axis2" />
      <text x="335" y="40" class="mono">e₁…e_k</text>
      <line x1="330" y1="115" x2="520" y2="60" class="newax" />
      <text x="528" y="56" class="mono teal">+Δ axis</text>
      <text x="560" y="140" class="small">small update,</text>
      <text x="560" y="158" class="small">no full re-SVD</text>
      <defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" class="ah" /></marker></defs>
    </svg>

    <!-- F : Procrustes map between model generations -->
    <svg v-else-if="id === 'F'" viewBox="0 0 720 230" class="fig" role="img">
      <ellipse cx="170" cy="115" rx="120" ry="80" class="space" />
      <ellipse cx="550" cy="115" rx="120" ry="80" class="space" />
      <text x="170" y="35" class="mid mono">model v1</text>
      <text x="550" y="35" class="mid mono">model v2</text>
      <circle cx="140" cy="95" r="5" class="pt" /><circle cx="200" cy="140" r="5" class="pt" /><circle cx="165" cy="120" r="5" class="pt" />
      <circle cx="520" cy="100" r="5" class="pt2" /><circle cx="580" cy="145" r="5" class="pt2" /><circle cx="545" cy="125" r="5" class="pt2" />
      <path d="M 290 115 C 360 70, 400 70, 430 112" class="arrow" marker-end="url(#ah2)" />
      <text x="352" y="62" class="mono teal">Ω (orthogonal)</text>
      <text x="360" y="205" class="mid small">re-embed a small anchor set → map everything else</text>
      <defs><marker id="ah2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" class="ah" /></marker></defs>
    </svg>

    <!-- G : evaluation hardening, three parts -->
    <svg v-else-if="id === 'G'" viewBox="0 0 720 230" class="fig" role="img">
      <rect x="25" y="45" width="200" height="140" rx="10" class="box" />
      <text x="125" y="75" class="mid small b">1 · human raters</text>
      <circle cx="85" cy="110" r="16" class="head" /><circle cx="165" cy="110" r="16" class="head" />
      <text x="125" y="165" class="mid mono">κ (chance-corrected)</text>
      <rect x="260" y="45" width="200" height="140" rx="10" class="box" />
      <text x="360" y="75" class="mid small b">2 · judge separation</text>
      <rect x="285" y="95" width="65" height="40" rx="7" class="chip" /><text x="317" y="120" class="mid mono">judge A</text>
      <rect x="370" y="95" width="65" height="40" rx="7" class="chip2" /><text x="402" y="120" class="mid mono">judge B</text>
      <text x="360" y="165" class="mid small">side-by-side</text>
      <rect x="495" y="45" width="200" height="140" rx="10" class="box" />
      <text x="595" y="75" class="mid small b">3 · held-out replay</text>
      <text x="595" y="120" class="mid mono">500 docs</text>
      <text x="595" y="145" class="mid small">document-disjoint</text>
      <text x="595" y="165" class="mid small">same protocol</text>
    </svg>

    <!-- H : three arms, where the labor happens -->
    <svg v-else-if="id === 'H'" viewBox="0 0 720 250" class="fig" role="img">
      <rect x="25" y="95" width="120" height="56" rx="10" class="box" />
      <text x="85" y="127" class="mid">corpus</text>
      <rect x="560" y="95" width="130" height="56" rx="10" class="box" />
      <text x="625" y="127" class="mid">reader</text>
      <line x1="145" y1="112" x2="560" y2="55" class="lane" />
      <line x1="145" y1="123" x2="560" y2="123" class="lane" />
      <line x1="145" y1="134" x2="560" y2="190" class="lane" />
      <text x="330" y="42" class="mono">QSR</text><text x="410" y="42" class="small">raw text · labor at read ⏱</text>
      <text x="300" y="112" class="mono">doc2query</text><text x="400" y="112" class="small">keys expanded · reader still gets raw text</text>
      <text x="330" y="207" class="mono teal">ISC</text><text x="380" y="207" class="small teal">payload compiled at ingest ✓</text>
    </svg>

    <!-- I : full-ledger accounting at scale -->
    <svg v-else-if="id === 'I'" viewBox="0 0 720 230" class="fig" role="img">
      <text x="30" y="45" class="small b">full ledger, measured end-to-end:</text>
      <rect x="30" y="60" width="120" height="34" class="seg1" /><text x="90" y="82" class="mid mono w">ingest</text>
      <rect x="150" y="60" width="150" height="34" class="seg2" /><text x="225" y="82" class="mid mono w">maintenance</text>
      <rect x="300" y="60" width="330" height="34" class="seg3" /><text x="465" y="82" class="mid mono">reads × R</text>
      <line x1="30" y1="130" x2="690" y2="130" class="ax" />
      <text x="640" y="150" class="lab">scale →</text>
      <text x="30" y="175" class="small">synthetic revisions → real revision streams (institutional docs, Wikipedia)</text>
      <text x="30" y="196" class="small">maintenance cost tracks change, not corpus size · break-even R* re-measured</text>
    </svg>

    <p class="cap">{{ t('plannedFig.' + id) }}</p>
  </v-card>
</template>

<style scoped lang="scss">
.fig-card { background: #fff; }
.fig { width: 100%; height: auto; display: block; }
.ax { stroke: var(--line); stroke-width: 2; }
.lab { font-size: 13px; fill: var(--mute); }
.small { font-size: 12.5px; fill: var(--mute); }
.b { font-weight: 700; fill: var(--navy); }
.mono { font-family: var(--mono); font-size: 13px; fill: var(--navy); }
.mid { text-anchor: middle; font-size: 14px; fill: var(--navy); }
.w { fill: #fff; }
.teal { fill: var(--teal); }
.qsr { stroke: #16263B; stroke-width: 3; }
.qsr-t { fill: #16263B; font-weight: 700; }
.isc { stroke: #5BC2B5; stroke-width: 3; }
.isc-t { fill: #5BC2B5; font-weight: 700; }
.star { fill: var(--teal); }
.dash, .newax { stroke: var(--teal); stroke-width: 2; stroke-dasharray: 5 4; }
.axis2 { stroke: #90A4B8; stroke-width: 2; }
.arrow { stroke: var(--teal); stroke-width: 2.5; fill: none; }
.ah { fill: var(--teal); }
.box { fill: #F6F9FB; stroke: var(--line); stroke-width: 1.5; }
.space { fill: #F6F9FB; stroke: var(--line); stroke-width: 1.5; }
.pt { fill: #16263B; } .pt2 { fill: #5BC2B5; }
.head { fill: #DCE9F2; stroke: var(--line); }
.chip { fill: #E9F2F0; stroke: #BFE0DA; } .chip2 { fill: #fff; stroke: var(--line); }
.lane { stroke: var(--line); stroke-width: 2; }
.seg1 { fill: #16263B; } .seg2 { fill: #46617F; } .seg3 { fill: #DCE9F2; }
.cap { margin: .7rem 0 0; font-size: .8rem; color: var(--mute); line-height: 1.55; }
</style>
