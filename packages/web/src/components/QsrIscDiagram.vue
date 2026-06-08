<script setup lang="ts">
// QsrIscDiagram.vue — QSR vs ISC explanatory figure.
// Self-contained inline SVG: crisp at any size, themeable via CSS custom properties.
// Override colors from a parent by setting --isc-* on any ancestor.
</script>

<template>
  <figure class="qsr-isc">
    <svg
      viewBox="0 0 1000 500"
      role="img"
      aria-labelledby="qsrIscTitle qsrIscDesc"
    >
      <title id="qsrIscTitle">QSR vs ISC — where the work happens</title>
      <desc id="qsrIscDesc">
        QSR reconstructs meaning on every query; ISC compiles meaning once at
        ingest and maintains it incrementally, so queries become a cheap lookup.
      </desc>

      <line class="div" x1="500" y1="54" x2="500" y2="404" />

      <!-- QSR (left) -->
      <text class="hdr qsr" x="40" y="34">QSR — every query repeats the work</text>

      <rect class="card" x="40" y="62" width="420" height="50" rx="10" />
      <text class="bx ink" x="250" y="92" text-anchor="middle">1. Query arrives</text>
      <text class="arr mute" x="250" y="130" text-anchor="middle">&#8595;</text>

      <rect class="card" x="40" y="138" width="420" height="62" rx="10" />
      <text class="bx ink" x="250" y="164" text-anchor="middle">2. Embed &#8594; fixed-dimension vector</text>
      <text class="bx mute" x="250" y="186" text-anchor="middle">(e.g., 1024 real numbers — not 1s and 0s)</text>
      <text class="arr mute" x="250" y="220" text-anchor="middle">&#8595;</text>

      <rect class="card" x="40" y="226" width="420" height="50" rx="10" />
      <text class="bx ink" x="250" y="256" text-anchor="middle">3. Similarity search (cosine / distance)</text>
      <text class="arr mute" x="250" y="294" text-anchor="middle">&#8595;</text>

      <rect class="card" x="40" y="300" width="420" height="62" rx="10" />
      <text class="bx ink" x="250" y="326" text-anchor="middle">4. LLM re-reads raw passages &#8594;</text>
      <text class="bx ink" x="250" y="348" text-anchor="middle">reconstructs meaning &#8594; answer</text>

      <text class="badge qsr" x="250" y="392" text-anchor="middle">&#8635; Repeated on every query</text>

      <!-- ISC (right) -->
      <text class="hdr isc" x="540" y="34">ISC — compile once, then maintain</text>

      <text class="tag isc" x="540" y="60">INGEST  (once / on change)</text>
      <rect class="card" x="540" y="70" width="420" height="50" rx="10" />
      <text class="bx ink" x="750" y="100" text-anchor="middle">New / updated doc &#8594; compile meaning once</text>
      <text class="arr mute" x="750" y="138" text-anchor="middle">&#8595;</text>

      <rect class="card" x="540" y="146" width="420" height="62" rx="10" />
      <text class="bx ink" x="750" y="172" text-anchor="middle">Substrate: orthonormal axes + meaning vectors</text>
      <text class="bx mute" x="750" y="194" text-anchor="middle">(maintained incrementally)</text>

      <text class="tag mute" x="540" y="246">QUERY  (cheap)</text>
      <rect class="card" x="540" y="256" width="420" height="50" rx="10" />
      <text class="bx ink" x="750" y="286" text-anchor="middle">Query &#8594; project + cheap lookup &#8594; answer</text>

      <text class="badge isc" x="750" y="392" text-anchor="middle">&#10003; Heavy work once; updates only on change</text>

      <text class="cap mute" x="500" y="446" text-anchor="middle">QSR cost grows with the number of queries &#183; ISC cost grows only with change</text>
    </svg>
  </figure>
</template>

<style scoped lang="scss">
.qsr-isc {
  // Brand palette (override these from a parent for dark mode / theming).
  --isc-card: #f4f6f8;
  --isc-ink: #1a1a1a;
  --isc-mute: #6b7280;
  --isc-qsr: #c0392b;
  --isc-teal: #1b998b;
  --isc-divider: #d9dee3;

  width: 100%;
  max-width: 960px;
  margin: 0 auto;

  svg {
    width: 100%;
    height: auto;
    font-family: inherit;
  }

  .card { fill: var(--isc-card); }
  .ink  { fill: var(--isc-ink); }
  .mute { fill: var(--isc-mute); }
  .qsr  { fill: var(--isc-qsr); }
  .isc  { fill: var(--isc-teal); }
  .div  { stroke: var(--isc-divider); stroke-width: 1; }

  .hdr   { font-size: 21px; font-weight: 700; }
  .bx    { font-size: 14.5px; }
  .tag   { font-size: 11px; font-weight: 700; letter-spacing: 0.04em; }
  .badge { font-size: 14.5px; font-weight: 700; }
  .arr   { font-size: 17px; }
  .cap   { font-size: 13px; }
}
</style>
