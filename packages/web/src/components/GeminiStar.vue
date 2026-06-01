<script setup lang="ts">
// Gemini-style four-point spark, with the blue→purple→rose gradient.
// Duplicate <defs> ids across instances are harmless (the browser resolves to the first).
</script>

<template>
  <svg class="gstar" viewBox="0 0 24 24" aria-hidden="true">
    <defs>
      <linearGradient id="gemini-grad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#4285F4" />
        <stop offset="50%" stop-color="#9168F0" />
        <stop offset="100%" stop-color="#D96570" />
      </linearGradient>
    </defs>
    <path
      fill="url(#gemini-grad)"
      d="M12 1.6c.5 4.6 2.8 7.9 9.4 10.4-6.6 2.5-8.9 5.8-9.4 10.4-.5-4.6-2.8-7.9-9.4-10.4 6.6-2.5 8.9-5.8 9.4-10.4Z"
    />
  </svg>
</template>

<style scoped lang="scss">
.gstar { width: 100%; height: 100%; display: block; }
</style>
